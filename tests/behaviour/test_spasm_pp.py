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


def test_that_it_does_pretty_print_comment_lines():
    input_lines = [
        "; a comment line starting with a semi-colon",
        "* a comment line starting with a star",
        " * not a comment line",
        ";* a comment line for documentation generator tools",
        "** another comment line for documentation generator tools",
        "* * a normal comment line",
        ";a space will be inserted before the beginning of this comment",
        "*       a comment line with a lot of white space before",
        "*\ta comment line with a tabulation before",
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """* a comment line starting with a semi-colon
* a comment line starting with a star
                              ; not a comment line
** a comment line for documentation generator tools
** another comment line for documentation generator tools
* * a normal comment line
* a space will be inserted before the beginning of this comment
*       a comment line with a lot of white space before
*   a comment line with a tabulation before
"""
        )


def test_that_it_does_pretty_print_statement_lines():
    input_lines = [
        "aShortLabel operation operand1,operand2 comment",
        "aVeryLongLabelThatWontFitInTheFirstThirtyCharacters: what ever",
        " aLabelWithoutFinalColon operation op1,op2 comment",
        " aLabelWithColon: operation op1,op2 comment",
        "aSpaceWithinOperand: operation op1, op2 comment",
        " operation comment missing semi-colon",
        " ; just a comment",
        "noComment: do something",
        " ;just a comment",
        " do other,thing a comment",
        "",
        " ;just a comment",
        " ;that will be aligned",
        " ;      like the previous ones",
        " do something",
        "* a comment line",
        " * a block of statement line ",
        " * with only comments",
        "that is all folks !",
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """                 aShortLabel: operation operand1,operand2 ; comment
aVeryLongLabelThatWontFitInTheFirstThirtyCharacters: what ever
                              aLabelWithoutFinalColon operation ; op1,op2 comment
             aLabelWithColon: operation op1,op2    ; comment
         aSpaceWithinOperand: operation op1,       ; op2 comment
                              operation comment    ; missing semi-colon
                                                   ; just a comment
                   noComment: do something
                              ; just a comment
                              do other,thing       ; a comment

                              ; just a comment
                              ; that will be aligned
                              ; like the previous ones
                              do something
* a comment line
                              ; a block of statement line
                              ; with only comments
                        that: is all               ; folks !
"""
        )


def test_that_it_output_empty_lines_when_there_is_only_a_marker_for_comment():
    """Bug report #3"""
    input_lines = [
        ";",
        " ;",
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """

"""
        )


def test_that_it_ignore_spaces_in_string_litteral_in_operands():
    """Bug report #4"""
    input_lines = [
        '"what a" cool world it is',
        'what "a cool "world it is',
        'what a "cool world" it is',
        'what a cool "world it" is',
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """                       \"what: a\" cool              ; world it is
                        what: \"a cool              ; \"world it is
                        what: a \"cool world\"       ; it is
                        what: a cool               ; \"world it\" is
"""
        )


def test_that_it_does_not_force_comment_at_pos_50_after_statement_line_without_comment():
    """Bug report #5"""
    input_lines = [
        "; ================================================================================================================",
        "IKBDHELP_test3",
        "                        ; ---",
        "                        ; prepare",
        "                        ;",
        "                        ; ---",
        "                        ; execute",
        "                        ;",
        "                        ikbd_withString         a6,#.ikbdStrBuffer",
        "                        ikbd_pushFirstByte      a6,#IKBD_CMD_MS_OFF",
        "                        ikbd_pushSecondByte     a6,#IKBD_CMD_ST_JS_EVT",
        "                        ; ---",
        "                        ; verify that IkbdString_length(a6) == 1",
        "                        ;",
        "                        moveq           #0,d0",
        "                        move.w          IkbdString_length(a6),d0",
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """* ================================================================================================================
              IKBDHELP_test3:
                              ; ---
                              ; prepare

                              ; ---
                              ; execute

                              ikbd_withString a6,#.ikbdStrBuffer
                              ikbd_pushFirstByte a6,#IKBD_CMD_MS_OFF
                              ikbd_pushSecondByte a6,#IKBD_CMD_ST_JS_EVT
                              ; ---
                              ; verify that IkbdString_length(a6) == 1

                              moveq #0,d0
                              move.w IkbdString_length(a6),d0
"""
        )


def test_that_it_forces_labels_at_first_position_for_macro_directives():
    """Bug report #6"""
    input_lines = [
        " Print: macro",
        " Print: macro.w",
        " Print: macro.l",
    ]
    baseArgs = ["prog"]
    with patch.object(sys, "argv", baseArgs):
        with patch.object(sys, "stdin", mockStdInput(input_lines)):
            with redirect_stdout(io.StringIO()) as out:
                returnCode = PrettyPrinterCli().run()
        assert returnCode == 0
        assert (
            out.getvalue()
            == """Print:                        macro
Print:                        macro.w
Print:                        macro.l
"""
        )
