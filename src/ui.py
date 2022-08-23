import utils


def init(lang) -> None:
    global transs
    transs = utils.read_yaml_file(utils.join_path("res", lang + ".yml"))


def newline() -> None:
    print("")


def get_trans(trans_key: str) -> str:
    try:
        trans = transs[trans_key]
    except:
        trans = "Translation not found: " + trans_key
    return trans


def say(trans_key: str, gen_newline: bool = True) -> None:
    print(get_trans(trans_key), end="")
    if gen_newline:
        newline()


def ask(trans_key: str, default: str = None) -> str:
    say(trans_key, False)
    if default:
        print(" [", end="")
        say("default", False)
        print(": " + default + "]")
    i = input(get_trans("enter_answer") + ": ")
    if not i:
        i = default
    return i


def menu(trans_key: str, sel: str) -> str:
    while True:
        newline()
        say(trans_key)
        i = input(transs["enter_selection"] + ": ")
        if i in sel:
            break
        else:
            say("invalid_input")
    return i