"""
NAME
    lab5, 70

DESCRIPTION
    This program prepare the results of students taking the exams of the winter session.

AUTHOR
    Holovko Eugene
"""

import loader_writer

from sys import argv
from information import Information


def _process(file_path):
    storage = Information()

    print(f"ini {file_path}:", end=" ")
    config = loader_writer.load_ini(file_path)
    print("OK")

    loader_writer.load(
        storage,
        config["input"]["csv"],
        config["input"]["json"],
        config["input"]["encoding"]
    )

    print(f"output {config['output']['fname']}:", end=" ")
    loader_writer.output(storage, config["output"]["fname"], config["output"]["encoding"])
    print("OK")


def process(file_path):
    """
    Reads the settings file and performs processing.

    Parameters
    ----------
    file_path : str
        Path to ini settings file.

    Raises
    ------
    ValueError
        Incorrect data

    KeyboardInterrupt
        The program was stopped by the user

    FileNotFoundError:
        File not exist

    LookupError
        Invalid encoding
    """

    try:
        _process(file_path)
    except Exception as exc:
        print("UPS")
        raise exc


def _main(args):
    print("This program prepare the results of students taking the exams of the winter session.")
    print("This program is coded by Holovko Eugene, K-12. Variant 70.")
    print("*****")

    try:
        process(args[1])
    except BaseException as exc:
        print("***** program aborted *****")
        print(type(exc), exc)


if __name__ == "__main__":
    _main(argv)
