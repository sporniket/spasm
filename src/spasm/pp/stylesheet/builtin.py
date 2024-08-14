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

SPORNIKET = {
    "tab_stops": {
        "labels": {"position": 30},
        "mnemonic": {"position": 30},
        "operands": {"position": 50},
    },
    "tabulation": {"width": 4},
    "labels": {
        "align": "right",
        "postfix": ":",
        "margin_space": 1,
        "force_postfix": True,
        "ignore_align_mnemonics": ["macro", "macro.w", "macro.l"],
    },
    "comment_lines": {"prefix": "*"},
    "comments": {"prefix": ";", "margin_space": 1},
}

HERITAGE = {
    "tab_stops": {
        "labels": {"position": 16},
        "mnemonic": {"position": 24},
        "operands": {"position": 32},
    },
    "tabulation": {"width": 8},
    "labels": {
        "align": "left",
        "postfix": ":",
        "margin_space": 1,
        "force_postfix": False,
        "ignore_align_mnemonics": None,
    },
    "comment_lines": {"prefix": "*"},
    "comments": {"prefix": ";", "margin_space": 1},
}
