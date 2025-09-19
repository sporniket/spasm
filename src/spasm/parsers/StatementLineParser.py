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

from .consts import (
    MARKERS__COMMENT,
    MARKERS__STRING,
    MARKERS__LABEL,
    WHITESPACES,
)
from .StatementLineParserListener import StatementLineParserListener

# state machine states for parsing a statement line
ACCUMULATE_LABEL = 0  # when first character is not whitespace --> WAIT_MNEMONIC
WAIT_LABEL_OR_MNEMONIC = 1  # when first character is not whitespace, until not whitespace --> ACCUMULATE_LABEL_OR_MNEMONIC
ACCUMULATE_LABEL_OR_MNEMONIC = (
    2  # until ':' --> WAIT_MNEMONIC ; or until whitespace --> WAIT_OPERANDS_OR_COMMENT
)
WAIT_MNEMONIC = 4  # until not whitespace --> ACCUMULATE_MNEMONIC
ACCUMULATE_MNEMONIC = 5  # until whitespace --> WAIT_OPERANDS_OR_COMMENT
WAIT_OPERANDS_OR_COMMENT = 6  # until not whitespace --> ACCUMULATE_OPERANDS
ACCUMULATE_OPERANDS = 7  # should understand string litterals ; until whitespace --> WAIT_COMMENT_OR_COMMENT_BODY
WAIT_COMMENT_OR_COMMENT_BODY = (
    8  # wait for comment marker or body --> ACCUMULATE_COMMENT
)
WAIT_COMMENT = 9  # wait for comment marker --> ACCUMULATE_COMMENT
WAIT_COMMENT_BODY = 10  # until not whitespace --> ACCUMULATE_COMMENT
ACCUMULATE_COMMENT = 11  # until end of line
INSIDE_STRING_LITTERAL = 12  # temporary state that waits for end of the string.


class StatementLineParser:
    """An ISA-agnostic statement line parser to locate the various fields of an assembly line of code.

    The 4 identifiables fields are : the label, the mnemonic, the operands and the comment.
    """

    def __init__(self):
        self._state = None
        self._listener = None

    @property
    def listener(self) -> StatementLineParserListener:
        return self._listener

    @listener.setter
    def listener(self, l: StatementLineParserListener):
        self._listener = l

    def parse(self, line: str) -> any:
        """Performs the actual parsing of a line, notifies a listener and returns the result of the later.

        Args:
            line (str): the line of code to parse
            listener (StatementLineParserEventListener, optional): the listener that will be notified, to perform actual processing. Defaults to StatementLineBuilderOnParse().

        Raises:
            ValueError: when the parser has a problem.

        Returns:
            any: whatever returns the listener.
        """
        listener = self.listener
        if listener is None:
            raise ValueError("no.listener")
        listener.onStartOfLine(line)
        start = 0
        stringMarker = '"'
        escapeStringMarker = False
        for i, c in enumerate(line):
            if i == 0:
                if c in MARKERS__COMMENT:
                    self._state = WAIT_COMMENT_BODY
                elif c not in WHITESPACES:
                    self._state = ACCUMULATE_LABEL
                else:
                    self._state = WAIT_LABEL_OR_MNEMONIC
                continue
            else:
                if self._state == ACCUMULATE_LABEL:
                    if c in MARKERS__COMMENT:
                        listener.onLabel(start, i)
                        self._state = WAIT_COMMENT_BODY
                        start = i
                        continue
                    elif c in WHITESPACES or c in MARKERS__LABEL:
                        listener.onLabel(start, i)
                        self._state = WAIT_MNEMONIC
                        start = i
                        continue
                    else:
                        continue
                elif self._state == WAIT_LABEL_OR_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_LABEL_OR_MNEMONIC
                        start = i
                        continue
                elif self._state == ACCUMULATE_LABEL_OR_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        listener.onMnemonic(
                            start, i
                        )  # disambiguation in favor of mnemonic
                        self._state = WAIT_COMMENT_BODY
                        start = i
                        continue
                    if c in MARKERS__LABEL:
                        listener.onLabel(start, i)  # disambiguation in favor of label
                        self._state = WAIT_MNEMONIC
                        start = i
                        continue
                    elif c in WHITESPACES:
                        listener.onMnemonic(
                            start, i
                        )  # disambiguation in favor of mnemonic
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        start = i
                        continue
                    else:
                        continue
                elif self._state == WAIT_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_MNEMONIC
                        start = i
                        continue
                elif self._state == ACCUMULATE_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        listener.onMnemonic(start, i)
                        self._state = WAIT_COMMENT_BODY
                        start = i
                        continue
                    if c in WHITESPACES:
                        listener.onMnemonic(start, i)
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        start = i
                        continue
                    else:
                        continue
                elif self._state == WAIT_OPERANDS_OR_COMMENT:
                    if c not in WHITESPACES:
                        if c in MARKERS__COMMENT:
                            self._state = WAIT_COMMENT_BODY
                            continue
                        else:
                            if c in MARKERS__STRING:
                                start = i
                                self._state = INSIDE_STRING_LITTERAL
                            else:
                                self._state = ACCUMULATE_OPERANDS
                                start = i
                            continue
                elif self._state == ACCUMULATE_OPERANDS:
                    if c in MARKERS__COMMENT:
                        listener.onOperands(start, i)
                        self._state = WAIT_COMMENT_BODY
                        start = i
                        continue
                    if c in MARKERS__STRING:
                        stringMarker = c
                        escapeStringMarker = False
                        self._state == INSIDE_STRING_LITTERAL
                        continue
                    elif c in WHITESPACES:
                        listener.onOperands(start, i)
                        self._state = WAIT_COMMENT_OR_COMMENT_BODY
                        start = i
                        continue
                    else:
                        continue
                elif self._state == WAIT_COMMENT_OR_COMMENT_BODY:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_COMMENT
                        start = i
                        continue
                    else:
                        continue
                elif self._state == WAIT_COMMENT:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                elif self._state == WAIT_COMMENT_BODY:
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_COMMENT
                        start = i
                        continue
                elif self._state == ACCUMULATE_COMMENT:
                    continue
                elif self._state == INSIDE_STRING_LITTERAL:
                    if c == stringMarker:
                        self._state = ACCUMULATE_OPERANDS
                    continue
                else:
                    raise ValueError(
                        f"Unknown state '{self._state}' at position {i}, character '{c}' while parsing line of code : {line}"
                    )
        if self._state == ACCUMULATE_LABEL:
            listener.onLabel(start, len(line))
        elif (
            self._state == ACCUMULATE_LABEL_OR_MNEMONIC
            or self._state == ACCUMULATE_MNEMONIC
        ):
            listener.onMnemonic(start, len(line))
        elif self._state == ACCUMULATE_OPERANDS:
            listener.onOperands(start, len(line))
        elif self._state == ACCUMULATE_COMMENT:
            listener.onComment(start, len(line))
        return listener.onEndOfLine()
