"""
Test suite using the custom stylesheet file `margin-comment.json`.
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

import os
import shutil
import time
import sys
import io
from typing import List, Union, Optional

from unittest.mock import patch
from contextlib import redirect_stdout

from spasm.pp import PrettyPrinterCli

from .utils import (
    makeTmpDirOrDie,
    mockStdInput,
    assert_that_source_is_converted_as_expected,
)


ARGS = ["prog", "--stylesheet", "file:tests/data/margin-comment.json"]


def test_that_it_supports_margin_space_specification_for_comments():
    input_lines = [
        " just short;comment",
        " line very,long,long,long,long,long,long,long,long,long,long ;comment",
    ]

    with patch.object(sys, "argv", ARGS):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """                just    short     ; comment
                line    very,long,long,long,long,long,long,long,long,long,long     ; comment
"""
        )
