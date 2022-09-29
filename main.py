from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

from dotenv import dotenv_values

from gui import sap_gui
from transactions import get_transaction, get_transaction_class, get_transaction_fields, transaction_list
from tx import Transaction

config = dotenv_values(".env")
path = config["PATH"]
file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"

def create_new_password(current_pass: str) -> str:
    """Crea una nueva contraseña para SAP con base en la actual

    Parameters
    ----------
    current_pass : str
        Contraseña de SAP actual con patrón: CadenaSinNumero+AñoMes = Prueba201701

    Returns
    -------
    str
        Devuelve una nueva contraseña can base en la actual cambiando la fecha dentro de la contraseña
    """
    today = datetime.now().date()
    pass_without_date = current_pass.split('2')[0]
    new_pass = f"{pass_without_date}{today.strftime('%Y%m')}"
    if new_pass == current_pass:
        one_month = timedelta(365/12)
        today = today + one_month
        new_pass = f"{pass_without_date}{today.strftime('%Y%m')}"
    return new_pass


def change_password(gui: sap_gui.SAP_Gui) -> bool:
    """_summary_

    Parameters
    ----------
    gui : sap_gui.SAP_Gui
        _description_

    Returns
    -------
    bool
        _description_
    """
    last_pass = config["PASS"]
    new_pass = create_new_password(last_pass)
    gui.open_gui()
    gui.create_session()
    result = gui.change_password(config["USER"], last_pass, new_pass)
    if result[1] != "":
        return False

    # TODO: Agregar codigo cambio de variables ambientales
    config["LAST_PASS"] = last_pass
    config["PASS"] = new_pass
    config["PASS_LAST_CHANGE"] = datetime.now().date().strftime("%d/%m/%Y")
    return True

def select_transaction(transaction: str = "") -> Optional[Transaction]:
    if not transaction:
        transaction = (input(f"[►] Ingrese cuál transacción desea de la siguiente lista, {', '.join([val for val in transaction_list.keys()])}: ")).strip()

    config = {
        "file_path": path,
        "file_name": file_name
    }
    transaction_class = get_transaction_class(transaction)
    if transaction_class:
        transaction_fields = get_transaction_fields(transaction_class).items()
        for field, hint in transaction_fields:
            value = (input(f"[►] Ingrese el valor para {field}, {hint}: ")).split(",")
            if "coma" in str(hint).lower():
                config[field] = [val.strip() for val in value]
            else:
                config[field] = value

        return get_transaction(transaction=transaction_class, config=config)

def exec_transaction(gui: sap_gui.SAP_Gui, tx: Transaction) -> str:
    gui.open(tx)[1]
    if not gui.hasAccess(tx):
        return f"No se cuenta con acceso a la transacción {tx.transaction_code}"
    gui.config(tx)[1]
    gui.exec(tx)[1]
    gui.config_report(tx)[1]
    gui.save(tx)[1]
    gui.close(tx)[1]

    return ""

def main() -> Tuple[bool, str]:
    gui = sap_gui.SAP_Gui(
        gui_path=config["GUI_PATH"],
        name=config["CONNECTION_NAME"],
        instance_number=config["INSTANCE_NUMBER"]
    )

    transaction = select_transaction()
    if not transaction:
        return False, "Transaccion no configurada en el programa"

    today = datetime.now().date()
    last_change_date = datetime.strptime(config["PASS_LAST_CHANGE"], "%d/%m/%Y").date()
    if (today - last_change_date).days >= 30:
        if not change_password(gui=gui):
            return False, "No se pudo realizar el cambio de contraseña"

    gui.open_gui()[0] \
        .create_session()[0] \
        .login(config["USER"], config["PASS"])

    if not gui.is_logged()[0]:
        gui.close_session()
        return False, "No se pudo iniciar sesión con las credenciales provistas"

    if not gui.is_only_session()[0]:
        result = input("[►] Existe una o más sesiones abiertas, desea cerrarlas y continuar? (S/N)").strip()
        if result.lower() == "s":
            gui.close_old_connections = True
            gui.open_gui()[0] \
                .create_session()[0] \
                .login(config["USER"], config["PASS"])
        else:
            gui.close_session()
            return False, "No se pudo iniciar sesión debido a que existen otras sesiones abiertas, \n" + \
                "use la opción close_old_conn = True para cerrar sesiones antiguas"

    result = exec_transaction(gui=gui, tx=transaction)
    gui.close_session()

    if result:
        return False, result

    result = Path(path) / transaction.file_name
    if result.exists():
        return True, f"Archivo creado correctamente: {result.name}"
    else:
        return False, "Transacción terminada, pero no fue generado ningún archivo"


if __name__ == "__main__":
    result = main()
    check_mark = "▲" if result[0] else "▼"
    print(f"[{check_mark}] {result[1]}")
