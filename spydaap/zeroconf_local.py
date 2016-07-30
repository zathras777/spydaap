""" Simple wrapper class for the all python zeroconf module. """
import socket
from zeroconf import ServiceInfo, Zeroconf as ZeroC

__all__ = ["Zeroconf"]


def find_local_ipaddress():
    """ Try to find a system IPv4 address we can use to advertise our service.
        This presently only works for IPv4.
        If no address is available, an exception is thrown.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('1.2.3.4', 56))
        interface = sock.getsockname()[0]
        sock.close()
        return socket.inet_aton(interface)
    except socket.error as err:
        raise Exception("Unable to find a local IP address to use. " + err)


class Zeroconf(object):
    """ A simple class to publish a network service using zeroconf. """

    def __init__(self, name, port, **kwargs):
        self.zconf = None
        stype = kwargs.get('stype', "_http._tcp.local.")

        full_name = name
        if not name.endswith('.'):
            full_name += '.' + stype

        props = {'txtvers': '1',
                 'iTSh Version': '131073', #'196609'
                 'Machine Name': name,
                 'Password': '0'}

        self.svc_info = ServiceInfo(stype,
                                    full_name,
                                    find_local_ipaddress(),
                                    port,
                                    0,
                                    0,
                                    props)

    def publish(self):
        """ Publish the service to the network. """
        if self.zconf is None:
            self.zconf = ZeroC()
            self.zconf.register_service(self.svc_info)

    def unpublish(self):
        """ Tell the network we're closed :-) """
        if self.zconf is not None:
            self.zconf.unregister_service(self.svc_info)
            self.zconf.close()
            self.zconf = None
