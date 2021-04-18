# -*- coding:utf-8 -*-
import json
import sys
from importlib import import_module
from importlib.util import find_spec

from owlmixin import OwlMixin, TOption
from owlmixin.util import load_json

from jumeaux.addons.res2res import Res2ResExecutor
from jumeaux.logger import Logger
from jumeaux.models import Res2ResAddOnPayload, Response, Request
from jumeaux.utils import when_filter

logger: Logger = Logger(__name__)
LOG_PREFIX = "[res2res/json]"


def wrap(anything: bytes, encoding: str) -> str:
    """Use for example of Transformer.function
    """
    return json.dumps({"wrap": load_json(anything.decode(encoding))}, ensure_ascii=False)


class Transformer(OwlMixin):
    module: str
    function: str = "transform"


class Config(OwlMixin):
    transformer: Transformer
    default_encoding: str = "utf8"
    when: TOption[str]


class Executor(Res2ResExecutor):
    def __init__(self, config: dict) -> None:
        self.config: Config = Config.from_dict(config or {})
        t: Transformer = self.config.transformer

        try:
            if not find_spec(t.module):
                raise ModuleNotFoundError
        except ModuleNotFoundError as e:
            logger.error(f"{LOG_PREFIX} Module {t.module} is not existed.")
            sys.exit(1)

        try:
            self.module = getattr(import_module(t.module), t.function)
        except AttributeError as e:
            logger.error(f"{LOG_PREFIX} {t.function} is not existed in {t.module} module")
            sys.exit(1)

    def exec(self, payload: Res2ResAddOnPayload) -> Res2ResAddOnPayload:
        req: Request = payload.req
        res: Response = payload.response

        if not self.config.when.map(lambda x: when_filter(x, {"req": req, "res": res})).get_or(
            True
        ):
            return payload

        json_str: str = self.module(res.body, res.encoding.get())
        new_encoding: str = res.encoding.get_or(self.config.default_encoding)

        return Res2ResAddOnPayload.from_dict(
            {
                "response": {
                    "body": json_str.encode(new_encoding, errors="replace"),
                    "type": "json",
                    "encoding": new_encoding,
                    "headers": res.headers,
                    "url": res.url,
                    "status_code": res.status_code,
                    "elapsed": res.elapsed,
                    "elapsed_sec": res.elapsed_sec,
                },
                "req": req,
                "tags": payload.tags,
            }
        )
