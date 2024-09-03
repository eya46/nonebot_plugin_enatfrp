from typing import Optional

from nonebot.plugin import get_plugin_config
from pydantic import BaseModel, Field, AnyUrl


class Config(BaseModel):
    api: AnyUrl = Field(default="https://api.natfrp.com/v4", alias="natfrp_api")
    token: Optional[str] = Field(default=None, alias="natfrp_token")
    at: bool = Field(default=False, alias="natfrp_at")
    reply: bool = Field(default=False, alias="natfrp_reply")
    use_start: bool = Field(default=True, alias="natfrp_use_start")
    use_sep: bool = Field(default=False, alias="natfrp_use_sep")

    cmd_help: list[str] = Field(default=["frp帮助"], alias="natfrp_cmd_help")
    cmd_powerOn: list[str] = Field(default=["开机"], alias="natfrp_cmd_powerOn")
    cmd_tunnels: list[str] = Field(default=["隧道状态"], alias="natfrp_cmd_tunnels")
    cmd_trafficHistory: list[str] = Field(default=["流量", "流量历史"], alias="natfrp_cmd_trafficHistory")
    cmd_trafficPlans: list[str] = Field(default=["流量包", "流量套餐"], alias="natfrp_cmd_trafficPlans")
    cmd_userInfo: list[str] = Field(default=["我的信息", "用户信息"], alias="natfrp_cmd_userInfo")
    cmd_announcement: list[str] = Field(default=["公告"], alias="natfrp_cmd_announcement")
    cmd_auth: list[str] = Field(default=["授权"], alias="natfrp_cmd_auth")
    cmd_showPCs: list[str] = Field(default=["计算机列表"], alias="natfrp_cmd_showPCs")


config: Config = get_plugin_config(Config)

__all__ = ["Config", "config"]
