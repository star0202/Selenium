import logging

from utils.gettime import get_time

RESET = "\033[0m"
CYAN = "\033[1;36m"
COLORS = {
    "DEBUG": "\033[1;37m",  # WHITE
    "INFO": "\033[1;34m",  # BLUE
    "WARNING": "\033[1;33m",  # YELLOW
    "ERROR": "\033[1;35m",  # MAGENTA
    "CRITICAL": "\033[1;31m"  # RED
}


class StreamFormatter(logging.Formatter):
    def __init__(self, formattype, datefmt, style):
        super().__init__(formattype, datefmt, style)

    def format(self, record: logging.LogRecord):
        space = 8 - len(record.levelname)
        levelname_color = COLORS[record.levelname] + record.levelname + RESET + " " * space
        record.levelname = levelname_color

        space = 22 - len(record.name)
        if space < 0:
            space = 0
        record.name = CYAN + record.name + RESET + " " * space

        return super().format(record)


def setup_logging():
    today = get_time()
    filehandler = logging.FileHandler(f"logs/{today.strftime('%Y-%m-%d-%H-%M-%S')}.log", "a", "utf-8")
    filehandler.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(StreamFormatter("%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S", "%"))
    handler.setLevel(logging.INFO)
    errorhandler = logging.FileHandler(f"errors/{today.strftime('%Y-%m-%d-%H-%M-%S')}.log", "a", "utf-8")
    errorhandler.setLevel(logging.ERROR)
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-22s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[filehandler, errorhandler, handler], level=logging.DEBUG
    )
