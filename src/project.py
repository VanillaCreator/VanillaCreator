import crafts, os, shutil, utils


def gen_meta(proj_attr, tmp_dir):
    target = proj_attr["target"]
    if target in ("1.19", "1.91.1") or target.replace(" ", "") == "1.19-1.91.1":
        proj_attr["pack_format"] = 10
        proj_attr.pop("target")
    with open(utils.join_path(tmp_dir, "pack.mcmeta"), "w", encoding="utf-8") as fs:
        fs.write(utils.gen_json({"pack": proj_attr}, True))


def pack(tmp_dir, proj_dir, proj_name, proj_attr):
    shutil.make_archive("%s %s" % (utils.join_path(proj_dir, proj_name), proj_attr["version"]), "zip", tmp_dir)
    shutil.rmtree(tmp_dir)


def build(proj_dir):
    proj_name = os.path.basename(proj_dir)
    proj_attr = utils.read_yaml_file(utils.join_path(proj_dir, "project.yml"))
    receipes = utils.read_yaml_file(utils.join_path(proj_dir, "receipes.yml"))
    tmp_dir = utils.join_path(proj_dir, "tmp")
    out_dir = utils.join_path(proj_dir, "out")
    func_dir = utils.join_path(tmp_dir, "data", proj_name, "functions")
    utils.smkdir(tmp_dir, True)
    utils.smkdir((out_dir, func_dir))
    gen_meta(proj_attr, tmp_dir)
    crafts.gen(proj_name, func_dir, receipes)
    pack(tmp_dir, proj_dir, proj_name, proj_attr)
