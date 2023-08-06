LX-Tokenizer
============

Segments text into lexically relevant tokens, using whitespace as the separator. Note that, in these examples, the ``|`` (vertical bar) symbol is used to mark the token boundaries more cleary.
::

    um exemplo → |um|exemplo|

Expands contractions. Note that the first element of an expanded contraction is marked with an ``_`` (underscore) symbol:
::

    do → |de_|o|

Marks spacing around punctuation or symbols. The ``\*`` and the ``*/`` symbols indicate a space to the left and a space to the right, respectively:
::

    um, dois e três → |um|,*/|dois|e|três|
    5.3 → |5|.|3|
    1. 2 → |1|.*/|2|
    8 . 6 → |8|\*.*/|6|

Detaches clitic pronouns from the verb. The detached pronoun is marked with a ``-`` (hyphen) symbol. When in mesoclisis, a ``-CL-`` mark is used to signal the original position of the detached clitic. Additionally, possible vocalic alterations of the verb form are marked with a ``#`` (hash) symbol:
::

    dá-se-lho → |dá|-se|-lhe|-o|
    afirmar-se-ia → |afirmar-CL-ia|-se|
    vê-las → |vê#|-las|

This tool also handles ambiguous strings. These are words that, depending on their particular occurrence, can be tokenized in different ways. For instance:
::

    deste → |deste| when occurring as a Verb
    deste → |de|este| when occurring as a contraction (Preposition + Demonstrative)

This tool achieves a f-score of 99.72%.


usage:
::

    lx-tok [options] [<input-file> [<output-file>]]

Options:

    -D, --debug   Print debug information to stderr.
