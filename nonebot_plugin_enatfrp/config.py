from typing import Optional, List

from nonebot import get_driver
from pydantic import BaseModel, Field, Extra, __version__, AnyUrl


class Config(BaseModel, extra=Extra.ignore):
    natfrp_api: AnyUrl = Field(default="https://api.natfrp.com/v4")
    natfrp_token: Optional[str] = Field(default=None)
    natfrp_at: bool = Field(default=False)
    natfrp_reply: bool = Field(default=False)
    natfrp_use_start: bool = Field(default=True)
    natfrp_use_sep: bool = Field(default=False)

    natfrp_cmd_help: List[str] = Field(default=["frp帮助"])
    natfrp_cmd_powerOn: List[str] = Field(default=["开机"])
    natfrp_cmd_tunnels: List[str] = Field(default=["隧道状态"])
    natfrp_cmd_trafficHistory: List[str] = Field(default=["流量", "流量历史"])
    natfrp_cmd_trafficPlans: List[str] = Field(default=["流量包", "流量套餐"])
    natfrp_cmd_userInfo: List[str] = Field(default=["我的信息", "用户信息"])
    natfrp_cmd_announcement: List[str] = Field(default=["公告"])
    natfrp_cmd_auth: List[str] = Field(default=["授权"])
    natfrp_cmd_showPCs: List[str] = Field(default=["计算机列表"])


if __version__[0] == "1":
    config: Config = Config.parse_obj(get_driver().config)  # type:ignore
elif __version__[0] == "2":
    config: Config = Config.model_validate(get_driver().config)  # type:ignore
else:
    raise Exception(f"不支持的pydantic版本:{__version__}")

__all__ = ["Config", "config"]
