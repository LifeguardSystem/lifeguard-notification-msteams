import unittest

from lifeguard_notification_msteams.settings import (
    MSTEAMS_DEFAULT_CHAT_ROOM,
    SETTINGS_MANAGER,
)


class SettingsTest(unittest.TestCase):
    def test_lifeguard_mongodb_database(self):
        self.assertEqual(MSTEAMS_DEFAULT_CHAT_ROOM, "")
        self.assertEqual(
            SETTINGS_MANAGER.settings["LIFEGUARD_MSTEAMS_DEFAULT_CHAT_ROOM"][
                "description"
            ],
            "Incoming webhook full address",
        )
