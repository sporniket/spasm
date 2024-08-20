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

from ..consts import (
    MARKERS__COMMENT,
    MARKERS__STRING,
    MARKERS__LABEL,
    WHITESPACES,
)
from .model import StatementLine

# state machine states for parsing a statement line
ACCUMULATE_LABEL = 0  # when first character is not whitespace --> DONE_LABEL
WAIT_LABEL_OR_MNEMONIC = 1  # when first character is not whitespace, until not whitespace --> ACCUMULATE_LABEL_OR_MNEMONIC
ACCUMULATE_LABEL_OR_MNEMONIC = (
    2  # until ':' --> WAIT_MNEMONIC ; or until whitespace --> WAIT_OPERANDS_OR_COMMENT
)
WAIT_MNEMONIC = 4  # until not whitespace --> ACCUMULATE_MNEMONIC
ACCUMULATE_MNEMONIC = 5  # until whitespace --> WAIT_OPERANDS_OR_COMMENT
WAIT_OPERANDS_OR_COMMENT = 6  # until not whitespace --> ACCUMULATE_OPERANDS
ACCUMULATE_OPERANDS = (
    7  # should understand string litterals ; until whitespace --> WAIT_COMMENT_BODY
)
WAIT_COMMENT_OR_COMMENT_BODY = (
    8  # wait for comment marker or body --> ACCUMULATE_COMMENT
)
WAIT_COMMENT = 9  # wait for comment marker --> ACCUMULATE_COMMENT
WAIT_COMMENT_BODY = 10  # until not whitespace --> ACCUMULATE_COMMENT
ACCUMULATE_COMMENT = 11  # until end of line
INSIDE_STRING_LITTERAL = 12  # temporary state that waits for end of the string.


class StatementLineParser:
    def __init__(self):
        self._state = None

    def parse(self, line: str) -> StatementLine:
        result = StatementLine()
        accumulator = ""
        stringMarker = '"'
        escapeStringMarker = False
        for i, c in enumerate(line):
            if i == 0:
                if c not in WHITESPACES:
                    self._state = ACCUMULATE_LABEL
                    accumulator = c
                    result.label = accumulator
                else:
                    self._state = WAIT_LABEL_OR_MNEMONIC
                    accumulator = ""
                continue
            else:
                if self._state == ACCUMULATE_LABEL:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c in WHITESPACES or c in MARKERS__LABEL:
                        accumulator = ""
                        self._state = WAIT_MNEMONIC
                        continue
                    else:
                        accumulator += c
                        result.label = accumulator
                        continue
                elif self._state == WAIT_LABEL_OR_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_LABEL_OR_MNEMONIC
                        accumulator = c
                        result.mnemonic = accumulator  # until disambiguation
                        continue
                elif self._state == ACCUMULATE_LABEL_OR_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in MARKERS__LABEL:
                        result.label = accumulator
                        result.mnemonic = None  # disambiguation in favor of label
                        accumulator = ""
                        self._state = WAIT_MNEMONIC
                        continue
                    elif c in WHITESPACES:
                        accumulator = ""
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        continue
                    else:
                        accumulator += c
                        result.mnemonic = accumulator  # until disambiguation
                        continue
                elif self._state == WAIT_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_MNEMONIC
                        accumulator = c
                        result.mnemonic = accumulator
                        continue
                elif self._state == ACCUMULATE_MNEMONIC:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in WHITESPACES:
                        accumulator = ""
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        continue
                    else:
                        accumulator += c
                        result.mnemonic = accumulator
                        continue
                elif self._state == WAIT_OPERANDS_OR_COMMENT:
                    if c not in WHITESPACES:
                        if c in MARKERS__COMMENT:
                            self._state = WAIT_COMMENT_BODY
                            continue
                        else:
                            if c in MARKERS__STRING:
                                self._state = INSIDE_STRING_LITTERAL
                            else:
                                self._state = ACCUMULATE_OPERANDS
                            accumulator = c
                            result.operands = accumulator
                            continue
                elif self._state == ACCUMULATE_OPERANDS:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in MARKERS__STRING:
                        accumulator += c
                        stringMarker = c
                        escapeStringMarker = False
                        self._state == INSIDE_STRING_LITTERAL
                        continue
                    elif c in WHITESPACES:
                        self._state = WAIT_COMMENT_OR_COMMENT_BODY
                        accumulator = ""
                        continue
                    else:
                        accumulator += c
                        result.operands = accumulator
                        continue
                elif self._state == WAIT_COMMENT_OR_COMMENT_BODY:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        accumulator = c
                        self._state = ACCUMULATE_COMMENT
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
                        accumulator = c
                        result.comment = accumulator
                        continue
                elif self._state == ACCUMULATE_COMMENT:
                    accumulator += c
                    result.comment = accumulator
                    continue
                elif self._state == INSIDE_STRING_LITTERAL:
                    accumulator += c
                    result.operands = accumulator
                    if c == stringMarker:
                        self._state = ACCUMULATE_OPERANDS
                    continue
                else:
                    raise ValueError(
                        f"Unknown state '{self._state}' at position {i}, character '{c}' while parsing line of code : {line}"
                    )

        return result
