---
name: Bug report -- Pretty Printer
about: Report incorrect result from Pretty Printer
title: "[bug][pp] expected behaviour"
labels: "bug, \U0001F58A️ Pretty Printer"
assignees: sporniket

---

> **Select the part that are appliable to your case**, and add relevant parts that are not provided here.

**Given** the stylesheet `foo.json`

```json
{the:stylesheet}
```
---
**Given** the source file `foo.s`
```asm
the source
```
---
**When** the pretty printer is invoked like this : `spasm_pp --stylesheet file:foo.json foo.s`
---
**When** the pretty printer is invoked like this : `spasm_pp --stylesheet file:foo.json` with the following content received from stdin :

```asm
; the relevant snippet
```
---
**Then** the pretty printer outputs : 

```
... the relevant output ...
```
---
**Then** the pretty printer produce the file `bar.s` that contains : 

```
... the relevant output ...
```
---
# Automated test

> Usually repeat the same snippet from the step to reproduce, with the expected response
> That part may be edited later if a more systematic suit can be devised
