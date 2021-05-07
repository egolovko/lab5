import re

from student import Student


class Exam:
    _compiled_pattern_subject = re.compile(r"^(?!\s)([\w\"\- ]{4,56})(?<!\s)$")
    _compiled_pattern_has_nums_and_underscore = re.compile(r"[0-9_]+")

    def __init__(self, subject):
        if not self._check_subject(subject):
            raise ValueError

        self._subject = subject
        self._students = []

    def __repr__(self):
        return f"{self.__class__.__name__}{self._subject}"

    def __eq__(self, other):
        return self._subject == other.subject

    def __iter__(self):
        self._i = 0
        return self

    def __len__(self):
        return len(self._students)

    def __next__(self):
        if self._i < len(self._students):
            temp = self._students[self._i]
            self._i += 1
            return temp
        raise StopIteration


    @property
    def subject(self):
        return self._subject

    def load(self, score, total_score_100, total_score_5, ngroup, lname, fname, patronymic, npass):
        try:
            student = self.find(npass)
        except ValueError:
            student = self.add(npass, ngroup)

        if student.ngroup != ngroup:
            raise ValueError

        student.load(score, total_score_100, total_score_5, lname, fname, patronymic)

    def add(self, npass, ngroup):
        new_student = Student(npass, ngroup)
        self._students.append(new_student)
        return new_student

    def find(self, npass) -> Student:
        index = self._students.index(Student(npass))
        student = self._students[index]
        return student

    def _check_subject(self, subject):
        if not isinstance(subject, str):
            raise ValueError

        main_check = Exam._compiled_pattern_subject.fullmatch(subject) is not None
        has_no_nums_and_udnerscore = Exam._compiled_pattern_has_nums_and_underscore.search(subject) is None

        return main_check and has_no_nums_and_udnerscore


