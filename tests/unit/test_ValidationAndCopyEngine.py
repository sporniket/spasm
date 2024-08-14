"""
---
(c) 2024 David SPORN
---
This is part of SPASM -- Sporniket's toolbox for assembly language.

SPASM is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

SPASM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with SPASM.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

import copy
import pprint

from spasm.pp.stylesheet.builtin import HERITAGE
from spasm.pp.stylesheet.validation import ValidationAndCopyEngine, SCHEMA_OF_STYLESHEET


def test_that_ValidationAndCopyEngine_performs_as_expected():
    stylesheet = {"comment_lines": {"prefix": ";"}, "comments": {"prefix": "*"}}
    recipient = copy.deepcopy(HERITAGE)
    assert recipient["comment_lines"]["prefix"] == "*"
    assert recipient["comments"]["prefix"] == ";"
    events = ValidationAndCopyEngine().perform(
        SCHEMA_OF_STYLESHEET, "<ROOT>", stylesheet, recipient
    )
    pprint.pp(recipient)
    pprint.pp(events)
    assert recipient["comment_lines"]["prefix"] == ";"
    assert recipient["comments"]["prefix"] == "*"
