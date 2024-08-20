"""
Test suite using rewrite mode.
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
    initializeTmpWorkspace,
    mockStdInput,
    assert_that_source_is_converted_as_expected,
)


ARGS = ["prog", "--rewrite"]
SOURCE_DATA_FILES = os.path.join(".", "tests", "data")


def test_that_it_rewrite_only_modified_files_from_given_input_files_list():
    # Prepare files
    fileNames = ["source1.s", "source2-formatted.s"]
    tmp_dir = initializeTmpWorkspace(
        [
            os.path.join(SOURCE_DATA_FILES, f)
            for f in fileNames + ["source1-formatted.s"]
        ]
    )
    targetFiles = [os.path.join(tmp_dir, f) for f in fileNames]
    timeStamps = [os.path.getmtime(f) for f in targetFiles]
    time.sleep(2.1)  # wait 2 seconds (and a little bit more) to detect file updates

    # execute
    with patch.object(sys, "argv", ARGS + targetFiles):
        with redirect_stdout(io.StringIO()) as out:
            returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert out.getvalue() == """"""
        for i, f in enumerate(targetFiles):
            if f.endswith("-formatted.s"):
                assert os.path.getmtime(f) - timeStamps[i] < 1
            else:
                assert os.path.getmtime(f) - timeStamps[i] > 2
                assert_that_source_is_converted_as_expected(f, f[:-2] + "-formatted.s")


def test_that_it_cannot_rewrite_without_given_input_files_list():

    with patch.object(sys, "argv", ARGS):
        with redirect_stdout(io.StringIO()) as out:
            with redirect_stderr(io.StringIO()) as err:
                returnCode = PrettyPrinterCli().run()
        assert returnCode != 0
        assert out.getvalue() == """"""
        assert (
            err.getvalue()
            == """ERROR -- rewrite mode requires a list of files
"""
        )
