# spasm -- SPorniket's tools for ASseMbly

![PyPI - Version](https://img.shields.io/pypi/v/spasm-by-sporniket)
![PyPI - License](https://img.shields.io/pypi/l/spasm-by-sporniket)


> [WARNING] Please read carefully this note before using this project. It contains important facts.

Content

1. What is **spasm -- SPorniket's tools for ASseMbly**, and when to use it ?
2. What should you know before using **spasm -- SPorniket's tools for ASseMbly** ?
3. How to use **spasm -- SPorniket's tools for ASseMbly** ?
4. Known issues
5. Miscellanous

## 1. What is **spasm -- SPorniket's tools for ASseMbly**, and when to use it ?

**spasm -- SPorniket's tools for ASseMbly** is a collection of generic tools for assembly language, that should work for any Instruction Set Architecture (ISA).

### What's new in v1.0.0

**spasm_pp**

  * Resolves #7 : [pp] 2 builtin styles and one used by default
  * Resolves #8 : [pp] Support a provided stylesheet
  * Resolves #9 : [pp][tech] Naming in the builtin structures
  * Resolves #10 : [pp] Process a given list of files
  * Resolves #11 : [pp] Replace input files by their formatted version if there is a difference
  * Fixes #13 : [bug][pp] A special comment line starts with a doubled comment line mark

### What's new in v0.0.1

* Initial release : `spasm_pp` with fixed formatting.

### Licence
 **spasm -- SPorniket's tools for ASseMbly** is free software: you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
 option) any later version.

 **spasm -- SPorniket's tools for ASseMbly** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 more details.

 You should have received a copy of the GNU General Public License along with **spasm -- SPorniket's tools for ASseMbly**.
 If not, see http://www.gnu.org/licenses/ .


## 2. What should you know before using **spasm -- SPorniket's tools for ASseMbly** ?

> **SECURITY WARNING** : **spasm -- SPorniket's tools for ASseMbly** is a set of tools for manipulating files, and thus WILL allows attacks on the files systems. Do not install this project on servers.

**spasm -- SPorniket's tools for ASseMbly** is written in [Python](http://python.org) language, version 3.9 or above, and consists of :

* [spasm_pp](./README-pp.md) : the Pretty Printer.

> Do not use **spasm -- SPorniket's tools for ASseMbly** if this project is not suitable for your project

## 3. How to use **spasm -- SPorniket's tools for ASseMbly** ?

### Requirements

Python 3.8 or later versions, `pip3` and `pdm` are required.

### From source

To get the latest available code, one must clone the git repository, build and install to the maven local repository.

	git clone https://github.com/sporniket/spasm.git
	cd spasm
	pdm build
    sudo pip3 install dist/spasm_by_sporniket-<version>-py3-none-any.whl

### From Pypi
Add any of the following dependencies that are appropriate to your project.

```
sudo pip3 install spasm_by_sporniket
```

### Documentation

* [User manual of `spasm_pp`](./README-pp.md) ; [Specifications of custom stylesheet files](./README-pp--stylesheet.md)

## 4. Known issues
See the [project issues](https://github.com/sporniket/spasm/issues) page.

## 5. Miscellanous

### Report issues
Use the [project issues](https://github.com/sporniket/spasm/issues) page.
