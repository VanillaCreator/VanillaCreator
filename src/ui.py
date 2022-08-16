import utils

lang = utils.read_yaml_file("config.yml")["lang"]
trans = utils.read_yaml_file(utils.join_path("res", lang + ".yml"))
pass
#hrt
#srs


def say(text, newline=True):
    if newline:
        end = None
    else:
        end = ""
    print(trans[text], end=end)


def menu(text, sel):
    while True:
        print(trans[text])
        i = input(trans["enter_selection"])
        if i in sel:
            break
        else:
            print(trans["invalid_input"])
            print("")
    return i