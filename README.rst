========
 Pengar
========

:Author: `Joar Wandborg <http://wandborg.se>`_
:License: AGPLv3 or later

Pengar is a work in progress.

.. _`swedbank's mobile site`: https://mobilbank.swedbank.se/


--------------
 Installation
--------------

-   Get the code:

    .. code-block:: bash

        git clone https://github.com/joar/pengar.git && cd pengar

-   Install ``python-virtualenv``:

    .. code-block:: bash

        sudo apt-get install python-virtualenv
        virtualenv . && source bin/activate

-   Install dependencies:

    .. code-block:: bash

        python setup.py develop


-------
 Usage
-------

.. code-block:: bash

    $ pengar
    Social security number: 9010240000
    Passcode:
    INFO:pengar.swedbank:Requesting CSRF token...
    INFO:pengar.swedbank:Submitting SSN login form...
    INFO:pengar.swedbank:Submitting code...
    INFO:pengar.swedbank:Requesting accounts...
    {{ account data }}
    INFO:pengar.swedbank:Requesting account 1, page 1
    INFO:pengar.swedbank:Requesting account 1, page 2
    INFO:pengar.swedbank:Requesting account 1, page 3
    {{ transaction data }}


----------
 Thank you
----------

-   `Björn Sällarp`_ whose code I inspected to get the URLs to  Swedbank's
    mobile site

-   `requests authors`_, without you my code would have been twice as
    unreadable


.. _`björn sällarp`: https://github.com/bjornsallarp
.. _`requests authors`: http://docs.python-requests.org/en/latest/dev/authors/
