from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from typing_extensions import Annotated
from typing import Literal

from arclet.alconna import Args
from nonebot_plugin_alconna import Alconna, Match, AlconnaMatch

from .api import API
from .tools import (
    send, bytes_to_human, timestamp_to_date, DAY_WEEK_MONTH, TRAFFIC_PLAN_TYPE, wrap_cmd, unescape_html, RawCommand,
    HELPS
)
from .config import config, Config

api = API(config.natfrp_api, config.natfrp_token)


@wrap_cmd(Alconna(config.natfrp_cmd_help, Args["index?", int]))
async def help_cmd_handle(index: Annotated[Match[int], AlconnaMatch("index")]):
    if index.available:
        await send(f"{index.result}.{HELPS[index.result]}")
    else:
        await send("\n".join(f"{i}.{h}" for i, h in enumerate(HELPS)))


@wrap_cmd(Alconna(config.natfrp_cmd_powerOn, Args["id", int]["password?", str, ""]))
async def power_on_cmd_handle(
        id_: Annotated[Match[int], AlconnaMatch("id")], password: Annotated[Match[str], AlconnaMatch("password")]
):
    await send(await api.computer_poweron(id_.result, password.result))


@wrap_cmd(Alconna(config.natfrp_cmd_tunnels))
async def tunnels_cmd_handle(cmd: Annotated[str, RawCommand()]):
    tunnels = await api.get_tunnels()
    msg = cmd + "：\n状态 ID 名称\n"
    for tunnel in tunnels:
        msg += f"{'在线🟢' if tunnel['online'] else '离线🔴'} {tunnel['id']} {tunnel['name']}\n"
    await send(msg)


@wrap_cmd(Alconna(
    config.natfrp_cmd_trafficHistory,
    Args["id?", int]["type?", Literal["day", "week", "month", "日", "周", "月"], "day"]
))
async def traffic_history_cmd_handle(
        cmd: Annotated[str, RawCommand()], id_: Annotated[Match[int], AlconnaMatch("id")],
        type_: Annotated[Match[str], AlconnaMatch("type")]
):
    msg = cmd + "：\n"
    if id_.available:
        history = await api.tunnel_traffic(id_.result)
        msg += "\n".join(f"{timestamp_to_date(x[0])} :\n    {bytes_to_human(x[1])}" for x in history.items())
    else:
        history = await api.user_trafficHistory(type_=DAY_WEEK_MONTH[type_.result])
        msg += "\n".join(f"{x[0]} :\n    {bytes_to_human(x[1])} / {bytes_to_human(x[2])}" for x in history)
    await send(msg)


@wrap_cmd(Alconna(config.natfrp_cmd_trafficPlans, Args[
    "type", Literal["valid", "invalid", "all", "可用", "不可用", "全部"], "all"
]))
async def traffic_plans_cmd_handle(
        cmd: Annotated[str, RawCommand()], type_: Annotated[Match[str], AlconnaMatch("type")]
):
    plans = await api.user_dataPlans(status=TRAFFIC_PLAN_TYPE[type_.result])
    msg = f"{cmd}({type_.result})：\n"
    msg += "\n".join(
        f"{timestamp_to_date(x['start_time'])}~{timestamp_to_date(x['end_time'])}:\n    "
        f"{bytes_to_human(x['remaining'])}/{bytes_to_human(x['total'])}({round(x['remaining'] / x['total'] * 100, 2)}%)"
        for x in plans
    )
    await send(msg)


@wrap_cmd(Alconna(config.natfrp_cmd_userInfo))
async def user_info_cmd_handle():
    u = await api.user_info()
    await send(
        f"-----账号-----\n"
        f"{u['name']}<{u['id']}>\n"
        f"{u['group']['name']}<{u['speed']}>\n"
        f"☆{timestamp_to_date(u['group']['expires'])}☆\n"
        f"-----流量-----\n"
        f"日消耗:{bytes_to_human(u['traffic'][0])}\n"
        f"总剩余:{bytes_to_human(u['traffic'][1])}\n"
        f"-----签到-----\n"
        f"总天数:{u['sign']['days']}\n"
        f"今日签到:{'是' if u['sign']['signed'] else '否'}\n"
        f"上次签到:{u['sign']['last']}\n"
        f"累计获取:{u['sign']['traffic']}GiB"
    )


@wrap_cmd(Alconna(config.natfrp_cmd_announcement, Args["index", int, 0]))
async def announcement_cmd_handle(index: Annotated[Match[int], AlconnaMatch("index")]):
    announcements = await api.system_bulletin()
    index = min(max(len(announcements) - 1, 0), index.result)
    a = announcements[index]
    await send(unescape_html(f"{a['icon']}{a['title']}{a['icon']}\n{a['time']}\n{a['content']}"))


@wrap_cmd(Alconna(config.natfrp_cmd_auth, Args["id", int]["ip", str]))
async def auth_cmd_handle(
        id_: Annotated[Match[int], AlconnaMatch("id")], ip: Annotated[Match[str], AlconnaMatch("ip")]
):
    await send("IP:" + await api.tunnel_auth(id_.result, ip.result))


@wrap_cmd(Alconna(config.natfrp_cmd_showPCs))
async def show_pcs_cmd_handle():
    pcs = await api.get_computers()
    await send("\n".join(f"{pc['id']}.{pc['name']}" + ("<加密>" if pc["type"] != 1 else "") for pc in pcs))


__plugin_meta__ = PluginMetadata(
    name="SakuraFrp",
    description="SakuraFrp管理插件，natfrp.com。",
    usage="\n".join(f"{i}.{h}" for i, h in enumerate(HELPS)),
    type="application",
    homepage="https://github.com/eya46/nonebot_plugin_enatfrp",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
