"""
DUMMY VALIDATION API/MODELIZATION
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
import types
import typing

# STUB VALIDATION API
class Validator:
    pass

class GreaterThan(Validator):
    def __init__(self,*,value:int,query:str=""):
        pass

class OneOf(Validator):
    def __init__(self,values:List[str]):
        pass


class Field:
    def __init__(self,*,doc:str="""""",type:type, validator=None):
        pass

class Structure:
    def __init__(self,*, doc:str="""""", body):
        pass

# SCHEMA INSTANCIATION
SCHEMA_OF_STYLESHEET = Structure(doc="""""",body={
    "tab_stops": Structure(doc="""Specifies key positions inside the line, that are expected to be 
filled by the fields of a statement""",body={
        "labels":Structure(doc="""""",body={
            "position":Field(doc="""when the label is short enough -including the postfix if appliable-
or when it is empty, supplemental spaces are added up to this position ;
as much margin spaces as specified by the "labels" specification will be added
after this point.""",type=int, validator=GreaterThan(value=0))
        }),
        "mnemonic": Structure(doc="""""",body={
            "position":Field(doc="""when the mnemonics is short enough
or when it is empty, supplemental spaces are added up to this position.""",type=int, validator=GreaterThan(query="tab_stops.labels")) 
        }),
        "operands": Structure(doc="""""",body={
            "position":Field(doc="""when the operands is short enough
or when it is empty, supplemental spaces are added up to this position.""",type=int, validator=GreaterThan(query="tab_stops.mnemonic")) 
        })
    }),
    "tabulation": Structure(doc="""""",body={
        "width":Field(doc="""in comment lines, leading tabulation are converted into spaces ; the number
                # of spaces per tabulation is defined here, and a the conversion add spaces until the nearest multiple
                # of the width to simulate the behaviour of a real tabulation.""",type=int, validator=GreaterThan(value=0))
    }),
    "labels": Structure(doc="""""",body={
        "align":Field(doc="""right alignment is done against the tab stop of labels.""",type=str, validator=OneOf(["left","right"])), 
        "postfix":Field(doc="""""",type=str, validator=OneOf([":"])),
        "margin_space":Field(doc="""minimal number of space to have after the label and the postfix""",type=int, validator=GreaterThan(value=0)),
        "force_postfix":Field(doc="""when set to true, left-aligned label WILL have a postfix """,type=boolean),
        "ignore_align_mnemonics":Array(doc="""list of mnemonics (string values) where the label MUST be aligned to the left.""",itemType=string,validator=NotEmpty())
    }),
    "comment_lines": Structure(doc="""""",body={
        "prefix":Field(doc="""""",type=str, validator=OneOf(["*",";"]))
    }),
    "comments": Structure(doc="""""",body={
        "prefix":Field(doc="""""",type=str, validator=OneOf(["*",";"])),
        "margin_space":Field(doc="""minimal number of space to have before the prefix""",type=int, validator=GreaterThan(value=0))
    })
})