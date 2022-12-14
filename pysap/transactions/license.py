from typing import List
import win32com.client

class License:
    """
        Clase que permite la conexión con SAP para obtener un archivo Excel con el listado de Licencias de la Compañía utilizando la transacción S_ALR_87011967
    """
    fields: dict = {"company_code": "Código de compañía separados por coma"}

    def __init__(self, company_code:List[str], file_path: str, file_name: str) -> None:
        self.transaction_code = "S_ALR_87011967"
        self.company_code = company_code
        self.file_path = file_path
        self.file_name = file_name
        self.variant = "LIC*"

    async def open(self, session: win32com.client.CDispatch) -> 'License':
        session.findById("wnd[0]/tbar[0]/okcd").text = f"/n{self.transaction_code}"
        session.findById("wnd[0]").sendVKey(0)

        return self

    async def config(self, session: win32com.client.CDispatch) -> 'License':
        session.findById("wnd[0]/tbar[1]/btn[17]").press()
        session.findById("wnd[1]/usr/txtV-LOW").text = self.variant
        session.findById("wnd[1]/usr/txtENAME-LOW").text = ""
        session.findById("wnd[1]/usr/txtENAME-LOW").setFocus()
        session.findById("wnd[1]/usr/txtENAME-LOW").caretPosition = 0
        session.findById("wnd[1]/tbar[0]/btn[8]").press()
        session.findById("wnd[0]/tbar[1]/btn[19]").press()
        session.findById("wnd[0]/usr/btn%_BUKRS_%_APP_%-VALU_PUSH").press()
        for i, val in enumerate(self.company_code):
            session.findById(f"wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,{i}]").text = val
        session.findById("wnd[1]/tbar[0]/btn[8]").press()

        return self

    async def exec(self, session: win32com.client.CDispatch) -> 'License':
        session.findById("wnd[0]/tbar[1]/btn[8]").press()

        return self

    async def config_report(self, session: win32com.client.CDispatch) -> 'License':
        return self

    async def save(self, session: win32com.client.CDispatch) -> 'License':
        session.findById("wnd[0]").sendVKey(9)
        session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
        session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[1]/usr/ctxtDY_PATH").setFocus()
        session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = 0
        session.findById("wnd[1]").sendVKey(4)
        session.findById("wnd[2]/usr/ctxtDY_PATH").text = self.file_path
        session.findById("wnd[2]/usr/ctxtDY_FILENAME").text = self.file_name
        session.findById("wnd[2]").sendVKey(0)
        session.findById("wnd[1]").sendVKey(0)

        return self

    async def close(self, session: win32com.client.CDispatch) -> None:
        for _ in range(5):
            session.findById("wnd[0]/tbar[0]/btn[12]").press()
