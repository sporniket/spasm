"""
Test suite using the custom stylesheet file `incorrect.json`.
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
from contextlib import redirect_stdout, redirect_stderr

from spasm.pp import PrettyPrinterCli

from .utils import (
    makeTmpDirOrDie,
    mockStdInput,
    assert_that_source_is_converted_as_expected,
)


ARGS = ["prog", "--stylesheet", "file:tests/data/incorrect.json"]


def test_that_it_rejects_stylesheet_with_invalid_values_and_reports_all_problems_in_stderr():
    input_lines = [
        "what ever",
    ]
    with patch.object(sys, "argv", ARGS):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                with redirect_stderr(io.StringIO()) as err:
                    returnCode = PrettyPrinterCli().run()
        assert returnCode != 0
        assert out.getvalue() == """"""
        assert (
            err.getvalue()
            == """ERROR -- Wrong values in stylesheet 'tests/data/incorrect.json' : 
* tab_stops.labels.position MUST be >= 0
* tab_stops.mnemonic.position MUST be >= tab_stops.labels.position
* tab_stops.operands.position MUST be >= tab_stops.mnemonic.position
* tabulation.width MUST be > 0
* labels.align MUST be one of ["left","right"]
* labels.postfix MUST be one of [":"]
* labels.margin_space MUST be > 0
* labels.force_postfix MUST be a bool
* labels.ignore_align_mnemonics MUST be an array of strings
* comment_lines.prefix MUST be one of ["*",";"]
* comments.prefix MUST be one of ["*",";"]
* comments.margin_space MUST be > 0
"""
        )
