import asyncio

from datetime import datetime
from typing import Tuple

if __name__ != "__main__":
    from . import transactions
    from .app import (
        get_transaction_class,
        get_transaction_fields,
        check_password,
        exec_transaction,
        login,
        check_file_exist
    )
    from .app.cli import read_transaction_num, read_transaction_config
    from .gui import sap_gui
    from .models.tx import Transaction
    from .settings import get_config
else:
    import transactions
    from app import (
        get_transaction_class,
        get_transaction_fields,
        check_password,
        exec_transaction,
        login,
        check_file_exist
    )
    from app.cli import read_transaction_num, read_transaction_config
    from gui import sap_gui
    from models.tx import Transaction
    from settings import get_config


async def get_transaction_name() -> Tuple[bool, str]:
    options_len = len(transactions.transaction_list)
    transaction_num = read_transaction_num(transactions.transaction_list)
    if transaction_num.isdigit() and (1 <= int(transaction_num) <= options_len ):
        return True, list(
            transactions.transaction_list.keys()
        )[int(transaction_num) - 1]

    return False, f"Opción incorrecta, debe ingresar un número entre 1 y {options_len}"

async def get_transaction_config(transaction_class: Transaction, config: dict) -> dict:
    fields = await get_transaction_fields(transaction_class)
    new_config = read_transaction_config(config, fields)
    return new_config


async def main(
    config: dict = {},
    path: str = "",
    file_name: str = "",
    transaction_name: str = "",
    tx_config: dict = {}
) -> Tuple[bool, str]:

    if not config:
        has_config, result, config = get_config()
        if not has_config:
            return has_config, result

    path = config["PYSAP_PATH"]
    file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"

    gui = sap_gui.SAP_Gui(
        gui_path=config["PYSAP_GUI_PATH"],
        name=config["PYSAP_CONNECTION_NAME"],
        instance_number=config["PYSAP_INSTANCE_NUMBER"]
    )

    if not transaction_name:
        result = await get_transaction_name()
    else:
        result = True, transaction_name

    if not result[0]:
        return result

    transaction_name = result[1]

    result = await get_transaction_class(transaction_name)
    if not result[0]:
        return result

    transaction_class = result[1]

    if not tx_config:
        tx_config = {
            "file_path": path,
            "file_name": f"{transaction_class.__qualname__.lower()}_{file_name}",
        }

        tx_config = await get_transaction_config(transaction_class, tx_config)

    transaction = await transactions.get_transaction(
        transaction=transaction_class,
        config=tx_config
    )

    result = await check_password(gui, config)

    if not result[0]:
        return result

    config = result[2]

    result = await login(gui, config["PYSAP_USER"], config["PYSAP_PASSWORD"])
    if not result[0]:
        return result

    result = await exec_transaction(gui=gui, tx=transaction)
    await gui.close_session()

    if not result[0]:
        return result

    return await check_file_exist(path, transaction.file_name)

if __name__ == "__main__":
    result = asyncio.run(main())
    check_mark = "▲" if result[0] else "▼"
    print(f"[{check_mark}] {result[1]}")
