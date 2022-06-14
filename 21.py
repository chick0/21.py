from logging import getLogger
from logging import StreamHandler
from logging import Formatter
from logging import INFO
from logging import WARNING
from waitress import serve
from app import create_app

logger = getLogger()


def init_logger():
    logger.setLevel(INFO)
    handler = StreamHandler()
    handler.setFormatter(fmt=Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(hdlr=handler)
    getLogger('apscheduler.executors.default').setLevel(WARNING)


def main():
    host, port = "127.0.0.1", 21212
    serve(app=create_app(), host=host, port=port, _quiet=False)


if __name__ == "__main__":
    init_logger()
    main()
