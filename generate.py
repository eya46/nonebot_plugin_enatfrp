from collections import Counter
from functools import cache
from pathlib import PurePosixPath, Path
from typing import Type, Iterable, Tuple, List, Union, Optional, Any, Set
from urllib.parse import urlparse, urlunparse

import httpx
import yaml
from openapi_pydantic import parse_obj
from openapi_pydantic.v3.v3_0_3 import OpenAPI, Paths, Operation, DataType, Schema, PYDANTIC_V2, Reference

BASE_URL = "https://api.natfrp.com/docs"


def join_path(path: str, url: str = BASE_URL) -> str:
    u = urlparse(url)
    t = [*u]
    t[2] = (PurePosixPath(u.path) / path).as_posix()
    return urlunparse(t)


def save_data(url: str, data: str):
    with open(Path("./test") / Path(url).name, "w", encoding="utf8") as f:
        f.write(data)


@cache
def get_scheme(path: Union[str, Reference], url: str = BASE_URL) -> Schema:
    if isinstance(path, Reference):
        path = path.ref
    url = join_path(path, url)
    text = httpx.get(url).text
    # save_data(url, text)
    if PYDANTIC_V2:
        return Schema.model_validate(yaml.safe_load(text))  # type:ignore
    return Schema.parse_obj(yaml.safe_load(text))  # type:ignore


@cache
def get_api() -> OpenAPI:
    data = yaml.safe_load(httpx.get(join_path("openapi.yaml")).text)
    # with open("openapi.yaml", encoding="utf8") as f:
    #     data = yaml.safe_load(f.read())
    api = parse_obj(data)
    assert api.openapi == "3.0.3"
    return api


def list2str(data: List[Any], seq: str = ",") -> str:
    return seq.join(map(str, data))


def type2pyType(type_: Union[DataType, List[DataType]]) -> List[str]:
    if isinstance(type_, DataType):
        type_ = [type_]
    return [
        {
            DataType.STRING: "str",
            DataType.NUMBER: "float",
            DataType.INTEGER: "int",
            DataType.BOOLEAN: "bool",
            DataType.ARRAY: "list",
            DataType.OBJECT: "Any"
        }.get(i) for i in type_
    ]


def operation2description(operation: Operation) -> str:
    """
    :return:
    """
    params = "\n" + "\n".join(
        f":param {i.name + '_' if getattr(__builtins__, i.name, None) else i.name}: "
        f"<{list2str(type2pyType(i.param_schema.type)) if i.param_schema.type else None}>"
        f"({'必要' if i.required else '非必要'}) "
        f"{i.description}" for i in operation.parameters
    ) if operation.parameters else ""
    return (
        f"{operation.summary}\n"
        f"tag: {','.join(operation.tags)}\n"
        f"status_code: {','.join(operation.responses.keys())}"
        f"{params}"
    )


def yield_api(paths: Paths) -> Iterable[Tuple[str, str, Optional[Operation]]]:
    """
    :return: path,method,Operation
    """
    for path, item in paths.items():
        yield from [
            (path, i, _) for i in ["get", "put", "post", "delete", "options", "head", "patch", "trace"]
            if (_ := getattr(item, i, None))
        ]


@cache
def get_path_count(if_print: bool = False) -> Counter:
    d = Counter()
    for ppp, _, _ in yield_api(get_api().paths):
        d[ppp] += 1
    if if_print:
        for i in d:
            print(f"{i} -> {d[i]}")
    return d


def path2name(path: str) -> str:
    # /user/set_value/my_name -> user_setValue_myName
    return (
        "_".join(
            (
                part
                if len(_ := part.split("_")) == 1 else
                _[0] + "".join(sub.title() for sub in _[1:]) for part in parts
            ) if (parts := path[1:].split("/")) and "_" in path else parts
        )
    )


# 获取函数名
def get_defName(path: str, method: str, strict: bool = False):
    return f"{method}_{path2name(path)}" if get_path_count()[path] > 1 or strict else path2name(path)


def parameter2annotated(
        parameter: Optional[Union[Reference, Schema]], url: str = BASE_URL
) -> Optional[Set[Tuple[str, str, Tuple]]]:
    if parameter is None:
        return None
    if isinstance(parameter, Reference):
        url = join_path(parameter.ref, url)
        scheme = get_scheme(parameter)
        schemes = scheme.oneOf or scheme.anyOf or scheme.allOf or scheme
        if isinstance(schemes, Schema):
            schemes = [schemes]
        res = []
        for i in schemes:
            if isinstance(i, Reference):
                res.append(parameter2annotated(i, url))
            else:
                if i.type == DataType.OBJECT:
                    for j in i.properties:
                        pass

                else:
                    res.append((i.title, type2pyType(i.type)[0],))


# 获取请求参数
def get_defParameters(method: str, operation: Operation):
    if method.lower() == "get":
        if operation.parameters is None:
            return None
        return {
            get_scheme(i) if isinstance(i, Reference) else i.name: i.param_schema.type
            for i in operation.parameters
        }
    else:
        if operation.requestBody is None:
            return None


# 获取返回值

def urlContent2py(content: dict) -> Type:
    return {
        "application/json": str
    }[content]


def main():
    api = get_api()
    for path, method, op in yield_api(api.paths):
        # print(f"{path}[{method}] -> {get_defName(path, method)}")
        print(f"""async def {get_defName(path, method)}(self):
\"\"\"
{operation2description(op)}
method: {method.upper()}
\"\"\"""")


if __name__ == "__main__":
    get_path_count(if_print=False)
    main()
