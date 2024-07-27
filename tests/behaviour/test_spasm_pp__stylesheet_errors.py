"""
Test suite about stylesheet errors.
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


def test_that_it_reject_wrong_builtin_stylesheet_names():
    input_lines = [
        "what ever",
    ]
    ARGS = ["prog", "--stylesheet", "builtin:whatever"]
    with patch.object(sys, "argv", ARGS):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                with redirect_stderr(io.StringIO()) as err:
                    returnCode = PrettyPrinterCli().run()
        assert returnCode != 0
        assert out.getvalue() == """"""
        assert (
            err.getvalue()
            == """ERROR -- wrong value 'builtin:whatever' for parameter 'stylesheet'
"""
        )
