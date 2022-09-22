from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

from gui import sap_gui
from transactions import license


config = dotenv_values(".env")

path = r"C:/Users/alobo/Desktop/Final"
file_name = f"license_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
license_company_code = "1000"

gui = sap_gui.SAP_Gui(
    gui_path=config["GUI_PATH"],
    name=config["CONNECTION_NAME"],
    instance_number=config["INSTANCE_NUMBER"]
)

lic = license.License(
    company_code=["1000",],
    file_path=path,
    file_name=file_name,
)
gui.open_gui().create_session().login(config["USER"], config["PASS"]).open_tx(lic).process_tx(lic).save_tx(lic).close_tx(lic).close_session()

result = Path(f"{path}/{file_name}")
if result.exists():
    print(f"Archivo creado correctamente: {result.name}")
