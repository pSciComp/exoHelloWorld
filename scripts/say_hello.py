"""
Execution script for the hello-world job.

This script acts as the entry point. It resolves file paths,
loads configurations, and orchestrates the processing utilities.
"""

import os
import argparse
from pathlib import Path

from exohw.utils import (
    load_json_file,
    load_config,
    prepare_output_dir
)
from exohw.hello import write_hello


def main() -> None:
    """
    Main execution pipeline for the hello world script.

    Parses command line arguments, loads configurations from the
    injected environment, loads the input data, prepares the output directory,
    and executes the greeting function.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    SystemExit
        If required paths are neither provided via CLI nor defined
        in the environment variables (handled by argparse).
    """
    parser = argparse.ArgumentParser(description="Run the hello world script.")
    parser.add_argument(
        '--config-file',
        type=str,
        default=os.environ.get("CONFIG_PATH", "./config/hello_to.json"),
        help='Path to config file. Default: CONFIG_PATH environment variable.'
    )
    parser.add_argument(
        '--input-json',
        type=str,
        default=os.environ.get("INPUT_JSON", "./data/raw/people.json"),
        help='Path to the file containing the input data.'
             'Default: INPUT_JSON environment variable.'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=os.environ.get("OUTPUT_DIR", "./data/final/"),
        help='Path to output directory.'
             'Default: OUTPUT_DIR environment variable.'
    )
    parser.add_argument(
        '--course-id',
        type=int,
        default=os.environ.get("COURSE_ID", None),
        help='The index of the course to process.'
             'Default: All courses are processed'
    )
    args = parser.parse_args()

    # 2. Execute core logic using the utilities
    #    - load config and create config namespace
    config_data = load_json_file(Path(args.config_file))
    cfg = load_config(config_data=config_data)
    #    - load input data
    people = load_json_file(Path(args.input_json))
    #    - ready output location
    out_dir = prepare_output_dir(args.output_dir)
    # Determine what courses to process
    if args.course_id is None:
        courses = cfg.all_courses
    else:
        courses = [cfg.all_courses[args.course_id]]
    # Create the greeting
    for course in courses:
        final_path = write_hello(people=people,
                                 course=course,
                                 output_dir=out_dir,
                                 cfg=cfg)

    print(f"Job completed. Results safely written to {final_path}")


if __name__ == "__main__":
    main()
