import os, project, sys, utils

debug = True


def show_help():
  print("./main.py build\t\t\tBuild projects")


def build_projects(ws_dir):
  project_dirs = os.listdir(ws_dir)
  if not project_dirs:
    print("No projects")
  else:
    for project_dir in project_dirs:
      project.build(utils.join_path(ws_dir, project_dir))


def main(argv):
  ws_dir = "workspace"
  utils.smkdir(ws_dir)
  print("Welcome to VanillaCreator!")
  if not debug:
    if len(argv) > 1:
      if argv[1] == "build":
        build_projects(ws_dir)
      else:
        show_help()
    else:
      show_help()
  else:
    build_projects(ws_dir)


if __name__ == "__main__":
  main(sys.argv)
