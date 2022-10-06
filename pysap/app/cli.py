
def read_transaction_num(transactions: dict):
    tx_options = '\n'.join(
        [
            f"{i}. {val}"
            for i, val in enumerate(transactions.keys(), 1)
        ]
    )
    return (
        input(f"[►] Ingrese el número de la transacción que desea ejecutar: \n{tx_options}\n")
    ).strip()


def read_transaction_config(tx_config: dict, tx_config_fields: dict):
    for field, hint in tx_config_fields:
        value = (input(f"[►] Ingrese el valor para {field}, {hint}: ")).split(",")
        if "coma" in str(hint).lower():
            tx_config[field] = [val.strip() for val in value]
        else:
            tx_config[field] = value

    return tx_config
