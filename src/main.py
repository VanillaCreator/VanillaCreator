import os, project, ui, utils, yaml


def env_init(ws_dir):
    config_file = "config.yml"
    utils.smkdir(ws_dir)
    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as fs:
            yaml.dump({"lang": "en_US"}, fs)


def build_projects(ws_dir):
    proj_names = os.listdir(ws_dir)
    if not proj_names:
        ui.say("no_projects")
    else:
        for proj_name in proj_names:
            proj_dir = utils.join_path(ws_dir, proj_name)
            if os.path.isdir(proj_dir):
                ui.say("building_project", False)
                print(proj_name)
                project.build(proj_dir)


def main():
    ws_dir = "workspace"
    env_init(ws_dir)
    ui.say("welcome")
    i = ui.menu("main_menu", ("b", "q"))
    if i == "b":
        build_projects(ws_dir)


if __name__ == "__main__":
    main()
