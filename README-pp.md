# pp -- the Pretty Printer

**Content**

1. User manual
2. Formatting rules

## User Manual

### Synopsys

`spasm_pp [--help] [--stylesheet <stylesheet>] [--rewrite] [<source files>...]`

#### Positional arguments

* `<source files>...` : an optionnal list of source files ; when no files are provided, use the standard input instead.

#### Options

*  `-h`, `--help`: shows an help message and exits.
*  `--stylesheet <stylesheet>` : specifies the formatting rules to follow, either `builtin:heritage` (the default), or `builtin:sporniket`, or `file:path/to/file`
*  `-r`, `--rewrite` : **when source files are provided**, replace each of the source files by their pretty-printed version **when there is a difference**. In other word, a source file that is already formatted according to the stylesheet is left untouched.


### Description

Reads the standard input or a list of input files, and either outputs each line as a formatted line of assembly 
code into the standard output, or rewrite each input file that has been modified by the format process.

The formatting follows a set rules parameterized through a _stylesheet_

### Typical invocation

**Given** a source file to format `mysource.s`

#### Using redirection

```
spasm_pp <mysource.s >somewhere.s
```

#### Using pipe

```
cat mysource.s | spasm_pp | cat > somewhere.s
```

#### Using a builtin stylesheet

There are 2 builtin stylesheets : `heritage` (the default) and `sporniket`

```
spasm_pp --stylesheet builtin:heritage <mysource.s
spasm_pp --stylesheet builtin:sporniket <mysource.s
```

#### Using a custom stylesheet

**Given** a stylesheet file `./config/mystylesheet.json`

```
spasm_pp --stylesheet file:./config/mystylesheet.json <mysource.s
```

#### Batch processing all the source files of the current folder

> _Written for the bash shell_

* Using the `--rewrite` option (recommended) :

```
spasm_pp --rewrite $(ls *.s)
```

* Using the pretty printer as a filter (each source file is unconditionnaly rewritten):

```
for fic in $(ls *.s); do mv $fic tmp.$fic ; spasm_pp <tmp.$fic >$fic ; rm tmp.$fic ; done
```

## Formatting

### Modelization of lines of codes

**spasm_pp** recognizes two types of lines in an assembly source :

* **Comment lines**, that start with a star `*` or a semi-colon `;`. _A doubled mark will be recognised as a **special comment line** (this is a convention specific to this tool)_
* **Statement lines**, that start with anything else, and break down into four optionnal parts, each separated by a space or a specified marker : 
  * a _label_ part to identify a line of code, when not starting at the beginning of the line, it MUST have the postfix colon `:` ; 
  * then a _mnemonic_ part that holds an operation code from the target ISA (Instruction Set Architecture), a macro name or a directive of the target assembler ; 
  * then a _operands_ part that is a comma separated list of operands (no spaces except in string litterals) ;
    * An operands part ALWAYS follows a mnemonic part ;
  * then a _comment_ part, that contains the rest of the line ;
    * when there is no operands part, it MUST start with a star `*` or a semi-colon `;` ; 
    * when there is an operand parts and when the comment part is started with a star `*`, then there MUST be a space ` ` between the two parts, otherwise the star `*` MAY be seen as a part of an arithmetical expression in the operands part by the target assembler.

> **WARNING** : please check that the output of **spasm_pp** is compatible with your target assembler before including it in your build process.
>
> **spasm_pp** has been written with the target assembler _Devpac_ for the "Motorola 68k" ISA in mind, and my target is to succesfully compile my programs using this syntax with [vasm](http://sun.hasenbraten.de/vasm/) and the switches `-devpac -warncomm -nomsg=2054`, but I believe that most assembler of that time where basically following those general principles.

### Stylesheet for setting the format

**spasm_pp** has 2 builtin stylesheets, and accept custom stylesheets that are json documents.

Custom stylesheets **overrides** the settings of the default stylesheets, meaning that it CAN be minimized to contains only the wanted differences.

See [README-pp-stylesheet.md](./README-pp--stylesheet.md) for the specification of the content of the stylesheet.

The builtin stylesheet `heritage` is the same as the following custom stylesheet : 

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
        "ignore_align_mnemonics":null
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

The builtin stylesheet `sporniket` is the same as the following custom stylesheet : 

```json
{
    "tab_stops":{
        "labels":{
            "position":30
        },
        "mnemonic":{
            "position":30
        },
        "operands":{
            "position":50
        }
    },
    "tabulation":{
        "width":4
    },
    "labels":{
        "align":"right",
        "postfix":":",
        "margin_space":1,
        "force_postfix":true,
        "ignore_align_mnemonics":[
            "macro",
            "macro.w",
            "macro.l"
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

### Formatting rules for comment lines

* The first char WILL be the one set by the stylesheet. For a _special comment line_, this first char is doubled.
* A space is added
* Leading tabulations `\t` are converted into a sequence of spaces, the actual number allowing to put the next char at a position that is a multiple of the tabulation width specified by the stylesheet.

### Formatting rules for statement lines

The principle is that the label field, the mnemonic field and the operands field have a _tabulation stop_ that allows the formatter to vertically align between lines (provided the content of a field is short enough).

> **Trivia** : for a width of 80 characters, the repartition 30-50 follows the golden ratio, rounded to the nearest tens (_80/phi ≈ 49.44_) ; the same for the 50 characters wide section the repartition 20-30 (_50/phi ≈ 30.90_). That's the guideline to chose the tabulation stops of the builtin style `sporniket`.

* When there is a label part, it can be _right-aligned to the tabulation stop_, in which case it WILL use the postfix marker, followed by at least the specified amount of space.
  * If the label is too large, it will push the mnemonic part as much as needed.
  * **Exception of the right-alignment** : when the mnemonic part is in the exclusion list, then the label will be _left-aligned_, in other words the line starts with the label.
  * Left-aligned labels WILL have the postfix mark ONLY if it is forced.
* When there is a mnemonic part, it WILL start from the label's tabulation stop, if possible.
* When there is an operands part, it WILL start from the mnemonic's tabulation stop, if possible. There is a least one space between the mnemonic and the operands.
* When there is a comment part, any leading and trailing whitespace (space ` ` and tabulation `\t`) of that part are removed.
  * When there is a mnemonic in the line, it WILL start from the tabulation stop of the operands, with at least the specified amount of space, then the comment mark, then a space.
  * For a statement line containing only a comment part :
    * When the latest line with a mnemonic part had a comment part too, the comment part will be seen as continuation of the initial comment, and WILL start from the tabulation stop of the operands. An empty line disables that behaviour for the following lines.
    * In any other case, the comment part WILL start from the tabulation stop of the label.