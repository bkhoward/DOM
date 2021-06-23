# List of packages to import
from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory
#
# import cobra.mit.request
# import cobra.model.fv
# import cobra.model.pol
import xlsxwriter
import urllib3
import requests
import json
import aciCredentials
from nodeList import nodeList
# import getToken

urllib3.disable_warnings()

# declare variables
url = str(aciCredentials.url)
user = str(aciCredentials.user)
password = str(aciCredentials.pwd)


# log into an APIC and create a directory object
ls = LoginSession(url, user, password)
md = MoDirectory(ls)
md.login()

# search by Class
# psu = md.lookupByClass("fabricNode", parentDn='topology/pod-1')

# print header
print("{:<10} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20} {:<20} {:<15}"\
    .format('NodeID', 'Interface', 'Status', 'Status Quality', 'Speed', 'DOM TX', 'DOM RX', 'DOM Temp', 'Optic Vendor', 'Optic Type', 'Optic P/N', 'Optic S/N'))


def domStatus(nodes):

    for nodeId in nodes:
        for i in range(1, (nodeId[2] + 1)):
            phy = '1/' + str(i)
            speedDn = md.lookupByDn('topology/pod-1/node-' + str(nodeId[0]) + '/sys/phys-[eth' + str(phy) + ']/phys')

            if speedDn.operSt == 'down':
                print('{:<10} {:<15} {:<15} {:<20} {:<15}' \
                    .format(nodeId[0], str(phy), speedDn.operSt, speedDn.operStQual, speedDn.operSpeed))
                continue

            else:
                opticDn = md.lookupByDn('topology/pod-1/node-' + str(nodeId[0]) + '/sys/phys-[eth' + str(phy) + ']/phys/fcot')

                if opticDn.typeName == 'SFP-H10GB-CU1M' or 'SFP-H10GB-CU3M':
                    print('{:<10} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20} {:<20} {:<15}' \
                        .format(nodeId[0], str(phy), speedDn.operSt, speedDn.operStQual, speedDn.operSpeed, '', '', '',
                                opticDn.guiName, opticDn.typeName, opticDn.guiPN, opticDn.guiSN))
                    continue

                elif opticDn.typeName == '1000base-T':
                    print('{:<10} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20} {:<20} {:<15}' \
                        .format(nodeId[0], str(phy), speedDn.operSt, speedDn.operStQual, speedDn.operSpeed, '', '', '',
                                opticDn.guiName, opticDn.typeName, opticDn.guiPN, opticDn.guiSN))
                    continue

                # search by DN
                domTXDn = md.lookupByDn('topology/pod-1/node-' + str(nodeId[0]) + '/sys/phys-[eth' + str(phy) + ']/phys/domstats/txpower')
                domRXDn = md.lookupByDn('topology/pod-1/node-' + str(nodeId[0]) + '/sys/phys-[eth' + str(phy) + ']/phys/domstats/rxpower')
                domTempDn = md.lookupByDn('topology/pod-1/node-' + str(nodeId[0]) + '/sys/phys-[eth' + str(phy) + ']/phys/domstats/temperature')

                print('{:<10} {:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20} {:<20} {:<15}' \
                    .format(nodeId[0], str(phy), speedDn.operSt, speedDn.operStQual, speedDn.operSpeed, domTXDn.value,
                            domRXDn.value, domTempDn.value, opticDn.guiName, opticDn.typeName, opticDn.guiPN, opticDn.guiSN))


# psuStatus(spineList)
domStatus(nodeList)

# Use the connected moDir queries and configuration...
md.logout()
