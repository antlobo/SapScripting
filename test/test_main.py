import pytest
from pysap import main
from .base_config import base_tx_config


@pytest.mark.asyncio
async def test_main_correct(base_tx_config):
    transaction_name = "licenciamiento"
    config = base_tx_config[0]
    path = base_tx_config[1].get("file_path")
    file_name = base_tx_config[1].get("file_name")
    tx_config = {
        "file_path": path,
        "file_name": f"license_{file_name}",
        "company_code": ["1000"]
    }
    result = await main.main(config, path, file_name, transaction_name, tx_config)
    print(result[1])
    assert "creado" in result[1]


@pytest.mark.asyncio
async def test_main_no_valid_transaction(base_tx_config):
    transaction_name = "no valido"
    config = base_tx_config[0]
    path = base_tx_config[1].get("file_path")
    file_name = base_tx_config[1].get("file_name")
    tx_config = {
        "file_path": path,
        "file_name": f"license_{file_name}",
        "company_code": ["1000"]
    }
    result = await main.main(config, path, file_name, transaction_name, tx_config)
    print(result[1])
    assert "no configurada" in result[1]


@pytest.mark.asyncio
async def test_main_invalid_auth(base_tx_config):
    transaction_name = "licenciamiento"
    config = base_tx_config[0]
    config["USER"] = "prueba"
    path = base_tx_config[1].get("file_path")
    file_name = base_tx_config[1].get("file_name")
    tx_config = {
        "file_path": path,
        "file_name": f"license_{file_name}",
        "company_code": ["1000"]
    }
    result = await main.main(config, path, file_name, transaction_name, tx_config)
    print(result[1])
    assert "credenciales provistas" in result[1]
