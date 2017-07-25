# -*- coding: utf-8 -*-

"""IP plugin."""

# Import system libs
try:
    import netifaces
    netifaces_tag = True
except ImportError:
    netifaces_tag = False

# Import libs
from sysmonitor.core.unicorn_logging import logger
from unicorn_plugin import UnicornPlugin


class Plugin(UnicornPlugin):

    """ IP Plugin.

    stats is a dict
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init the stats
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @UnicornPlugin._log_result_decorator
    def update(self):
        """Update IP stats using the input method.

        Stats is dict
        """
        # Reset stats
        self.reset()

        if self.input_method == 'local' and netifaces_tag:
            # Update stats using the netifaces lib
            try:
                default_gw = netifaces.gateways()['default'][netifaces.AF_INET]
            except KeyError:
                logger.debug("Can not grab the default gateway")
            else:
                try:
                    self.stats['address'] = netifaces.ifaddresses(default_gw[1])[netifaces.AF_INET][0]['addr']
                    self.stats['mask'] = netifaces.ifaddresses(default_gw[1])[netifaces.AF_INET][0]['netmask']
                    self.stats['mask_cidr'] = self.ip_to_cidr(self.stats['mask'])
                    self.stats['gateway'] = netifaces.gateways()['default'][netifaces.AF_INET][0]
                except KeyError as e:
                    logger.debug("Can not grab IP information (%s)".format(e))

        elif self.input_method == 'snmp':
            # Not implemented yet
            pass

        # Update the view
        self.update_views()

        return self.stats

    def update_views(self):
        """Update stats views."""
        # Call the father's method
        UnicornPlugin.update_views(self)

        # Add specifics informations
        # Optional
        for key in self.stats.keys():
            self.views[key]['optional'] = True

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # Only process if stats exist and display plugin enable...
        if not self.stats or args.disable_ip:
            return ret

        # Build the string message
        msg = ' - '
        ret.append(self.curse_add_line(msg))
        msg = 'IP '
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = '{0:}/{1}'.format(self.stats['address'], self.stats['mask_cidr'])
        ret.append(self.curse_add_line(msg))

        return ret

    @staticmethod
    def ip_to_cidr(ip):
        """Convert IP address to CIDR.

        Example: '255.255.255.0' will return 24
        """
        return sum(map(lambda x: int(x) << 8, ip.split('.'))) // 8128
