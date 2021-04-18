
class Exam:
    def __init__(self, subject):
        self._subject = subject
        self._score = None
        self._total_score_100 = None
        self._total_score_5 = None

    def __eq__(self, other):
        return self._subject == other.subject

    @property
    def subject(self):
        return self._subject

    @property
    def score(self):
        return self._score

    @property
    def total_score_100(self):
        return self._total_score_100

    @property
    def total_score_5(self):
        return self._total_score_5

    def load(self, score, total_score_100, total_score_5):
        self._score = score
        self._total_score_100 = total_score_100
        self._total_score_5 = total_score_5