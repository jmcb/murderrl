********
MurderRL
********
**A rogue-like murder mystery game in Python.**

Support and Documentation
=========================

Documentation can be found in the ``doc/`` sub-directory. A complete index
sorted by module can be found in ``doc/index.rst``, while per-module
documentation can be found in ``doc/<module>.rst``.

You can access the documentation for trunk on-line via github's wonderful
rst2html conversion:

- `Index`_
 - `coord module`_
 - `shape module`_
 - `database module`_
 - `docparser module`_

*Nota bene: Due to limitations of github, anchors are suppressed, therefore
internal hyperlink sare non-functioning. You can view the complete but possibly
outdated documentation at the* `MurderRL page`_ *on github pages.*

General information
===================

MurderRL is a rogue-like in the vein of the seminal Rogue_, `Dungeon Crawl
Stone Soup`_, and NetHack_. Unlike these it is not a role-playing game;
instead, it is a "whodunnit" in the style of Agatha Christie many "country
house" mysteries, the `Gosford Park`_, and so on.

Like the aforementioned rogue-likes, the plot of the game, the characters, the
setting and the location will be completely randomised [#]_. This means that the game
is infinitely replayable.

The game will feature varying difficulty levels and a large pool of random
information. While you may encounter similarly named characters or find a clue
that you've seen before, you can know for certain that their role in previous
games is unrelated to the current one.

Installation and usage
======================

From source
-----------

Run::

    git clone git://github.com/jmcb/murderrl
    cd murderrl
    python game.py

License
=======

Where relevant, MurderRL is licensed under the terms of the following MIT
license:

Copyright (c) 2010 Jon McManus, Johanna Ploog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Footnotes
=========

.. [#] Arinbjarnar, María. *Murder She Programmed: Dynamic Plot Generating
       Engine for Murder Mystery Games*. Thesis. Reykjavik University. Web_.
       December, 2010.

.. Links
.. =====

.. _Web: http://www-users.cs.york.ac.uk/~maria/greinar/BSc.pdf

.. _Dungeon Crawl Stone Soup: http://crawl.develz.org

.. _NetHack: http://www.nethack.org/

.. _Rogue: http://en.wikipedia.org/wiki/Rogue_(computer_game)

.. _Gosford Park: http://en.wikipedia.org/wiki/Gosford_Park

.. _Index: https://github.com/jmcb/murderrl/tree/master/doc/index.rst

.. _shape module: https://github.com/jmcb/murderrl/tree/master/doc/shape.rst

.. _coord module: https://github.com/jmcb/murderrl/tree/master/doc/coord.rst

.. _docparser module: https://github.com/jmcb/murderrl/tree/master/doc/docparser.rst

.. _database module: https://github.com/jmcb/murderrl/tree/master/doc/database.rst

.. _Murder RL page: http://jmcb.github.com/murderrl/index.html
