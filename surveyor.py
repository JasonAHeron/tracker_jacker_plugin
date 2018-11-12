import sys
import yaml
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def parse_wifi_map(map_path):
    with open(map_path, 'r') as f:
        data = f.read()

    wifi_map = yaml.load(data)
    devices = set()

    if not wifi_map:
        return

    os.system('clear')
    for ssid in wifi_map:
        print('ssid = {}'.format(ssid))
        ssid_node = wifi_map[ssid]
        for bssid in ssid_node:
            # print('\tbssid = {}'.format(bssid))
            bssid_node = ssid_node[bssid]
            if 'devices' in bssid_node:
                for device in bssid_node['devices']:
                    devices |= {device}
                    print('\t\tdevice = {}'.format(device))

    print('\n\nSSID count: {}, Device count: {}'.format(len(wifi_map), len(devices)))

class Event(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('wifi_map.yaml'):
            parse_wifi_map('wifi_map.yaml')

if __name__ == "__main__":
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()