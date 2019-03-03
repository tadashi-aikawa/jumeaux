# -*- coding:utf-8 -*-

import os
import shutil

from jumeaux.addons.final import FinalExecutor
from jumeaux.models import FinalAddOnPayload, FinalAddOnReference
from jumeaux.logger import Logger

logger: Logger = Logger(__name__)
LOG_PREFIX = "[final/viewer]"
VIEWER = os.path.abspath(f"{os.path.dirname(__file__)}/../../sample/viewer/index.html")


class Executor(FinalExecutor):
    def __init__(self, config: dict):
        pass

    def exec(self, payload: FinalAddOnPayload, reference: FinalAddOnReference) -> FinalAddOnPayload:
        dst_path = f"{payload.result_path}/index.html"
        shutil.copy(VIEWER, dst_path)
        logger.info_lv1(f"{LOG_PREFIX} Create {dst_path}")

        if not os.path.exists(f"{payload.result_path}/report.json"):
            logger.warning(f"{LOG_PREFIX} report.json doesn't exist in {payload.result_path}.")
            logger.warning(f"{LOG_PREFIX} Please use a `final/json` add-on to create report.json if you can't to access viewer correctlly.")
        return payload
