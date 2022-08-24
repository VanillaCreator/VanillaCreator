import os, statics, ui, utils

coords = {"in": "~ ~ ~", "on": "~ ~-1 ~", "under": "~ ~1 ~"}


class TypeException(Exception):

    def __init__(self, trans_key) -> None:
        super().__init__(trans_key)
        self.trans_key = trans_key


def lcf(text: str) -> str:
    return text[0].lower() + text[1:]


def ucf(text: str) -> str:
    return text[0].upper() + text[1:]


def get_block_coordinates(block: dict) -> str:
    return coords[block["pos"]]


def get_item_id(item: dict | str) -> str:
    if type(item) is dict:
        id = item["id"]
    else:
        id = item
    return id


def get_item_count(item: dict) -> str:
    if type(item) is dict and "count" in item:
        count = item["count"]
    else:
        count = "1"
    count += "b"
    return count


# Minecraft你要用json就全用json呀
def gen_item_tag_display(item: dict) -> str:
    display = ""
    if "name" in item:
        if not (type(item["name"]) is dict or type(item["name"]) is str):
            raise TypeException("multiline_name")
        display += "Name:'%s'" % (utils.gen_json(item["name"]))
    if display:
        display += ","
    if "description" in item:
        lore = ""
        lores = utils.smap(utils.gen_json, item["description"])
        for l in lores:
            lore += "'%s'," % (l)
        lore = lore[:-1]
        display += "Lore:[%s]" % (lore)
    return display


# 这种半json的nbt夹杂着json文件是什么鬼
def gen_item_tag(item: dict) -> str:
    tag = ""
    if "mod_id" in item:
        tag += "id:\"%s\"" % (item["mod_id"])
    tag_display = gen_item_tag_display(item)
    if tag_display:
        if tag:
            tag += ","
        tag += "display:{%s}" % (tag_display)
    return tag


# 快给我螺内酯啊啊啊
def replace_item(cmd: str, item: dict) -> str:
    nbt = "{id:\"%s\",Count:%s}" % (get_item_id(item), get_item_count(item))
    if type(item) is dict:
        nbt_tag = gen_item_tag(item)
        if nbt_tag:
            nbt = nbt.replace("}", ",tag:{%s}}" % (nbt_tag))
    cmd = cmd.replace("%%ITEM%%", nbt)
    return cmd


def replace_xcf_names(cmd: str, ns: str, craft_name: str) -> str:
    cmd = cmd.replace("%%NS_LCF%%", lcf(ns))
    cmd = cmd.replace("%%RECEIPE_LCF%%", ucf(craft_name))
    return cmd


def cmd_detect_main(ns: str, craft_name: str, material: dict) -> str:
    cmd = statics.craft_bases["detect"]["main"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_clear_others(ns: str, craft_name: str, material: dict) -> str:
    cmd = statics.craft_bases["clear_others"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_detect_tag(ns: str, craft_name: str) -> str:
    cmd = statics.craft_bases["detect"]["tag"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    return cmd


def cmd_clear_self(ns: str, craft_name: str) -> str:
    cmd = statics.craft_bases["clear_self"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    return cmd


def cmd_run_func(ns: str, craft_name: str) -> str:
    cmd = statics.craft_bases["run_func"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    cmd = cmd.replace("%%RECEIPE%%", craft_name)
    return cmd


def cmd_detect_others(material: dict) -> str:
    cmd = statics.craft_bases["detect"]["others"]
    cmd = replace_item(cmd, material)
    return cmd


def cmd_gen_item(product: dict) -> str:
    cmd = statics.craft_bases["gen_item"]
    cmd = replace_item(cmd, product)
    return cmd


def cmd_detect_block(block: dict) -> str:
    cmd = statics.craft_bases["detect"]["block"]
    cmd = cmd.replace("%%POS%%", get_block_coordinates(block))
    cmd = cmd.replace("%%ID%%", block["id"])
    return cmd


def write_craft_file(ns: str, craft_file: str, receipe: dict) -> None:
    with open(craft_file, "w") as fs:
        material_or_s = receipe["material"]
        first_material = utils.sfirst(material_or_s)
        fs.write(cmd_detect_main(ns, receipe["name"], first_material))
        if "block" in receipe:

            def func(block: dict) -> None:
                fs.write(cmd_detect_block(block))

            utils.smap(func, receipe["block"])
        if utils.is_list_like(material_or_s):
            for material in material_or_s[1:]:
                fs.write(cmd_detect_others(material))
        fs.write(cmd_detect_tag(ns, receipe["name"]))
        if utils.is_list_like(material_or_s):
            for material in material_or_s[1:]:
                fs.write(cmd_clear_others(ns, receipe["name"], material))
        fs.write(cmd_run_func(ns, receipe["name"]))
        fs.write(cmd_clear_self(ns, receipe["name"]))


def write_item_file(item_file: str, receipe: dict) -> None:
    with open(item_file, "w") as fs:

        def func(product: dict) -> None:
            fs.write(cmd_gen_item(product))

        utils.smap(func, receipe["product"])


def gen_receipe(func_dir: str, ns: str, receipe: dict) -> None:
    func_ext = ".mcfunction"
    crafts_dir = utils.join_path(func_dir, "crafts")
    items_dir = utils.join_path(func_dir, "items")
    utils.smap(utils.smkdir, (crafts_dir, items_dir))
    craft_file = utils.join_path(crafts_dir, receipe["name"] + func_ext)
    item_file = utils.join_path(items_dir, receipe["name"] + func_ext)
    write_craft_file(ns, craft_file, receipe)
    write_item_file(item_file, receipe)
    with open(utils.join_path(func_dir, "craft" + func_ext), "a") as fs:
        fs.write("function %s:crafts/%s" % (ns, receipe["name"]))


def gen_per_ns(tmp_dir: str, receipes: list | dict, ns: str) -> None:

    def func(receipe: dict) -> None:
        gen_receipe(func_dir, ns, receipe)

    data_dir = utils.join_path(tmp_dir, "data", ns)
    func_dir = utils.join_path(data_dir, "functions")
    func_tags_dir = utils.join_path(data_dir, "tags", "functions")
    utils.smkdir(func_tags_dir)
    utils.smap(func, receipes[ns])
    with open(utils.join_path(func_tags_dir, "tick.json"), "w") as fs:
        fs.write(utils.gen_json({"values": "%s:craft" % (ns)}, True))


def gen(tmp_dir: str, receipes: list | dict) -> None:

    def func(ns: str) -> None:
        gen_per_ns(tmp_dir, receipes, ns)

    try:
        if not type(receipes) is dict:
            project_name = os.path.basename(os.path.dirname(tmp_dir))
            receipes = {project_name: receipes}
        nss = tuple(receipes.keys())
        utils.smap(func, nss)
    except TypeException as e:
        ui.say(e.trans_key)
        return -1