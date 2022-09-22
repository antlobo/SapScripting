from typing import Optional
from tx import Transaction
from transactions import license

def get_transaction(transaction: str, config: dict) -> Optional[Transaction]:
    if transaction == "license":
        return license.License(
            company_code=config["company_code"],
            file_path=config["path"],
            file_name=f'license_{config["file_name"]}',
        )
    else:
        return None
