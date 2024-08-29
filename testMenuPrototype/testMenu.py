from unittest import TestCase, mock
from source.menu import main, passwordManager, getInput
import curses	

# This class contains the tests for the menu.py file.
# Here is no hopefully no need to test the curses library
# as it is a standard library and should work as expected
# The only thing that is tested is the input function TODO
class testMenu(TestCase):
    def testMain(self) -> None:
        self.assertIsNone(main())

    def testPasswordManager(self) -> None:
        self.assertIsNone(passwordManager())

    @mock.patch('curses.initscr', create=True)
    @mock.patch('source.menu.getInput', create=True)
    @mock.patch('curses.window', create=True)
    def testGetInput(self,mockedInitscr: mock.MagicMock, mockedInput: mock.MagicMock, mockedWindow: mock.MagicMock) -> None:
        mockedInput.call_args_list = []
        mockedInput.side_effect = ['Hello', 'World']
        mockedWindow.getmaxyx.return_value = (10, 10)
        mockedWindow.initscr.return_value = mockedWindow
        mockedWindow.newwin.side_effect = [mockedWindow, mockedWindow]
        mockedWindow.newwin.return_value = mockedWindow
        mockedInitscr.return_value = mockedWindow
        self.assertEqual(getInput(mockedWindow, "go"), 'Hello')
        self.assertEqual(getInput(mockedWindow, "hi"), 'World')
    
    