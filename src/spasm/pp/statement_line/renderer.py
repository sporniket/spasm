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
        # REMOVE minimalLength = tabStop - marginWidth
        isLeftAlign = stylesheet["labels"]["align"] == "left"
        isRightAlign = ~isLeftAlign
        supplementalMarginOfShortLabels = (
            len(stylesheet["labels"]["postfix"])
            if stylesheet["labels"]["force_postfix"] or isRightAlign
            else 0
        )
        lenOfShortLabel = tabStop - supplementalMarginOfShortLabels - marginWidth

        if _is_empty_string(line.label):
            # no label
            return " " * (tabStop)
        elif len(line.label) > lenOfShortLabel:
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
                isLeftAlign
                or line.mnemonic.lower()
                in stylesheet["labels"]["ignore_align_mnemonics"]
            ):
                padding = " " * (tabStop)
                postfix = (
                    stylesheet["labels"]["postfix"]
                    if stylesheet["labels"]["force_postfix"]
                    else ""
                )
                return f"{line.label}{postfix}{padding}"[:tabStop]
            else:
                padding = " " * (tabStop)
                postfix = stylesheet["labels"]["postfix"]
                postpadding = " " * marginWidth
                return f"{padding}{line.label}{postfix}{postpadding}"[-tabStop:]

    def renderLineBody(
        self,
        line: StatementLine,
        stylesheet,
        endOfLabel: int,
        previousSpacing: int = 0,
    ) -> str:
        requiredSpacing = stylesheet["labels"]["margin_space"] - previousSpacing
        padding = " " * requiredSpacing if requiredSpacing > 0 else ""
        startPosition = stylesheet["tab_stops"]["labels"]["position"]
        tabStopMnemonic = stylesheet["tab_stops"]["mnemonic"]["position"]
        tabStopsOperands = stylesheet["tab_stops"]["operands"]["position"]

        # Verify and adjust each position
        if startPosition < endOfLabel:
            startPosition = endOfLabel
        if tabStopMnemonic < startPosition:
            tabStopMnemonic = startPosition
        if tabStopsOperands < tabStopMnemonic:
            tabStopsOperands = tabStopMnemonic
        widthOfMnemonic = tabStopMnemonic - startPosition
        widthOfOperands = tabStopsOperands - tabStopMnemonic
        widthOfOperation = tabStopsOperands - startPosition

        if line.isNoOperation():
            return " " * widthOfOperation
        elif _is_empty_string(line.operands):
            rendered = f"{padding}{line.mnemonic}"
            postMnemonicPadding = " " * widthOfOperation
            return (
                rendered
                if len(rendered) >= widthOfOperation
                else f"{rendered}{postMnemonicPadding}"[:widthOfOperation]
            )
        else:
            postMnemonicPadding = " " * widthOfMnemonic
            rendered = f"{padding}{line.mnemonic}"
            mnemonicPart = (
                rendered
                if len(rendered) >= widthOfMnemonic
                else f"{rendered}{postMnemonicPadding}"[:widthOfMnemonic]
            )

            postOperandsPadding = " " * widthOfOperands
            paddingOperands = (
                " " if len(mnemonicPart.rstrip()) == len(mnemonicPart) else ""
            )
            rendered = f"{mnemonicPart}{paddingOperands}{line.operands}"
            return (
                rendered
                if len(rendered) >= widthOfOperation
                else f"{rendered}{postOperandsPadding}"[:widthOfOperation]
            )

    def renderComment(
        self, line: StatementLine, stylesheet, previousSpacing: int = 0
    ) -> str:
        if _is_empty_string(line.comment):
            return ""
        else:
            requiredSpacing = stylesheet["comments"]["margin_space"] - previousSpacing
            padding = " " * requiredSpacing if requiredSpacing > 0 else ""
            prefix = stylesheet["comments"]["prefix"]
            toRender = line.comment
            return f"{padding}{prefix} {toRender}"

    def render(self, line: StatementLine, stylesheet) -> str:
        """Apply formatting rules"""
        if line.isEmpty():
            return ""
        if line.isCommentOnly() and self.commentBlockEnabled:
            prefix = " " * stylesheet["tab_stops"]["labels"]["position"]
            renderedComment = self.renderComment(line, stylesheet, len(prefix))
            return f"{prefix}{renderedComment}".rstrip()
        else:
            renderedLabel = self.renderLabel(line, stylesheet)
            startOfLineBody = len(renderedLabel)
            spacingBeforeLineBody = startOfLineBody - len(renderedLabel.rstrip())
            renderedLineBody = self.renderLineBody(
                line, stylesheet, startOfLineBody, spacingBeforeLineBody
            )
            spacingBeforeComment = (
                spacingBeforeLineBody
                if line.isNoOperation()
                else len(renderedLineBody) - len(renderedLineBody.rstrip())
            )
            renderedComment = self.renderComment(line, stylesheet, spacingBeforeComment)
            return f"{renderedLabel}{renderedLineBody}{renderedComment}".rstrip()
