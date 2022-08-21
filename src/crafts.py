import os, statics, utils

block_coordinates = {"in": "~ ~ ~", "on": "~ ~-1 ~", "under": "~ ~1 ~"}


def lcf(text: str) -> str:
    return text[0].lower() + text[1:]


def ucf(text: str) -> str:
    return text[0].upper() + text[1:]


def get_block_coordinates(block: dict) -> str:
    return block_coordinates[block["pos"]]


def get_item_count(item: dict) -> str:
    if type(item) is dict and "count" in item:
        count = item["count"]
    else:
        count = "1"
    return count


def get_item_id(item: str | dict) -> str:
    if type(item) is dict:
        id = item["id"]
    else:
        id = item
    return id


def replace_item(cmd: str, item: dict) -> str:
    cmd = cmd.replace("%%ID%%", get_item_id(item))
    cmd = cmd.replace("%%COUNT%%", get_item_count(item))
    if "mod_id" in item:
        cmd = cmd.replace("%%MOD_ID%%", item["mod_id"])
    if "name" in item:
        cmd = cmd.replace("%%NAME%%", utils.gen_json(item["name"]))
    if "description" in item:
        cmd = cmd.replace("%%LORE%%", utils.gen_json(item["description"]))
    return cmd


def replace_xcf_names(cmd: str, project_name: str, craft_name: str) -> str:
    cmd = cmd.replace("%%PROJECT_NAME_LCF%%", lcf(project_name))
    cmd = cmd.replace("%%CRAFT_NAME_UCF%%", ucf(craft_name))
    return cmd


def cmd_detect_main(project_name: str, craft_name: str, material: dict) -> str:
    cmd = statics.craft_bases["detect"]["main"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_clear_others(project_name: str, craft_name: str, material: dict) -> str:
    cmd = statics.craft_bases["clear_others"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_detect_tag(project_name: str, craft_name: str) -> str:
    cmd = statics.craft_bases["detect"]["tag"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    return cmd


def get_craft_cmd_clear_self(project_name: str, craft_name: str) -> str:
    cmd = statics.craft_bases["clear_self"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    return cmd


def get_craft_cmd_run_func(project_name: str, craft_name: str) -> str:
    cmd = statics.craft_bases["run_func"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = cmd.replace("%%CRAFT_NAME%%", craft_name)
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
    cmd = cmd.replace("%%BLOCK_POS%%", get_block_coordinates(block))
    cmd = cmd.replace("%%BLOCK_ID%%", block["id"])
    return cmd


def write_craft_file(project_name: str, craft_file: str, receipe: dict) -> None:
    with open(craft_file, "w") as fs:
        material_or_s = receipe["material"]
        first_material = utils.sfirst(material_or_s)
        fs.write(cmd_detect_main(project_name, receipe["name"], first_material))
        if "block" in receipe:

            def func(block: dict) -> None:
                fs.write(cmd_detect_block(block))

            utils.smap(func, receipe["block"])
        if utils.is_list_like(material_or_s):
            for material in material_or_s[1:]:
                fs.write(cmd_detect_others(material))
        fs.write(cmd_detect_tag(project_name, receipe["name"]))
        if utils.is_list_like(material_or_s):
            for material in material_or_s[1:]:
                fs.write(cmd_clear_others(project_name, receipe["name"], material))
        fs.write(get_craft_cmd_run_func(project_name, receipe["name"]))
        fs.write(get_craft_cmd_clear_self(project_name, receipe["name"]))


def write_item_file(item_file: str, receipe: dict) -> None:
    with open(item_file, "w") as fs:

        def func(product: dict) -> None:
            fs.write(get_craft_cmd_gen_item(product))

        utils.smap(func, receipe["product"])


def gen(tmp_dir: str, receipes: list) -> None:
    project_name = os.path.basename(os.path.dirname(tmp_dir))
    data_dir = utils.join_path(tmp_dir, "data", project_name)
    func_dir = utils.join_path(data_dir, "functions")
    func_tags_dir = utils.join_path(data_dir, "tags", "functions")
    func_ext = ".mcfunction"
    craft_func_file = utils.join_path(func_dir, "craft" + func_ext)
    crafts_dir = utils.join_path(func_dir, "crafts")
    items_dir = utils.join_path(func_dir, "items")
    utils.smap(utils.smkdir, (func_tags_dir, crafts_dir, items_dir))
    for receipe in receipes:
        craft_file = utils.join_path(crafts_dir, receipe["name"] + func_ext)
        item_file = utils.join_path(items_dir, receipe["name"] + func_ext)
        write_craft_file(project_name, craft_file, receipe)
        write_item_file(item_file, receipe)
        with open(craft_func_file, "a") as fs:
            fs.write("function %s:crafts/%s" % (project_name, receipe["name"]))
    with open(utils.join_path(func_tags_dir, "tick.json"), "w") as fs:
        fs.write(utils.gen_json({"values": "%s:crafts" % (project_name)}, True))
