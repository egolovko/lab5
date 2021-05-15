"""
NAME
    loader_writer

DESCRIPTION
    This module contain functions for reading, saving data from file
    and outputting prepared information to file

AUTHOR
    Holovko Eugene
"""

import json

from builder import Builder


def load(storage, csv_file, json_file, encoding="utf-8"):
    """
    Load the main, additional file and checks their content.

    Parameters
    ----------
    storage : information.Information
        Storage in which data from csv file will be added.

    csv_file : str
        Path to csv file with main data.

    json_file : str
        Path to json file with statistics info.

    encoding : str
        Files encoding.
        Default utf-8.

    Raises
    ------
    ValueError
        Incorrect data
    """

    print(f"input-csv {csv_file}:", end=" ")
    load_data(storage, csv_file, encoding)
    print("OK")

    print(f"input-json {json_file}:", end=" ")
    stat = load_stat(json_file, encoding)
    print("OK")

    print(f"json?=csv:", end=" ")
    if not fit(storage, stat):
        raise ValueError(f"Comparison error")
    print("OK")


def load_ini(path):
    """
    Load the settings file.

    Parameters
    ----------
    path : str
        Path to file

    Raises
    ------
    ValueError
        Incorrect data

    Returns
    -------
    dict
        Dictionary with settings data
    """

    with open(path, "r") as ini_file:
        data = json.load(ini_file)

    if not _check_ini_structure(data):
        raise ValueError(f"Incorrect data format in ini file")

    return data


def load_data(storage, path, encoding="utf-8"):
    """
    Load the csv file with main data.

    Parameters
    ----------
    storage : information.Information
        Storage in which data from csv file will be added.

    path : str
        Path to file.

    encoding : str
        File encoding.
        Default utf-8.

    Raises
    ------
    ValueError
        Incorrect data
    """

    with open(path, "r", encoding=encoding) as data_file:
        builder = Builder()
        builder.load(storage, data_file)


def load_stat(path, encoding="utf-8"):
    """
    Load the additional file with statistics.

    Parameters
    ----------
    path : str
        Path to file.

    encoding : str
        File encoding.
        Default utf-8.

    Raises
    ------
    ValueError
        Incorrect data

    Returns
    -------
    Dict
        Dictionary with statistics data
    """

    with open(path, 'r', encoding=encoding) as stat_file:
        data = json.load(stat_file)

    if not _check_stat_structure(data):
        raise ValueError(f"Incorrect data format in stat file")

    if not _check_stat_values(data):
        raise ValueError(f"Incorrect data format in stat file")

    prepared_data = _prepare_stat(data)
    return prepared_data


def fit(storage, stat):
    """
    Check content in storage and stat file.

    Parameters
    ----------
    storage : information.Information
        Storage with processed information

    stat : dict
        Dictionary with statistics

    Returns
    -------
    bool
        True if equals, else False
    """

    return storage.records_count == stat["total_records_count"] and \
           storage.scores_100_count == stat["count_rating_100"]


def output(storage, path, encoding="utf-8"):
    """
    Save prepared information in file.

    Parameters
    ----------
    storage : information.Information
        Storage with processed information

    path : str
        Path to file.

    encoding : str
        File encoding.
        Default utf-8.
    """
    with open(path, "w", encoding=encoding) as out_file:
        _output(storage, out_file)


def _output(storage, file):
    result_data = _get_subjects_list_with_max_mean(storage)
    for info in result_data:
        file.write(f"{info['exam'].subject}\t{info['mean']:.1f}\t{info['count_of_failed']}\n")
        for student in info["less_than_95"]:
            file.write(f"\t{student.lname}\t{student.fname}\t{student.patronymic}\t{student.npass}" +
                       f"\t{student.total_score_100}\t{student.total_score_5}\n")


def _get_subjects_list_with_max_mean(storage):
    result_data = []

    all_results = _get_all_results(storage)
    max_mean = _get_max_mean(all_results)
    for info in all_results:
        if info["mean"] == max_mean:
            result_data.append(info)

    return result_data


def _get_max_mean(all_results):
    max_mean = all_results[0]["mean"]

    for info in all_results:
        if info["mean"] > max_mean:
            max_mean = info["mean"]
    return max_mean


def _get_all_results(storage):
    res = []
    for exam in storage:
        info = {
            "exam": exam,
            "mean": _get_subject_mean_total_score(exam),
            "count_of_failed": _get_count_of_exam_failed(exam),
            "less_than_95": _get_less_than_95(exam)
        }
        info["less_than_95"].sort(key=lambda x: x.npass)
        res.append(info)
    return res


def _get_subject_mean_total_score(exam):
    return sum(student.total_score_100 for student in exam) / len(exam)


def _get_count_of_exam_failed(exam):
    return sum(1 for student in exam if student.total_score_5 < 3)


def _get_less_than_95(exam):
    return [student for student in exam if student.total_score_100 < 95]


def _check_ini_structure(data):
    if "input" not in data:
        return False
    elif not all(key in data["input"] for key in ["csv", "json", "encoding"]):
        return False

    if "output" not in data:
        return False
    elif not all(key in data["output"] for key in ["fname", "encoding"]):
        return False

    return True


def _check_stat_structure(data):
    if not all(key in data for key in ["загальна кiлькiсть записiв", "кiлькiсть оцiнок 100", "SMILE"]):
        return False

    return True


def _prepare_stat(data):
    new_data = {
        "total_records_count": int(data["загальна кiлькiсть записiв"]),
        "count_rating_100": int(data["кiлькiсть оцiнок 100"])
    }
    return new_data


def _check_stat_values(data):
    total_records_count = data["загальна кiлькiсть записiв"]
    count_rating_100 = data["кiлькiсть оцiнок 100"]

    return isinstance(total_records_count, int) and isinstance(count_rating_100, int)
