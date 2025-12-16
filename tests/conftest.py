from argparse import Namespace
from systemrdl import RDLCompiler
from peakrdl_rawheader.__peakrdl__ import HeaderGeneratorDescriptor
from pathlib import Path

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"


def default_options(format):
    return Namespace(**{
        "template": None,
        "base_name": None,
        "format": format,
        "license_str": None
    })


def parse(file):
    rdlc = RDLCompiler()
    rdlc.compile_file(file)
    return rdlc.elaborate().top


def generate_header(file, format):
    return HeaderGeneratorDescriptor().format(parse(file), default_options(format))


def check_header(generated, expected):
    with open(expected, "r") as f:
        expected_content = f.read()
    assert generated == expected_content
