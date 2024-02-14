from typing import Optional, List

from nonebot import get_driver
from pydantic import BaseModel, Field, AnyUrl


class Config(BaseModel):
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


config: Config = Config(**get_driver().config.dict())

__all__ = ["Config", "config"]
