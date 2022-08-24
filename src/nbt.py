# minecraft你要用json就全用呀
# 这种奇怪的nbt格式什么鬼
# 有时还套整个json文件
# 给我螺内酯啊啊啊
def gen(obj: object) -> str:
    nbt = ""
    tobj = type(obj)
    if tobj is str:
        if "," in obj or ":" in obj:
            obj = "\"" + obj + "\""
        nbt += obj
    elif tobj is int:
        nbt += str(obj) + "b"
    elif tobj is list:
        nbt += "["
        for obj2 in obj:
            nbt += gen(obj2)
            nbt += ","
        nbt = nbt[:-1] + "]"
    elif tobj is dict:
        keys = obj.keys()
        nbt += "{"
        for key in keys:
            obj2 = obj[key]
            nbt += key + ":"
            nbt += gen(obj2)
            nbt += ","
        nbt = nbt[:-1] + "}"
    return nbt


test = gen({"a": "b:b", "c": 1, "d": {"e": 2, "f": {"g": "h,i", "j": "k", "l": ["a", "b", 3, {"aaa": "bbb"}]}}})
print(test)