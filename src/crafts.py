import os, statics, utils

block_coordinates = {"in": "~ ~ ~", "on": "~ ~-1 ~", "under": "~ ~1 ~"}


def lcf(text: str) -> str:
    return text[0].lower() + text[1:]


def ucf(text: str) -> str:
    return text[0].upper() + text[1:]


def get_block_coordinates(block: dict) -> str:
    return block_coordinates[block["pos"]]


def get_item_count(item: dict) -> str:
    if "count" in item:
        count = item["count"]
    else:
        count = "1"
    count += "b"
    return count


# 应对Minecraft奇怪的嵌套json文件
def gen_item_tag_display_ph(item: dict) -> dict:
    display = {}
    if "name" in item:
        display["Name"] = "%%NAME%%"
    if "description" in item:
        display["Lore"] = "%%LORE%%"
    return display


# 快给我螺内酯啊啊啊
def gen_item_tag_display(cmd: str, item: dict) -> str:
    if "name" in item:
        cmd = cmd.replace('"%%NAME%%"', "'%s'" % (utils.gen_json(item["name"])))
    if "description" in item:
        cmd = cmd.replace('"%%LORE%%"', "'%s'" % (utils.gen_json(item["description"])))
    return cmd


def gen_item_tag(item: dict) -> dict:
    tag = {}
    if "mod_id" in item:
        tag["id"] = item["mod_id"]
    tag_display = gen_item_tag_display_ph(item)
    if tag_display:
        tag["display"] = tag_display
    return tag


def replace_item(cmd: str, item: dict) -> str:
    if not type(item) is dict:
        nbt = {"id": item, "Count": "1b"}
    else:
        nbt = {"id": item["id"], "Count": get_item_count(item)}
        nbt_tag = gen_item_tag(item)
        if nbt_tag:
            nbt["tag"] = nbt_tag
    cmd = cmd.replace("%%ITEM%%", utils.gen_json(nbt))
    cmd = gen_item_tag_display(cmd, item)
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


def get_craft_cmd_clear_self(ns: str, craft_name: str) -> str:
    cmd = statics.craft_bases["clear_self"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    return cmd


def get_craft_cmd_run_func(ns: str, craft_name: str) -> str:
    cmd = statics.craft_bases["run_func"]
    cmd = replace_xcf_names(cmd, ns, craft_name)
    cmd = cmd.replace("%%RECEIPE%%", craft_name)
    return cmd


def cmd_detect_others(material: dict) -> str:
    cmd = statics.craft_bases["detect"]["others"]
    cmd = replace_item(cmd, material)
    return cmd


def get_craft_cmd_gen_item(product: dict) -> str:
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
        fs.write(get_craft_cmd_run_func(ns, receipe["name"]))
        fs.write(get_craft_cmd_clear_self(ns, receipe["name"]))


def write_item_file(item_file: str, receipe: dict) -> None:
    with open(item_file, "w") as fs:

        def func(product: dict) -> None:
            fs.write(get_craft_cmd_gen_item(product))

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


def gen(tmp_dir: str, receipes: list | dict) -> None:
    if not type(receipes) is dict:
        project_name = os.path.basename(os.path.dirname(tmp_dir))
        receipes = {project_name: receipes}
    nss = tuple(receipes.keys())

    def func(ns: str) -> None:

        def func2(receipe: dict) -> None:
            gen_receipe(func_dir, ns, receipe)

        data_dir = utils.join_path(tmp_dir, "data", ns)
        func_dir = utils.join_path(data_dir, "functions")
        func_tags_dir = utils.join_path(data_dir, "tags", "functions")
        utils.smkdir(func_tags_dir)
        utils.smap(func2, receipes[ns])
        with open(utils.join_path(func_tags_dir, "tick.json"), "w") as fs:
            fs.write(utils.gen_json({"values": "%s:craft" % (ns)}, True))

    utils.smap(func, nss)
