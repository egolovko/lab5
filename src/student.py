class Student:
    def __init__(self, npass):
        self._npass: str = npass
        self._fname: str = None
        self._lname: str = None
        self._patronymic: str = None
        self._exams = []

    def __eq__(self, other):
        return self._npass == other.npass

    def load(self, fname, lname, patronymic, subject, score, total_score_100, total_score_5):
        self._fname = fname
        self._lname = lname
        self._patronymic = patronymic


