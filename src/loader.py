import json
import csv

from information import Information
from builder import Builder
from loading_exception import LoadingException


def load(storage, csv_file, json_file, encoding):
    print(f"input-csv {csv_file}:", end=" ")
    data = load_data(storage, csv_file, encoding)
    print("OK")

    print(f"input-json {json_file}:", end=" ")
    stat = load_stat(json_file, encoding)
    print("OK")

    print(f"json?=csv: OK", end=" ")
    if not fit(data, stat):
        raise LoadingException(f"Comparation error")
    print("OK")


def load_ini(path):
    with open(path, "r") as ini_file:
        data = json.load(ini_file)

    if not _check_ini_structure(data):
        raise LoadingException(f"incorrect data format in ini file")

    return data


def load_data(storage, path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as data_file:
        builder = Builder()
        builder.load(storage, data_file)

    raise LoadingException("implementation error")


def load_stat(path, encoding="utf-8"):
    with open(path, 'r', encoding=encoding) as stat_file:
        data = json.load(stat_file)

    if not _check_stat_structure(data):
        raise LoadingException(f"incorrect data format in stat file")

    if not _check_stat_values(data):
        raise LoadingException(f"incorrect data format in stat file")

    prepared_data = _prepare_stat(data)
    return prepared_data


def fit(storage: Information, stat: object):
    return storage.records_count == stat["total_records_count"] and storage.scores_100_count == stat["count_rating_100"]


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


def _prepare_stat(data: object):
    new_data = {
        "total_records_count": int(data["загальна кiлькiсть записiв"]),
        "count_rating_100": int(data["кiлькiсть оцiнок 100"])
    }
    return new_data


def _check_stat_values(data: object):
    total_records_count = data["загальна кiлькiсть записiв"]
    count_rating_100 = data["кiлькiсть оцiнок 100"]

    return total_records_count.isdigit() and count_rating_100.isdigit()


if __name__ == "__main__":
    from information import Information
    with open("data.csv", "r") as f:
        builder = Builder()
        builder.load(Information.get_instance(), f)

