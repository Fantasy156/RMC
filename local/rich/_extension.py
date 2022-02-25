from typing import Any


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from local.rich.pretty import install
    from local.rich.traceback import install as tr_install

    install()
    tr_install()
