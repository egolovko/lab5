"""
NAME
    information

DESCRIPTION
    This module contain class Information, that contain information about exams.

AUTHOR
    Holovko Eugene
"""

from exam import Exam


class Information:
    """
    Contain information about exams.

    Attributes
    ----------
    records_count : int
        Count of records.

    scores_100_count : int
        Count of students who have 100 by total score.
    """

    _instance = None

    def __init__(self):
        self._exams = []
        self._records_count = 0
        self._scores_100_count = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.clear()

    def __len__(self):
        return len(self._exams)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < len(self._exams):
            temp = self._exams[self.__i]
            self.__i += 1
            return temp
        raise StopIteration

    @property
    def records_count(self):
        """
        Returns
        -------
        int
            Total count of records in information.
        """
        return self._records_count

    @property
    def scores_100_count(self):
        """
        Returns
        -------
        int
            Count of scores 100.
        """
        return self._scores_100_count

    def clear(self):
        """
        Reset class fields.
        """

        self._records_count = 0
        self._scores_100_count = 0
        self._exams.clear()

    def load(self, ngroup, subject, lname, total_score_100, score, fname, total_score_5, patronymic, npass):
        """
        Finds the exam by the subject, if not exist - add.

        Parameters
        ----------
        ngroup : str
            The group code.
            Іs non-empty string and consists of no more than 3 letters.
            In addition to the letters of the alphabet, it can contain decimal numbers and a hyphen.

        subject : str
            Exam subject name.
            Must have from 4 to 56 characters inclusive. In addition to the
            letters of the alphabet, it can contain double quotes, spaces, and hyphens.

        lname : str
            Last name.
            Can have up to 28 characters.
            In addition to the letters of the alphabet, they can contain an apostrophe, a hyphen, and a space.

        total_score_100 : int
            Sum of points scored in the semester and in the exam.
            Can not exceed 100 and must be positive.
            The total score in points is the sum of points scored in the semester and in the exam.
            The total score in points and on the state scale should be agreed with each other.

        score : int
            Exam scores. Can not exceed 40 and must be positive. The scores scored on the exam must be at
            least 24 or equal to 0 (in the latter case, the assessment cannot be satisfactory).

        fname: str
            First name.
            Can have up to 27 characters.
            In addition to the letters of the alphabet, they can contain an apostrophe, a hyphen, and a space.

        total_score_5 : int
            The score on the state scale.
            Can take values: 2-5 - as usual, 0 - did not appear, 1 - not allowed.
            Grades 3-5 are considered satisfactory, the others - unsatisfactory. The points are whole and integral.

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
            exam = self.find(subject)
        except ValueError:
            exam = self.add(subject)

        exam.load(score, total_score_100, total_score_5, ngroup, lname, fname, patronymic, npass)

        self._records_count += 1
        if total_score_100 == 100:
            self._scores_100_count += 1

    def find(self, subject):
        """
        Finds the exma by the subject name.

        Parameters
        ----------
        subject : str
            Exam subject name.
            Must have from 4 to 56 characters inclusive. In addition to the
            letters of the alphabet, it can contain double quotes, spaces, and hyphens.

        Raises
        ------
        ValueError
            Exam not with this subject name not in exist.

        Returns
        -------
        Exam
            Exam with this subject name.
        """
        index = self._exams.index(Exam(subject))
        exam = self._exams[index]
        return exam

    def add(self, subject):
        """
        Add exam with this subject name.

        Parameters
        ----------
        subject : str
            Exam subject name.
            Must have from 4 to 56 characters inclusive. In addition to the
            letters of the alphabet, it can contain double quotes, spaces, and hyphens.

        Returns
        -------
        Exam
            Added exam.
        """
        new_exam = Exam(subject)
        self._exams.append(new_exam)
        return new_exam

