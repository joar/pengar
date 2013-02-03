========
 Pengar
========

:Author: `Joar Wandborg <http://wandborg.se>`_
:License: AGPLv3 or later

Pengar is a library interface to `Swedbank's mobile site`_.

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

        pip install -r requirements.txt


-------
 Usage
-------

The ``swedbank.py`` library can be run directly from the command line:

.. code-block:: bash

    $ python swedbank.py
    Social security number: 9010240000
    Passcode:
    INFO:__main__:Requesting CSRF token...
    INFO:__main__:Submitting SSN login form...
    INFO:__main__:Submitting code...
    INFO:__main__:Requesting accounts...
    {{ account data }}
    INFO:__main__:Requesting account 1, page 1
    INFO:__main__:Requesting account 1, page 2
    INFO:__main__:Requesting account 1, page 3
    {{ transaction data }}

However, it's intended use is to be accessed from third party scripts.

----------
 Thank you
----------

-   `Björn Sällarp`_ whose code I inspected to get the URLs to  Swedbank's
    mobile site

-   `requests authors`_, without you my code would have been twice as
    unreadable


.. _`björn sällarp`: https://github.com/bjornsallarp
.. _`requests authors`: http://docs.python-requests.org/en/latest/dev/authors/
