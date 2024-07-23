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

MARKERS__COMMENT = [";", "*"]
MARKERS__STRING = ['"', "'"]
MARKERS__LABEL = [":"]
WHITESPACES = [" ", "\t"]
DIRECTIVES__MACRO = ["macro", "macro.w", "macro.l"]


def is_comment_line(line: str) -> bool:
    return line[0] in MARKERS__COMMENT


def compute_next_tab(pos: int) -> int:
    return (pos + 4) // 4 * 4


def process_comment_line(line: str) -> str:
    body = line[1:]
    if is_empty_string(body):
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


def process_line(line: str) -> str:
    cleaned_line = line.rstrip()
    if len(cleaned_line) == 0:
        # Sanity check, no need to do anything
        return cleaned_line
    if is_comment_line(cleaned_line):
        return process_comment_line(cleaned_line)
    return cleaned_line


def is_empty_string(s: str) -> bool:
    return True if s == None or len(s) == 0 else False


# state machine states for parsing a statement line
ACCUMULATE_LABEL = 0  # when first character is not whitespace --> DONE_LABEL
WAIT_LABEL_OR_MNEMONICS = 1  # when first character is not whitespace, until not whitespace --> ACCUMULATE_LABEL_OR_MNEMONICS
ACCUMULATE_LABEL_OR_MNEMONICS = (
    2  # until ':' --> DONE_LABEL ; or until whitespace --> WAIT_OPERANDS_OR_COMMENT
)
DONE_LABEL = 3  # when accumulating label (':' optionnal), or accumulating "label or mnemonics" (requires ':') --> WAIT_MNEMONICS
WAIT_MNEMONICS = 4  # until not whitespace --> ACCUMULATE_MNEMONICS
ACCUMULATE_MNEMONICS = 5  # until whitespace --> WAIT_OPERANDS_OR_COMMENT
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


class StatementLine:
    """Model of a statement line
    ---
    A line parser would extract the various parts of a statement line and set them up inside this model.

    Then a renderer can process a model instance to perform a pretty print."""

    def __init__(self):
        self._label = None
        self._mnemonic = None
        self._operands = None
        self._comment = None

    ##############################################
    # Label part
    ##############################################

    @property
    def label(self) -> str:
        """The label part of the line, without any marker"""
        return self._label if self._label is not None else ""

    @label.setter
    def label(self, value: str):
        self._label = value

    ##############################################
    # Mnemonic part
    ##############################################

    @property
    def mnemonic(self) -> str:
        """The mnemonic part of the line."""
        return self._mnemonic if self._mnemonic is not None else ""

    @mnemonic.setter
    def mnemonic(self, value: str):
        self._mnemonic = value

    ##############################################
    # Operands part
    ##############################################

    @property
    def operands(self) -> str:
        """The operands list."""
        return self._operands if self._operands is not None else ""

    @operands.setter
    def operands(self, value: str):
        self._operands = value

    ##############################################
    # Comment part
    ##############################################

    @property
    def comment(self) -> str:
        """The comment line, without any marker and whitespace striped on both ends"""
        return self._comment if self._comment is not None else ""

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    ##############################################
    # Queries
    ##############################################

    def isEmpty(self) -> bool:
        return (
            is_empty_string(self.comment)
            and is_empty_string(self.label)
            and is_empty_string(self.mnemonic)
            and is_empty_string(self.operands)
        )

    def isCommentOnly(self) -> bool:
        return (
            not is_empty_string(self.comment)
            and is_empty_string(self.label)
            and is_empty_string(self.mnemonic)
            and is_empty_string(self.operands)
        )

    def isCommentedOperation(self) -> bool:
        return not is_empty_string(self.mnemonic) and not is_empty_string(self.comment)

    def isOperationWithoutComment(self) -> bool:
        return not is_empty_string(self.mnemonic) and is_empty_string(self.comment)

    def isMacroDeclaration(self) -> bool:
        m = self.mnemonic.lower()
        return m in DIRECTIVES__MACRO


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
                    self._state = WAIT_LABEL_OR_MNEMONICS
                    accumulator = ""
                continue
            else:
                if self._state == ACCUMULATE_LABEL:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c in WHITESPACES or c in MARKERS__LABEL:
                        accumulator = ""
                        self._state = WAIT_MNEMONICS
                        continue
                    else:
                        accumulator += c
                        result.label = accumulator
                        continue
                elif self._state == WAIT_LABEL_OR_MNEMONICS:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    elif c not in WHITESPACES:
                        self._state = ACCUMULATE_LABEL_OR_MNEMONICS
                        accumulator = c
                        result.mnemonic = accumulator  # until disambiguation
                        continue
                elif self._state == ACCUMULATE_LABEL_OR_MNEMONICS:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c in MARKERS__LABEL:
                        result.label = accumulator
                        result.mnemonic = None  # disambiguation in favor of label
                        accumulator = ""
                        self._state = WAIT_MNEMONICS
                        continue
                    elif c in WHITESPACES:
                        accumulator = ""
                        self._state = WAIT_OPERANDS_OR_COMMENT
                        continue
                    else:
                        accumulator += c
                        result.mnemonic = accumulator  # until disambiguation
                        continue
                elif self._state == DONE_LABEL:
                    # seems useless
                    raise NotImplementedError(
                        f"Not yet implemented state '{self._state}' at position {i}, character '{c}' while parsing line of code : {line}"
                    )
                elif self._state == WAIT_MNEMONICS:
                    if c in MARKERS__COMMENT:
                        self._state = WAIT_COMMENT_BODY
                        continue
                    if c not in WHITESPACES:
                        self._state = ACCUMULATE_MNEMONICS
                        accumulator = c
                        result.mnemonic = accumulator
                        continue
                elif self._state == ACCUMULATE_MNEMONICS:
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
        if is_empty_string(line.label):
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
        if is_empty_string(lineBody):
            return "                     "
        elif len(lineBody) >= 20:
            return f"{lineBody} "
        else:
            paddedLineBody = f"{lineBody}                    "[:20]
            return f"{paddedLineBody} "

    def renderComment(self, line: StatementLine) -> str:
        if is_empty_string(line.comment):
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
