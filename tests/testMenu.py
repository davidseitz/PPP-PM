import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import time
from source.menu import *

class testMenu(unittest.TestCase):
    """

        @patch("builtins.open", new_callable=mock_open, read_data='{}')
        def test_save_user(self, mock_file):
            username = "testuser"
            password = "testpass"
            save_user(username, password)
            mock_file.assert_called_with(f"{username}_user.json", "w", encoding="utf-8")
            handle = mock_file()
            written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
            saved_data = json.loads(written_data)
            self.assertEqual(saved_data["username"], username)
            self.assertEqual(saved_data["password"], password)

        @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "username": "testuser", "password": "testpass", "failed_attempts": 0, "lockout_time": 0
        }))
        @patch("time.time", return_value=time.time())
        def test_validate_user_success(self):
            username = "testuser"
            password = "testpass"
            result, message = validate_user(username, password)
            self.assertTrue(result)
            self.assertEqual(message, "Login successful.")

        @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
            "username": "testuser", "password": "wrongpass", "failed_attempts": 0, "lockout_time": 0
        }))
        @patch("time.time", return_value=time.time())
        def test_validate_user_fail(self):
            username = "testuser"
            password = "testpass"
            result, message = validate_user(username, password)
            self.assertFalse(result)
            self.assertEqual(message, "Invalid username or password.")

        @patch("os.path.exists", return_value=True)
        @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{
            "site": "example.com", "password": "oldpassword", "old_passwords": []
        }]))
        def test_save_password_update(self, mock_file):
            username = "testuser"
            site = "example.com"
            new_password = "newpassword"
            result = save_password(username, site, new_password)
            self.assertTrue(result)
            handle = mock_file()
            written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
            saved_data = json.loads(written_data)
            self.assertEqual(saved_data[0]["password"], new_password)
            self.assertIn("oldpassword", saved_data[0]["old_passwords"])

        @patch("os.path.exists", return_value=False)
        @patch("builtins.open", new_callable=mock_open)
        def test_save_password_new(self, mock_file):
            username = "testuser"
            site = "newsite.com"
            new_password = "newpassword"
            result = save_password(username, site, new_password)
            self.assertTrue(result)
            handle = mock_file()
            written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
            saved_data = json.loads(written_data)
            self.assertEqual(saved_data[0]["site"], site)
            self.assertEqual(saved_data[0]["password"], new_password)
            self.assertEqual(saved_data[0]["old_passwords"], [])

        @patch("os.path.exists", return_value=True)
        def test_user_exists(self):
            username = "testuser"
            self.assertTrue(user_exists(username))

        @patch("os.path.exists", return_value=False)
        def test_user_not_exists(self):
            username = "newuser"
            self.assertFalse(user_exists(username))

        @patch("menu.get_input", return_value="example.com")
        @patch("menu.save_password", return_value=True)
        def test_add_password(self, mock_save_password):
            stdscr = MagicMock()
            username = "testuser"
            add_password(stdscr, username)
            self.assertTrue(mock_save_password.called)

        @patch("menu.get_input", return_value="16")
        @patch("curses.newwin")
        def test_generate_password(self, mock_newwin):
            stdscr = MagicMock()
            mock_win = MagicMock()
            mock_newwin.return_value = mock_win

            with patch('curses.initscr', return_value=stdscr):
                with patch('curses.start_color'):
                    with patch('curses.init_pair'):
                        with patch('curses.color_pair', return_value=1):
                            generate_password(stdscr)
                            stdscr.addstr.assert_any_call(1, 0, "Generated password:")


    if __name__ == "__main__":
        unittest.main()
    """