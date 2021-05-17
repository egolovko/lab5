"""
NAME
    builder

DESCRIPTION
    This module contain class Builder, that allow the user to build storage class by file with data.

AUTHOR
    Holovko Eugene
"""

import csv


class Builder:
    """
    Reads lines of the file, analyzes empty and "missing" those that have the wrong number of fields.

    Attributes
    ----------
    COUNT_OF_COLUMNS : int
        Count of column that must be read from input file.
    """

    COUNT_OF_COLUMNS = 9

    def __init__(self):
        self._line = None

        self._npass = None
        self._ngroup = None
        self._fname = None
        self._lname = None
        self._patronymic = None
        self._subject = None
        self._score = None
        self._total_score_100 = None
        self._total_score_5 = None

    def reset(self):
        """
        Reset builder state.
        """

        self._line = None
        self._npass = None
        self._ngroup = None
        self._fname = None
        self._lname = None
        self._patronymic = None
        self._subject = None
        self._score = None
        self._total_score_100 = None
        self._total_score_5 = None

    def load(self, storage, file):
        """
        Loads the main file; downloads an additional file;
        checks the correspondence of the information of the main and additional files.

        Parameters
        ----------
        storage : information.Information
            Storage where processed lines will be added.

        file : IO
            Binary file.

        Raises
        ------
        ValueError
            Invalid input data in file.
        """

        storage.clear()

        with storage as st:
            reader = csv.reader(file, delimiter=";")
            for row in reader:

                if len(row) == 0:
                    continue

                self._line = row
                self._prepare_current_line()
                st.load(self._ngroup, self._subject, self._lname, self._total_score_100, self._score,
                        self._fname, self._total_score_5, self._patronymic, self._npass)

    def _prepare_current_line(self):

        if len(self._line) < Builder.COUNT_OF_COLUMNS:
            raise ValueError

        self._convert_fields()

    def _convert_fields(self):
        if not (self._line[3].isdigit() or self._line[4].isdigit() or self._line[6].isdigit()):
            raise ValueError

        self._ngroup = self._line[0]
        self._subject = self._line[1]
        self._lname = self._line[2]
        self._total_score_100 = int(self._line[3])
        self._score = int(self._line[4])
        self._fname = self._line[5]
        self._total_score_5 = int(self._line[6])
        self._patronymic = self._line[7]
        self._npass = self._line[8]
