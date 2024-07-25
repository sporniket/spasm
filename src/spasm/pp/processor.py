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

from .consts import MARKERS__COMMENT, WHITESPACES
from ._utils import _is_empty_string
from .statement_line import StatementLineParser, StatementLineRenderer


def is_comment_line(line: str) -> bool:
    return line[0] in MARKERS__COMMENT


def compute_next_tab(pos: int) -> int:
    return (pos + 4) // 4 * 4


def process_comment_line(line: str) -> str:
    body = line[1:]
    if _is_empty_string(body):
        # sanity check
        return ""

    prefix = "*" if body[0] == "*" else "* "
    current_pos = len(prefix)
    next_tab = compute_next_tab(current_pos)
    for i, c in enumerate(body):
        if c in WHITESPACES:
            if i == 0 and c == " ":
                continue  # first space has already been accounted for
            prefix = prefix + c if c == " " else (prefix + "    ")[0:next_tab]
            current_pos = len(prefix)
            next_tab = compute_next_tab(current_pos)
        else:
            body = body[i:]
            break
    return f"{prefix}{body}"


class SourceProcessor:
    def __init__(self):
        self._parser = StatementLineParser()
        self._renderer = StatementLineRenderer()

    ##############################################
    # Processing dispatcher
    ##############################################

    def process_line(self, line: str) -> str:
        cleaned_line = line.rstrip()
        if len(cleaned_line) == 0:
            # Sanity check, no need to do anything
            # -- except to manage block comments
            self._renderer.allowCommentBlock()
            return cleaned_line

        if is_comment_line(cleaned_line):
            self._renderer.allowCommentBlock()
            return process_comment_line(cleaned_line)

        statementLine = self._parser.parse(cleaned_line)
        if statementLine.isCommentedOperation():
            self._renderer.denyCommentBlock()
        elif statementLine.isEmpty() or statementLine.isOperationWithoutComment():
            self._renderer.allowCommentBlock()
        return self._renderer.render(statementLine)
