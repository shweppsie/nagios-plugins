#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

if len(sys.argv) != 2:
	print "This is a script to check the status of Cisco switch ports"
	print "Usage: %s IPAddress" % sys.argv[0]
	exit(3)

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.CommunityData('public', mpModel=0),
    cmdgen.UdpTransportTarget((sys.argv[1], 161)),
    '.1.3.6.1.2.1.2.2.1.7',
    '.1.3.6.1.2.1.2.2.1.8',
)

if errorIndication:
    print(errorIndication)
    exit(3)
elif errorStatus:
    print('%s at %s' % (
        errorStatus.prettyPrint(),
        errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
        )
    )
    exit(3)

operupcount = 0
admindown = []
up = 1
down = 2

for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
	mib = name.asTuple()
	
	type = mib[-2]
	port = mib[-1]
	status = val
	
	if type == 7: # Admin
		if status == down:
			admindown.append(port)
	elif type == 8: # Oper
		if status == up:
			operupcount += 1

opertext = "(%d ports operational)" % operupcount
if len(admindown) == 1:
	print "Port number %s down! %s" % (str(admindown[0]),opertext)
	exit(2)
elif len(admindown) > 1:
	print "Port numbers %s are down! %s" % (",".join([str(i) for i in admindown]),opertext)
	exit(2)
else:
	print "All Ports are up %s" % (opertext)
	exit(0)
