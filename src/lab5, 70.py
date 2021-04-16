"""
NAME
    Lab5, 70

DESCRIPTION
    This program preapre the results of students taking the exams of the winter session.
"""

import sys
import loader

from information import Information
from loading_exception import LoadingException


def process(init_file_path: str) -> None:

    print(f"ini {init_file_path}:", end=" ")
    config = loader.load_ini(init_file_path)
    print("OK")

    loader.load(
        Information.get_instance,
        config["input"]["csv"],
        config["input"]["json"],
        config["input"]["encoding"])


def _main(args):
    print(f"This program preapre the results of students taking the exams of the winter session.")
    print("This program is coded by Holovko Eugene, K-12.")
    print("*****")

    try:
        process(args[1])
    except IndexError as ie:
        print("***** program aborted *****")
        print(ie)
    except LoadingException as le:
        print("UPS")
        print("***** program aborted *****")
        print(le)
    except FileNotFoundError as fnfe:
        print("UPS")
        print("***** program aborted *****")
        print(fnfe)


if __name__ == "__main__":
    _main(sys.argv)