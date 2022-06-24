from aiogram import executor
from dispatcher import dp
import handlers
import logging
import sys
from logging import INFO, DEBUG

_ = handlers.__init__
is_debug_run = True if "debug_run" in sys.argv else False
log_format = "%(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    format=log_format,
    level=DEBUG if is_debug_run else INFO)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, relax=0.05)
