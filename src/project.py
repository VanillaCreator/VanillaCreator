import crafts, os, shutil, utils


def gen_meta(config, tmp_dir):
    target = config["target"]
    if target in ("1.19", "1.91.1") or target.replace(" ", "") == "1.19-1.91.1":
        config["pack_format"] = 10
        config.pop("target")
    with open(utils.join_path(tmp_dir, "pack.mcmeta"), "w", encoding="utf-8") as fs:
        fs.write(utils.gen_json({"pack": config}, True))


def pack(tmp_dir, project_dir, project_name, config):
    shutil.make_archive("%s %s" % (utils.join_path(project_dir, project_name), config["version"]), "zip", tmp_dir)
    shutil.rmtree(tmp_dir)


def build(project_dir):
    project_name = os.path.basename(project_dir)
    config = utils.read_yaml_file(utils.join_path(project_dir, "config.yml"))
    receipes = utils.read_yaml_file(utils.join_path(project_dir, "crafts.yml"))
    tmp_dir = utils.join_path(project_dir, "tmp")
    func_dir = utils.join_path(tmp_dir, "data", project_name, "functions")
    utils.smkdir(tmp_dir, True)
    utils.smkdir(func_dir)
    gen_meta(config, tmp_dir)
    crafts.gen(project_name, func_dir, receipes)
    pack(tmp_dir, project_dir, project_name, config)
