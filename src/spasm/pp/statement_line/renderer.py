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

from .._utils import _is_empty_string
from .model import StatementLine


class StatementLineRenderer:
    def __init__(self):
        self.allowCommentBlock()  # the first statement lines containing only comments will be starting at position #30

    ##############################################
    # Management of statement lines containing only comments
    ##############################################

    @property
    def commentBlockEnabled(self) -> bool:
        """Management of statement lines containing only comments
        ---
        * when True, a comment-only statement line will start at position 30
        * when False, a comment-only statement line will start at position 50"""
        return self._commentBlockEnabled

    def denyCommentBlock(self):
        """From now statement lines containing only comments start at position 50"""
        self._commentBlockEnabled = False

    def allowCommentBlock(self):
        """From now statement lines containing only comment start at position 30"""
        self._commentBlockEnabled = True

    def renderLabel(self, line: StatementLine) -> str:
        if _is_empty_string(line.label):
            return "                              "
        elif len(line.label) >= 28:
            return f"{line.label}: "
        else:
            return (
                f"{line.label}:                             "[:30]
                if line.isMacroDeclaration()
                else f"                            {line.label}: "[-30:]
            )

    def renderLineBody(self, line: StatementLine) -> str:
        lineBody = f"{line.mnemonic} {line.operands}".rstrip()
        if _is_empty_string(lineBody):
            return "                     "
        elif len(lineBody) >= 20:
            return f"{lineBody} "
        else:
            paddedLineBody = f"{lineBody}                    "[:20]
            return f"{paddedLineBody} "

    def renderComment(self, line: StatementLine) -> str:
        if _is_empty_string(line.comment):
            return ""
        else:
            toRender = line.comment
            return f"; {toRender}"

    def render(self, line: StatementLine) -> str:
        """Apply formatting rules"""
        if line.isEmpty():
            return ""
        if line.isCommentOnly() and self.commentBlockEnabled:
            return f"                              ; {line.comment}".rstrip()
        else:
            return (
                self.renderLabel(line)
                + self.renderLineBody(line)
                + self.renderComment(line)
            ).rstrip()
