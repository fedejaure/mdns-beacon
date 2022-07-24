=====
Usage
=====

Blink
-----

Announce an example service on the local network:

.. code-block:: shell

    $ mdns-beacon blink example --alias sub1.example --address 127.0.0.1 --type http --protocol tcp
    ⠋ Announcing services (Press CTRL+C to quit) ...

Supervisord
^^^^^^^^^^^

Supervisord example config.

.. code-block:: toml

    [program:mdns-beacon]
    command=mdns-beacon blink example --alias sub1.example --address 127.0.0.1 --type http --protocol tcp --delay-startup 180
    numprocs=1
    autostart=true
    autorestart=true
    startsecs=140
    startretries=3
    redirect_stderr=true
    stderr_logfile=/var/log/mdns-beacon-err.log
    stdout_logfile=/var/log/mdns-beacon-out.log
    stopsignal=INT
    killasgroup=true
    stopasgroup=true

Listen
------

Listen to a specific service type:

.. code-block:: shell

    $ mdns-beacon listen --service _http._tcp.local.

                                        🚨📡 mDNS Beacon Listener 📡🚨
    ┏━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━┓
    ┃ # ┃ Type              ┃ Name                           ┃ Address IPv4 ┃ Port ┃ Server              ┃ TTL ┃
    ┡━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━┩
    │ 0 │ _http._tcp.local. │ example._http._tcp.local.      │ 127.0.0.1    │ 80   │ example.local.      │ 120 │
    │ 1 │ _http._tcp.local. │ sub1.example._http._tcp.local. │ 127.0.0.1    │ 80   │ sub1.example.local. │ 120 │
    └───┴───────────────────┴────────────────────────────────┴──────────────┴──────┴─────────────────────┴─────┘

    ⠧ Listen for services (Press CTRL+C to quit) ...
