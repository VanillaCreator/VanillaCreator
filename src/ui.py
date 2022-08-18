import utils


def init(lang) -> None:
    global trans
    trans = utils.read_yaml_file(utils.join_path("res", lang + ".yml"))


def newline() -> None:
    print("")


def say(trans_key: str, gen_newline: bool = True) -> None:
    print(trans[trans_key], end="")
    if gen_newline:
        newline()


def ask(trans_key: str, default: str = None) -> str:
    say(trans_key, False)
    if default:
        print(" [", end="")
        say("default", False)
        print(": " + default + "]")
    i = input(trans["enter_answer"] + ": ")
    if not i:
        i = default
    return i


def menu(trans_key: str, sel: str) -> str:
    while True:
        say(trans_key)
        i = input(trans["enter_selection"] + ": ")
        if i in sel:
            break
        else:
            say("invalid_input")
            newline()
    return i