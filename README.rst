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

    $ pengar debug
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

or if you want to put the results in a database for easy querying:

.. code-block:: bash

    pengar dbupdate # Creates the tables in the database
    pengar update
    [...]

then

.. code-block:: bash

    sqlite3 pengar.sqlite

now you can execute queries on the data:

.. code-block:: sql

    SELECT note,
        SUM(amount),
        COUNT(amount)
    FROM transaction
    GROUP BY note
    ORDER BY SUM(amount);

+----------------------------------+--------+-------+
| note                             | sum    | count |
+==================================+========+=======+
| ICA SUPERMARKET                  |  -6948 |    28 |
+----------------------------------+--------+-------+
| Överföring Spar, 3k              |  -6000 |     2 |
+----------------------------------+--------+-------+
| Dalpay.is                        |  -1712 |     1 |
+----------------------------------+--------+-------+
| Bankomatuttag                    |  -1500 |     1 |
+----------------------------------+--------+-------+

Also, there's a simple web server that displays a basic graph of the data in
the database.

.. code-block:: bash

    pengar serve


----------
 Thank you
----------

-   `Björn Sällarp`_ whose code I inspected to get the URLs to  Swedbank's
    mobile site

-   `requests authors`_, without you my code would have been twice as
    unreadable


.. _`björn sällarp`: https://github.com/bjornsallarp
.. _`requests authors`: http://docs.python-requests.org/en/latest/dev/authors/
