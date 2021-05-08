"""
NAME
    Lab5, 70

DESCRIPTION
    This program preapre the results of students taking the exams of the winter session.
"""

import loader

from sys import argv
from information import Information


def process(init_file_path):
    """
    Reads the settings file and performs processing.

    Parameters
    ----------
    init_file_path : str
        Path to ini settings file.
    """

    storage = Information()

    print(f"ini {init_file_path}:", end=" ")
    config = loader.load_ini(init_file_path)
    print("OK")

    loader.load(
        storage,
        config["input"]["csv"],
        config["input"]["json"],
        config["input"]["encoding"]
    )

    print(f"output {config['output']['fname']}:", end=" ")
    storage.output(config["output"]["fname"], config["output"]["encoding"])
    print("OK")


def _main(args: list):
    print(f"This program preapre the results of students taking the exams of the winter session.")
    print("This program is coded by Holovko Eugene, K-12.")
    print("*****")

    try:
        process(args[1])
    except IndexError as ie:
        print("***** program aborted *****")
        print(ie)
    except (ValueError, ValueError, KeyboardInterrupt) as exc:
        print("UPS")
        print("***** program aborted *****")
        print(exc)


if __name__ == "__main__":
    _main(argv)