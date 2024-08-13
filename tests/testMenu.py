from unittest import TestCase, mock
from source.menu import main, passwordManager, getInput
import curses	

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
    
    