# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
The base request handlers used by other modules.

This should only contain request handlers and the get_module_info function.
"""

from __future__ import annotations

import inspect
import logging
import random
import re
import sys
import time
import traceback
import uuid
from asyncio import Future
from base64 import b64decode
from collections.abc import Awaitable, Callable, Coroutine
from datetime import date, datetime, timedelta, timezone, tzinfo
from http.client import responses
from typing import Any, cast
from urllib.parse import SplitResult, quote, unquote, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import elasticapm  # type: ignore
import html2text
import orjson as json
import yaml
from accept_types import get_best_match  # type: ignore
from ansi2html import Ansi2HTMLConverter  # type: ignore
from bs4 import BeautifulSoup
from dateutil.easter import easter
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ElasticsearchException
from redis.asyncio import Redis
from sympy.ntheory import isprime
from tornado.web import HTTPError, MissingArgumentError, RequestHandler

from .. import (
    EVENT_ELASTICSEARCH,
    EVENT_REDIS,
    GH_ORG_URL,
    GH_PAGES_URL,
    GH_REPO_URL,
    NAME,
    ORJSON_OPTIONS,
)
from .static_file_handling import fix_static_url
from .utils import (
    TEXT_CONTENT_TYPES,
    THEMES,
    ModuleInfo,
    Permission,
    add_args_to_url,
    anonymize_ip,
    bool_to_str,
    geoip,
    hash_bytes_b64,
    normalized_levenshtein,
    replace_umlauts,
    str_to_bool,
)

logger = logging.getLogger(__name__)


def get_module_info() -> ModuleInfo:
    """Create and return the ModuleInfo for this module."""
    return ModuleInfo(
        name="Utilities",
        description="Nützliche Werkzeuge für alle möglichen Sachen.",
        handlers=(
            (
                r"/error",
                ZeroDivision if sys.flags.dev_mode else NotFoundHandler,
                {},
            ),
            (r"/([1-5][0-9]{2}).html?", ErrorPage, {}),
        ),
        hidden=True,
    )


class BaseRequestHandler(RequestHandler):
    """The base request handler used by every page and API."""

    # pylint: disable=too-many-instance-attributes, too-many-public-methods

    ELASTIC_RUM_URL = (
        "/@elastic/apm-rum@^5/dist/bundles/elastic-apm-rum"
        f".umd{'.min' if not sys.flags.dev_mode else ''}.js"
    )

    MAX_BODY_SIZE: None | int = None
    ALLOWED_METHODS: tuple[str, ...] = ("GET",)
    POSSIBLE_CONTENT_TYPES: tuple[str, ...] = ()
    REQUIRED_PERMISSION: None | Permission = None
    # the following should be False on security relevant endpoints
    ALLOW_COOKIE_AUTHENTICATION = True

    module_info: ModuleInfo
    # info about page, can be overridden in module_info
    title: str = "Das Asoziale Netzwerk"
    short_title: str = "Asoziales Netzwerk"
    description: str = "Die tolle Webseite des Asozialen Netzwerkes"
    content_type: None | str = None
    active_origin_trials: set[bytes]
    auth_failed: bool = False
    now: datetime
    apm_script: None | str

    def initialize(
        self,
        *,
        module_info: ModuleInfo,
        # default is true, because then empty args dicts are
        # enough to specify that the defaults should be used
        default_title: bool = True,
        default_description: bool = True,
    ) -> None:
        """
        Get title and description from the kwargs.

        If title and description are present in the kwargs they
        override self.title and self.description.
        """
        self.module_info = module_info
        if not default_title:
            page_info = self.module_info.get_page_info(self.request.path)
            self.title = page_info.name
            self.short_title = page_info.short_name or self.title
        if not default_description:
            self.description = self.module_info.get_page_info(
                self.request.path
            ).description

    def data_received(self, chunk: Any) -> None:
        """Do nothing."""

    @property
    def redis(self) -> Redis:  # type: ignore[type-arg]
        """Get the Redis client from the settings."""
        return cast(Redis, self.settings.get("REDIS"))  # type: ignore[type-arg]

    @property
    def redis_prefix(self) -> str:
        """Get the Redis prefix from the settings."""
        return self.settings.get("REDIS_PREFIX", NAME)

    @property
    def elasticsearch(self) -> AsyncElasticsearch:
        """Get the Elasticsearch client from the settings."""
        return cast(AsyncElasticsearch, self.settings.get("ELASTICSEARCH"))

    @property
    def elasticsearch_prefix(self) -> str:
        """Get the Elasticsearch prefix from the settings."""
        return self.settings.get("ELASTICSEARCH_PREFIX", NAME)

    @property
    def elastic_apm_client(self) -> None | elasticapm.Client:
        """Get the Elastic APM client from the settings."""
        return self.settings.get("ELASTIC_APM_CLIENT")

    def set_csp_header(self) -> None:
        """Set the Content-Security-Policy header."""
        script_src = ["'self'"]
        if self.elastic_apm_enabled():
            script_src.append(
                f"'sha256-{self.settings['ELASTIC_APM']['INLINE_SCRIPT_HASH']}'"
            )
        self.set_header(
            "Content-Security-Policy",
            "default-src 'self';"
            f"script-src {' '.join(script_src)};"
            "style-src 'self' 'unsafe-inline';"
            "img-src 'self' https://img.zeit.de https://github.asozial.org;"
            "report-to default;"
            + (
                f"report-uri {self.get_reporting_api_endpoint()};"
                if self.settings.get("REPORTING")
                else ""
            )
            + (
                f"connect-src 'self' {self.settings['ELASTIC_APM']['SERVER_URL']};"
                if self.elastic_apm_enabled()
                else ""
            ),
        )

    def get_reporting_api_endpoint(self) -> None | str:
        """Get the endpoint for the reporting API."""
        if not self.settings.get("REPORTING"):
            return None
        endpoint = self.settings.get("REPORTING_ENDPOINT")

        if not endpoint or not endpoint.startswith("/"):
            return endpoint

        return f"{self.request.protocol}://{self.request.host}{endpoint}"

    def set_default_headers(self) -> None:
        """Set default headers."""
        self.set_csp_header()
        self.active_origin_trials = set()
        if self.settings.get("REPORTING"):
            endpoint = self.get_reporting_api_endpoint()
            self.set_header("Reporting-Endpoints", f'default="{endpoint}"')
            self.set_header(
                "Report-To",
                json.dumps(
                    {
                        "group": "default",
                        "max_age": 2592000,
                        "endpoints": [{"url": endpoint}],
                    },
                    option=ORJSON_OPTIONS,
                ),
            )
            self.set_header("NEL", '{"report_to":"default","max_age":2592000}')
        # dev.mozilla.org/docs/Web/HTTP/Headers
        self.set_header("Access-Control-Max-Age", "7200")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header(
            "Access-Control-Allow-Methods",
            ", ".join(self.get_allowed_methods()),
        )
        # opt out of all FLoC cohort calculation
        self.set_header("Permissions-Policy", "interest-cohort=()")
        # don't send the Referer header for cross-origin requests
        self.set_header("Referrer-Policy", "same-origin")
        # dev.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
        self.set_header(
            "Cross-Origin-Opener-Policy", "same-origin; report-to=default"
        )
        if self.request.path == "/kaenguru-comics-alt":  # TODO: improve this
            self.set_header(
                "Cross-Origin-Embedder-Policy",
                "credentialless; report-to=default",
            )
        else:
            self.set_header(
                "Cross-Origin-Embedder-Policy",
                "require-corp; report-to=default",
            )
        if self.settings.get("HSTS"):
            # dev.mozilla.org/docs/Web/HTTP/Headers/Strict-Transport-Security
            self.set_header("Strict-Transport-Security", "max-age=63072000")
        if (
            onion_address := self.settings.get("ONION_ADDRESS")
        ) and not self.request.host_name.endswith(".onion"):
            # community.torproject.org/onion-services/advanced/onion-location
            self.set_header(
                "Onion-Location",
                onion_address
                + self.request.path
                + (f"?{self.request.query}" if self.request.query else ""),
            )
        if self.settings.get("debug"):
            self.set_header("X-Debug", bool_to_str(True))
            for permission in Permission:
                if permission.name:
                    self.set_header(
                        f"X-Permission-{permission.name}",
                        bool_to_str(bool(self.is_authorized(permission))),
                    )
        if self.auth_failed:
            self.set_header("WWW-Authenticate", "Bearer")
        self.origin_trial(
            "AjM7i7vhQFI2RUcab3ZCsJ9RESLDD9asdj0MxpwxHXXtETlsm8dEn+HSd646oPr1dKjn+EcNEj8uV3qFGJzObgsAAAB3eyJvcmlnaW4iOiJodHRwczovL2Fzb3ppYWwub3JnOjQ0MyIsImZlYXR1cmUiOiJTZW5kRnVsbFVzZXJBZ2VudEFmdGVyUmVkdWN0aW9uIiwiZXhwaXJ5IjoxNjg0ODg2Mzk5LCJpc1N1YmRvbWFpbiI6dHJ1ZX0="  # noqa: B950  # pylint: disable=line-too-long, useless-suppression
        )

    def origin_trial(self, token: bytes | str) -> bool:
        """Enable an experimental feature."""
        # pylint: disable=protected-access
        data = b64decode(token)
        payload = json.loads(data[69:])
        origin = urlsplit(payload["origin"])
        url = urlsplit(self.request.full_url())
        if data in self.active_origin_trials:
            return True
        if url.port is None and url.scheme in {"http", "https"}:
            url = url._replace(
                netloc=f"{url.hostname}:{443 if url.scheme == 'https' else 80}"
            )
        if self.request._start_time > payload["expiry"]:
            return False
        if url.scheme != origin.scheme:
            return False
        if url.netloc != origin.netloc and not (
            payload.get("isSubdomain")
            and url.netloc.endswith(f".{origin.netloc}")
        ):
            return False
        self.add_header("Origin-Trial", token)
        self.active_origin_trials.add(data)
        return True

    def set_cookie(  # pylint: disable=too-many-arguments
        self,
        name: str,
        value: str | bytes,
        domain: None | str = None,
        expires: None | float | tuple[int, ...] | datetime = None,
        path: str = "/",
        expires_days: None | float = 365,  # changed
        **kwargs: Any,
    ) -> None:
        """Override the set_cookie method to set expires days."""
        if "samesite" not in kwargs:
            # default for same site should be strict
            kwargs["samesite"] = "Strict"

        super().set_cookie(
            name,
            value,
            domain,
            expires,
            path,
            expires_days,
            **kwargs,
        )

    @property
    def dump(self) -> Callable[[Any], str | bytes]:
        """Get the function for dumping the output."""
        if self.content_type == "application/json":
            option = ORJSON_OPTIONS
            if self.get_bool_argument("pretty", False):
                option |= json.OPT_INDENT_2
            return lambda spam: json.dumps(spam, option=option)

        if self.content_type == "application/yaml":
            return yaml.dump

        return lambda spam: spam  # type: ignore[no-any-return]

    def write(self, chunk: str | bytes | dict[str, Any]) -> None:
        """Write the given chunk to the output buffer.

        To write the output to the network, use the ``flush()`` method.
        """
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")

        self.set_content_type_header()

        if isinstance(chunk, dict):
            chunk = self.dump(chunk)

        super().write(chunk)

    def finish(
        self, chunk: None | str | bytes | dict[str, Any] = None
    ) -> Future[None]:
        """Finish this response, ending the HTTP request.

        Passing a ``chunk`` to ``finish()`` is equivalent to passing that
        chunk to ``write()`` and then calling ``finish()`` with no arguments.

        Returns a ``Future`` which may optionally be awaited to track the sending
        of the response to the client. This ``Future`` resolves when all the response
        data has been sent, and raises an error if the connection is closed before all
        data can be sent.
        """
        if self._finished:
            raise RuntimeError("finish() called twice")

        if chunk is not None:
            self.write(chunk)

        if (
            self.content_type in TEXT_CONTENT_TYPES
            and self._write_buffer
            and not self._write_buffer[-1].endswith(b"\n")
        ):
            self.write(b"\n")

        return super().finish()

    def set_content_type_header(self) -> None:
        """Set the Content-Type header based on `self.content_type`."""
        if str(self.content_type).startswith("text/"):  # RFC2616 3.7.1
            self.set_header(
                "Content-Type", f"{self.content_type};charset=utf-8"
            )
        elif self.content_type is not None:
            self.set_header("Content-Type", self.content_type)

    def raise_non_acceptable(
        self, possible_content_types: tuple[str, ...]
    ) -> None:
        """Only call this if we cannot respect the Accept header."""
        self.clear_header("Content-Type")
        self.set_status(406)
        self.finish("\n".join(possible_content_types) + "\n")

    def handle_accept_header(
        self, possible_content_types: tuple[str, ...]
    ) -> None:
        """Handle the Accept header and set `self.content_type`."""
        if not possible_content_types:
            return
        content_type = get_best_match(
            self.request.headers.get("Accept") or "*/*",
            possible_content_types,
        )
        if content_type is None:
            self.raise_non_acceptable(possible_content_types)
            return
        self.content_type = content_type
        self.set_content_type_header()

    def elastic_apm_enabled(self) -> bool:
        """Return whether elastic apm is enabled."""
        return (
            "ELASTIC_APM" in self.settings
            and self.settings["ELASTIC_APM"]["ENABLED"]
        )

    async def prepare(  # noqa: C901
        self,
    ) -> None:
        """Check authorization and call self.ratelimit()."""
        # pylint: disable=invalid-overridden-method, too-complex
        self.now = await self.get_time()
        self.handle_accept_header(self.POSSIBLE_CONTENT_TYPES)

        if self.request.method == "GET":

            if self.redirect_to_canonical_domain():
                return

            if not self.settings.get("TESTING"):
                if (days := random.randint(0, 31337)) in {69, 420, 1337, 31337}:
                    self.set_cookie("c", "s", expires_days=days / 24, path="/")

        if self.request.method != "OPTIONS":

            required_permission = self.REQUIRED_PERMISSION
            required_permission_for_method = getattr(
                self, f"REQUIRED_PERMISSION_{self.request.method}", None
            )

            if required_permission is None:
                required_permission = required_permission_for_method
            elif required_permission_for_method is not None:
                required_permission |= required_permission_for_method

            if required_permission is not None:
                is_authorized = self.is_authorized(required_permission)
                if not is_authorized:
                    self.auth_failed = True
                    logger.warning(
                        "Unauthorized access to %s from %s",
                        self.request.path,
                        anonymize_ip(str(self.request.remote_ip)),
                    )
                    raise HTTPError(401 if is_authorized is None else 403)

            if self.MAX_BODY_SIZE is not None:
                if len(self.request.body) > self.MAX_BODY_SIZE:
                    logger.warning(
                        "%s > MAX_BODY_SIZE (%s)",
                        len(self.request.body),
                        self.MAX_BODY_SIZE,
                    )
                    raise HTTPError(413)

            if not await self.ratelimit(True):
                await self.ratelimit()

    def redirect_to_canonical_domain(self) -> bool:
        """Redirect to the canonical domain."""
        if (
            not (domain := self.settings.get("DOMAIN"))
            or not self.request.headers.get("Host")
            or self.request.host_name == domain
            or self.request.host_name.endswith((".onion", ".i2p"))
            or re.fullmatch(r"/[\u2800-\u28FF]+/?", self.request.path)
        ):
            return False
        port = urlsplit(f"//{self.request.headers['Host']}").port
        self.redirect(
            urlsplit(self.request.full_url())
            ._replace(netloc=f"{domain}:{port}" if port else domain)
            .geturl(),
            permanent=True,
        )
        return True

    async def ratelimit(self, global_ratelimit: bool = False) -> bool:
        """Take b1nzy to space using Redis."""
        # pylint: disable=too-complex
        if (
            not self.settings.get("RATELIMITS")
            or self.request.method == "OPTIONS"
            or self.is_authorized(Permission.RATELIMITS)
        ):
            return False
        remote_ip = hash_bytes_b64(
            cast(str, self.request.remote_ip).encode("ascii")
        )
        method = self.request.method
        if method == "HEAD":
            method = "GET"
        if global_ratelimit:
            key = f"{self.redis_prefix}:ratelimit:{remote_ip}"
            max_burst = 99  # limit = 100
            count_per_period = 20  # 20 requests per second
            period = 1
            tokens = 10 if self.settings.get("UNDER_ATTACK") else 1
        else:
            bucket = getattr(
                self,
                f"RATELIMIT_{method}_BUCKET",
                self.__class__.__name__.lower(),
            )
            limit = getattr(self, f"RATELIMIT_{method}_LIMIT", 0)
            if not limit:
                return False
            key = f"{self.redis_prefix}:ratelimit:{remote_ip}:{bucket}"
            max_burst = limit - 1
            count_per_period = getattr(  # request count per period
                self,
                f"RATELIMIT_{method}_COUNT_PER_PERIOD",
                30,
            )
            period = getattr(
                self, f"RATELIMIT_{method}_PERIOD", 60  # period in seconds
            )
            tokens = 1 if self.request.method != "HEAD" else 0
        if not EVENT_REDIS.is_set():
            logger.warning(
                "Ratelimits are enabled, but Redis is not available. "
                "This can happen shortly after starting the website.",
            )
            raise HTTPError(503)
        result = await self.redis.execute_command(  # type: ignore[no-untyped-call]
            "CL.THROTTLE",
            key,
            max_burst,
            count_per_period,
            period,
            tokens,
        )
        # fmt: off
        # pylint: disable=line-too-long
        if result[0]:
            retry_after = result[3] + 1  # TODO: remove after brandur/redis-cell#58 is merged and a new release was made  # noqa: B950
            self.set_header("Retry-After", retry_after)
            if global_ratelimit:
                self.set_header("X-RateLimit-Global", "true")
        if not global_ratelimit:
            reset_after = result[4] + 1  # TODO: remove after brandur/redis-cell#58 is merged and a new release was made  # noqa: B950
            self.set_header("X-RateLimit-Limit", str(result[1]))
            self.set_header("X-RateLimit-Remaining", str(result[2]))
            self.set_header("X-RateLimit-Reset", str(time.time() + reset_after))
            self.set_header("X-RateLimit-Reset-After", str(reset_after))
            self.set_header(
                "X-RateLimit-Bucket", hash_bytes_b64(bucket.encode("ascii")),
            )
        # fmt: on
        if result[0]:
            if self.now.date() == date(self.now.year, 4, 20):
                self.set_status(420)
                self.write_error(420)
            else:
                self.set_status(429)
                self.write_error(429)
        return bool(result[0])

    @classmethod
    def supports_head(cls) -> bool:
        """Check whether this request handler supports HEAD requests."""
        signature = inspect.signature(cls.get)
        return (
            "head" in signature.parameters
            and signature.parameters["head"].kind
            == inspect.Parameter.KEYWORD_ONLY
        )

    @classmethod
    def get_allowed_methods(cls) -> list[str]:
        """Get allowed methods."""
        methods = ["OPTIONS"]
        if "GET" in cls.ALLOWED_METHODS and cls.supports_head():
            methods.append("HEAD")
        methods.extend(cls.ALLOWED_METHODS)
        return methods

    def options(self, *args: Any, **kwargs: Any) -> None:
        """Handle OPTIONS requests."""
        # pylint: disable=unused-argument
        self.set_header("Allow", ", ".join(self.get_allowed_methods()))
        self.set_status(204)
        self.finish()

    def head(self, *args: Any, **kwargs: Any) -> None | Awaitable[None]:
        """Handle HEAD requests."""
        if self.get.__module__ == "tornado.web":
            raise HTTPError(405)
        if not self.supports_head():
            raise HTTPError(501)

        kwargs["head"] = True
        return self.get(*args, **kwargs)

    def get_error_page_description(self, status_code: int) -> str:
        """Get the description for the error page."""
        # pylint: disable=too-many-return-statements
        # https://developer.mozilla.org/docs/Web/HTTP/Status
        if 100 <= status_code <= 199:
            return "Hier gibt es eine total wichtige Information."
        if 200 <= status_code <= 299:
            return "Hier ist alles super! 🎶🎶"
        if 300 <= status_code <= 399:
            return "Eine Umleitung ist eingerichtet."
        if 400 <= status_code <= 499:
            if status_code == 404:
                return f"{self.request.path} wurde nicht gefunden."
            if status_code == 451:
                return "Hier wäre bestimmt geiler Scheiß."
            return "Ein Client-Fehler ist aufgetreten."
        if 500 <= status_code <= 599:
            return "Ein Server-Fehler ist aufgetreten."
        raise ValueError(
            f"{status_code} is not a valid HTTP response status code."
        )

    def get_error_message(self, **kwargs: Any) -> str:
        """
        Get the error message and return it.

        If the serve_traceback setting is true (debug mode is activated),
        the traceback gets returned.
        """
        if "exc_info" in kwargs and not issubclass(
            kwargs["exc_info"][0], HTTPError
        ):
            if self.settings.get("serve_traceback") or self.is_authorized(
                Permission.TRACEBACK
            ):
                return "".join(
                    traceback.format_exception(*kwargs["exc_info"])
                ).strip()
            return "".join(
                traceback.format_exception_only(*kwargs["exc_info"][:2])
            ).strip()
        if "exc_info" in kwargs and issubclass(
            kwargs["exc_info"][0], MissingArgumentError
        ):
            return cast(str, kwargs["exc_info"][1].log_message)
        return str(self._reason)

    def get_user_id(self) -> str:
        """Get the user id saved in the cookie or create one."""
        _user_id = self.get_secure_cookie(
            "user_id",
            max_age_days=90,
            min_version=2,
        )
        user_id = (
            str(uuid.uuid4()) if _user_id is None else _user_id.decode("ascii")
        )
        # save it in cookie or reset expiry date
        if not self.get_secure_cookie(
            "user_id", max_age_days=30, min_version=2
        ):
            self.set_secure_cookie(
                "user_id",
                user_id,
                expires_days=90,
                path="/",
                samesite="Strict",
            )
        return user_id

    def get_module_infos(self) -> tuple[ModuleInfo, ...]:
        """Get the module infos."""
        return self.settings.get("MODULE_INFOS") or tuple()

    def fix_url(  # noqa: C901
        self,
        url: None | str | SplitResult = None,
        new_path: None | str = None,
        **query_args: None | str | bool | float,
    ) -> str:
        """
        Fix a URL and return it.

        If the URL is from another website, link to it with the redirect page.
        Otherwise just return the URL with no_3rd_party appended.
        """
        if url is None:
            url = self.request.full_url()
        if isinstance(url, str):
            url = urlsplit(url)
        if url.netloc and url.netloc.lower() != self.request.host.lower():
            url = urlsplit(f"/redirect?to={quote(url.geturl())}")
        path = url.path if new_path is None else new_path  # the path of the url
        if path.startswith(("/static/", "/soundboard/files/")):
            query_args.update(no_3rd_party=None, theme=None, dynload=None)
        else:
            query_args.setdefault("no_3rd_party", self.get_no_3rd_party())
            query_args.setdefault("theme", self.get_theme())
            query_args.setdefault("dynload", self.get_dynload())
            if query_args["no_3rd_party"] == self.get_saved_no_3rd_party():
                query_args["no_3rd_party"] = None
            if query_args["theme"] == self.get_saved_theme():
                query_args["theme"] = None
            if query_args["dynload"] == self.get_saved_dynload():
                query_args["dynload"] = None

        return add_args_to_url(
            urlunsplit(
                (
                    self.request.protocol,
                    self.request.host,
                    path.rstrip("/"),
                    url.query,
                    url.fragment,
                )
            ),
            **query_args,
        )

    def get_no_3rd_party_default(self) -> bool:
        """Get the default value for the no_3rd_party param."""
        return self.request.host_name.endswith((".onion", ".i2p"))

    def get_saved_no_3rd_party(self) -> bool:
        """Get the saved value for no_3rd_party."""
        default = self.get_no_3rd_party_default()
        no_3rd_party = self.get_cookie("no_3rd_party")
        if no_3rd_party is None:
            return default
        return str_to_bool(no_3rd_party, default)

    def get_no_3rd_party(self) -> bool:
        """Return the no_3rd_party query argument as boolean."""
        return self.get_bool_argument(
            "no_3rd_party", default=self.get_saved_no_3rd_party()
        )

    def get_saved_dynload(self) -> bool:
        """Get the saved value for dynload."""
        default = False  # TODO: change this
        dynload = self.get_cookie("dynload")
        if dynload is None:
            return default
        return str_to_bool(dynload, default)

    def get_dynload(self) -> bool:
        """Return the dynload query argument as boolean."""
        return self.get_bool_argument("dynload", self.get_saved_dynload())

    def get_saved_theme(self) -> str:
        """Get the theme saved in the cookie."""
        theme = self.get_cookie("theme")
        if theme in THEMES:
            return theme
        return "default"

    def get_theme(self) -> str:
        """Get the theme currently selected."""
        theme = self.get_argument("theme", default=None)
        if theme in THEMES:
            return theme
        return self.get_saved_theme()

    def get_display_theme(self) -> str:
        """Get the theme currently displayed."""
        if "random" not in (theme := self.get_theme()):
            return theme

        ignore_themes = ["random", "random-dark"]

        if theme == "random-dark":
            ignore_themes.extend(("light", "light-blue", "fun"))

        return random.choice(
            tuple(theme for theme in THEMES if theme not in ignore_themes)
        )

    def get_int_argument(
        self,
        name: str,
        default: None | int = None,
        *,
        max_: None | int = None,
        min_: None | int = None,
    ) -> int:
        """Get an argument parsed as integer."""
        value: int
        if default is None:
            str_value = self.get_argument(name)
            try:
                value = int(str_value)
            except ValueError as err:
                raise HTTPError(400, f"{str_value} is not an integer") from err
        else:
            try:
                value = int(self.get_argument(name, None) or default)
            except ValueError:
                value = default

        if max_ is not None:
            value = min(max_, value)
        if min_ is not None:
            value = max(min_, value)

        return value

    def get_bool_argument(
        self,
        name: str,
        default: None | bool = None,
    ) -> bool:
        """Get an argument parsed as boolean."""
        if default is not None:
            return str_to_bool(self.get_argument(name, None) or "", default)
        value = str(self.get_argument(name))
        try:
            return str_to_bool(value)
        except ValueError as err:
            raise HTTPError(400, f"{value} is not a boolean") from err

    def is_authorized(self, permission: Permission) -> None | bool:
        """Check whether the request is authorized."""

        def keydecode(token: str) -> None | str:
            try:
                return b64decode(token).decode("utf-8")
            except ValueError:
                return None

        api_secrets = self.settings.get("TRUSTED_API_SECRETS", {})
        found_keys: tuple[None | str, ...] = (
            *(
                (keydecode(_[7:]) if _.lower().startswith("bearer ") else _)
                for _ in self.request.headers.get_list("Authorization")
            ),
            *(keydecode(_) for _ in self.get_arguments("access_token")),
            *self.get_arguments("key"),
            keydecode(cast(str, self.get_cookie("access_token", default="")))
            if self.ALLOW_COOKIE_AUTHENTICATION
            else None,
            self.get_cookie("key", default=None)
            if self.ALLOW_COOKIE_AUTHENTICATION
            else None,
        )

        if not any(key and key in api_secrets for key in found_keys):
            return None

        permissions = Permission(0)
        for key in found_keys:
            if key and key in api_secrets:
                permissions |= api_secrets[key]

        return permission in permissions

    def geoip(
        self,
        ip: None | str = None,  # pylint: disable=invalid-name
        database: str = geoip.__defaults__[0],  # type: ignore
    ) -> Coroutine[Any, Any, None | dict[str, Any]]:
        """Get GeoIP information."""
        if not ip:
            ip = str(self.request.remote_ip)
        if not EVENT_ELASTICSEARCH.is_set():
            return geoip(ip, database)
        return geoip(ip, database, self.elasticsearch)

    async def get_time(self) -> datetime:
        """Get the start time of the request in the users timezone."""
        tz: tzinfo = timezone.utc  # pylint: disable=invalid-name
        try:
            geoip = await self.geoip()  # pylint: disable=redefined-outer-name
        except ElasticsearchException as exc:
            logger.exception(exc)
            apm: None | elasticapm.Client = self.settings.get(
                "ELASTIC_APM_CLIENT"
            )
            if apm:
                apm.capture_exception()
        else:
            if geoip and "timezone" in geoip:
                tz = ZoneInfo(geoip["timezone"])  # pylint: disable=invalid-name
        return datetime.fromtimestamp(
            self.request._start_time, tz=tz  # pylint: disable=protected-access
        )


class HTMLRequestHandler(BaseRequestHandler):
    """A request handler that serves HTML."""

    POSSIBLE_CONTENT_TYPES: tuple[str, ...] = (
        "text/html",
        "text/plain",
        "text/markdown",
        "application/json",
    )
    used_render = False

    def get_form_appendix(self) -> str:
        """Get HTML to add to forms to keep important query args."""
        form_appendix = (
            "<input name='no_3rd_party' class='hidden' "
            f"value='{bool_to_str(self.get_no_3rd_party())}'>"
            if "no_3rd_party" in self.request.query_arguments
            and self.get_no_3rd_party() != self.get_saved_no_3rd_party()
            else ""
        )
        if self.get_dynload() != self.get_saved_dynload():
            form_appendix += (
                "<input name='dynload' class='hidden' "
                f"value='{bool_to_str(self.get_dynload())}'>"
            )
        if (theme := self.get_theme()) != self.get_saved_theme():
            form_appendix += (
                f"<input name='theme' class='hidden' value='{theme}'>"
            )
        return form_appendix

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        """Render the error page with the status_code as a HTML page."""
        self.render(
            "error.html",
            status=status_code,
            reason=self.get_error_message(**kwargs),
            description=self.get_error_page_description(status_code),
            is_traceback="exc_info" in kwargs
            and not issubclass(kwargs["exc_info"][0], HTTPError)
            and (
                self.settings.get("serve_traceback")
                or self.is_authorized(Permission.TRACEBACK)
            ),
        )

    def get_template_namespace(self) -> dict[str, Any]:
        """
        Add useful things to the template namespace and return it.

        They are mostly needed by most of the pages (like title,
        description and no_3rd_party).
        """
        namespace = super().get_template_namespace()
        namespace.update(
            ansi2html=Ansi2HTMLConverter(inline=True, scheme="xterm"),
            as_html=self.content_type == "text/html",
            c=self.settings.get("TESTING")
            or self.now.date() == date(self.now.year, 4, 1)
            or str_to_bool(self.get_cookie("c", "f") or "f", False),
            canonical_url=self.fix_url(
                self.request.full_url().upper()
                if self.request.path.upper().startswith("/LOLWUT")
                else self.request.full_url().lower()
            ).split("?")[0],
            description=self.description,
            dynload=self.get_dynload(),
            elastic_rum_url=self.ELASTIC_RUM_URL,
            fix_static=lambda url: self.fix_url(fix_static_url(url)),
            fix_url=self.fix_url,
            form_appendix=self.get_form_appendix(),
            GH_ORG_URL=GH_ORG_URL,
            GH_PAGES_URL=GH_PAGES_URL,
            GH_REPO_URL=GH_REPO_URL,
            keywords="Asoziales Netzwerk, Känguru-Chroniken"
            + (
                f", {self.module_info.get_keywords_as_str(self.request.path)}"
                if self.module_info
                else ""
            ),
            lang="de",  # TODO: add language support
            no_3rd_party=self.get_no_3rd_party(),
            now=self.now,
            settings=self.settings,
            short_title=self.short_title,
            theme=self.get_display_theme(),
            title=self.title,
            apm_script=self.settings["ELASTIC_APM"]["INLINE_SCRIPT"]
            if self.elastic_apm_enabled()
            else None,
        )
        namespace.update(
            {
                "🥚": self.settings.get("TESTING")
                or timedelta()
                <= self.now.date() - easter(self.now.year)
                < timedelta(days=2),
                "🦘": self.settings.get("TESTING")
                or isprime(self.now.microsecond),  # type: ignore[no-untyped-call]
            }
        )
        return namespace

    def render(self, template_name: str, **kwargs: Any) -> Future[None]:
        """Render a template."""
        self.used_render = True
        return super().render(template_name, **kwargs)

    def finish(
        self, chunk: None | str | bytes | dict[Any, Any] = None
    ) -> Future[None]:
        """Finish the request."""
        as_json: bool = self.content_type == "application/json"
        as_plain_text: bool = self.content_type == "text/plain"
        as_markdown: bool = self.content_type == "text/markdown"
        if (
            not isinstance(chunk, bytes | str)
            or not self.used_render
            or getattr(self, "IS_NOT_HTML", False)
            or not (as_json or as_plain_text or as_markdown)
        ):
            return super().finish(chunk)

        chunk = chunk.decode("utf-8") if isinstance(chunk, bytes) else chunk

        if as_markdown:
            return super().finish(
                f"# {self.title}\n\n"
                + html2text.html2text(chunk, self.request.full_url()).strip()
            )

        soup = BeautifulSoup(chunk, features="lxml")
        if as_plain_text:
            return super().finish(soup.get_text("\n", True))

        dictionary: dict[str, Any] = dict(
            url=self.fix_url(),  # request url
            title=self.title,
            short_title=self.short_title
            if self.title != self.short_title
            else None,
            body="".join(
                str(_el)
                for _el in soup.find_all(name="main", id="body")[0].contents
            ).strip(),
            scripts=[
                {
                    "src": _s.get("src"),
                    # "script": _s.string,  # not in use because of csp
                    # "onload": _s.get("onload"),  # not in use because of csp
                }
                for _s in soup.find_all("script")
            ]
            if soup.head
            else [],
            stylesheets=[
                str(_s.get("href")).strip()
                for _s in soup.find_all("link", rel="stylesheet")
            ]
            if soup.head
            else [],
            css="\n".join(str(_s.string or "") for _s in soup.find_all("style"))
            if soup.head
            else "",
        )
        return super().finish(dictionary)


class APIRequestHandler(BaseRequestHandler):
    """
    The base API request handler.

    It overrides the write error method to return errors as JSON.
    """

    POSSIBLE_CONTENT_TYPES: tuple[str, ...] = (
        "application/json",
        "application/yaml",
    )
    IS_NOT_HTML = True

    def finish_dict(self, **kwargs: Any) -> Future[None]:
        """Finish the request with a JSON response."""
        return self.finish(kwargs)

    def write_error(self, status_code: int, **kwargs: dict[str, Any]) -> None:
        """Finish with the status code and the reason as dict."""
        self.finish_dict(
            status=status_code,
            reason=self.get_error_message(**kwargs),
        )


class NotFoundHandler(HTMLRequestHandler):
    """Show a 404 page if no other RequestHandler is used."""

    def initialize(self, *args: Any, **kwargs: Any) -> None:
        """Do nothing to have default title and description."""
        if "module_info" not in kwargs:
            kwargs["module_info"] = None
        super().initialize(*args, **kwargs)

    async def prepare(self) -> None:  # pylint: disable=too-complex # noqa: C901
        """Throw a 404 HTTP error or redirect to another page."""
        self.now = await self.get_time()

        self.handle_accept_header(self.POSSIBLE_CONTENT_TYPES)

        if self.request.method not in ("GET", "HEAD"):
            raise HTTPError(404)
        new_path = re.sub(r"/+", "/", self.request.path.rstrip("/")).replace(
            "_", "-"
        )
        for ext in (".html", ".htm", ".php"):
            new_path = new_path.removesuffix(f"/index{ext}").removesuffix(ext)

        new_path = replace_umlauts(new_path)

        if new_path.lower() in {
            "/-profiler/phpinfo",
            "/.aws/credentials",
            "/.env.bak",
            "/.ftpconfig",
            "/admin/controller/extension/extension",
            "/assets/filemanager/dialog",
            "/assets/vendor/server/php",
            "/aws.yml",
            "/boaform/admin/formlogin",
            "/phpinfo",
            "/public/assets/jquery-file-upload/server/php",
            "/root",
            "/settings/aws.yml",
            "/uploads",
            "/vendor/phpunit/phpunit/src/util/php/eval-stdin",
            "/wordpress",
            "/wp",
            "/wp-admin",
            "/wp-admin/css",
            "/wp-includes",
            "/wp-login",
            "/wp-upload",
        }:
            self.set_status(469, reason="Nice Try")
            return self.write_error(469)

        if new_path != self.request.path:
            return self.redirect(self.fix_url(new_path=new_path), True)

        this_path_stripped = unquote(new_path).strip("/")  # "/%20/" → " "

        if len(this_path_stripped) == 1:
            return self.redirect(self.fix_url(new_path="/"))

        distances: list[tuple[float, str]] = []
        max_dist = 0.5

        for module_info in self.get_module_infos():
            if module_info.path is not None:
                dist = min(  # get the smallest distance with the aliases
                    normalized_levenshtein(this_path_stripped, path.strip("/"))
                    for path in (*module_info.aliases, module_info.path)
                    if path != "/z"  # do not redirect to /z
                )
                if dist <= max_dist:
                    # only if the distance is less than or equal {max_dist}
                    distances.append((dist, module_info.path))
            if len(module_info.sub_pages) > 0:
                distances.extend(
                    (
                        normalized_levenshtein(
                            this_path_stripped, sub_page.path.strip("/")
                        ),
                        sub_page.path,
                    )
                    for sub_page in module_info.sub_pages
                    if sub_page.path is not None
                )

        if len(distances) > 0:
            # sort to get the one with the smallest distance in index 0
            distances.sort()
            dist, path = distances[0]
            # redirect only if the distance is less than or equal {max_dist}
            if dist <= max_dist:
                return self.redirect(self.fix_url(new_path=path), False)

        if len(this_path_stripped) == 1:
            return self.redirect(self.fix_url(new_path="/"), False)

        raise HTTPError(404)


class ErrorPage(HTMLRequestHandler):
    """A request handler that shows the error page."""

    async def get(self, code: str) -> None:
        """Show the error page."""
        status_code: int = int(code)
        if status_code == 420:
            reason = "Enhance Your Calm"
        elif status_code == 469:
            reason = "Nice Try"
        else:
            reason = responses.get(status_code, "")
        # set the status code if it is allowed
        if status_code not in (204, 304) and not 100 <= status_code < 200:
            self.set_status(status_code, reason)
        return await self.render(
            "error.html",
            status=status_code,
            reason=reason,
            description=self.get_error_page_description(status_code),
            is_traceback=False,
        )


class ZeroDivision(HTMLRequestHandler):
    """A request handler that raises an error."""

    async def prepare(self) -> None:
        """Divide by zero and raise an error."""
        self.now = await self.get_time()
        self.handle_accept_header(self.POSSIBLE_CONTENT_TYPES)
        if not self.request.method == "OPTIONS":
            420 / 0  # pylint: disable=pointless-statement
