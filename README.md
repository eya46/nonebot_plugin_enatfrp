<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin eNatFrp
SakuraFrp管理插件

![License](https://img.shields.io/github/license/eya46/nonebot_plugin_enatfrp)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![NoneBot](https://img.shields.io/badge/nonebot-2.0.1+-blueviolet)
</div>

## 安装方式

### 依赖管理

- `pip install nonebot-plugin-enatfrp`
- `poetry add nonebot-plugin-enatfrp`
- `pdm add nonebot-plugin-enatfrp`

> 在 `bot.py` 中添加 `nonebot.load_plugin("nonebot_plugin_enatfrp")`

### nb-cli

- `nb plugin install nonebot-plugin-enatfrp`

## 使用方式

- frp帮助 `[index: int]`
- 开机 `<id: int>` `[password: str = ]`
- 隧道状态
- 流量│流量历史 `[id: int]` `[type: week|月|day|日|周|month = day]`
- 流量包│流量套餐 `<type: invalid|all|可用|不可用|全部|valid = all>`
- 我的信息│用户信息
- 公告 `<index: int = 0>`
- 授权 `<id: int> <ip: str>`
  -计算机列表

## 配置项

### 非必要配置项

- `natfrp_api`: natfrp api地址
- `natfrp_token`: natfrp api token
- `natfrp_at`: 是否at
- `natfrp_reply`: 是否回复
- `natfrp_use_start`: 是否使用nb配置的command_start
- `natfrp_use_sep`: 是否使用nb配置的command_sep

- `natfrp_cmd_help`: `frp帮助`
- `natfrp_cmd_powerOn`: `开机`
- `natfrp_cmd_tunnels`: `隧道状态`
- `natfrp_cmd_trafficHistory`: `流量` `流量历史`
- `natfrp_cmd_trafficPlans`: `流量包` `流量套餐`
- `natfrp_cmd_userInfo`: `我的信息` `用户信息`
- `natfrp_cmd_announcement`: `公告`
- `natfrp_cmd_auth`: `授权`
- `natfrp_cmd_showPCs`: `计算机列表`

## 依赖项

- [nonebot2](https://github.com/nonebot/nonebot2) >=2.0.1
- [plugin-alconna](https://github.com/nonebot/plugin-alconna) ^0.35.1