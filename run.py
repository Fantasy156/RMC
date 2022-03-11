from platform import machine, python_version

from local.main import run

if python_version() < '3.10':
    raise ValueError("Python Version more than the 3.10")


def cpu():
    match machine():
        case 'x86_64':
            return 'PC'

        case 'aarch64' | 'arm*':
            return 'AARCH64'

        case _:
            raise LookupError(f'Not Support {machine()}')


run(cpu())

