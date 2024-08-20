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

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .processor import SourceProcessor
from .stylesheet.builtin import SPORNIKET, HERITAGE
from .stylesheet.loader import StylesheetLoader
from ._utils import _is_empty_string


class PrettyPrinterCli:
    @staticmethod
    def createArgParser() -> ArgumentParser:
        parser = ArgumentParser(
            prog="python3 -m spasm.pp",
            description="Pretty prints a source file written in assembly language.",
            epilog="""---
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
""",
            formatter_class=RawDescriptionHelpFormatter,
            allow_abbrev=False,
        )

        # Add the arguments
        parser.add_argument(
            "--stylesheet",
            metavar="<stylesheet>",
            type=str,
            help="the formatting rules to follow, either 'builtin:heritage' (the default) or 'builtin:sporniket'",
        )

        parser.add_argument(
            "sources",
            metavar="<source files...>",
            type=str,
            nargs="*",
            help="a list of source files",
        )

        commandGroup = parser.add_mutually_exclusive_group(required=False)
        commandGroup.add_argument(
            "-r",
            "--rewrite",
            action="store_true",
            help=f"Replace the source files by their pretty-printed version WHEN THERE IS A DIFFERENCE.",
        )

        return parser

    def __init__(self):
        self._processor = SourceProcessor()

    def processLine(self, line: str, stylesheet):
        print(self._processor.process_line(line, stylesheet))

    def retrieveStyleSheet(self, stylesheetSpec: str):
        ERROR = ValueError(
            f"ERROR -- wrong value '{stylesheetSpec}' for parameter 'stylesheet'"
        )

        specKindMarkPosition = stylesheetSpec.find(":")
        if specKindMarkPosition < 0:
            raise ERROR

        specKind = stylesheetSpec[:specKindMarkPosition]
        if specKind not in ["builtin", "file"]:
            raise ERROR

        specValue = stylesheetSpec[specKindMarkPosition + 1 :]
        if specKind == "builtin":
            if specValue == "sporniket":
                return SPORNIKET
            elif specValue == "heritage":
                return HERITAGE
            else:
                raise ERROR
        elif specKind == "file":
            return StylesheetLoader(specValue).perform()
        else:
            raise ERROR

    def run(self):
        try:
            args = PrettyPrinterCli.createArgParser().parse_args()
            stylesheet = (
                HERITAGE
                if _is_empty_string(args.stylesheet)
                else self.retrieveStyleSheet(args.stylesheet)
            )
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        else:
            if len(args.sources) > 0:
                # EITHER process given list of files...
                sourcesErrors = []

                # -- Check the list of files
                for source in args.sources:
                    if os.path.exists(source):
                        if os.path.isfile(source):
                            # NO PROBLEM
                            continue
                        else:
                            sourcesErrors += [
                                {"errorType": "NOT_A_FILE", "path": source}
                            ]
                    else:
                        sourcesErrors += [{"errorType": "MISSING_FILE", "path": source}]
                if len(sourcesErrors) > 0:
                    report = []
                    for e in sourcesErrors:
                        message = (
                            f"* MISSING : {e['path']}"
                            if e["errorType"] == "MISSING_FILE"
                            else f"* NOT A FILE : {e['path']}"
                        )
                        report += [message]
                    report = "\n".join(report)
                    print(
                        f"ERROR -- in given list of files :\n{report}", file=sys.stderr
                    )
                    return 1

                # -- Proceed
                for source in args.sources:
                    with open(source, "rt") as f:
                        lines = f.readlines()
                    if args.rewrite:
                        # Rewrite mode
                        result = []
                        isDifferent = False
                        for line in lines:
                            # -- remove trailing "\n"
                            # -- because it triggers false difference
                            sourceLine = line[:-1] if line.endswith("\n") else line
                            processedLine = self._processor.process_line(
                                sourceLine, stylesheet
                            )
                            result += [processedLine]
                            isDifferent = isDifferent or processedLine != sourceLine
                        if isDifferent:
                            with open(source, "wt") as f:
                                f.write("\n".join(result))
                                f.write("\n")
                    else:
                        # Normal mode
                        for line in lines:
                            self.processLine(line, stylesheet)
                        print("")
            else:
                # ...OR process standard input

                # -- unless it is rewrite mode
                if args.rewrite:
                    print(
                        "ERROR -- rewrite mode requires a list of files",
                        file=sys.stderr,
                    )
                    return 1

                # -- Proceed
                for line in sys.stdin:
                    self.processLine(line, stylesheet)

            return 0
