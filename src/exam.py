"""
NAME
    exam

DESCRIPTION
    This module contain class Exam, that contain information about subject
    and about the students who took this subject.

AUTHOR
    Holovko Eugene
"""


import re

from student import Student


class Exam:
    """
    Information about exam

    Parameters
    ----------
    subject : str
        Name of exam subject

    Attributes
    ----------
    subject : str
        Name of exam subject

    Raises
    ------
    ValueError
        Incorrect subject parameter
    """

    _COMPILED_PATTERN_SUBJECT = re.compile(r"^(?!\s)(((?![\d_])[\w\"\- ]){4,56})(?<!\s)$")

    def __init__(self, subject):
        if not self._check_subject(subject):
            raise ValueError

        self._subject = subject
        self._students = []

    def __repr__(self):
        return f"{self.__class__.__name__}{self._subject}"

    def __eq__(self, other):
        return self._subject == other.subject

    def __len__(self):
        return len(self._students)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < len(self._students):
            temp = self._students[self.__i]
            self.__i += 1
            return temp
        raise StopIteration

    @property
    def subject(self):
        """
        Returns
        -------
        str
            Name of exam subject.
        """
        return self._subject

    def load(self, score, total_score_100, total_score_5, ngroup, lname, fname, patronymic, npass):
        """
        Finds the student by the number of the record book, if not, add, if any, check its
        group number record data.

        Parameters
        ----------
        score : int
            Exam scores. Can not exceed 40 and must be positive. The scores scored on the exam must be at
            least 24 or equal to 0 (in the latter case, the assessment cannot be satisfactory).


        total_score_100 : int
            Sum of points scored in the semester and in the exam.
            Can not exceed 100 and must be positive.
            The total score in points is the sum of points scored in the semester and in the exam.
            The total score in points and on the state scale should be agreed with each other.

        total_score_5 : int
            The score on the state scale.
            Can take values: 2-5 - as usual, 0 - did not appear, 1 - not allowed.
            Grades 3-5 are considered satisfactory, the others - unsatisfactory. The points are whole and integral.

        ngroup : str
            The group code.
            Іs non-empty string and consists of no more than 3 letters.
            In addition to the letters of the alphabet, it can contain decimal numbers and a hyphen.

        lname : str
            Last name.
            Can have up to 28 characters.
            In addition to the letters of the alphabet, they can contain an apostrophe, a hyphen, and a space.

        fname: str
            First name.
            Can have up to 27 characters.
            In addition to the letters of the alphabet, they can contain an apostrophe, a hyphen, and a space.

        patronymic : str
            Patronymic.
            Can have up to 20 characters.
            In addition to the letters of the alphabet, they can contain an apostrophe, a hyphen, and a space.

        npass : str
            The record book number.
            Uniquely identifies the student and consists of 7 decimal digits.

        Raises
        ------
        ValueError
            Incorrect data.
        """

        try:
            student = self.find(npass)
        except ValueError:
            student = self.add(npass, ngroup)

        if student.ngroup != ngroup:
            raise ValueError

        student.load(score, total_score_100, total_score_5, lname, fname, patronymic)

    def add(self, npass, ngroup):
        """
        Add students with record book number and group code.

        Parameters
        ----------
        ngroup : str
            The group code
            Іs non-empty string and consists of no more than 3 letters.
            In addition to the letters of the alphabet, it can contain decimal numbers and a hyphen.

        npass : str
            The record book number.
            Uniquely identifies the student and consists of 7 decimal digits.

        Returns
        -------
        Student
            Added student.
        """

        new_student = Student(npass, ngroup)
        self._students.append(new_student)
        return new_student

    def find(self, npass) -> Student:
        """
        Finds the student by the number of the record book.

        Parameters
        ----------
        npass : str
            The record book number.
            Uniquely identifies the student and consists of 7 decimal digits.

        Raises
        ------
        ValueError
            Student not with this npass not in exist.

        Returns
        -------
        Student
            Student with this npass.
        """

        index = self._students.index(Student(npass))
        student = self._students[index]
        return student

    def _check_subject(self, subject):
        if not isinstance(subject, str):
            return False

        main_check = Exam._COMPILED_PATTERN_SUBJECT.fullmatch(subject) is not None

        return main_check


