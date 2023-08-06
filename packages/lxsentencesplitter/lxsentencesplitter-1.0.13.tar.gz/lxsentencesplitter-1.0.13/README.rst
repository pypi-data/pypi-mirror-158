.. image:: https://gitlab.nlx.di.fc.ul.pt/lx/lxsentencesplitter/badges/master/pipeline.svg?style=flat
.. image:: https://gitlab.nlx.di.fc.ul.pt/lx/lxsentencesplitter/badges/master/coverage.svg?style=flat

LX-SentenceSplitter
===================

Marks sentence boundaries with ``<s>…</s>``, and paragraph boundaries with ``<p>…</p>``.
Unwraps sentences split over different lines.

A f-score of 99.94% was obtained when testing on a 12,000 sentence corpus accurately hand tagged with respect to sentence and paragraph boundaries.

usage:
::

    lx-sentencesplitter [options] [<input-file> [<output-file>]]

Options:
::

    -D, --debug      Print debug information to stderr.
    -T, --no-tags    Print sentences one per line, without <s>...</s>
                    tags and paragraphs separated by empty lines.
    -B, --blank-line-paragraphs
                    Assume paragraphs are separated by an empty line.