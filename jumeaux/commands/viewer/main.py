"""Boot Jumeaux Viewer
Usage:
  {cli} [--port <port>] [--responses-dir=<responses_dir>]
  {cli} (-h | --help)

Options:
  --port <port>                       Running port [default: 8000]
  --responses-dir <responses_dir>     Directory which has responses [default: responses]
  -h --help                           Show this screen.
"""

from owlmixin import OwlMixin
from livereload import Server
from jumeaux.logger import Logger, init_logger

logger: Logger = Logger(__name__)


class Args(OwlMixin):
    port: int
    responses_dir: str


def reload():
    logger.info_lv1(f"Reload viewer.")


def run(args: Args):
    init_logger(0)
    server = Server()
    server.watch(f"{args.responses_dir}/latest/report.json", reload)
    server.serve(
        root=f"{args.responses_dir}/latest",
        port=args.port,
        restart_delay=0,
        open_url_delay=1,
        open_url=True,
    )
