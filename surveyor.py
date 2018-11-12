__apiversion__ = 1
__config__ = {'power': -100, 'log_level': 'ERROR', 'trigger_cooldown': 1}


class Trigger:
    def __init__(self):
        pass

    def __call__(self,
                 dev_id=None,
                 dev_type=None,
                 num_bytes=None,
                 data_threshold=None,
                 vendor=None,
                 power=None,
                 power_threshold=None,
                 bssid=None,
                 ssid=None,
                 iface=None,
                 channel=None,
                 frame_type=None,
                 frame=None,
                 **kwargs):

        print('\tdev_id = {}, dev_type = {}, vendor = {}, '
              'power = {}, bssid = {}, ssid = {}, channel = {}'
              'frame_type = {}'
              .format(dev_id, dev_type, vendor,
                      power, bssid, ssid, channel,
                      frame_type))