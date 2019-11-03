def unkebab(s):
    return " ".join(s.split("-"))


def space_to_kebab(s):
    return "-".join(s.split(" "))


def camel_to_space(s):
    return " ".join(s.split("_"))
