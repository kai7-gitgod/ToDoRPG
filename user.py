class user:
    userid = 0
    name = ""
    level = 0
    exp = 0

    def __init__(self, userid, name, level, exp) -> None:
        self.userid = userid
        self.name = name
        self.level = level
        self.exp = exp