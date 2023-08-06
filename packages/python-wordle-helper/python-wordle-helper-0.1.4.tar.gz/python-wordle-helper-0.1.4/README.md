# Cheat at wordle!

`wordle-helper` takes a list of arguments that constrain the possibile letter placements. The arguments
take the form of \<letter\>\<operation\>\<locations\>, where \<letter\> is the letter that this
constraint applies to, \<operation\> is the type of constraint, and \<locations\> is the list of
locations in the string to apply the constraint. The valid values for \<operation\> are:

"y": represents yellow letters. For example, if your guess has a yellow letter "e" in the second
position, you would type "ey1". And if your next guess had a yellow "e" in the fifth position, you
would update that to "ey14".

"b": represents unused letters. For example, if your guess has unused letter "w" (in any position)
you would type "wb". This operation takes zero locations, because it does not appear anywhere.

"g": represents green letters. For example, if your guess has a green letter "e" in the third
position, you would type "eg2".

You can specify multiple constraints for multiple letters, like so:

```bash
~$ wordle-helper ey143 wb ab rb yb cb ob nb tb ig1 dg4
Found 3 possibilites, the most common one is field
All valid guesses, sorted by frequency:
field
bield
sield
```

# Installation

`wordle-helper` is available on [PyPI](https://pypi.org/project/python-wordle-helper/):

```bash
~$ pip install python-wordle-helper
...
~$ wordle-helper -h
```

## Installation from source

This assumes you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python 3.9+](https://www.python.org/downloads/), and [poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) installed already.

```bash
~$ git clone git@gitlab.com:henxing/wordle_helper.git
~$ cd wordle_helper
wordle_helper$ poetry install
...
wordle_helper$ poetry run wordle-helper -h
```
