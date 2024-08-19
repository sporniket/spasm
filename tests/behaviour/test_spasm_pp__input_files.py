"""
Test suite using provided input files.
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


ARGS = ["prog"]


def test_that_it_processes_given_input_files_list():

    with patch.object(
        sys, "argv", ARGS + ["tests/data/source1.s", "tests/data/source2.s"]
    ):
        with redirect_stdout(io.StringIO()) as out:
            returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """                from    source1

                from    source2

"""
        )


def test_that_it_reports_any_problem_with_given_input_files_list():

    with patch.object(
        sys,
        "argv",
        ARGS
        + [
            "tests/data/nope1.s",
            "tests/data/source1.s",
            "tests/data/nope2.s",
            "tests/data",
        ],
    ):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = PrettyPrinterCli().run()
        assert returnCode != 0
        assert out.getvalue() == """"""
        assert (
            err.getvalue()
            == """ERROR -- in given list of files :
* MISSING : tests/data/nope1.s
* MISSING : tests/data/nope2.s
* NOT A FILE : tests/data
"""
        )
