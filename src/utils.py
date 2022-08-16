import os, shutil, json, yaml

join_path = os.path.join


def is_list_like(obj):
    return type(obj) is list or type(obj) is tuple


def sfirst(obj):
    if is_list_like(obj):
        obj = obj[0]
    return obj


def smap(func, obj):
    if is_list_like(obj):
        for o in obj:
            func(o)
    else:
        func(obj)


def smkdir(dir, clear=False):
    if os.path.exists(dir):
        if clear:
            shutil.rmtree(dir)
        else:
            return
    os.makedirs(dir)


def read_yaml_file(yaml_file):
    with open(yaml_file, encoding="utf-8") as f:
        return yaml.safe_load(f)


def gen_json(obj, pretty=False):
    if pretty:
        indent = 4
    else:
        indent = None
    return json.dumps(obj, ensure_ascii=False, indent=indent)