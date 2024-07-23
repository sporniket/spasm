# pp -- the Pretty Printer

## Synopsys

spasm_pp

## Description

Reads the standard input, and outputs each line as a formatted line of assembly 
code, following the builtin formatting rules.

## Typical invocation

**Given** a source file to format `mysource.s`

### Using redirection

```
spasm_pp <mysource.s >somewhere.s
```

### Using pipe

```
cat mysource.s | spasm_pp | echo > somewhere.s
```
