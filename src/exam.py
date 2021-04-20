import re


class Exam:
    _compiled_pattern_subject = re.compile(r"^(?<!\s)([\w\"\-][\w\"\- ]{2,54}[\w\"\-])(?!\s)$")
    _compiled_pattern_has_nums_and_underscore = re.compile(r"[0-9_]+")

    def __init__(self, subject):
        if not self._check_subject(subject):
            raise ValueError

        self._subject = subject
        self._score = None
        self._total_score_100 = None
        self._total_score_5 = None

    def __repr__(self):
        return f"{self.__class__.__name__}{self._subject, self._score, self._total_score_100, self._total_score_5}"

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
        if not self._check_numerical_fileds(score, total_score_100, total_score_5):
            raise ValueError

        self._score = score
        self._total_score_100 = total_score_100
        self._total_score_5 = total_score_5

    def _check_subject(self, subject):
        if not isinstance(subject, str):
            raise ValueError

        main_check = Exam._compiled_pattern_subject.fullmatch(subject) is not None
        has_no_nums_and_udnerscore = Exam._compiled_pattern_has_nums_and_underscore.search(subject) is None

        return main_check and has_no_nums_and_udnerscore

    def _check_numerical_fileds(self, score, total_score_100, total_score_5):
        if not self._check_score(score):
            return False

        if not self._check_total_score_100(total_score_100):
            return False

        if not self._check_total_score_5(total_score_5):
            return False

        if not self._check_conformity(total_score_100, total_score_5, score):
            return False

        return True

    def _check_score(self, score):
        return isinstance(score, int) and (score == 0 or 24 <= score <= 40)

    def _check_total_score_100(self, total_score_100):
        return isinstance(total_score_100, int) and 0 <= total_score_100 <= 100

    def _check_total_score_5(self, total_score_5):
        return isinstance(total_score_5, int) and 0 <= total_score_5 <= 5

    def _check_conformity(self, total_score_100, total_score_5, score):

        if total_score_100 >= 90 and total_score_5 != 5:
            return False

        elif 75 <= total_score_100 <= 89 and total_score_5 != 4:
            return False

        elif 60 <= total_score_100 <= 74 and total_score_5 != 3:
            return False

        elif total_score_100 <= 59 and total_score_5 >= 3:
            return False

        if score < 24 and total_score_5 >= 3:
            return False

        semester_score = total_score_100 - score
        if not (0 <= semester_score <= 60):
            return False

        return True
