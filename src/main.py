import os, project, ui, utils, yaml


def env_init(ws_dir):
    config_file = "config.yml"
    utils.smkdir(ws_dir)
    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as fs:
            yaml.dump({"lang": "en_US"}, fs)


def build_projects(ws_dir):
    project_dirs = os.listdir(ws_dir)
    if not project_dirs:
        ui.say("no_projects")
    else:
        for project_dir in project_dirs:
            project_dir_full = utils.join_path(ws_dir, project_dir)
            if os.path.isdir(project_dir_full):
                ui.say("building_project", False)
                print(project_dir)
                project.build(project_dir_full)


def main():
    ws_dir = "workspace"
    env_init(ws_dir)
    ui.say("welcome")
    i = ui.menu("main_menu", ("b", "q"))
    if i == "b":
        build_projects(ws_dir)


if __name__ == "__main__":
    main()
