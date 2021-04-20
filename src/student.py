import re

from exam import Exam


class Student:
    _compiled_pattern_has_nums = re.compile(r"[0-9]+")
    _compiled_pattern_has_underscore = re.compile(r"[_]+")
    _compiled_pattern_fname = re.compile(r"^([\w`'\-][\w`'\- ]{,25}[\w`'\-])$")
    _compiled_pattern_lname = re.compile(r"^([\w`'\-][\w`'\- ]{,26}[\w`'\-])$")
    _compiled_pattern_patronymic = re.compile(r"^([\w`'\-][\w`'\- ]{,18}[\w`'\-])$")
    _compiled_pattern_ngroup = re.compile(r"^(?<!\s)([\w0-9\-]{1,3})(?!\s)$")
    _compiled_pattern_npass = re.compile(r"^(?<!\s)([0-9]{7})(?!\s)$")

    def __init__(self, npass, ngroup=None, fname=None, lname=None, patronymic=None):
        if not self._check_npass(npass):
            raise ValueError

        if ngroup is not None and not self._check_ngroup(ngroup):
            raise ValueError

        if fname is not None and not self._check_fname(fname):
            raise ValueError

        if lname is not None and not self._check_lname(lname):
            raise ValueError

        if patronymic is not None and not self._check_patronymic(patronymic):
            raise ValueError

        self._npass = npass
        self._ngroup = ngroup
        self._fname = fname
        self._lname = lname
        self._patronymic = patronymic
        self._exams = []

    def __eq__(self, other):
        return self._npass == other.npass

    def __repr__(self):
        return f"{self.__class__.__name__}{self._npass, self._fname, self._lname, self._patronymic}"

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self._exams):
            raise StopIteration
        exam = self._exams[self._index]
        self._index += 1
        return exam

    def load(self, subject, score, total_score_100, total_score_5):
        try:
            exam = self.find(subject)
        except ValueError:
            exam = self.add(subject)

        exam.load(score, total_score_100, total_score_5)

    def find(self, subject):
        index = self._exams.index(Exam(subject))
        exam = self._exams[index]
        return exam

    def add(self, subject):
        new_exam = Exam(subject)
        self._exams.append(new_exam)
        return new_exam

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

    def _check_fname(self, fname):
        if not isinstance(fname, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(fname) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(fname) is None
        has_no_underscore = Student._compiled_pattern_has_nums.search(fname) is None

        return main_check and has_no_nums and has_no_underscore or (len(fname) == 1 and not fname.isspace())

    def _check_lname(self, lname):
        if not isinstance(lname, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(lname) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(lname) is None
        has_no_underscore = Student._compiled_pattern_has_underscore.search(lname) is None

        return main_check and has_no_nums and has_no_underscore or (len(lname) == 1 and not lname.isspace())

    def _check_patronymic(self, patronymic):
        if not isinstance(patronymic, str):
            raise ValueError

        main_check = Student._compiled_pattern_fname.fullmatch(patronymic) is not None
        has_no_nums = Student._compiled_pattern_has_nums.search(patronymic) is None
        has_no_underscore = Student._compiled_pattern_has_nums.search(patronymic) is None

        return main_check and has_no_nums and has_no_underscore or (len(patronymic) == 1 and not patronymic.isspace())

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


if __name__ == "__main__":
    s = Student("123")
    subjects = [
        ("asdasd", 1),
        ("asdd", 1),
        ("  sd", 0),
        ("asd   ", 0),
        (" asd ", 0),
        ("ASDD", 1),
        ("as-d", 1),
        ("as\"d", 1),
        ("as\\'d", 0),
        ("!asdasd", 0),
        ("      ", 0),
    ]
    for word, status in subjects:
        print(word, "\t", status, "\t", status == s._check_subject(word))

    print()
    print()

    names = [
        ("asdasd", 1),
        ("  asdads", 0),
        ("asdasd   ", 0),
        ("asas dd", 1),
        ("!asd!", 0),
        ("s", 1),
        (" ", 0),
        ("      ", 0)
    ]

    for word, status in names:
        print(word, status, status == s._check_fname(word))

    print()
    print()

    gcodes = [
        (" asd ", 0),
        ("asd ", 0),
        (" asd", 0),
        ("a s", 0),
        ("", 0),
        ("asd", 1),
        ("a_d", 0),
        ("K12", 1),
        ("R-3", 1)
    ]

    for word, status in gcodes:
        print(word, status, status == s._check_ngroup(word))

    print()
    print()

    ncodes = [
        ("1234567", 1),
        ("  12345", 0),
        ("14567  ", 0),
        ("12345678", 0),
        ("123 567", 0),
        ("1234a67", 0),
        ("12345_7", 0)
    ]

    for word, status in ncodes:
        print(word, status, status == s._check_npass(word))

    print()
    print()


