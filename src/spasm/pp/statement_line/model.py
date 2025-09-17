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

from dataclasses import dataclass, field
from .._utils import _is_empty_string


@dataclass
class StatementLine:
    """Model of a statement line
    ---
    A line parser would extract the various parts of a statement line and set them up inside this model.

    Then a renderer can process a model instance to perform a pretty print."""

    label: str = field(default_factory=str)
    """The label part of the line, without any marker"""

    mnemonic: str = field(default_factory=str)
    """The mnemonic part of the line."""

    operands: str = field(default_factory=str)
    """The operands list part of the line."""

    comment: str = field(default_factory=str)
    """The comment part of the line, without any marker and whitespace striped on both ends"""

    ##############################################
    # Queries
    ##############################################

    def isEmpty(self) -> bool:
        return (
            _is_empty_string(self.comment)
            and _is_empty_string(self.label)
            and _is_empty_string(self.mnemonic)
            and _is_empty_string(self.operands)
        )

    def isCommentOnly(self) -> bool:
        return (
            not _is_empty_string(self.comment)
            and _is_empty_string(self.label)
            and _is_empty_string(self.mnemonic)
            and _is_empty_string(self.operands)
        )

    def isCommentedOperation(self) -> bool:
        return not _is_empty_string(self.mnemonic) and not _is_empty_string(
            self.comment
        )

    def isNoOperation(self) -> bool:
        return _is_empty_string(self.mnemonic) and _is_empty_string(self.operands)

    def isOperationWithoutComment(self) -> bool:
        return not _is_empty_string(self.mnemonic) and _is_empty_string(self.comment)
