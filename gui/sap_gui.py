from time import sleep
import win32com.client
from subprocess import call
from typing import Any, Optional
from pathlib import Path

from error_handle import error_handler
from tx import Transaction


class SAP_Gui:
    __application: Any
    __connection: Any
    __session: Any

    def __init__(self, gui_path:str, name: str, instance_number: str) -> None:
        self.gui_path = gui_path
        self.name = name
        self.instance_number = instance_number

    @error_handler
    def open_gui(self):
        win32com.client.Dispatch("WScript.Shell")
        call(f'{Path(self.gui_path).joinpath("SAPgui.exe").as_posix()} {self.name} {self.instance_number}')
        sleep(20)

        return self

    @error_handler
    def create_session(self) -> Optional['SAP_Gui']:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        self.__application = SapGuiAuto.GetScriptingEngine
        if not type(self.__application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return

        self.__connection = self.__application.Children(0)
        if not type(self.__connection) == win32com.client.CDispatch:
            self.__application = None
            SapGuiAuto = None
            return

        self.__session = self.__connection.Children(0)
        if not type(self.__session) == win32com.client.CDispatch:
            self.__connection = None
            self.__application = None
            SapGuiAuto = None
            return

        return self

    @error_handler
    def close_session(self) -> None:
        if self.__session:
            self.__session = None
            self.__connection.closeSession("ses[0]")
            self.__connection = None
            sleep(5)
            self.__application = None

    @error_handler
    def login(self, user, password) -> 'SAP_Gui':
        self.__session.findById("wnd[0]").resizeWorkingPane(173, 36, 0)
        self.__session.findById("wnd[0]/usr/txtRSYST-BNAME").text = user
        self.__session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
        self.__session.findById("wnd[0]").sendVKey(0)
        sleep(5)
        return self

    @error_handler
    def open_tx(self, tr: Transaction) -> 'SAP_Gui':
        tr.open(self.__session)
        return self

    @error_handler
    def process_tx(self, tr: Transaction) -> 'SAP_Gui':
        tr.process(self.__session)
        sleep(2)
        return self

    @error_handler
    def save_tx(self, tr: Transaction) -> 'SAP_Gui':
        tr.save(self.__session)
        return self

    @error_handler
    def close_tx(self, tr: Transaction) -> 'SAP_Gui':
        tr.close(self.__session)
        return self
