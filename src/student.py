import re


class Student:
    _compiled_pattern_has_nums = re.compile(r"[0-9]+")
    _compiled_pattern_has_underscore = re.compile(r"[_]+")
    _compiled_pattern_fname = re.compile(r"^(?!\s)([\w`'\- ]{,27})(?<!\s)$")
    _compiled_pattern_lname = re.compile(r"^(?!\s)([\w`'\- ]{,28})(?<!\s)$")
    _compiled_pattern_patronymic = re.compile(r"^(?!\s)([\w`'\- ]{,20})(?<!\s)$")
    _compiled_pattern_ngroup = re.compile(r"^(?!\s)([\w\-]{1,3})(?<!\s)$")
    _compiled_pattern_npass = re.compile(r"^(?!\s)([0-9]{7})(?<!\s)$")

    def __init__(self, npass, ngroup=None):
        if not self._check_npass(npass):
            raise ValueError

        if ngroup is not None and not self._check_ngroup(ngroup):
            raise ValueError

        self._npass = npass
        self._ngroup = ngroup
        self._fname = None
        self._lname = None
        self._patronymic = None
        self._score = None
        self._total_score_100 = None
        self._total_score_5 = None

    def __eq__(self, other):
        return self._npass == other.npass

    def __repr__(self):
        return f"{self.__class__.__name__}({self._npass}, {self._ngroup}, {self._fname}, {self._lname}, " + \
               f"{self._patronymic}, {self._score}, {self._total_score_100}, {self.total_score_5})"

    @property
    def npass(self):
        return self._npass

    @property
    def ngroup(self):
        return self._ngroup

    @property
    def fname(self):
        return self._fname

    @property
    def lname(self):
        return self._lname

    @property
    def patronymic(self):
        return self._patronymic

    @property
    def score(self):
        return self._score

    @property
    def total_score_100(self):
        return self._total_score_100

    @property
    def total_score_5(self):
        return self._total_score_5

    def load(self, score, total_score_100, total_score_5, lname, fname, patronymic):
        if not self._check_numerical_fileds(score, total_score_100, total_score_5):
            raise ValueError

        if fname is not None and not self._check_fname(fname):
            raise ValueError

        if lname is not None and not self._check_lname(lname):
            raise ValueError

        if patronymic is not None and not self._check_patronymic(patronymic):
            raise ValueError

        self._score = score
        self._total_score_100 = total_score_100
        self._total_score_5 = total_score_5
        self._lname = lname
        self._fname = fname
        self._patronymic = patronymic

    def _check_fname(self, fname):
        if not isinstance(fname, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(fname) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(fname) is None
        has_no_underscore = Student._compiled_pattern_has_nums.search(fname) is None

        return main_check and has_no_nums and has_no_underscore

    def _check_lname(self, lname):
        if not isinstance(lname, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(lname) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(lname) is None
        has_no_underscore = Student._compiled_pattern_has_underscore.search(lname) is None

        return main_check and has_no_nums and has_no_underscore

    def _check_patronymic(self, patronymic):
        if not isinstance(patronymic, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(patronymic) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(patronymic) is None
        has_no_underscore = Student._compiled_pattern_has_nums.search(patronymic) is None

        return main_check and has_no_nums and has_no_underscore

    def _check_ngroup(self, ngroup):
        if not isinstance(ngroup, str):
            raise ValueError

        main_check = Student._compiled_pattern_ngroup.fullmatch(ngroup) is not None
        has_no_underscore = Student._compiled_pattern_has_underscore.search(ngroup) is None

        return main_check and has_no_underscore

    def _check_npass(self, npass):
        if not isinstance(npass, str):
            raise ValueError

        main_check = Student._compiled_pattern_npass.fullmatch(npass) is not None

        return main_check

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


