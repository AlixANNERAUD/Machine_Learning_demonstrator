from django.apps import AppConfig

import pandas
import logging
import dotenv
import os
import traceback


class LoggingFormatterClass(logging.Formatter):
    EMOJIS = {
        logging.DEBUG: "🐛",
        logging.INFO: "📝",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥",
    }

    def __init__(self):
        super().__init__("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record):
        emoji = self.EMOJIS.get(record.levelno, "")
        record.msg = f"{emoji} - {record.msg}"
        return super().format(record)


class ApplicationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "application"

    def load_environment_variables(self):
        logging.info("Loading environment variables ...")
        dotenv.load_dotenv()

        self.data_path = os.getenv("DATA_PATH", "data")

        self.audio_path = os.getenv("AUDIO_PATH", "/tmp/deez_nalyzer")

    def ready(self):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().handlers[0].setFormatter(LoggingFormatterClass())

        self.load_environment_variables()

        logging.info("Application ready ✅")
