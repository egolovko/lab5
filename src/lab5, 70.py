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


def _print_description():
    print("This program is coded by Holovko Eugene, K-12. Variant 70.")
    print("This program prepare the results of students taking the exams of the winter session.")
    print("""
        Обробляються резльтати складання студентами екзаменiв зимовоЁ сесiї.
        Записи основного файлу мiстять поля: код групи, предмет, прiзвище, сумарна оцiнка в балах за 100-
        бально системою, набранi на екзаменi бали, iм'я, оцiнка за державно шкалою, по-батьковi, номер
        залiковоЁ книжки.
        У допомiжному файлi наявнi ключi: загальна кiлькiсть записiв, кiлькiсть оцiнок 100, SMILE.
        Знайти предмети з найкращою середньо оцiнкою. Вивести по кожному з них iнформацiю:
        - на першому рядку:
            предмет, середня оцiнка (округлений до 1 знаку), кiлькiсть студентiв, що не склали;
        - на наступних ядках, почина чи з табуляцiЁ, вивести для п едмета студентiв, що от имали з нього 
        менше 95 балiв (по одному на ядок):
            прiзвище, iм'я, по-батьковi, номер залiкової книжки, оцiнка в балах, оцiнка за державно шкалою
            у такому сортуваннi: номер залiкової книжки.
    """)


def _process(file_path):
    storage = Information()

    print(f"ini {file_path}:", end=" ")
    config = loader_writer.load_ini(file_path, "utf-8")
    print("OK")

    is_correct_loading = loader_writer.load(
        storage,
        config["input"]["csv"],
        config["input"]["json"],
        config["input"]["encoding"]
    )

    print(f"json?=csv:", end=" ")
    if is_correct_loading:
        print("OK")
    else:
        print("UPS")

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


def main(args):
    _print_description()
    print("*****")

    try:
        process(args[1])
    except BaseException as exc:
        print("\n***** program aborted *****")


if __name__ == "__main__":
    main(argv)
