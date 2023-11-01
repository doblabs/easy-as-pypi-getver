############
Installation
############

.. vim:tw=0:ts=3:sw=3:et:norl:nospell:ft=rst

.. |virtualenv| replace:: ``virtualenv``
.. _virtualenv: https://virtualenv.pypa.io/en/latest/

.. |workon| replace:: ``workon``
.. _workon: https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html?highlight=workon#workon

To install system-wide, run as superuser::

    $ pip3 install easy-as-pypi-getver

To install user-local, simply run::

    $ pip3 install -U easy-as-pypi-getver

To install within a |virtualenv|_, try::

    $ cd "$(mktemp -d)"

    $ python3 -m venv .venv

    $ . ./.venv/bin/activate

    (easy-as-pypi-getver) $ pip install easy-as-pypi-getver

To develop on the project, link to the source files instead::

    (easy-as-pypi-getver) $ deactivate
    $ git clone git@github.com:doblabs/easy-as-pypi-getver.git
    $ cd easy-as-pypi-getver
    $ python3 -m venv easy-as-pypi-getver
    $ . ./.venv/bin/activate
    (easy-as-pypi-getver) $ make develop

After creating the virtual environment, it's easy to start
developing from a fresh terminal::

    $ cd easy-as-pypi-getver
    $ . ./.venv/bin/activate
    (easy-as-pypi-getver) $ ...

