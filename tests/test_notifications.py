import unittest
from unittest.mock import patch, MagicMock, call

from lifeguard_notification_msteams.notifications import MSTeamsNotificationBase

MOCK_LOGGER = MagicMock(name="logger")
MOCK_MSTEAMS = MagicMock(name="pymsteams")


class MSTeamsNotificationBaseTest(unittest.TestCase):
    def setUp(self):
        self.notification = MSTeamsNotificationBase()
        self.mock_card = MagicMock(name="card")

        MOCK_MSTEAMS.connectorcard.return_value = self.mock_card

    def test_get_name(self):
        self.assertEqual(self.notification.name, "msteams")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_send_single_message(self):
        self.notification.send_single_message("content", {})

        self.mock_card.title.assert_called_with("Single Notification")
        self.mock_card.text.assert_called_with("content")
        self.mock_card.send.assert_called()

        MOCK_MSTEAMS.connectorcard.assert_called_with("")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_send_multiple_single_message(self):
        self.notification.send_single_message(["line1", "line2"], {})

        self.mock_card.title.assert_called_with("Single Notification")
        self.mock_card.text.assert_called_with("line1\nline2")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_init_thread(self):
        self.notification.init_thread("content", {})

        self.mock_card.title.assert_called_with("Problem Found")
        self.mock_card.text.assert_called_with("content")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_init_thread_with_multiples_messages(self):

        threads = self.notification.init_thread(["line1", "line2"], {})

        self.mock_card.title.assert_called_with("Problem Found")
        self.mock_card.text.assert_called_with("line1\nline2")

        self.assertEqual(threads, [])

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_update_thread(self):
        self.notification.update_thread(["thread"], "content", {})

        self.mock_card.title.assert_called_with("Updating Problem Status")
        self.mock_card.text.assert_called_with("content")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams", MOCK_MSTEAMS)
    def test_close_thread(self):
        self.notification.close_thread(["thread"], "content", {})

        self.mock_card.title.assert_called_with("Problem Solved")
        self.mock_card.text.assert_called_with("content")

    @patch("lifeguard_notification_msteams.notifications.logger", MOCK_LOGGER)
    @patch("lifeguard_notification_msteams.notifications.pymsteams")
    def test_init_multiple_threads_with_multiples_messages(self, mock_pymsteams):
        mock_card = MagicMock(name="card")

        mock_pymsteams.connectorcard.return_value = mock_card

        self.notification.init_thread(
            ["line1", "line2"],
            {"notification": {"msteams": {"channels": ["r1", "r2"]}}},
        )

        self.mock_card = MagicMock(name="card")
        mock_pymsteams.connectorcard.assert_has_calls([call("r1"), call("r2")])
