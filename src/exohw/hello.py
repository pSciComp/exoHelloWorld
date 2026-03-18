"""
Core processing functions for the hello-world service.

This module contains the business logic for generating greetings and
saving output files.
"""

import os
from collections.abc import Collection
from types import SimpleNamespace


def write_hello(people: Collection[dict[str, str]],
                course: str,
                output_dir: str,
                cfg: SimpleNamespace) -> str:
    """
    Write a greeting list for all members of a course into a text file.

    Parameters
    ----------
    people : Colleciton[dict[str, str]]
        A collection of person specific information.
    course : str
        The course for which a greeting should be created.
    output_dir : str
        The directory where the output file 'output_hello.txt' will be saved.
    cfg : SimpleNamespace
        Holding the configuration parameters.

    Returns
    -------
    str
        The full path to the created output file.
    """
    greetings = []
    # create a list of lines for the file
    for person in people:
        if course in person[cfg.courses]:
            # '\n' is the newline character
            greetings.append(f"Hello {person[cfg.name]}\n")

    output_file = os.path.join(output_dir, f"hello_for_{course}.txt")

    with open(output_file, 'w') as f:
        f.writelines(greetings)

    return output_file
