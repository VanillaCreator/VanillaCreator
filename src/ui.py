import utils

lang = utils.read_yaml_file("config.yml")["lang"]
trans = utils.read_yaml_file(utils.join_path("res", lang + ".yml"))
pass
#hrt
#srs


def newline():
    print("")


def say(text, gen_newline=True):
    print(trans[text], end="")
    if gen_newline:
        newline()


def ask(text, default=None):
    say(text, False)
    if default:
        print(" [", end="")
        say("default: ", False)
        print("]")
    i = input(trans["enter_answer"] + ": ")
    if not i:
        i = default
    return i


def menu(text, sel):
    while True:
        say(text)
        i = input(trans["enter_selection"] + ": ")
        if i in sel:
            break
        else:
            say("invalid_input")
            newline()
    return i