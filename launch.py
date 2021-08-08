from logging import getLogger
from logging import FileHandler
from argparse import ArgumentParser

from waitress import serve
from paste.translogger import TransLogger

from app import create_app


if __name__ == "__main__":
    parser = ArgumentParser(description="서버 런처")
    parser.add_argument("--set-port", metavar="PORT",
                        help="서버를 작동 시킬 포트 번호를 지정합니다.",
                        action="store", type=int, default=21212)

    args = parser.parse_args()

    logger = getLogger("wsgi")
    logger.addHandler(FileHandler("wsgi.log"))
    serve(app=TransLogger(create_app(), setup_console_handler=False), port=args.set_port, _quiet=True)
