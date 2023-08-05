#!/usr/bin/env python3
import datetime
import logging
import os
import platform
import plistlib
import sys
import uuid
from pathlib import Path
from typing import Mapping

from packaging.version import Version

from pymobiledevice3 import usbmux
from pymobiledevice3.ca import ca_do_everything
from pymobiledevice3.exceptions import *
from pymobiledevice3.service_connection import ServiceConnection
from pymobiledevice3.usbmux import PlistMuxConnection
from pymobiledevice3.utils import sanitize_ios_version

# we store pairing records and ssl keys in ~/.pymobiledevice3
HOMEFOLDER = Path.home() / '.pymobiledevice3'
MAXTRIES = 20

LOCKDOWN_PATH = {
    'win32': Path(os.environ.get('ALLUSERSPROFILE', ''), 'Apple', 'Lockdown'),
    'darwin': Path('/var/db/lockdown/'),
    'linux': Path('/var/lib/lockdown/'),
}


def write_home_file(filename, data):
    HOMEFOLDER.mkdir(parents=True, exist_ok=True)
    filepath = HOMEFOLDER / filename
    filepath.write_bytes(data)
    return str(filepath)


def reconnect_on_remote_close(f):
    """
    lockdownd's _socket_select will close the connection after 60 seconds of "radio-silent" (no data has been
    transmitted). When this happens, we'll attempt to reconnect.
    """

    def _reconnect_on_remote_close(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BrokenPipeError:
            self = args[0]

            # first we release the socket on our end to avoid a ResourceWarning
            self.close()

            # now we re-establish the connection
            self.logger.debug('remote device closed the connection. reconnecting...')
            self.service = ServiceConnection.create(self.udid, self.SERVICE_PORT,
                                                    connection_type=self.usbmux_device.connection_type)
            self.validate_pairing()
            return f(*args, **kwargs)

    return _reconnect_on_remote_close


DOMAINS = ['com.apple.disk_usage',
           'com.apple.disk_usage.factory',
           'com.apple.mobile.battery',
           # FIXME: For some reason lockdownd segfaults on this, works sometimes tho
           # 'com.apple.mobile.debug',
           'com.apple.iqagent',
           'com.apple.purplebuddy',
           'com.apple.PurpleBuddy',
           'com.apple.mobile.chaperone',
           'com.apple.mobile.third_party_termination',
           'com.apple.mobile.lockdownd',
           'com.apple.mobile.lockdown_cache',
           'com.apple.xcode.developerdomain',
           'com.apple.international',
           'com.apple.mobile.data_sync',
           'com.apple.mobile.tethered_sync',
           'com.apple.mobile.mobile_application_usage',
           'com.apple.mobile.backup',
           'com.apple.mobile.nikita',
           'com.apple.mobile.restriction',
           'com.apple.mobile.user_preferences',
           'com.apple.mobile.sync_data_class',
           'com.apple.mobile.software_behavior',
           'com.apple.mobile.iTunes.SQLMusicLibraryPostProcessCommands',
           'com.apple.mobile.iTunes.accessories',
           'com.apple.mobile.internal',  # < iOS 4.0+
           'com.apple.mobile.wireless_lockdown',  # < iOS 4.0+
           'com.apple.fairplay',
           'com.apple.iTunes',
           'com.apple.mobile.iTunes.store',
           'com.apple.mobile.iTunes',
           'com.apple.fmip',
           'com.apple.Accessibility', ]


class LockdownClient(object):
    DEFAULT_CLIENT_NAME = 'pymobiledevice3'
    SERVICE_PORT = 62078

    def __init__(self, udid=None, client_name=DEFAULT_CLIENT_NAME, autopair=True, connection_type=None):
        device = usbmux.select_device(udid, connection_type=connection_type)
        if device is None:
            if udid:
                raise ConnectionFailedError()
            else:
                raise NoDeviceConnectedError()

        self.usbmux_device = device
        self.logger = logging.getLogger(__name__)
        self.paired = False
        self.SessionID = None
        self.service = ServiceConnection.create(udid, self.SERVICE_PORT, connection_type=device.connection_type)
        self.host_id = self.generate_host_id()
        self.system_buid = None
        self.label = client_name
        self.pair_record = None

        if self.query_type() != 'com.apple.mobile.lockdown':
            raise IncorrectModeError()

        self.all_values = self.get_value()
        self.udid = self.all_values.get('UniqueDeviceID', self.usbmux_device.serial)
        self.unique_chip_id = self.all_values.get('UniqueChipID')
        self.device_public_key = self.all_values.get('DevicePublicKey')
        self.ios_version = self.all_values.get('ProductVersion')
        self.identifier = self.udid

        if not self.identifier:
            if self.unique_chip_id:
                self.identifier = '%x' % self.unique_chip_id
            else:
                raise PyMobileDevice3Exception('Could not get UDID or ECID, failing')

        if not self.validate_pairing():
            # device is not paired

            if not autopair:
                # but pairing by default was not requested
                return

            self.pair()
            if not self.validate_pairing():
                raise FatalPairingError()
            self.service = ServiceConnection.create(udid, self.SERVICE_PORT,
                                                    connection_type=self.usbmux_device.connection_type)

        # reload data after pairing
        self.all_values = self.get_value()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def query_type(self):
        return self.service.send_recv_plist({'Label': self.label, 'Request': 'QueryType'}).get('Type')

    @property
    def all_domains(self) -> Mapping:
        result = self.all_values

        for domain in DOMAINS:
            result.update(self.get_value(domain))

        return result

    @property
    def short_info(self) -> Mapping:
        keys_to_copy = ['DeviceClass', 'DeviceName', 'BuildVersion', 'ProductVersion', 'ProductType']
        result = {
            'ConnectionType': self.usbmux_device.connection_type,
            'Serial': self.usbmux_device.serial,
        }
        for key in keys_to_copy:
            result[key] = self.all_values.get(key)
        return result

    @property
    def enable_wifi_connections(self):
        return self.get_value('com.apple.mobile.wireless_lockdown').get('EnableWifiConnections', False)

    @enable_wifi_connections.setter
    def enable_wifi_connections(self, value: bool):
        self.set_value(value, 'com.apple.mobile.wireless_lockdown', 'EnableWifiConnections')

    @property
    def ecid(self):
        return self.all_values['UniqueChipID']

    @property
    def date(self):
        return datetime.datetime.fromtimestamp(self.get_value(key='TimeIntervalSince1970'))

    @property
    def language(self):
        return self.get_value(key='Language', domain='com.apple.international')

    @property
    def locale(self):
        return self.get_value(key='Locale', domain='com.apple.international')

    @property
    def preflight_info(self):
        return self.get_value(key='FirmwarePreflightInfo')

    @property
    def sanitized_ios_version(self):
        return sanitize_ios_version(self.ios_version)

    def set_language(self, language: str):
        self.set_value(language, key='Language', domain='com.apple.international')

    def set_locale(self, locale: str):
        self.set_value(locale, key='Locale', domain='com.apple.international')

    @staticmethod
    def generate_host_id() -> str:
        hostname = platform.node()
        host_id = uuid.uuid3(uuid.NAMESPACE_DNS, hostname)
        return str(host_id).upper()

    @reconnect_on_remote_close
    def enter_recovery(self):
        self.service.send_plist({'Request': 'EnterRecovery'})
        return self.service.recv_plist()

    def stop_session(self):
        if self.SessionID and self.service:
            self.service.send_plist({'Label': self.label, 'Request': 'StopSession', 'SessionID': self.SessionID})
            self.SessionID = None
            res = self.service.recv_plist()
            if not res or res.get('Result') != 'Success':
                raise CannotStopSessionError()
            return res

    def get_itunes_pairing_record(self):
        platform_type = 'linux' if not sys.platform.startswith('linux') else sys.platform
        filename = LOCKDOWN_PATH[platform_type] / f'{self.identifier}.plist'
        try:
            with open(filename, 'rb') as f:
                pair_record = plistlib.load(f)
        except (PermissionError, FileNotFoundError, plistlib.InvalidFileException):
            return None
        return pair_record

    def get_usbmux_pairing_record(self):
        mux = usbmux.create_mux()
        if not isinstance(mux, PlistMuxConnection):
            return None
        pairing_record = mux.get_pair_record(self.udid)
        mux.close()
        return pairing_record

    def get_local_pairing_record(self):
        self.logger.debug('Looking for pymobiledevice3 pairing record')
        path = HOMEFOLDER / f'{self.identifier}.plist'
        if not path.exists():
            self.logger.error(f'No pymobiledevice3 pairing record found for device {self.identifier}')
            return None
        return plistlib.loads(path.read_bytes())

    def validate_pairing(self):
        pair_record = self.get_itunes_pairing_record()
        if pair_record is not None:
            self.logger.info(f'Using iTunes pair record: {self.identifier}.plist')
        elif Version(self.ios_version) >= Version('13.0'):
            pair_record = self.get_usbmux_pairing_record()
        else:
            pair_record = self.get_local_pairing_record()

        if pair_record is None:
            return False

        self.pair_record = pair_record

        cert_pem = pair_record['HostCertificate']
        private_key_pem = pair_record['HostPrivateKey']

        if Version(self.ios_version) < Version('11.0'):
            validate_pair = {'Label': self.label, 'Request': 'ValidatePair', 'PairRecord': pair_record}
            self.service.send_plist(validate_pair)
            r = self.service.recv_plist()
            if (not r) or ('Error' in r):
                self.logger.error('ValidatePair fail', validate_pair)
                return False

        self.host_id = pair_record.get('HostID', self.host_id)
        self.system_buid = pair_record.get('SystemBUID', self.system_buid)
        start_session = self.service.send_recv_plist(
            {'Label': self.label, 'Request': 'StartSession', 'HostID': self.host_id, 'SystemBUID': self.system_buid}
        )
        self.SessionID = start_session.get('SessionID')
        if start_session.get('EnableSessionSSL'):
            lf = b'\n'
            self.ssl_file = write_home_file(f'{self.identifier}_ssl.txt', cert_pem + lf + private_key_pem)
            self.service.ssl_start(self.ssl_file, self.ssl_file)

        self.paired = True
        return True

    @reconnect_on_remote_close
    def pair(self):
        self.device_public_key = self.get_value('', 'DevicePublicKey')
        if not self.device_public_key:
            self.logger.error('Unable to retrieve DevicePublicKey')
            self.service.close()
            raise PairingError()

        self.logger.info('Creating host key & certificate')
        cert_pem, private_key_pem, device_certificate = ca_do_everything(self.device_public_key)

        pair_record = {'DevicePublicKey': self.device_public_key,
                       'DeviceCertificate': device_certificate,
                       'HostCertificate': cert_pem,
                       'HostID': self.host_id,
                       'RootCertificate': cert_pem,
                       'SystemBUID': '30142955-444094379208051516'}

        pair = self.service.send_recv_plist({'Label': self.label, 'Request': 'Pair', 'PairRecord': pair_record,
                                             'ProtocolVersion': '2', 'PairingOptions': {'ExtendedPairingErrors': True}})

        if pair.get('Error') == 'PasswordProtected':
            self.service.close()
            raise NotTrustedError()
        elif pair.get('Result') != 'Success' and 'EscrowBag' not in pair:
            self.logger.error(pair.get('Error'))
            self.service.close()
            raise PairingError()

        pair_record['HostPrivateKey'] = private_key_pem
        pair_record['EscrowBag'] = pair.get('EscrowBag')
        write_home_file(f'{self.identifier}.plist', plistlib.dumps(pair_record))

        record_data = plistlib.dumps(pair_record)

        client = usbmux.create_mux()
        if isinstance(client, PlistMuxConnection):
            client.save_pair_record(self.udid, self.usbmux_device.devid, record_data)

        self.paired = True

    @reconnect_on_remote_close
    def unpair(self) -> Mapping:
        req = {'Label': self.label, 'Request': 'Unpair', 'PairRecord': self.pair_record, 'ProtocolVersion': '2'}
        return self.service.send_recv_plist(req)

    @reconnect_on_remote_close
    def get_value(self, domain=None, key=None):
        if isinstance(key, str) and hasattr(self, 'record') and hasattr(self.pair_record, key):
            return self.pair_record[key]

        req = {'Label': self.label, 'Request': 'GetValue'}

        if domain:
            req['Domain'] = domain
        if key:
            req['Key'] = key

        res = self.service.send_recv_plist(req)
        if res:
            r = res.get('Value')
            if hasattr(r, 'data'):
                return r.data
            return r

    @reconnect_on_remote_close
    def set_value(self, value, domain=None, key=None):
        req = {'Request': 'SetValue', 'Label': self.label}

        if domain:
            req['Domain'] = domain
        if key:
            req['Key'] = key

        req['Value'] = value
        self.service.send_plist(req)
        response = self.service.recv_plist()
        self.logger.debug(response)
        return response

    def get_service_connection_attributes(self, name, escrow_bag=None) -> dict:
        if not self.paired:
            self.logger.info('NotPaired')
            raise NotPairedError()

        request = {'Label': self.label, 'Request': 'StartService', 'Service': name}
        if escrow_bag is not None:
            request['EscrowBag'] = escrow_bag

        self.service.send_plist(request)
        response = self.service.recv_plist()
        if not response or response.get('Error'):
            if response.get('Error', '') == 'PasswordProtected':
                raise PasswordRequiredError(
                    'your device is protected with password, please enter password in device and try again')
            raise StartServiceError(response.get("Error"))
        return response

    @reconnect_on_remote_close
    def start_service(self, name, escrow_bag=None) -> ServiceConnection:
        attr = self.get_service_connection_attributes(name, escrow_bag=escrow_bag)
        service_connection = ServiceConnection.create(self.udid, attr['Port'],
                                                      connection_type=self.usbmux_device.connection_type)
        if attr.get('EnableServiceSSL', False):
            service_connection.ssl_start(self.ssl_file, self.ssl_file)
        return service_connection

    async def aio_start_service(self, name, escrow_bag=None) -> ServiceConnection:
        attr = self.get_service_connection_attributes(name, escrow_bag=escrow_bag)
        service_connection = ServiceConnection.create(self.udid, attr['Port'],
                                                      connection_type=self.usbmux_device.connection_type)
        if attr.get('EnableServiceSSL', False):
            await service_connection.aio_ssl_start(self.ssl_file, self.ssl_file)
        return service_connection

    def start_developer_service(self, name, escrow_bag=None) -> ServiceConnection:
        try:
            return self.start_service(name, escrow_bag)
        except (StartServiceError, ConnectionFailedError):
            self.logger.error(
                'Failed to connect to required service. Make sure DeveloperDiskImage.dmg has been mounted. '
                'You can do so using: pymobiledevice3 mounter mount'
            )
            raise

    def close(self):
        self.service.close()
