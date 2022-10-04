from datetime import datetime
from typing import Tuple
import pytest

from dotenv import dotenv_values

@pytest.fixture
def base_tx_config() -> Tuple[dict, dict]:
    config = dotenv_values(".env")
    path = config["PATH"]
    file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    return config, {
        "file_path": path,
        "file_name": f"license_{file_name}",
        "company_code": ["1000"]
    }
