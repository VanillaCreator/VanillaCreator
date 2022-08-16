import statics, utils


def lcf(str):
    return str[0].lower() + str[1:]


def ucf(str):
    return str[0].upper() + str[1:]


def get_block_pos(block):
    if block["pos"] == "in":
        pos = "~ ~ ~"
    elif block["pos"] == "on":
        pos = "~ ~-1 ~"
    return pos


def get_count(item):
    if type(item) is dict and "count" in item:
        count = item["count"]
    else:
        count = "1"
    return count


def get_id(item):
    if type(item) is dict:
        id = item["id"]
    else:
        id = item
    return id


def replace_item(cmd, item):
    cmd = cmd.replace("%%ID%%", get_id(item))
    cmd = cmd.replace("%%COUNT%%", get_count(item))
    return cmd


def replace_name_xcf(cmd, project_name, craft_name):
    cmd = cmd.replace("%%PROJECT_NAME_LCF%%", lcf(project_name))
    cmd = cmd.replace("%%CRAFT_NAME_UCF%%", ucf(craft_name))
    return cmd


def get_craft_cmd(part,
                  craft_name=None,
                  material=None,
                  block=None,
                  product=None,
                  project_name=None):
    part_splited = part.split(".")
    cmd = statics.craft_bases[part_splited[0]]
    if len(part_splited) > 1:
        cmd = cmd[part_splited[1]]
    if part in ("detect.main", "clear_others"):
        cmd = replace_name_xcf( cmd,project_name,craft_name)
        cmd = replace_item(cmd, material)
    elif part in ("detect.tag", "clear_self"):
        cmd = replace_name_xcf(cmd,project_name,craft_name)
    elif part == "detect.others":
        cmd = replace_item(cmd, material)
    elif part == "detect.block":
        cmd = cmd.replace("%%BLOCK_POS%%", get_block_pos(block))
        cmd = cmd.replace("%%BLOCK_ID%%", block["id"])
    elif part == "run_func":
        cmd = replace_name_xcf(cmd,project_name,craft_name)
        cmd = cmd.replace("%%CRAFT_NAME%%", craft_name)
    elif part == "gen_item":
        cmd = replace_item(cmd, product)
        cmd = cmd.replace("%%MOD_ID%%", product["mod_id"])
        cmd = cmd.replace("%%NAME%%", utils.gen_json(product["name"]))
        cmd = cmd.replace("%%LORE%%", utils.gen_json(product["description"]))
    return cmd


def gen(project_name, receipes, func_dir):
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
            fs_craft.write(get_craft_cmd("detect.main", craft_name, material,project_name=project_name))
            if "block" in receipe:
                fs_craft.write(
                    get_craft_cmd("detect.block", block=receipe["block"]))
            if utils.is_list_like(material_or_s):
                for per_material in material_or_s[1:]:
                    fs_craft.write(
                        get_craft_cmd("detect.others", material=per_material))
            fs_craft.write(get_craft_cmd("detect.tag", craft_name,project_name=project_name))
            if utils.is_list_like(material_or_s):
                for per_material in material_or_s[1:]:
                    fs_craft.write(
                        get_craft_cmd("clear_others", craft_name,
                                      per_material,project_name=project_name))
            fs_craft.write(get_craft_cmd("run_func", craft_name,project_name=project_name))
            fs_craft.write(get_craft_cmd("clear_self", craft_name,project_name=project_name))
        with open(item_file,"w") as fs_item:

            def func(product):
                fs_item.write(get_craft_cmd("gen_item", product=product))

            utils.smap(func, receipe["product"])
