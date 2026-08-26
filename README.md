

# mDNS Beacon

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)
[![tests](https://github.com/fedejaure/mdns-beacon/actions/workflows/tests.yml/badge.svg)](https://github.com/fedejaure/mdns-beacon/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/fedejaure/mdns-beacon/branch/main/graph/badge.svg)](https://codecov.io/gh/fedejaure/mdns-beacon)
[![Read the Docs](https://readthedocs.org/projects/mdns-beacon/badge/)](https://mdns-beacon.readthedocs.io/)
[![PyPI - License](https://img.shields.io/pypi/l/mdns-beacon.svg)](https://pypi.python.org/pypi/mdns-beacon)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)

</div>

Multicast DNS (mDNS) Beacon to announce multiple CNAME aliases across your local network. Under development. Use by your own risk❗


* GitHub repo: <https://github.com/fedejaure/mdns-beacon.git>
* Documentation: <https://mdns-beacon.readthedocs.io>
* Free software: MIT


## Features

* ✅ Announce multiple aliases on the local network.
* ✅ Listening utility to discover services during development.
* ❌ Configuration file.
* ❌ Windows support.

## Quickstart

Install `mdns-beacon` from the [Python Package Index][pypi]:

```
$ pip install mdns-beacon
```

Supports Python 3.10 through 3.12.

#### Usage

```
$ mdns-beacon --help
Usage: mdns-beacon [OPTIONS] COMMAND [ARGS]...

  Simple multicast DNS (mDNS) command line interface utility.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  blink   Announce aliases on the local network.
  listen  Listen for services on the local network.
```

Announce an example service:

```
$ mdns-beacon blink example --alias sub1.example --address 127.0.0.1 --type http --protocol tcp
⠋ Announcing services (Press CTRL+C to quit) ...
```

Listen to a specific service type:

```
$ mdns-beacon listen --service _http._tcp.local.

                                       🚨📡 mDNS Beacon Listener 📡🚨
┏━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━┓
┃ # ┃ Type              ┃ Name                           ┃ Address IPv4 ┃ Port ┃ Server              ┃ TTL ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━┩
│ 0 │ _http._tcp.local. │ example._http._tcp.local.      │ 127.0.0.1    │ 80   │ example.local.      │ 120 │
│ 1 │ _http._tcp.local. │ sub1.example._http._tcp.local. │ 127.0.0.1    │ 80   │ sub1.example.local. │ 120 │
└───┴───────────────────┴────────────────────────────────┴──────────────┴──────┴─────────────────────┴─────┘

⠧ Listen for services (Press CTRL+C to quit) ...
```

## Credits

This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
[pypi]: https://pypi.org/
