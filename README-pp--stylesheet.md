# Stylesheet specification for the Pretty Printer

A stylesheet for the pretty printer is a JSON file.

## A sample, fully defined stylesheet

```json
{
    "tab_stops":{
        "labels":{
            "position":16
        },
        "mnemonic":{
            "position":24
        },
        "operands":{
            "position":32
        }
    },
    "tabulation":{
        "width":8
    },
    "labels":{
        "align":"left",
        "postfix":":",
        "margin_space":1,
        "force_postfix":false,
        "ignore_align_mnemonics":[
            "whatever"
        ]
    },
    "comment_lines":{
        "prefix":"*"
    },
    "comments":{
        "prefix":";",
        "margin_space":1
    }
}

```

## Schema

The root node MAY contains the following nodes :

* `tab_stops`
* `tabulation`
* `labels`
* `comment_lines`
* `comments`

### The `tab_stops` node

Specifies key positions inside the line, that are expected to be 
filled by the fields of a statement

This node MAY contains the following nodes : 

* `labels`
* `mnemonic`
* `operands`

#### The `labels` node

This node MAY contains the following attribute :

* `position` : when the label is short enough -including the postfix if appliable-
or when it is empty, supplemental spaces are added up to this position ;
as much margin spaces as specified by the "labels" specification will be added
after this point.
  * **type** : int
  * **constraint** : greater than or equal to 0

#### The `mnemonic` node

This node MAY contains the following attribute : 

* `position` : when the mnemonics is short enough
or when it is empty, supplemental spaces are added up to this position.
  * **type** : int
  * **constraint** : greater than or equal to the value at `tab_stops.labels.position`

#### The `operands` node

This node MAY contains the following attribute : 

* `position` : when the operands is short enough
or when it is empty, supplemental spaces are added up to this position.
  * **type** : int
  * **constraint** : greater than or equal to the value at `tab_stops.mnemonic.position`

### The `tabulation` node

This node MAY contains the following attribute : 

* `width` : in comment lines, leading tabulation are converted into spaces ; the number
of spaces per tabulation is defined here, and a the conversion add spaces until the nearest multiple
of the width to simulate the behaviour of a real tabulation.
  * **type** : int
  * **constraint** : greater than 0

### The `labels` node

This node MAY contains the following attribute : 

* `align` : right alignment is done against the tab stop of labels.
  * **type** : int
  * **constraint** : greater than 0
* `postfix` : the mark that follows a label when it is right-aligned or when forced.
  * **type** : string
  * **constraint** : only `:` is valid
* `force_postfix` : when set to true, left-aligned labels WILL have a postfix.
  * **type** : boolean
  * **constraint** : None.
* `margin_space` : minimal number of space to have after the label and the postfix.
  * **type** : int
  * **constraint** : greater than 0
* `ignore_align_mnemonics` : list of mnemonics (string values) where the label MUST be aligned to the left.
  * **type** : list of strings
  * **constraint** : None

### The `comment_lines` node

This node MAY contains the following attribute : 

* `prefix` : 
  * **type** : string
  * **constraint** : Either `*` or `;`


### The `comments` node

This node MAY contains the following attribute : 

* `prefix` : 
  * **type** : string
  * **constraint** : Either `*` or `;`
* `margin_space` : minimal number of space to have before the prefix.
  * **type** : int
  * **constraint** : greater than 0

