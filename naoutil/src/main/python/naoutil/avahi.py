# Copyright 2013 Axel Voitier
# All rights reserved (until a FOSS licence is found)

import dbus, gobject
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

# Use the following sources:
# http://avahi.org/wiki/PythonBrowseExample
# http://avahi.org/download/doxygen/index.html
# http://avahi.org/download/ServiceResolver.introspect.xml
# http://avahi.org/wiki/ProgrammingDocs
#
# http://www.freedesktop.org/wiki/IntroductionToDBus
# http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
# http://cgit.freedesktop.org/dbus/dbus-python/tree/examples
# http://www.no-ack.org/2010/07/writing-simple-dbus-client-in-python.html

# Constant definition coming from the python-avahi module.
# The python-avahi module is not installed by default on Nao or usual OSs.
# But it is mainly made of constant definitions. So I replicate here the important ones.
AVAHI_DBUS_NAME = 'org.freedesktop.Avahi'
AVAHI_DBUS_INTERFACE_SERVER = AVAHI_DBUS_NAME + '.Server'
AVAHI_DBUS_INTERFACE_SERVICE_BROWSER = AVAHI_DBUS_NAME + '.ServiceBrowser'
AVAHI_IF_UNSPEC = -1
AVAHI_PROTO_UNSPEC, AVAHI_PROTO_INET, AVAHI_PROTO_INET6  = -1, 0, 1

def service_resolved(*args):
    global nbServicesFound, servicesFound, gloop
    #print 'service resolved'
    labels = ['interface', 'protocol', 'name', 'type', 'domain', 'host', 'aprotocol', 'address', 'port', 'txt', 'flags']
    #servicesFound.append(dict(zip(labels, args)))
    servicesFound.append({
        'robot_name': str(args[labels.index('name')]),
        'host_name': str(args[labels.index('host')]),
        'ip_address': str(args[labels.index('address')]),
        'naoqi_port': int(args[labels.index('port')])
    })
    if len(servicesFound) == nbServicesFound:
        gloop.quit()

def print_error(*args):
    global gloop
    print 'error', args
    gloop.quit()
    
def myhandler(interface, protocol, name, stype, domain, flags):
    global server, nbServicesFound
    #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
    nbServicesFound += 1

    if flags & 8:
        # local service, skip
        pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, AVAHI_PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)
        

nbServicesFound = 0
servicesFound = []
gloop = None
server = None

def findAllNAOs(ipv6=False):
    global nbServicesFound, servicesFound, server, gloop
    nbServicesFound = 0
    servicesFound = []
    
    bus = dbus.SystemBus(mainloop=DBusGMainLoop())

    server = dbus.Interface( bus.get_object(AVAHI_DBUS_NAME, '/'),
            AVAHI_DBUS_INTERFACE_SERVER)
            
    protoInet = AVAHI_PROTO_INET6 if ipv6 else AVAHI_PROTO_INET

    sbrowser = dbus.Interface(bus.get_object(AVAHI_DBUS_NAME,
            server.ServiceBrowserNew(AVAHI_IF_UNSPEC,
                protoInet, '_naoqi._tcp', 'local', dbus.UInt32(0))),
            AVAHI_DBUS_INTERFACE_SERVICE_BROWSER)

    sbrowser.connect_to_signal("ItemNew", myhandler)

    gloop = gobject.MainLoop()
    gloop.run()
    
    return servicesFound
