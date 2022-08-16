import statics, utils

coordinates = {"in": "~ ~ ~", "on": "~ ~-1 ~", "under": "~ ~1 ~"}


def lcf(str):
    return str[0].lower() + str[1:]


def ucf(str):
    return str[0].upper() + str[1:]


def get_block_coordinates(block):
    return coordinates[block["pos"]]


def get_item_count(item):
    if type(item) is dict and "count" in item:
        count = item["count"]
    else:
        count = "1"
    return count


def get_item_id(item):
    if type(item) is dict:
        id = item["id"]
    else:
        id = item
    return id


def replace_item(cmd, item):
    cmd = cmd.replace("%%ID%%", get_item_id(item))
    cmd = cmd.replace("%%COUNT%%", get_item_count(item))
    return cmd


def replace_xcf_names(cmd, project_name, craft_name):
    cmd = cmd.replace("%%PROJECT_NAME_LCF%%", lcf(project_name))
    cmd = cmd.replace("%%CRAFT_NAME_UCF%%", ucf(craft_name))
    return cmd


def cmd_detect_main(project_name, craft_name, material):
    cmd = statics.craft_bases["detect"]["main"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_clear_others(project_name, craft_name, material):
    cmd = statics.craft_bases["clear_others"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = replace_item(cmd, material)
    return cmd


def cmd_detect_tag(project_name, craft_name):
    cmd = statics.craft_bases["detect"]["tag"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    return cmd


def get_craft_cmd_clear_self(project_name, craft_name):
    cmd = statics.craft_bases["clear_self"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    return cmd


def get_craft_cmd_run_func(project_name, craft_name):
    cmd = statics.craft_bases["run_func"]
    cmd = replace_xcf_names(cmd, project_name, craft_name)
    cmd = cmd.replace("%%CRAFT_NAME%%", craft_name)
    return cmd


def cmd_detect_others(material):
    cmd = statics.craft_bases["detect"]["others"]
    cmd = replace_item(cmd, material)
    return cmd


def get_craft_cmd_gen_item(product):
    cmd = statics.craft_bases["gen_item"]
    cmd = replace_item(cmd, product)
    cmd = cmd.replace("%%MOD_ID%%", product["mod_id"])
    cmd = cmd.replace("%%NAME%%", utils.gen_json(product["name"]))
    cmd = cmd.replace("%%LORE%%", utils.gen_json(product["description"]))
    return cmd


def cmd_detect_block(block):
    cmd = statics.craft_bases["detect"]["block"]
    cmd = cmd.replace("%%BLOCK_POS%%", get_block_coordinates(block))
    cmd = cmd.replace("%%BLOCK_ID%%", block["id"])
    return cmd


def gen(project_name, func_dir, receipes):
    func_ext = ".mcfunction"
    crafts_dir = utils.join_path(func_dir, "crafts")
    items_dir = utils.join_path(func_dir, "items")
    utils.smap(utils.smkdir, (crafts_dir, items_dir))
    for receipe in receipes:
        craft_name = receipe["name"]
        craft_file = utils.join_path(crafts_dir, craft_name + func_ext)
        item_file = utils.join_path(items_dir, craft_name + func_ext)
        with open(craft_file, "w") as fs_craft:
            material_or_s = receipe["material"]
            material = utils.sfirst(material_or_s)
            fs_craft.write(cmd_detect_main(project_name, craft_name, material))
            if "block" in receipe:
                fs_craft.write(cmd_detect_block(receipe["block"]))
            if utils.is_list_like(material_or_s):
                for per_material in material_or_s[1:]:
                    fs_craft.write(cmd_detect_others(per_material))
            fs_craft.write(cmd_detect_tag(project_name, craft_name))
            if utils.is_list_like(material_or_s):
                for per_material in material_or_s[1:]:
                    fs_craft.write(cmd_clear_others(project_name, craft_name, per_material))
            fs_craft.write(get_craft_cmd_run_func(project_name, craft_name))
            fs_craft.write(get_craft_cmd_clear_self(project_name, craft_name))
        with open(item_file, "w") as fs_item:

            def func(product):
                fs_item.write(get_craft_cmd_gen_item(product))

            utils.smap(func, receipe["product"])
