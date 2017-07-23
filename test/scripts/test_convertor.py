from biokit.scripts import converter
from biokit import biokit_data
import pytest
from easydev import TempFile

prog = "converter"



def test_prog():
    try:
        converter.main([prog])
        assert False
    except SystemExit:
        pass
    else:
        raise Exception

def test_version():
    try:
        converter.main([prog, '--version'])
        assert False
    except SystemExit:
        pass
    else:
        raise Exception


def test_help():
    try:
        converter.main([prog, '--help'])
        assert False
    except SystemExit:
        pass
    else:
        raise Exception


def test_formats():
    try:
        converter.main([prog, "--formats"])
    except SystemExit:
        pass


def test_input_output():

    infile = biokit_data("converters/measles.sorted.bam")
    with TempFile(suffix=".bed") as outfile:
        try:
            converter.main([prog, infile, outfile.name, "--logging-level", "ERROR"])
        except Exception:
            raise Exception

    # Test the input-format option
    with TempFile(suffix=".bed") as outfile:
        try:
            converter.main([prog, infile, outfile.name, '--input-format', "bam",
                "--logging-level", "ERROR"])
        except:
            assert False

    # Test wrong output format
    with TempFile(suffix=".bedd") as outfile:
        try:
            converter.main([prog, infile, outfile.name])
            assert False
        except SystemExit:
            assert True
    

