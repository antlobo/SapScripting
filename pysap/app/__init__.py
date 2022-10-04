from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Tuple

try:
    import transactions
    from gui import sap_gui
    from models.tx import Transaction
except ModuleNotFoundError:
    from .. import transactions
    from ..gui import sap_gui
    from ..models.tx import Transaction


async def get_transaction_class(
    transaction: str
) -> Tuple[bool, Transaction | str]:
    transaction_class = await transactions.get_transaction_class(transaction)
    if transaction_class:
        return True, transaction_class

    return False, "Transaccion no configurada en el programa"


async def get_transaction_fields(transaction_class: Transaction) -> dict:
    result = await transactions.get_transaction_fields(
        transaction_class
    )
    return result.items()


async def create_new_password(current_pass: str) -> str:
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


async def change_password(
    gui: sap_gui.SAP_Gui,
    config: dict
) -> bool:
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
    new_pass = await create_new_password(last_pass)
    await gui.open_gui()
    await gui.create_session()
    result = await gui.change_password(config["USER"], last_pass, new_pass)
    if result[1] != "":
        return False

    # TODO: Agregar codigo cambio de variables ambientales
    config["LAST_PASS"] = last_pass
    config["PASS"] = new_pass
    config["PASS_LAST_CHANGE"] = datetime.now().date().strftime("%d/%m/%Y")
    return True


async def check_password(
    gui: sap_gui.SAP_Gui,
    last_change_date: date
) -> Tuple[bool, str]:

    today = datetime.now().date()
    if (today - last_change_date).days >= 30:
        if not await change_password(gui=gui):
            return False, "No se pudo realizar el cambio de contraseña"

    return True, ""


async def exec_transaction(
    gui: sap_gui.SAP_Gui,
    tx: Transaction
) -> Tuple[bool, str]:

    await gui.open(tx)
    has_access = await gui.hasAccess(tx)
    if not has_access:
        return False, f"No se cuenta con acceso a la transacción {tx.transaction_code}"
    await gui.config(tx)
    await gui.exec(tx)
    await gui.config_report(tx)
    await gui.save(tx)
    await gui.close(tx)

    return True, ""


async def login(
    gui: sap_gui.SAP_Gui,
    user: str,
    password: str
) -> Tuple[bool, str]:

    await gui.open_gui()
    await gui.create_session()
    await gui.login(user, password)

    is_logged = await gui.is_logged()
    if not is_logged[0]:
        await gui.close_session()
        return False, "No se pudo iniciar sesión con las credenciales provistas"

    return True, ""

async def check_file_exist(
    path: str,
    file_name: str
) -> Tuple[bool, str]:

    file = Path(path) / file_name
    if file.exists():
        return True, f"Archivo creado correctamente: {file.name}"
    else:
        return False, "Transacción terminada, pero no fue generado ningún archivo"