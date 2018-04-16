from rest_framework.test import APITestCase

from app_system import utils


class SystemTests(APITestCase):
    def setUp(self):
        pass

    def test(self):
        data = {
            "system_ip": "45.77.51.246",
            "system_name": "root",
            "system_pass": "cZ$73Dj*)}a3?[6M",
            "ss_port": "8388",
            "ss_pass": "plover.cloud",
            "is_share": "plover.cloud",
        }
        utils.config_ss(**data)

    def test2(self):
        data = {
            "system_ip": "45.77.51.246",
            "system_name": "root",
            "system_pass": "cZ$73Dj*)}a3?[6M",
            "ss_port": "8388",
            "ss_pass": "plover.cloud",
        }
        utils.reboot_ss(**data)
