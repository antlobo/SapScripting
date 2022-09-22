from datetime import datetime
from pathlib import Path

from dotenv import dotenv_values

from gui import sap_gui
from transactions import get_transaction

config = dotenv_values(".env")
path = config["PATH"]
file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"

def main() -> str:
    gui = sap_gui.SAP_Gui(
        gui_path=config["GUI_PATH"],
        name=config["CONNECTION_NAME"],
        instance_number=config["INSTANCE_NUMBER"]
    )

    transaction = get_transaction(
        transaction="license",
        config={
            "company_code": ["1000"],
            "path": path,
            "file_name": file_name
        })

    if not transaction:
        return "Transaccion no encontrada"

    gui.open_gui() \
        .create_session() \
        .login(config["USER"], config["PASS"]) \
        .open(transaction) \
        .config(transaction) \
        .exec(transaction) \
        .config_report(transaction) \
        .save(transaction) \
        .close(transaction) \
        .close_session()

    result = Path(f"{path}/{transaction.file_name}")
    if result.exists():
        return f"Archivo creado correctamente: {result.name}"


if __name__ == "__main__":
    print(main())
