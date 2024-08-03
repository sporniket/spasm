"""
Test suite using the default builtin stylesheet.
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

from .factory_of_verifications_for_stylesheet_default import (
    FACTORY_OF__it_does_not_force_comment_at_comment_tabstop_after_statement_line_without_comment,
    FACTORY_OF__it_does_pretty_print_comment_lines,
    FACTORY_OF__it_does_pretty_print_statement_lines,
    FACTORY_OF__it_forces_labels_at_first_position_for_macro_directives,
    FACTORY_OF__it_ignores_spaces_in_string_litteral_in_operands,
    FACTORY_OF__it_output_empty_lines_when_there_is_only_a_marker_for_comment,
)


ARGS = ["prog"]


def test_that_it_does_pretty_print_comment_lines():
    FACTORY_OF__it_does_pretty_print_comment_lines(ARGS)


def test_that_it_does_pretty_print_statement_lines():
    FACTORY_OF__it_does_pretty_print_statement_lines(ARGS)


def test_that_it_output_empty_lines_when_there_is_only_a_marker_for_comment():
    FACTORY_OF__it_output_empty_lines_when_there_is_only_a_marker_for_comment(ARGS)


def test_that_it_ignores_spaces_in_string_litteral_in_operands():
    FACTORY_OF__it_ignores_spaces_in_string_litteral_in_operands(ARGS)


def test_that_it_does_not_force_comment_at_comment_tabstop_after_statement_line_without_comment():
    FACTORY_OF__it_does_not_force_comment_at_comment_tabstop_after_statement_line_without_comment(
        ARGS
    )


def test_that_it_forces_labels_at_first_position_for_macro_directives():
    FACTORY_OF__it_forces_labels_at_first_position_for_macro_directives
