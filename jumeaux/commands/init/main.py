"""Initialize a project template for Jumeaux
Usage:
  {cli} (-h | --help)
  {cli} [<name>]

Options:
  <name>                              Initialize template name
  -h --help                           Show this screen.
"""

import os
import shutil

from owlmixin import OwlMixin
from owlmixin import TOption

from jumeaux.logger import Logger, init_logger

logger: Logger = Logger(__name__)
SAMPLE_DIR = os.path.abspath(f"{os.path.dirname(__file__)}/../../sample")


class Args(OwlMixin):
    name: TOption[str]


def run(args: Args):
    init_logger(0)

    # TODO: refactoring
    if args.name.get() == "addon":
        addon_dir = f"{SAMPLE_DIR}/addon"
        for f in os.listdir(addon_dir):
            if os.path.isdir(f"{addon_dir}/{f}"):
                shutil.copytree(f"{addon_dir}/{f}", f)
            else:
                shutil.copy(f"{addon_dir}/{f}", f)
            logger.info_lv1(f"✨ [Create] {f}")
        return

    sample_dir = f"{SAMPLE_DIR}/template"
    target_dir = f"{sample_dir}/{args.name.get()}"

    if os.path.exists(target_dir):
        for f in ["config.yml", "requests"]:
            shutil.copy(f"{target_dir}/{f}", ".")
            logger.info_lv1(f"✨ [Create] {f}")
        shutil.copytree(f"{target_dir}/api", "api")
        logger.info_lv1(f"✨ [Create] templates with a api directory")
        return

    if not os.path.exists(target_dir):
        exit(
            f"""
Please specify a valid name.

✨ [Valid names] ✨
{os.linesep.join(os.listdir(sample_dir))}
        """.strip()
        )
