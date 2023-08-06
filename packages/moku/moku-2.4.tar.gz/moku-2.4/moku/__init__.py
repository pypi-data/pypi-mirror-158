import hashlib
import logging
import os
import tarfile

from moku.exceptions import IncompatibleMokuException
from moku.session import RequestSession
from moku.utilities import validate_range
from moku.version import compat_fw
from pkg_resources import get_distribution, resource_filename


logger = logging.getLogger("moku")
logger.level = logging.INFO

__version__ = get_distribution("moku").version
DATA_PATH = os.path.expanduser(os.environ.get('MOKU_DATA_PATH') or (
    resource_filename("moku", 'data')))


class Moku:
    def __init__(self, ip, force_connect, ignore_busy,
                 persist_state, connect_timeout,
                 read_timeout):

        self.session = RequestSession(ip, connect_timeout, read_timeout)
        self.claim_ownership(force_connect, ignore_busy, persist_state)
        description = self.describe()

        if int(description['firmware']) < compat_fw:
            raise IncompatibleMokuException(
                f"Incompatible Moku, firmware version should be "
                f"{compat_fw} or above")

        self.firmware_version = description['firmware']
        self.hardware = description['hardware'].replace(":", "").lower()
        self.bitstreams = description['bitstreams']

    def _get_server_bitstreams(self, bs_name):
        for b in self.bitstreams:
            if b.get('name') == bs_name:
                return bs_name, b.get('checksum')
        return None, None

    def _read_and_upload_stream(self, bs_name, chksum):
        upload_required = True
        with tarfile.open(self._get_data_file(self.firmware_version)) as _ts:
            bs_tarinfo = _ts.getmember(f"{self.hardware}/{bs_name}")
            bs_file = _ts.extractfile(bs_tarinfo)
            bs_data = bs_file.read()
            if chksum:
                local_chksum = hashlib.sha256(bs_data).hexdigest()
                upload_required = local_chksum != chksum
            if upload_required:
                self.upload("bitstreams", bs_name, bs_data)
            bs_file.close()

    def upload_bitstream(self, id):
        bs_name = f'01-{id:03}-00'
        _, pf_chksum = self._get_server_bitstreams('01-000')
        _, bs_chksum = self._get_server_bitstreams(bs_name)
        self._read_and_upload_stream('01-000', pf_chksum)
        self._read_and_upload_stream(bs_name, bs_chksum)

    def set_connect_timeout(self, value):
        if not isinstance(value, tuple([int, float])):
            raise Exception(
                "set_connect_timeout value should be either integer or float")
        self.session.connect_timeout = value

    def set_read_timeout(self, value):
        if not isinstance(value, tuple([int, float])):
            raise Exception(
                "read_timeout value should be either integer or float")
        self.session.read_timeout = value

    @staticmethod
    def _get_data_file(firmware_version):
        file_name = f'mokudata-{firmware_version}.tar.gz'
        path = os.path.join(DATA_PATH, file_name)
        if not os.path.exists(path):
            raise Exception(
                'Instrument files not available, please run `moku download --fw_ver={}` to'
                'download latest instrument data'.format(firmware_version))
        return path

    def claim_ownership(
            self,
            force_connect=True,
            ignore_busy=False,
            persist_state=False):
        """
        Claim the ownership of Moku.

        :type force_connect: `boolean`
        :param force_connect: Force connection to Moku disregarding any existing connections

        :type ignore_busy: `boolean`
        :param ignore_busy: Ignore the state of instrument including any in progress data logging sessions and proceed with the deployment

        :type persist_state: `boolean`
        :param persist_state: When true, tries to retain the previous state of the instrument(if available)

        """
        operation = "claim_ownership"
        params = dict(
            force_connect=force_connect,
            ignore_busy=ignore_busy,
            persist_state=persist_state,
        )
        return self.session.post("moku", operation, params)

    def relinquish_ownership(self):
        """
        Relinquish the ownership of Moku.
        """
        operation = "relinquish_ownership"
        return self.session.post("moku", operation)

    def name(self):
        """
        name.
        """
        operation = "name"
        return self.session.get("moku", operation)

    def serial_number(self):
        """
        serial_number.
        """
        operation = "serial_number"
        return self.session.get("moku", operation)

    def summary(self):
        """
        summary.
        """
        operation = "summary"
        return self.session.get("moku", operation)

    def describe(self):
        """
        describe.
        """
        operation = "describe"
        return self.session.get("moku", operation)

    def firmware_version(self):
        """
        firmware_version.
        """
        operation = "firmware_version"
        return self.session.get("moku", operation)

    def get_power_supplies(self):
        """
        get_power_supplies.
        """
        operation = "get_power_supplies"
        return self.session.get("moku", operation)

    def get_power_supply(self, id):
        """
        get_power_supply.

        :type id: `integer`
        :param id: ID of the power supply

        """
        operation = "get_power_supply"
        params = dict(id=id,)
        return self.session.post("moku", operation, params)

    def set_power_supply(self, id, enable=True, voltage=3, current=0.1):
        """
        set_power_supply.

        :type id: `integer`
        :param id: ID of the power supply to configure

        :type enable: `boolean`
        :param enable: Enable/Disable power supply

        :type voltage: `number`
        :param voltage: Voltage set point

        :type current: `number`
        :param current: Current set point

        """
        operation = "set_power_supply"
        params = dict(
            id=id,
            enable=enable,
            voltage=voltage,
            current=current,
        )
        return self.session.post("moku", operation, params)

    def has_external_clock(self):
        """
        has_external_clock.
        """
        operation = "has_external_clock"
        return self.session.get("moku", operation)

    def using_external_clock(self):
        """
        using_external_clock.
        """
        operation = "using_external_clock"
        return self.session.get("moku", operation)

    def enable_external_clock(self, external=True):
        """
        enable_external_clock.

        :type external: `boolean`
        :param external: Switch between external and internal reference clocks

        """
        operation = "enable_external_clock"
        params = dict(external=external,)
        return self.session.post("moku", operation, params)

    def upload(self, target, file_name, data):
        """
        Upload files to bitstreams, ssd, persist.

        :type target: `string`, (bitstreams, ssd, persist)
        :param target: Destination where the file should be uploaded to.

        :type file_name: `string`
        :param file_name: Name of the file to be uploaded

        :type data: `bytes`
        :param data: File content

        """
        target = validate_range(target, list(['bitstreams', 'ssd', 'persist']))
        operation = f"upload/{file_name}"
        return self.session.post_file(target, operation, data)

    def delete(self, target, file_name):
        """
        Delete files from bitstreams, ssd, persist.

        :type target: `string`, (bitstreams, ssd, persist)
        :param target: Destination where the file should be uploaded to.

        :type file_name: `string`
        :param file_name: Name of the file to be deleted

        """
        target = validate_range(target, list(['bitstreams', 'ssd', 'persist']))
        operation = f"delete/{file_name}"
        return self.session.delete_file(target, operation)

    def list(self, target):
        """
        List files at bitstreams, ssd, logs, persist.

        :type target: `string`, (bitstreams, ssd, persist)
        :param target: Target directory to list files for

        """
        target = validate_range(target, list(
            ['bitstreams', 'ssd', 'logs', 'persist']))
        operation = "list"
        return self.session.get(target, operation)

    def download(self, target, file_name, local_path):
        """
        Download files from bitstreams, ssd, logs, persist.

        :type target: `string`, (bitstreams, ssd, persist)
        :param target: Destination where the file should be downloaded from.

        :type file_name: `string`
        :param file_name: Name of the file to be downloaded

        :type local_path: `string`
        :param local_path: Local path to download the file

        """
        target = validate_range(target, list(
            ['bitstreams', 'ssd', 'logs', 'persist']))
        operation = f"download/{file_name}"
        return self.session.get_file(target, operation, local_path)
