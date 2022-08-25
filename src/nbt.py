import utils


# minecraft你要用json就全用呀
# 这种奇怪的nbt格式什么鬼
# 有时还套整个json文件
# 给我螺内酯啊啊啊
def gen(obj: object) -> str:
    nbt = ""
    obj_type = type(obj)
    if obj_type is str:
        if (not (obj[0] == "'" and obj[-1] == "'")) and ("," in obj or ":" in obj):
            obj = "\"%s\"" % (obj)
        nbt += obj
    elif obj_type is int:
        nbt += str(obj)
    elif utils.is_list_like(obj):
        nbt += "["
        for obj2 in obj:
            nbt += gen(obj2)
            nbt += ","
        nbt = nbt[:-1] + "]"
    elif obj_type is dict:
        keys = obj.keys()
        nbt += "{"
        for key in keys:
            nbt += "%s:%s" % (key, gen(obj[key]))
            nbt += ","
        nbt = nbt[:-1] + "}"
    return nbt
