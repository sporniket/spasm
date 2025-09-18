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


class StatementLineParserListener:
    """Abstraction of a listenor for StatementLineParser."""

    def onStartOfLine(self, sourceLine: str):
        """Allows the listener to know the line of code that will be processed.

        Args:
            sourceLine (str): the line of code.
        """
        pass

    def onLabel(self, start: int, end: int):
        """Message received when a label field has been fully located.

        Args:
            start (int): start of the field in the line of code (included)
            end (int): end of the field in the line of code (excluded)
        """
        pass

    def onMnemonic(self, start: int, end: int):
        """Message received when a mnemonic field has been fully located.

        Args:
            start (int): start of the field in the line of code (included)
            end (int): end of the field in the line of code (excluded)
        """
        pass

    def onOperands(self, start: int, end: int):
        """Message received when a operands field has been fully located.

        Args:
            start (int): start of the field in the line of code (included)
            end (int): end of the field in the line of code (excluded)
        """
        pass

    def onComment(self, start: int, end: int):
        """Message received when a comment field has been fully located.

        Args:
            start (int): start of the field in the line of code (included)
            end (int): end of the field in the line of code (excluded)
        """
        pass

    def onEndOfLine(self) -> any:
        """Processing is done, returns something.

        Returns:
            any: the something returned depends on the implementation
        """
        pass
