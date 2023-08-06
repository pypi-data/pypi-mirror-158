# Cheat at wordle!

`wordle-helper` takes a list of arguments that constrain the possibile letter placements. The arguments
take the form of \<letter\>\<operation\>\<locations\>, where \<letter\> is the letter that this
constraint applies to, \<operation\> is the type of constraint, and \<locations\> is the list of
locations in the string to apply the constraint. The valid values for \<operation\> are:

"y": represents yellow letters. For example, if your guess has a yellow letter "e" in the second
position, you would type "ey2". And if your next guess had a yellow "e" in the fifth position, you
would update that to "ey25".

"b": represents unused letters. For example, if your guess has unused letter "w" (in any position)
you would type "wb". This operation takes zero locations, because it does not appear anywhere.

"g": represents green letters. For example, if your guess has a green letter "e" in the third
position, you would type "eg3".

"c": represents the count, i.e. minimum and maximum number of occurrences of the letter in the word.
For example, if you have a green letter "a" in one spot and a yellow "a" in another (for the same
guess), you know there must be at least two a's in the word and you would type "ac25".

You can specify multiple constraints for multiple letters, like so:

```bash
~$ wordle-helper ey254 wb ab rb yb cb ob nb tb ig2 dg5
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
