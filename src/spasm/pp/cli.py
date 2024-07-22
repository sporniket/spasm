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

import sys

from .processor import process_line, SourceProcessor


class PrettyPrinterCli:
    def __init__(self):
        self._processor = SourceProcessor()

    def processLine(self, line: str):
        print(self._processor.process_line(line))

    def run(self):
        for line in sys.stdin:
            self.processLine(line)

        return 0

    def runTMP(self):
        if len(args.sources) > 0:
            for source in args.sources:
                if source == "-":
                    for line in sys.stdin:
                        self.processLine(line)
                else:
                    with open(source, "rt") as f:
                        lines = f.readlines()
                    for line in lines:
                        self.processLine(line)
        else:
            for line in sys.stdin:
                self.processLine(line)

        return 0
