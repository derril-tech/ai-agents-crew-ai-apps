# Env config
import os

DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")
DEFAULT_BILLING_PERIOD = os.getenv("DEFAULT_BILLING_PERIOD", "monthly")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
