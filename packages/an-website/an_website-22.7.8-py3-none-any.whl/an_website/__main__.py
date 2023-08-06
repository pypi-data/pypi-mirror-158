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

"""Nobody inspects the spammish repetition."""

from __future__ import annotations

import sys
import warnings

if sys.flags.dev_mode and not sys.warnoptions:
    warnings.simplefilter("error", DeprecationWarning)
warnings.filterwarnings("ignore", module="defusedxml")


from . import patches  # pylint: disable=wrong-import-position  # noqa: E402

patches.apply()


from .main import main  # pylint: disable=wrong-import-position  # noqa: E402

sys.exit(main())
