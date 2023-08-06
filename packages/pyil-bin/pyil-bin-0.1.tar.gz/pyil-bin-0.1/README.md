# pyil - PYthon InLine

**Simple in Python, but hard in BASH? pyil is here to help!**

A small utility to use Python expressions in bash scripts

[![badge](https://badge.fury.io/py/pyil-bin.svg)](https://pypi.python.org/pypi/pyil-bin)


# Installation

```bash
$ pip3 install pyil-bin
```

# Examples

### Print squares

```bash
$ echo nums.txt
1
2
3
$ cat nums.txt | pyil "int(i) ** 2"
1
4
9
```

`pyil` evaluates the expression using Python, by default once per each line.
The line is provided in `i` variable to the expression evaluation context (without the trailing `\n`)

### Print only even numbers

```bash
$ echo nums.txt
1
2
3
$ cat nums.txt | pyil -g "int(i) % 2 == 0"
2
```

The `-g` (`--grep`) option enables line filtering mode - the expression is not printed, but used to determine if the line should be printed


# Usage

```
usage: pyil [-h] [-l | -g | -t | -n] [-i] [-j] E

Shortcut for using Python for line processing

positional arguments:
  E               expression to evaluate

optional arguments:
  -h, --help      show this help message and exit
  -l, --lines     Evaluate expression once, with the `lines` generator
  -g, --grep      Instead of printing the value use it for filtering lines
  -t, --truish    Print only values where bool(val) == True
  -n, --none      Print only values where val != None
  -i, --iterable  Threat resulting value as iterable of separate lines. Usefull with --lines, ignored with --grep
  -j, --json      Print value using json.dump(). Together with --iterable results in NDJSON, ignored with --grep
```

# More examples

TBD

Please report all bugs to [GitLab issues](https://gitlab.com/qwolphin/pyil)
