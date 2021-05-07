"""
NAME
    Lab5, 70

DESCRIPTION
    This program preapre the results of students taking the exams of the winter session.
"""

import loader

from sys import argv
from information import Information
from loading_exception import LoadingException


def process(init_file_path: str) -> None:

    storage = Information.get_instance()

    print(f"ini {init_file_path}:", end=" ")
    config = loader.load_ini(init_file_path)
    print("OK")

    loader.load(
        storage,
        config["input"]["csv"],
        config["input"]["json"],
        config["input"]["encoding"])

    print(f"output {config['output']['fname']}:", end=" ")
    storage.output(config["output"]["fname"], config["output"]["encoding"])
    print("OK")


def _main(args):
    print(f"This program preapre the results of students taking the exams of the winter session.")
    print("This program is coded by Holovko Eugene, K-12.")
    print("*****")

    try:
        process(args[1])
    except IndexError as ie:
        print("***** program aborted *****")
        print(ie)

    except ValueError as ve:
        print("UPS")
        print("***** program aborted *****")
        print(ve)
    except LoadingException as le:
        print("UPS")
        print("***** program aborted *****")
        print(le)
    except FileNotFoundError as fnfe:
        print("UPS")
        print("***** program aborted *****")
        print(fnfe)


if __name__ == "__main__":
    _main(argv)