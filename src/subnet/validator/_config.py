import sys
from loguru import logger
from pydantic import ConfigDict
from dotenv import load_dotenv
import threading
import time
import os
import json
import requests
from pydantic_settings import BaseSettings


def load_environment(env: str):
    if env == 'mainnet':
        dotenv_path = os.path.abspath('../env/.env.validator.mainnet')
    elif env == 'testnet':
        dotenv_path = os.path.abspath('../env/.env.validator.testnet')
    else:
        raise ValueError(f"Unknown environment: {env}")

    load_dotenv(dotenv_path=dotenv_path)


logger.remove()
logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <blue>{message}</blue>",
        level="DEBUG",
    )


class ValidatorSettings(BaseSettings):
    ITERATION_INTERVAL: int
    MAX_ALLOWED_WEIGHTS: int
    NET_UID: int
    VALIDATOR_KEY: str

    PORT: int = 9900
    WORKERS: int = 4

    WEIGHTS_FILE_NAME: str = 'weights.pkl'
    DATABASE_URL: str
    API_RATE_LIMIT: int
    REDIS_URL: str

    QUERY_TIMEOUT: int   # cross check query timeout

    LLM_API_KEY: str
    LLM_TYPE: str

    TWITTER_BEARER_TOKENS: str


    model_config = ConfigDict(
        extra='ignore',
        frozen=True  # Make settings immutable for thread safety
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls,
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            cls.fetch_github_settings,
        )

    @staticmethod
    def fetch_github_settings():
        local_config_path = 'subnet/validator/config.json'
        url = f'https://raw.githubusercontent.com/moonsht/moonshoot-subnet/main/src/{local_config_path}'
        data = {}
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            logger.debug("Fetched settings from GitHub.")
        except requests.RequestException:
            logger.error("Error fetching settings from GitHub")
            if os.path.exists(local_config_path):
                try:
                    with open(local_config_path, 'r') as f:
                        data = json.load(f)
                    logger.debug("Loaded settings from local config file")
                except Exception:
                    logger.error("Error reading local config file")
            else:
                logger.error("Local config file not found")
        return data


class SettingsManager:
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._settings_lock = threading.Lock()
            self._settings = ValidatorSettings()
            self._stop_event = threading.Event()
            self._reload_interval = 600
            self._thread = threading.Thread(target=self._background_reloader, daemon=True)
            self._thread.start()
            self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _background_reloader(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self._reload_interval)
            self.reload()
            logger.debug("Settings reloaded")

    def reload(self):
        new_settings = ValidatorSettings()
        with self._settings_lock:
            self._settings = new_settings

    def get_settings(self):
        with self._settings_lock:
            return self._settings

    def stop_reloader(self):
        self._stop_event.set()
        self._thread.join()
