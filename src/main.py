import os, project, ui, utils, yaml


def config_init():
    config_file = "config.yml"
    if not (os.path.exists(config_file) and ()utils.read_yaml_file(config_file)):
        config = {}
        if ui.menu("set_language", ("e", "c")) == "c":
            config["lang"] = "zh_CN"
        else:
            config["lang"] = "en_US"
        config["workspace"] = ui.ask("enter_workspace", "./workspace")
        with open(config_file, "w", encoding="utf-8") as fs:
            yaml.dump(config, fs)


def build_projects(ws_dir):
    proj_names = os.listdir(ws_dir)
    if not proj_names:
        ui.say("no_projects")
    else:
        for proj_name in proj_names:
            proj_dir = utils.join_path(ws_dir, proj_name)
            if os.path.isdir(proj_dir):
                ui.say("building_project", False)
                print(": " + proj_name)
                project.build(proj_dir)


def main():
    ws_dir = "workspace"
    config_init()
    ui.say("welcome")
    i = ui.menu("main_menu", ("b", "q"))
    if i == "b":
        build_projects(ws_dir)


if __name__ == "__main__":
    main()
