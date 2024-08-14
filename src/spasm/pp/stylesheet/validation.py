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
from typing import List

from .._utils import _is_empty_string


# *****************************************************************************
# STUB VALIDATION API
# -----------------------------------------------------------------------------
# This part could be extracted into its own library, provided a proper
# set of behavioral tests are written
# *****************************************************************************


# -----------------------------------
# Validators
# -----------------------------------
class Validator:
    """Base class of validators

    Defines the `message` property (read only).
    """

    @property
    def message(self):
        return self._message


def _get_value_from(path: str, source):
    """Basic tree walking
    ---
    `path` MUST be a dot separated value, e.g. "sub_name1.sub_name2.and.so.on"
    `source` MUST be defined (unless path is empty)

    For now, no support for integer index notation, e.g. "what.ever[2]"
    """
    valueRef = source
    for sub in path.split("."):
        valueRef = valueRef[sub]
    return valueRef


class GreaterThan(Validator):
    """Validates values that are STRICTLY greater than a provided int threshold.

    Constructor Args:
        value (int, optional): the threshold. Defaults to None.
        query (str, optional): when provided instead of `value`, a path in the context object, containing the threshold. Defaults to "".

    Raises:
        ValueError: when no value nor query is provided.
    """

    def __init__(self, *, value: int = None, query: str = ""):
        cleanQuery = query.strip()
        if value is None and _is_empty_string(cleanQuery):
            raise ValueError(f"Must provide value or query")
        pass
        self._value = value
        self._query = cleanQuery
        self._message = (
            f"MUST be > {self._query}"
            if self._value is None
            else f"MUST be > {self._value}"
        )

    def validate(self, value, context=None):
        if self._value is None:
            # extract value from context
            if context is None:
                return False
            valueRef = _get_value_from(self._query, context)
            return value > valueRef
        else:
            return value > self._value


class GreaterThanOrEqual(Validator):
    """Validates values that are greater than or equal to a provided int threshold.

    Constructor Args:
        value (int, optional): the threshold. Defaults to None.
        query (str, optional): when provided instead of `value`, a path in the context object, containing the threshold. Defaults to "".

    Raises:
        ValueError: when no value nor query is provided.
    """

    def __init__(self, *, value: int = None, query: str = ""):
        cleanQuery = query.strip()
        if value is None and _is_empty_string(cleanQuery):
            raise ValueError(f"Must provide value or query")
        pass
        self._value = value
        self._query = cleanQuery
        self._message = (
            f"MUST be >= {self._query}"
            if self._value is None
            else f"MUST be >= {self._value}"
        )

    def validate(self, value, context=None):
        if self._value is None:
            # extract value from context
            if context is None:
                return False
            valueRef = _get_value_from(self._query, context)
            return value >= valueRef
        else:
            return value >= self._value


class OneOf(Validator):
    """Validates values that are contained in a provided list of allowed values.

    Constructor Args:
        values (List[str]): the list of allowed values.

    Raises:
        ValueError: when no list is not provided or is empty.
    """

    def __init__(self, values: List[str]):
        if values is None or len(values) == 0:
            raise ValueError("Must provide non-empty list of allowed values")
        self._allowed = values
        valuesForMessage = list(map(lambda v: repr(v).replace("'", '"'), values))
        self._message = f"MUST be one of [{','.join(valuesForMessage)}]"

    def validate(self, value, context=None):
        return value in self._allowed


# -----------------------------------
# Schema description
# -----------------------------------
class Field:
    def __init__(self, *, doc: str = """""", typeOfValue, validator=None):
        self.doc = doc
        self.typeOfValue = typeOfValue
        self.validator = validator


class Structure:
    def __init__(self, *, doc: str = """""", body):
        self.doc = doc
        self.body = body


class Array:
    def __init__(self, *, doc: str = """""", typeOfItem, validator=None):
        self.doc = doc
        self.typeOfItem = typeOfItem
        self.validator = validator


# *****************************************************************************
# SCHEMA INSTANCIATION
# -----------------------------------------------------------------------------
# Starting from a json payload :
# * convert `{...}` into `Structure(body={...})
# * convert simple values into `Field(...)`
# * convert list values into `Array(...)`
#
# One MUST provide type of values and items, and MAY provides
# documentation strings on any structure, field or list.
# *****************************************************************************
SCHEMA_OF_STYLESHEET = Structure(
    doc="""""",
    body={
        "tab_stops": Structure(
            doc="""Specifies key positions inside the line, that are expected to be 
filled by the fields of a statement""",
            body={
                "labels": Structure(
                    doc="""""",
                    body={
                        "position": Field(
                            doc="""when the label is short enough -including the postfix if appliable-
or when it is empty, supplemental spaces are added up to this position ;
as much margin spaces as specified by the "labels" specification will be added
after this point.""",
                            typeOfValue=int,
                            validator=GreaterThanOrEqual(value=0),
                        )
                    },
                ),
                "mnemonic": Structure(
                    doc="""""",
                    body={
                        "position": Field(
                            doc="""when the mnemonics is short enough
or when it is empty, supplemental spaces are added up to this position.""",
                            typeOfValue=int,
                            validator=GreaterThanOrEqual(
                                query="tab_stops.labels.position"
                            ),
                        )
                    },
                ),
                "operands": Structure(
                    doc="""""",
                    body={
                        "position": Field(
                            doc="""when the operands is short enough
or when it is empty, supplemental spaces are added up to this position.""",
                            typeOfValue=int,
                            validator=GreaterThanOrEqual(
                                query="tab_stops.mnemonic.position"
                            ),
                        )
                    },
                ),
            },
        ),
        "tabulation": Structure(
            doc="""""",
            body={
                "width": Field(
                    doc="""in comment lines, leading tabulation are converted into spaces ; the number
                # of spaces per tabulation is defined here, and a the conversion add spaces until the nearest multiple
                # of the width to simulate the behaviour of a real tabulation.""",
                    typeOfValue=int,
                    validator=GreaterThan(value=0),
                )
            },
        ),
        "labels": Structure(
            doc="""""",
            body={
                "align": Field(
                    doc="""right alignment is done against the tab stop of labels.""",
                    typeOfValue=str,
                    validator=OneOf(["left", "right"]),
                ),
                "postfix": Field(doc="""""", typeOfValue=str, validator=OneOf([":"])),
                "margin_space": Field(
                    doc="""minimal number of space to have after the label and the postfix""",
                    typeOfValue=int,
                    validator=GreaterThan(value=0),
                ),
                "force_postfix": Field(
                    doc="""when set to true, left-aligned label WILL have a postfix """,
                    typeOfValue=bool,
                ),
                "ignore_align_mnemonics": Array(
                    doc="""list of mnemonics (string values) where the label MUST be aligned to the left.""",
                    typeOfItem=str,
                ),
            },
        ),
        "comment_lines": Structure(
            doc="""""",
            body={
                "prefix": Field(
                    doc="""""", typeOfValue=str, validator=OneOf(["*", ";"])
                )
            },
        ),
        "comments": Structure(
            doc="""""",
            body={
                "prefix": Field(
                    doc="""""", typeOfValue=str, validator=OneOf(["*", ";"])
                ),
                "margin_space": Field(
                    doc="""minimal number of space to have before the prefix""",
                    typeOfValue=int,
                    validator=GreaterThan(value=0),
                ),
            },
        ),
    },
)


# *****************************************************************************
# VALIDATION ENGINE
# -----------------------------------------------------------------------------
# The engine explore the given source object (restricted to fields listed in
# the schema) and emits events (especially error events).
# When a valid nested value is found in the source object, it is copied into
# the recipient object.
# Then it is expected to use only the resulting recipient object.
# *****************************************************************************


class ValidationEvent:
    def __init__(self, eventType, path, message):
        self.type = eventType
        self.path = path
        self.message = message


class ValidationAndCopyEngine:
    def __init__(self):
        pass

    def perform(
        self, schema, currentPath, objectFrom, recipient, context=None
    ) -> List[ValidationEvent]:
        result = []
        typeOfSchema = type(schema).__name__
        if typeOfSchema == "Structure":
            for sub in schema.body:
                if sub in objectFrom:
                    # There is something to copy
                    nextPath = f"{currentPath}.{sub}"
                    subSchema = schema.body[sub]
                    typeOfSubSchema = type(subSchema).__name__
                    if typeOfSubSchema == "Structure":
                        # dive one level
                        if sub not in recipient:
                            recipient[sub] = {}
                        result += [
                            ValidationEvent("ENTER", nextPath, f"Going inside {sub}")
                        ]
                        result += self.perform(
                            subSchema,
                            nextPath,
                            objectFrom[sub],
                            recipient[sub],
                            context,
                        )
                    elif typeOfSubSchema == "Field":
                        # copy value if valid
                        # TODO validation
                        # ---
                        # type validation :
                        gotType = type(objectFrom[sub]).__name__
                        expectedType = subSchema.typeOfValue.__name__
                        if gotType != expectedType:
                            result += [
                                ValidationEvent(
                                    "ERROR",
                                    nextPath,
                                    f"MUST be a {expectedType}",
                                )
                            ]

                        # ---
                        # value validation
                        if subSchema.validator is not None:
                            if not subSchema.validator.validate(
                                objectFrom[sub], context
                            ):
                                result += [
                                    ValidationEvent(
                                        "ERROR", nextPath, subSchema.validator.message
                                    )
                                ]
                                continue
                        recipient[sub] = objectFrom[sub]
                    elif typeOfSubSchema == "Array":
                        # copy array of value
                        # ---
                        # type validation
                        gotType = type(objectFrom[sub]).__name__
                        if gotType != "list":
                            result += [
                                ValidationEvent(
                                    "ERROR", nextPath, "MUST be an array of strings"
                                )
                            ]
                            continue

                        # ---
                        # item type validation
                        expectedType = subSchema.typeOfItem.__name__
                        for v in objectFrom[sub]:
                            if type(v).__name__ != expectedType:
                                result += [
                                    ValidationEvent(
                                        "ERROR",
                                        nextPath,
                                        f"MUST have {expectedType} items",
                                    )
                                ]
                                break

                        # ---
                        # actual copy
                        recipient[sub] = [v for v in objectFrom[sub]]
        else:
            result += [
                ValidationEvent(
                    "ERROR",
                    currentPath,
                    f"CANNOT work on given schema of type {typeOfSchema}",
                )
            ]
        return result
