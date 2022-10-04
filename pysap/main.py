import asyncio

from datetime import datetime
from typing import Tuple

from dotenv import dotenv_values

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
    from .gui import sap_gui
    from .models.tx import Transaction
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
    from gui import sap_gui
    from models.tx import Transaction


async def get_transaction_name() -> str:
    tx_options = '\n'.join(
        [
            f"{i}. {val}"
            for i, val in enumerate(transactions.transaction_list.keys(), 1)
        ]
    )
    transaction_num = (
        input(f"[►] Ingrese el número de la transacción que desea ejecutar: \n{tx_options}\n")
    ).strip()
    return [
        (tx.split(".")[1]).strip()
        for tx in tx_options.split("\n")
        if tx.split(".")[0] == transaction_num
    ][0]

async def get_transaction_config(transaction_class: Transaction, config: dict) -> dict:
    fields = await get_transaction_fields(transaction_class)
    for field, hint in fields:
        value = (input(f"[►] Ingrese el valor para {field}, {hint}: ")).split(",")
        if "coma" in str(hint).lower():
            config[field] = [val.strip() for val in value]
        else:
            config[field] = value

    return config


async def main(
    config: dict,
    path: str,
    file_name: str,
    transaction_name: str = "",
    tx_config: dict = {}
) -> Tuple[bool, str]:
    gui = sap_gui.SAP_Gui(
        gui_path=config["GUI_PATH"],
        name=config["CONNECTION_NAME"],
        instance_number=config["INSTANCE_NUMBER"]
    )

    if not transaction_name:
        transaction_name = await get_transaction_name()

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

    last_change_date = datetime.strptime(
        config["PASS_LAST_CHANGE"], "%d/%m/%Y"
    ).date()
    result = await check_password(gui, last_change_date)
    if not result[0]:
        return result

    result = await login(gui, config["USER"], config["PASSWORD"])
    if not result[0]:
        return result

    result = await exec_transaction(gui=gui, tx=transaction)
    await gui.close_session()

    if not result[0]:
        return result

    return await check_file_exist(path, transaction.file_name)

if __name__ == "__main__":
    config = dotenv_values(".env")
    path = config["PATH"]
    file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    result = asyncio.run(main(config, path, file_name))
    check_mark = "▲" if result[0] else "▼"
    print(f"[{check_mark}] {result[1]}")
