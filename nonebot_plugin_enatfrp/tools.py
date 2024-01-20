import time
from functools import wraps
from html import unescape
from json import loads
from typing import Union, Any, Callable, Optional, List

from arclet.alconna import Alconna
from nonebot import get_driver
from nonebot.internal.driver import HTTPClientMixin, Request
from nonebot.internal.matcher import current_matcher
from nonebot.internal.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.typing import T_Handler, T_State
from nonebot_plugin_alconna import UniMessage, on_alconna, ALCONNA_RESULT
from nonebot_plugin_alconna.uniseg import Receipt

from .config import config
from .exception import eNatFrpAPIException

if isinstance(driver := get_driver(), HTTPClientMixin):  # type:ignore
    driver: HTTPClientMixin


    async def request(method: str, url: str, headers, **data) -> Any:

        resp = await driver.request(Request(
            method, url,
            headers=headers,
            **({"params": data} if method == "GET" else {"json": data})
        ))

        res = loads(resp.content)
        if resp.status_code == 500:
            raise eNatFrpAPIException(res.get("code", -1), res.get("msg", str(resp.content)))
        return res
else:
    from httpx import AsyncClient


    async def request(method: str, url: str, headers, **data) -> Any:
        async with AsyncClient() as client:
            resp = await client.request(
                method, url, headers=headers,
                **({"params": data} if method == "GET" else {"json": data})
            )
            res = loads(resp.content)
            if resp.status_code == 500:
                raise eNatFrpAPIException(res.get("code", -1), res.get("msg", str(resp.content)))
            return res

# 日_周_月
DAY_WEEK_MONTH = {
    "日": "day",
    "周": "week",
    "月": "month",
    "day": "day",
    "week": "week",
    "month": "month"
}

TRAFFIC_PLAN_TYPE = {
    "可用": "valid",
    "不可用": "invalid",
    "全部": "all",
    "valid": "valid",
    "invalid": "invalid",
    "all": "all"
}

HELPS: List[str] = []


async def send(msg: Union[Any, UniMessage]) -> Receipt:
    if not isinstance(msg, UniMessage):
        msg = UniMessage(msg)
    return await msg.send(at_sender=config.natfrp_at, reply_to=config.natfrp_reply)


def bytes_to_human(data: int) -> str:
    if data < 1024:
        return f"{data}B"
    elif data < 1024 * 1024:
        return f"{round(data / 1024, 1)}KiB"
    elif data < 1024 * 1024 * 1024:
        return f"{round(data / 1024 / 1024, 1)}MiB"
    elif data < 1024 * 1024 * 1024 * 1024:
        return f"{round(data / 1024 / 1024 / 1024, 1)}GiB"
    else:
        return f"{round(data / 1024 / 1024 / 1024 / 1024, 1)}TiB"


# 时间戳转日期
def timestamp_to_date(timestamp: Any) -> str:
    if not isinstance(timestamp, int):
        timestamp = int(timestamp)
    return time.strftime("%Y/%m/%d %Hh", time.localtime(timestamp))


def wrap_cmd(acl: Alconna) -> Callable:
    @wraps(acl)
    def wrapper(func: T_Handler) -> T_Handler:
        @wraps(func)
        async def _catch(*args, **kwargs):
            try:
                await func(*args, **kwargs)
            except eNatFrpAPIException as e:
                await send(
                    f"命令 {_raw_command()} 失败<{e.code}> ->\n"
                    f"{e.message}"
                )

        HELPS.append(acl.get_help().replace("\nUnknown", "").strip())
        on_alconna(
            acl, permission=SUPERUSER, use_cmd_sep=config.natfrp_use_sep, use_cmd_start=config.natfrp_use_start
        ).handle()(_catch)
        return func

    return wrapper


def unescape_html(text: str) -> str:
    return unescape(text)


def _raw_command(state: Optional[T_State] = None) -> str:
    return (state if state else current_matcher.get().state)[ALCONNA_RESULT].result.header_match.result


def RawCommand() -> str:
    return Depends(_raw_command)
