class quest:

    from user import user

    questid = 0
    userid = 0
    beschreibung = ""
    exp = 0 
    dtm = 0 
    diff = 0 
    state = 0 

    def __init__(self, questid, userid, beschreibung, exp, dtm, diff, state) -> None:
        self.questid = questid
        self.userid = userid
        self.beschreibung = beschreibung
        self.exp = exp
        self.dtm = dtm
        self.diff = diff
        self.state = state
    
    def returnAsList(self):
        return [self.questid, self.beschreibung, self.exp, self.dtm, self.diff, self.state]
    
        


    
        
    