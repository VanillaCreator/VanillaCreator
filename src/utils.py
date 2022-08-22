import os, shutil, json, yaml

join_path = os.path.join


def is_list_like(obj: object) -> bool:
    return type(obj) is list or type(obj) is tuple


def sfirst(obj: object) -> object:
    if is_list_like(obj):
        obj = obj[0]
    return obj


def smap(func: object, obj: object) -> None:
    if is_list_like(obj):
        for o in obj:
            func(o)
    else:
        func(obj)


def smkdir(dir: str, clear: bool = False) -> None:
    if os.path.exists(dir):
        if clear:
            shutil.rmtree(dir)
        else:
            return
    os.makedirs(dir)


def read_yaml_file(yaml_file: str) -> dict:
    with open(yaml_file, encoding="utf-8") as f:
        return yaml.safe_load(f)


def gen_json(obj: object, pretty: bool = False) -> str:
    if pretty:
        indent = 4
        separators = (",", ": ")
    else:
        indent = None
        separators = (",", ":")
    return json.dumps(obj, ensure_ascii=False, indent=indent, separators=separators)
