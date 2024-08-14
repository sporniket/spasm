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

import copy
import json
import os

from .builtin import HERITAGE
from .validation import SCHEMA_OF_STYLESHEET, ValidationAndCopyEngine


class StylesheetLoader:
    def __init__(self, pathToFile: str, *, reference=HERITAGE):
        if not os.path.isfile(pathToFile):
            raise ValueError(f"File not found or not a regular file : {pathToFile}")
        self._sourceFile = pathToFile
        self._reference = reference

    def perform(self):
        result = copy.deepcopy(self._reference)

        with open(self._sourceFile) as sourceJson:
            source = json.load(sourceJson)

        # copy existing supported values from source to result
        # TODO
        events = ValidationAndCopyEngine().perform(
            SCHEMA_OF_STYLESHEET, "<ROOT>", source, result, source
        )
        errors = list(
            map(
                lambda e: f"* {e.path[len('<ROOT>.'):]} {e.message}",
                list(filter(lambda e: e.type == "ERROR", events)),
            )
        )

        if len(errors) > 0:
            listOfErrors = "\n".join(errors)
            raise ValueError(
                f"ERROR -- Wrong values in stylesheet '{self._sourceFile}' : \n{listOfErrors}"
            )

        return result
