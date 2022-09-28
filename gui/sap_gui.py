from time import sleep
import win32com.client
from subprocess import call
from typing import Any, Optional, Tuple
from pathlib import Path

from gui.error_handle import error_handler
from tx import Transaction


class SAP_Gui:
    """Clase que permite la conexión entre python y SAP Logon. Se debe usar de la siguiente manera:
        1. Se ingresan los valores base del SAP Logon: ejecutable, nombre de la conexión y número de instancia
        2. Se abre la gui mediante la función open_gui()
        3. Se crea la sesión nueva mediante la función create_session()
        4. Se inicia sesión mediante la función login()
        5. Se valida que se haya podido iniciar sesión mediante la función is_logged()
        6. Se ejecuta la transacción de SAP en el siguiente orden:
            1. open
            2. config
            3. hasAccess
             3.1. exec
             3.2. config_report
             3.3. save
             3.4. close
        7. Se cierra la conexión con SAP mediante la función close_session()
    """
    __application: Any
    __connection: Any
    __session: Any

    def __init__(self, gui_path:str, name: str, instance_number: str, close_old_conn: bool = False) -> None:
        self.gui_path = gui_path
        self.name = name
        self.instance_number = instance_number
        self.close_old_connections = close_old_conn

    @error_handler
    def open_gui(self):
        win32com.client.Dispatch("WScript.Shell")
        call(f'{Path(self.gui_path).joinpath("SAPgui.exe").as_posix()} {self.name} {self.instance_number}')
        sleep(20)

        return self

    @error_handler
    def create_session(self) -> Tuple[Optional['SAP_Gui'], str]:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return None

        self.__application = SapGuiAuto.GetScriptingEngine
        if not type(self.__application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return None

        if self.close_old_connections:
            self.__close_old_connections()

        self.__connection = self.__application.Children(
            self.__application.Children.count - 1
        )
        if not type(self.__connection) == win32com.client.CDispatch:
            self.__application = None
            SapGuiAuto = None
            return None

        self.__session = self.__connection.Children(
            self.__connection.Children.count - 1
        )
        if not type(self.__session) == win32com.client.CDispatch:
            self.__connection = None
            self.__application = None
            SapGuiAuto = None
            return None

        return self

    @error_handler
    def __close_old_connections(self) -> None:
        """Cierra todas las ventanas abiertas de SAP Logon (conexiones abiertas)
        """
        while self.__application.Children.count > 1:
            connection = self.__application.Children(0)
            session = connection.Children(0)
            connection.closeSession(
                str(session.Id).split("/")[-1]
            )
            connection.CloseConnection()

    @error_handler
    def close_session(self) -> None:
        """Cierra la ventana abierta de SAP Logon (sesión actual)
        """
        if self.__session:
            self.__connection.closeSession(str(self.__session.Id).split("/")[-1])
            self.__connection.CloseConnection()
            sleep(5)
            self.__application = None

    @error_handler
    def login(self, user: str, password: str) -> Tuple['SAP_Gui', str]:
        """Realiza el login en SAP Logon con el usuario y contraseña provistos

        Returns
        -------
        _type_
            Retorna la misma clase y un mensaje en blanco en caso de no haber error
        """
        if self.__session:
            self.__session.findById("wnd[0]").resizeWorkingPane(173, 36, 0)
            self.__session.findById("wnd[0]/usr/txtRSYST-BNAME").text = user
            self.__session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
            self.__session.findById("wnd[0]").sendVKey(0)
        return self

    @error_handler
    def is_logged(self) -> Tuple[bool, str]:
        """Revisa que se haya logrado iniciado sesión con base en 3 elementos que aparecen o desaparecen al inciar sesión

        Returns:
            bool: Regresa verdadero si se logra inciar sesión con las credenciales provistas, en caso contrario retorna Falso
        """
        if self.__session and self.__session.findById("wnd[1]/tbar[0]/btn[0]", False) or \
                self.__session.findById("wnd[0]/tbar[1]/btn[5]", False) is None or \
                self.__session.findById("wnd[1]/usr/btnOK1", False):
            return True
        return False

    @error_handler
    def is_only_session(self) -> Tuple[bool, str]:
        if self.__session and self.__application:
            return self.__application.Children.count == 1 and \
                self.__connection.Children.count == 1
        return False

    @error_handler
    def change_password(self, user: str, password: str, new_password: str) -> Tuple['SAP_Gui', str]:
        if self.__session:
            self.__session.findById("wnd[0]/usr/txtRSYST-BNAME").text = user
            self.__session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
            self.__session.findById("wnd[0]/tbar[1]/btn[5]").press()
            self.__session.findById("wnd[1]/usr/pwdRSYST-NCODE").text = new_password
            self.__session.findById("wnd[1]/usr/pwdRSYST-NCOD2").text = new_password
            self.__session.findById("wnd[1]/tbar[0]/btn[0]").press()
            self.__session.findById("wnd[2]/tbar[0]/btn[0]").press()
        return self

    @error_handler
    def open(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.open(self.__session)
        return self

    def hasAccess(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.__session.Info.Transaction == tr.transaction_code

    @error_handler
    def config(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.config(self.__session)
        return self

    @error_handler
    def exec(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.exec(self.__session)
        return self

    @error_handler
    def config_report(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.config_report(self.__session)
        return self

    @error_handler
    def save(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.save(self.__session)
        return self

    @error_handler
    def close(self, tr: Transaction) -> Tuple['SAP_Gui', str]:
        if self.__session:
            tr.close(self.__session)
        return self
