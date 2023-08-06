# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordle_helper']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.0,<2.0.0', 'requests>=2.28.1,<3.0.0', 'wordfreq>=3.0.1,<4.0.0']

entry_points = \
{'console_scripts': ['wordle-helper = wordle_helper.cli:main']}

setup_kwargs = {
    'name': 'python-wordle-helper',
    'version': '0.2.1',
    'description': 'Cheat at Wordle!',
    'long_description': '# Cheat at wordle!\n\n`wordle-helper` takes a list of arguments that constrain the possibile letter placements. The arguments\ntake the form of \\<letter\\>\\<operation\\>\\<locations\\>, where \\<letter\\> is the letter that this\nconstraint applies to, \\<operation\\> is the type of constraint, and \\<locations\\> is the list of\nlocations in the string to apply the constraint. The valid values for \\<operation\\> are:\n\n"y": represents yellow letters. For example, if your guess has a yellow letter "e" in the second\nposition, you would type "ey2". And if your next guess had a yellow "e" in the fifth position, you\nwould update that to "ey25".\n\n"b": represents unused letters. For example, if your guess has unused letter "w" (in any position)\nyou would type "wb". This operation takes zero locations, because it does not appear anywhere.\n\n"g": represents green letters. For example, if your guess has a green letter "e" in the third\nposition, you would type "eg3".\n\n"c": represents the count, i.e. minimum and maximum number of occurrences of the letter in the word.\nFor example, if you have a green letter "a" in one spot and a yellow "a" in another (for the same\nguess), you know there must be at least two a\'s in the word and you would type "ac25".\n\nYou can specify multiple constraints for multiple letters, like so:\n\n```bash\n~$ wordle-helper ey254 wb ab rb yb cb ob nb tb ig2 dg5\nFound 3 possibilites, the most common one is field\nAll valid guesses, sorted by frequency:\nfield\nbield\nsield\n```\n\n# Installation\n\n`wordle-helper` is available on [PyPI](https://pypi.org/project/python-wordle-helper/):\n\n```bash\n~$ pip install python-wordle-helper\n...\n~$ wordle-helper -h\n```\n\n## Installation from source\n\nThis assumes you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python 3.9+](https://www.python.org/downloads/), and [poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) installed already.\n\n```bash\n~$ git clone git@gitlab.com:henxing/wordle_helper.git\n~$ cd wordle_helper\nwordle_helper$ poetry install\n...\nwordle_helper$ poetry run wordle-helper -h\n```\n',
    'author': 'Hugh Enxing',
    'author_email': 'henxing@gmail.com',
    'maintainer': 'Hugh Enxing',
    'maintainer_email': 'henxing@gmail.com',
    'url': 'https://gitlab.com/henxing/wordle_helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
