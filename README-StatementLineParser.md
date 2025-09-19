# StatementLineParser

## Overview

This parser locate the four fields that MAY be found in a line of code from an assembly source : 

* the _label_ part, 
* the _mnemonic_ part,
* the _operands_ part,
* the _comment_ part.

This parser uses a light implementation of the [Observer](https://refactoring.guru/design-patterns/observer) pattern to delegate the handling of a field when it is spotted.

## Usage

The parser requires an implementation of `StatementLineParserListener`. This implementation MUST return an object that will contain the information about the various fields of a line of assembly code, in whatever fashion that you want. _See `StatementLineParserListener.onEndOfLine()`_


Then, simply call the `parse(lineOfCode)` on each line of code to get.

## Typical application

The following code is a summary of how `pp` actually uses `StatementLineParser`.

```py
from spasm.parsers import StatementLineParser, StatementLineParserListener

@dataclass
class StatementLine:
    label: str = field(default_factory=str)
    mnemonic: str = field(default_factory=str)
    operands: str = field(default_factory=str)
    comment: str = field(default_factory=str)

class StatementLineBuilderOnParse(StatementLineParserListener):
    def onStartOfLine(self, sourceLine: str):
        self._currentLineContent = sourceLine
        self._wipStatement = StatementLine()

    def onLabel(self, start: int, end: int):
        self._wipStatement.label = self._currentLineContent[start:end]

    def onMnemonic(self, start: int, end: int):
        self._wipStatement.mnemonic = self._currentLineContent[start:end]

    def onOperands(self, start: int, end: int):
        self._wipStatement.operands = self._currentLineContent[start:end]

    def onComment(self, start: int, end: int):
        self._wipStatement.comment = self._currentLineContent[start:end]

    def onEndOfLine(self) -> any:
        self._currentLineContent = None
        return self._wipStatement

def processSourceLines(lines:list[str])->list[StatementLine]:
    parser = StatementLineParser()
    parser.listener = StatementLineBuilderOnParse()
    return [parser.parse(l) for l in lines]

```