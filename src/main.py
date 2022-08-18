import os, project, sys, ui, utils, yaml


def set_language(settings: dict) -> None:
    if ui.menu("set_language", ("e", "c")) == "c":
        settings["lang"] = "zh_CN"
    else:
        settings["lang"] = "en_US"


def set_workspace(settings: dict) -> None:
    settings["workspace"] = ui.ask("enter_workspace", "./workspace")


def write_settings(settings: dict, settings_file: str) -> None:
    with open(settings_file, "w", encoding="utf-8") as fs:
        yaml.dump(settings, fs)


def change_settings(settings: str, settings_file: str) -> None:
    i = ui.menu("change_settings", ("l", "w"))
    if i == "l":
        set_language(settings)
    elif i == "w":
        set_workspace(settings)
    write_settings(settings, settings_file)


def init_settings(settings_file: str) -> dict:
    settings = {}
    set_language(settings)
    settings = set_workspace(settings)
    write_settings(settings, settings_file)
    return settings


def build_projects(ws_dir: str) -> None:
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


def main() -> int:
    settings_file = "settings.yml"
    if not os.path.exists(settings_file):
        settings = init_settings(settings_file)
    else:
        settings = utils.read_yaml_file(settings_file)
    ui.init()
    ui.say("welcome")
    while True:
        i = ui.menu("main_menu", ("b", "s", "q"))
        if i == "b":
            build_projects(settings["workspace"])
        elif i == "s":
            change_settings(settings, settings_file)
        else:
            return 0


if __name__ == "__main__":
    sys.exit(main())
