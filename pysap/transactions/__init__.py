from typing import Optional

try:
    from models.tx import Transaction
except ModuleNotFoundError:
    from ..models.tx import Transaction

from . import license, system_assets

transaction_list = {
    "licenciamiento": license.License,
    "activos sistemas": system_assets.System_Assets
}

async def get_transaction_class(transaction: str = "") -> Optional[Transaction]:
    return transaction_list.get(transaction, None)

async def get_transaction_fields(transaction: Transaction = None) -> dict:
    if transaction:
        return transaction.fields

async def get_transaction(transaction: Transaction = None, config: dict = None) -> Transaction:
    if transaction and config:
        return transaction(**config)
