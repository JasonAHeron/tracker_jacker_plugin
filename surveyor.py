from firebase_admin import credentials
from firebase_admin import firestore
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import firebase_admin
import logging
import os
import sys
import time
import yaml


def parse_wifi_map(map_path):
    with open(map_path, 'r') as f:
        data = f.read()

    wifi_map = yaml.load(data)
    devices = set()

    if not wifi_map:
        return

    os.system('clear')
    print('*' * 40)
    for ssid in wifi_map:
        ssid_node = wifi_map[ssid]
        print('ssid = {}'.format(ssid))
        doc_ref = db.collection('networksa').document(ssid)
        doc_ref.set({
            'ssid': ssid,
        })
        for bssid in ssid_node:
            # print('\tbssid = {}'.format(bssid))
            bssid_node = ssid_node[bssid]
            if 'devices' in bssid_node:
                for device in bssid_node['devices']:
                    devices |= {device}
                    print('\tdevice = {}, vendor = {}, last_seen = {} seconds ago'.format(
                        device, bssid_node['devices'][device]['vendor'], time.time() - bssid_node['devices'][device]['last_seen']))

    print('\n\nSSID count: {}, Device count: {}'.format(
        len(wifi_map), len(devices)))


class Event(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('wifi_map.yaml'):
            parse_wifi_map('wifi_map.yaml')


if __name__ == "__main__":
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })
    db = firestore.client()
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
