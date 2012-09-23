# check_ports #

## Dependencies ##

This script requires pyasn1 and pysnmp.

    $ sudo aptitude install python-pyasn1 python-pysnmp2

## Usage ##

This script checks the status of ports on a cisco 2950, but likely works the same with other cisco switches.

    $ ./check_ports ADDRESS

When all ports are administratively up the output will look like this:

    All Ports are up (21 ports operational)

If some ports are adminstratively down the output will look like this:

    Port numbers 10,12 are down! (15 ports operational)

