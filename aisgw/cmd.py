#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python AIS Gateway Commands."""

import argparse
import datetime
import json
import socket
import time

import ais.stream
import requests

import aisgw

__author__ = 'Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__license__ = 'GNU General Public License, Version 3'  # NOQA pylint: disable=R0801


def cli() -> None:
    """Command Line interface for AIS Gateway."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--port', help='UDP Listen port', default=aisgw.DEFAULT_PORT)
    parser.add_argument(
        '-p', '--password', help='APRS.FI AIS API Password', required=True)
    parser.add_argument(
        '-c', '--callsign', help='APRS.FI Login/Callsign', required=True)

    opts = parser.parse_args()

    api_url = 'http://aprs.fi/jsonais/post/' + opts.password
    path = {'name': opts.callsign, 'url': api_url}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', opts.port))

    import ais.stream
    while 1:
        for msg in ais.stream.decode(sock.makefile('r'), keep_nmea=True):
            rxtime = datetime.datetime.utcnow().strftime(
                "%Y%m%d%H%M%S") # YYYYMMDDHHMMSS
            parsed = json.loads(json.dumps(msg))

            ais = {
                'msgtype': parsed['id'],
                'mmsi': parsed['mmsi'],
                'rxtime': rxtime
            }

            if 'x' in parsed:
                ais['lon'] = parsed['x']
            if 'y' in parsed:
                ais['lat'] = parsed['y']
            if 'sog' in parsed:
                ais['speed'] = parsed['sog']
            if 'cog' in parsed:
                ais['course'] = parsed['cog']
            if 'true_heading' in parsed:
                ais['heading'] = parsed['true_heading']
            if 'nav_status' in parsed:
                ais['status'] = parsed['nav_status']
            if 'type_and_cargo' in parsed:
                ais['shiptype'] = parsed['type_and_cargo']
            if 'part_num' in parsed:
                ais['partno'] = parsed['part_num']
            if 'callsign' in parsed:
                ais['callsign'] = parsed['callsign']

            # Seeing '@' char getting added to end of ship name - parsing err?
            if 'name' in parsed:
                ais['shipname'] = parsed['name'].replace('@', '')

            if 'vendor_id' in parsed:
                ais['vendorid'] = parsed['vendor_id']
            if 'dim_a' in parsed:
                ais['ref_front'] = parsed['dim_a']
            if 'dim_c' in parsed:
                ais['ref_left'] = parsed['dim_c']
            if 'draught' in parsed:
                ais['draught'] = parsed['draught']
            if 'length' in parsed:
                ais['length'] = parsed['length']
            if 'width' in parsed:
                ais['width'] = parsed['width']
            if 'destination' in parsed:
                ais['destination'] = parsed['destination']
            if 'persons' in parsed:
                ais['persons_on_board'] = parsed['persons']

            groups = {'path': [path], 'msgs':[ais]}

            output = {
                'encodetime': rxtime,
                'protocol': 'jsonais',
                'groups':  [groups]
            }

            post = json.dumps(output)
            r = requests.post(api_url, files={'jsonais': (None, post)})
            # dump non common packets for debugging
            if parsed['id'] not in (1, 2, 3, 4):
                print('---')
                print('NMEA: {}'.format(parsed['nmea']))
                print('Parsed: {}'.format(parsed))
                print('Post: {}'.format(post))
                print('Result: {}'.format(json.loads(r.text)['description']))


if __name__ == '__main__':
    cli()
