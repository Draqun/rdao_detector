#!/usr/bin/env python3.8

__author__ = "Damian Giebas"
__email__ = "damian.giebas@gmail.com"
__license__ = "GNU/GPLv3"
__version__ = "0.4"

import argparse
from collections import deque
from helpers.path import collect_c_project_files
from helpers.purifier import purify_file, purify_files
import logging
from mascm import create_mascm
from os.path import join, dirname
from pycparser import parse_file

parser = argparse.ArgumentParser(description='Process AST to MASCM')
parser.add_argument('path', type=str, help="Paths to source code")
parser.add_argument('--cflags', type=str, default="", help="Compiler flags needed for compilation")
parser.add_argument(
    '--log-level', type=int, choices=(logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL),
    default=logging.INFO
)
# TODO: Add parameter for compiler flags


def create_ast(path: str, cflags: str = "") -> deque:
    """Function converting C code to AST
    :param path: Path to source code
    :param cflags: C compiler flags needed to compilation
    :return: deque object
    """
    try:
        ast = deque()
        ast.append(parse_file(purify_file(path, cflags=cflags)))
        return ast
    except IsADirectoryError:
        pass
    pure_files = purify_files(collect_c_project_files(path), cflags=cflags)
    ast = deque()
    for file in pure_files:
        ast.append(parse_file(file))
    return ast


def main() -> None:
    """ Main function
    """
    args = parser.parse_args()
    logging.basicConfig(filename=join(dirname(__file__), "mascm_generator.log"), level=args.log_level)
    mascm = create_mascm(create_ast(args.path, args.cflags))
    print(mascm)


if "__main__" == __name__:
    main()
