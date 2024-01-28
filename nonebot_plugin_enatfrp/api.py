from typing import TYPE_CHECKING, Protocol, Any, Literal, Dict

from yarl import URL

from .tools import request

if TYPE_CHECKING:
    class _ApiCall(Protocol):
        async def __call__(self, **data: Any) -> Any:
            ...


class API:
    def __init__(self, api: str, token: str):
        self.api = URL(api)
        self.headers = {"Authorization": f"Bearer {token}"}

    async def call_api(
            self,
            path: str, method: Literal["GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], **data: Any
    ) -> Any:
        return await request(method, str(self.api / path), self.headers, **data)

    async def system_bulletin(self) -> list:
        """
        获取平台公告
        tag: 系统信息
        code: 200,500
        """
        return await self.call_api("system/bulletin", "GET")

    async def system_clients(self) -> dict:
        """
        获取客户端软件信息
        tag: 系统信息
        code: 200,500
        """
        return await self.call_api("system/clients", "GET")

    async def system_policy(self, type_: Literal["tos", "content", "privacy", "rule", "refund"]) -> dict:
        """
        获取服务条款和策略
        tag: 系统信息
        code: 200,500
        :param type_: <str>(必要) 策略类型
        """
        return await self.call_api("system/policy", "GET", type=type_)

    async def user_info(self) -> dict:
        """
        获取用户基本信息
        tag: 用户信息
        code: 200,500
        """
        return await self.call_api("user/info", "GET")

    async def user_resetToken(self) -> str:
        """
        重置用户访问密钥
        tag: 用户信息
        code: 200,500
        """
        return await self.call_api("user/reset_token", "POST")

    async def user_dataPlans(self, status: Literal["valid", "invalid", "all"] = "valid") -> list:
        """
        获取用户流量包
        tag: 用户信息
        code: 200,500
        :param status: <str>(非必要) 流量包状态
        """
        return await self.call_api("user/data_plans", "GET", status=status)

    async def user_trafficHistory(self, type_: Literal["day", "week", "month"] = "day") -> list:
        """
        获取用户流量历史
        tag: 用户信息
        code: 200,500
        :param type_: <str>(必要) 查询时间类型
        """
        return await self.call_api("user/traffic_history", "GET", type=type_)

    async def nodes(self) -> dict:
        """
        列出所有节点
        tag: 节点管理
        code: 200,500
        """
        return await self.call_api("nodes", "GET")

    async def get_tunnels(self) -> list:
        """
        列出所有隧道
        tag: 隧道管理
        code: 200,500
        """
        return await self.call_api("tunnels", "GET")

    async def post_tunnels(
            self, name: str, type_: Literal["tcp", "udp", "http", "https", "wol", "etcp", "eudp"], note: str,
            extra: str, local_ip: str, local_port: int, remote: str
    ) -> dict:
        """
        创建隧道
        tag: 隧道管理
        code: 201,500
        :param name: <str>(必要) 隧道名称
        :param type_: <str>(必要) 隧道类型
        :param note: <str>(必要) 隧道备注
        :param extra: <str>(必要) 额外参数
        :param local_ip: <str>(必要) 本地 IP
        :param local_port: <int>(必要) 本地端口
        :param remote: <str>(必要) 远程地址(节点的host)
        """
        return await self.call_api(
            "tunnels", "POST", name=name, type=type_, note=note, extra=extra, local_ip=local_ip,
            local_port=local_port, remote=remote
        )

    async def tunnel_config(self, query: str) -> str:
        """
        获取隧道配置文件
        tag: 隧道管理
        code: 200,500
        :param query: <str>(必要) 隧道 ID / 多个隧道ID 用 , 分隔 / n<节点ID>
        """
        return await self.call_api("tunnel/config", "POST", query=query)

    async def tunnel_edit(self, id_: int, note: str, local_ip: str, local_port: int, extra: str) -> dict:
        """
        编辑隧道
        tag: 隧道管理
        code: 200,500
        :param id_: <int>(必要) 隧道 ID
        :param note: <str>(必要) 隧道备注
        :param local_ip: <str>(必要) 本地 IP
        :param local_port: <int>(必要) 本地端口
        :param extra: <str>(必要) 额外参数
        """
        return await self.call_api(
            "tunnel/edit", "POST", id=id_, note=note, local_ip=local_ip, local_port=local_port, extra=extra
        )

    async def tunnel_migrate(self, id_: int, node: int) -> dict:
        """
        迁移隧道
        tag: 隧道管理
        code: 204,500
        :param id_: <int>(必要) 隧道 ID
        :param node: <int>(必要) 节点 ID
        """
        return await self.call_api("tunnel/migrate", "POST", id=id_, node=node)

    async def tunnel_delete(self, ids: str) -> dict:
        """
        删除隧道
        tag: 隧道管理
        code: 200,500
        :param ids: <str>(必要) 隧道 ID / 多个隧道ID 用 , 分隔
        """
        return await self.call_api("tunnel/delete", "POST", ids=ids)

    async def tunnel_traffic(self, id_: int) -> Dict[str, int]:
        """
        获取流量使用记录
        tag: 隧道管理
        code: 200,500
        :param id_: <int>(必要) 隧道 ID
        """
        return await self.call_api("tunnel/traffic", "GET", id=id_)

    async def tunnel_auth(self, id_: int, ip: str) -> str:
        """
        授权 IP 访问隧道
        tag: 访问认证
        code: 200,500
        :param id_: <int>(必要) 隧道 ID
        :param ip: <str>(必要) IP 地址
        """
        return await self.call_api("tunnel/auth", "POST", id=id_, ip=ip)

    async def tunnel_authQuery(self, id_: int, port: int) -> dict:
        """
        根据节点 IP 和端口查询隧道，用于访问认证授权
        tag: 访问认证
        code: 200,500
        :param id_: <int>(必要) 节点 ID
        :param port: <int>(必要) 端口
        """
        return await self.call_api("tunnel/auth_query", "GET", id=id_, port=port)

    async def get_computers(self) -> list:
        """
        获取计算机列表
        tag: 计算机管理
        code: 200,500
        """
        return await self.call_api("computers", "GET")

    async def post_computers(self, name: str, type_: Literal[1, 2], data: str, media: str) -> dict:
        """
        添加计算机
        tag: 计算机管理
        code: 201,500
        :param name: <str>(必要) 计算机名称
        :param type_: <int>(必要) 1:WOL 2:WOL (密码保护)
        :param data: <str>(必要) MAC地址
        :param media: <str>(必要) 节点ID
        """
        return await self.call_api("computers", "POST", name=name, type=type_, data=data, media=media)

    async def patch_computers(self, id_: int, name: str, type_: Literal[1, 2], data: str, media: str) -> str:
        """
        更新计算机信息
        tag: 计算机管理
        code: 204,500
        :param id_: <int>(必要) 计算机ID
        :param name: <str>(必要) 计算机名称
        :param type_: <int>(必要) 1:WOL 2:WOL (密码保护)
        :param data: <str>(必要) MAC地址
        :param media: <str>(必要) 节点ID
        """
        return await self.call_api(
            "computers", "PATCH", id=id_, name=name, type=type_, data=data, media=media
        )

    async def computer_delete(self, id_: int) -> str:
        """
        删除计算机
        tag: 计算机管理
        code: 204,500
        :param id_: <int>(必要) 计算机ID
        """
        return await self.call_api("computer/delete", "POST", id=id_)

    async def computer_poweron(self, id_: int, password: str) -> str:
        """
        执行远程开机
        tag: 计算机管理
        code: 204,500
        :param id_: <int>(必要) 计算机ID
        :param password: <str>(必要) 计算机密码
        """
        return await self.call_api("computer/poweron", "POST", id=id_, password=password)


__all__ = ["API"]
