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
cat mysource.s | spasm_pp | echo > somewhere.s
```

#### Using a custom stylesheet

**Given** a styleshee file `./config/mystylesheet.json`

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

## Formatting rules

**spasm_pp** recognizes two types of lines in an assembly source :

* **Comment lines**, that start with a star `*` or a semi-colon `;`.
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

### Formatting rules for comment lines

* The first char WILL be the star `*`
* If the second characters from the source line is a star `*`, it will be output just after the first star, otherwise a space ` ` is added.
* Leading tabulations `\t` are converted into a sequence of at most 4 spaces ` `, the actual number allowing to put the next char at a position that is a multiple of 4.

### Formatting rules for statement lines

The principle is that there is a margin at position 30 where the mnemonic part WILL start.

> **Trivia** : for a width of 80 characters, the repartition 30-50 follows the golden ratio, rounded to the nearest tens (_80/phi ≈ 49.44_) ; the same for the 50 characters wide section the repartition 20-30 (_50/phi ≈ 30.90_) 

* When there is a label part, it WILL be _right-aligned to that margin_, use the postfix marker `:` (colon) followed by a space.
  * If the label is too large, it will push the mnemonic part as much as needed.
  * **Exception of the right-alignment** : when the mnemonic part is the _macro_ directive (`macro`, `macro.w` or `macro.l`), then the label will be _left-aligned_, in other words the line starts with the label, still followed by the colon `:` and at least a space ` `.
* When there is a mnemonic part, it WILL start at position 30.
* When there is an operands part, it WILL start just after a space ` ` put just after the mnemonic part.
* When there is a comment part, any leading and trailing whitespace (space ` ` and tabulation `\t`) are removed.
  * When there is a mnemonic in the line, it WILL start just after the mnemonic + operands part AND at least position 50, prefixed with a space followed by a semi-colon followed by a space ` ; `.
  * When the latest line with a mnemonic part had a comment part too, the following lines with only a comment part will be seen as continuation of the initial comment, and WILL start at position 50
  * In any other case, the comment part WILL start at position 30.