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

    def renderLabel(self, line: StatementLine, stylesheet) -> str:
        """Render the label, INCLUDING A SEPARATING SPACE"""
        tabStop = stylesheet["tab_stops"]["labels"]["position"]
        marginWidth = stylesheet["labels"]["margin_space"]
        minimalLength = tabStop + marginWidth
        supplementalMarginOfShortLabels = (
            len(stylesheet["labels"]["postfix"])
            if stylesheet["labels"]["force_postfix"]
            or stylesheet["labels"]["align"] != "left"
            else 0
        )
        lenOfShortLabel = tabStop - supplementalMarginOfShortLabels

        if _is_empty_string(line.label):
            # no label
            return " " * (minimalLength)
        elif len(line.label) >= lenOfShortLabel:
            # long label
            postpadding = " " * marginWidth
            postfix = (
                stylesheet["labels"]["postfix"]
                if stylesheet["labels"]["force_postfix"]
                else ""
            )
            return f"{line.label}{postfix}{postpadding}"
        else:
            # short label
            align = stylesheet["labels"]["align"]
            if (
                align == "left"
                or line.mnemonic.lower()
                in stylesheet["labels"]["ignore_align_mnemonics"]
            ):
                padding = " " * (minimalLength)
                postfix = (
                    stylesheet["labels"]["postfix"]
                    if stylesheet["labels"]["force_postfix"]
                    else ""
                )
                return f"{line.label}{postfix}{padding}"[:minimalLength]
            else:
                padding = " " * (tabStop)
                postfix = stylesheet["labels"]["postfix"]
                postpadding = " " * marginWidth
                return f"{padding}{line.label}{postfix}{postpadding}"[-minimalLength:]

    def renderLineBody(
        self, line: StatementLine, stylesheet, lenOfRenderedLabel: int
    ) -> str:
        startPosition = (
            stylesheet["tab_stops"]["labels"]["position"]
            + stylesheet["labels"]["margin_space"]
        )
        tabStopOperands = stylesheet["tab_stops"]["operands"]["position"]
        widthOfMnemonics = tabStopOperands - startPosition
        tabStopsComments = stylesheet["tab_stops"]["comments"]["position"]
        widthOfOperands = tabStopsComments - tabStopOperands - 1
        widthOfOperation = tabStopsComments - startPosition

        if line.isNoOperation():
            return " " * widthOfOperation
        elif _is_empty_string(line.operands):
            postMnemonicsPadding = " " * widthOfOperation
            return (
                f"{line.mnemonic}"
                if len(line.mnemonic) >= widthOfMnemonics
                or len(line.mnemonic) + lenOfRenderedLabel >= tabStopsComments
                else f"{line.mnemonic}{postMnemonicsPadding}"[:widthOfOperation]
            )
        else:
            postMnemonicsPadding = " " * widthOfMnemonics
            mnemonicPart = (
                f"{line.mnemonic}"
                if len(line.mnemonic) >= widthOfMnemonics
                or len(line.mnemonic) + lenOfRenderedLabel >= tabStopOperands
                else f"{line.mnemonic}{postMnemonicsPadding}"[:widthOfMnemonics]
            )

            postOperandsPadding = " " * widthOfOperands
            return (
                f"{mnemonicPart} {line.operands}"
                if len({line.operands}) >= widthOfOperands
                or len(mnemonicPart) + 1 + len(line.operands) + lenOfRenderedLabel
                >= tabStopsComments
                else f"{mnemonicPart} {line.operands}{postOperandsPadding}"[
                    :widthOfOperation
                ]
            )

    def renderComment(self, line: StatementLine, stylesheet) -> str:
        if _is_empty_string(line.comment):
            return ""
        else:
            padding = " " * stylesheet["comments"]["margin_space"]
            prefix = stylesheet["comments"]["prefix"]
            toRender = line.comment
            return f"{padding}{prefix} {toRender}"

    def render(self, line: StatementLine, stylesheet) -> str:
        """Apply formatting rules"""
        if line.isEmpty():
            return ""
        if line.isCommentOnly() and self.commentBlockEnabled:
            prefix = " " * stylesheet["tab_stops"]["labels"]["position"]
            return f"{prefix} ; {line.comment}".rstrip()
        else:
            renderedLabel = self.renderLabel(line, stylesheet)
            renderedLineBody = self.renderLineBody(line, stylesheet, len(renderedLabel))
            renderedComment = self.renderComment(line, stylesheet)
            return f"{renderedLabel}{renderedLineBody}{renderedComment}".rstrip()
