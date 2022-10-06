import os
from typing import Tuple
import dotenv

basic_keys = [
    "PYSAP_GUI_PATH",
    "PYSAP_CONNECTION_NAME",
    "PYSAP_INSTANCE_NUMBER",
    "PYSAP_USER",
    "PYSAP_PASSWORD",
    "PYSAP_PASS_LAST_CHANGE",
    "PYSAP_PATH",
]

dotenv_file = None


def get_config() -> Tuple[bool, str, dict]:
    env_conf = __config_env()

    if env_conf[0]:
        return env_conf

    return False, f"{env_conf[1]}", {}


def write_config(new_config: dict) -> None:
    for key, val in new_config.items():
        dotenv.set_key(dotenv_file, key, val)


def __config_env() -> Tuple[bool, str, dict]:
    global dotenv_file
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    config = {key: val for key, val in os.environ.items() if key in basic_keys}

    if not len(config):
        return (
            False,
            "No se encontró el archivo .env",
            {}
        )

    not_in_config = []
    for val in basic_keys:
        if val not in config:
            not_in_config.append(val)

    if not_in_config:
        return (
            False,
            f"No se encontró valor a las variables: {str.join(', ', not_in_config)}",
            {}
        )

    return True, "", config


def __config_os() -> Tuple[bool, str, dict]:
    not_in_config = []
    config = os.environ
    for val in basic_keys:
        if val not in config.keys():
            not_in_config.append(val)

    if not_in_config:
        return (
            False,
            f"No se encontraron las siguientes variables de entorno: {str.join(', ', not_in_config)}",
            {}
        )

    config = {key: val for key, val in os.environ.items() if key in basic_keys}
    return True, "", config
