from typing import Optional
from tx import Transaction
from transactions import license, system_assets

transaction_list = {
    "licenciamiento": license.License,
    "activos sistemas": system_assets.System_Assets
}

def get_transaction_class(transaction: str = "") -> Optional[Transaction]:
    return transaction_list.get(transaction, None)

def get_transaction_fields(transaction: Transaction = None) -> dict:
    if transaction:
        return transaction.fields

def get_transaction(transaction: Transaction = None, config: dict = None) -> Transaction:
    if transaction and config:
        return transaction(**config)
