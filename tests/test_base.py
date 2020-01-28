import configparser
from configreader.base import ConfigReaderBase

import pytest


@pytest.fixture(scope="module")
def mockConfigAndExpectation():
    config = configparser.ConfigParser()
    config.optionxform = str

    """
    [Section1l]
    Option1 : Value1

    [Section2]
    ListOption : elem1,elem2

    [Section3]
    Multiline :
            option1 : line1
            option2 : line2
    MultilineList :
            option3 : elem3,elem4
            option4 : elem5
    """
    expectation = {}
    expectation["Section1"] = { "Option1" : "Value1" }
    expectation["Section2"] = { "ListOption" : "elem1,elem2" }
    expectation["Section3"] = { "Multiline" : "\noption1 : line1\noption2 : line2",
                                "MultilineList" : "\noption3 : elem3,elem4\noption4 : elem5"}
    expectation["Section4"] = { "FloatOption" : 1.2,
                                "IntOption" : 1,
                                "BoolOption": False,
                                "intlistOption" : "1,2,3",
                                "listOption" : "elem1,elem2",
                                "NoneOption" : "None",
                                "strOption" : "Someoutput"}

    config['Section1'] = expectation["Section1"]
    config['Section2'] = expectation["Section2"]
    config['Section3'] = expectation["Section3"]
    config['Section4'] = expectation["Section4"]

    return config, expectation


def test_ConfigReaderBase_init(mocker):
    mocker.patch.object(ConfigReaderBase, "readConfig")

    config = ConfigReaderBase("/path/to/config.cfg")

    assert config.path == "/path/to/config.cfg"
    ConfigReaderBase.readConfig.assert_called_once_with("/path/to/config.cfg")


def test_ConfigReaderBase_list(mocker, mockConfigAndExpectation):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    assert config.getListOption("Section2", "ListOption") == configExpectation["Section2"]["ListOption"].split(",")


def test_ConfigReaderBase_multiline(mocker, mockConfigAndExpectation):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    expectedElems = {}
    for line in configExpectation["Section3"]["Multiline"].split("\n"):
        if line == "":
            continue
        else:
            name, val = line.split(" : ")
            expectedElems[name] = val

    assert config.readMulitlineOption("Section3", "Multiline", "Single") == expectedElems


def test_ConfigReaderBase_multilinelist(mocker, mockConfigAndExpectation):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    expectedElems = {}
    for line in configExpectation["Section3"]["MultilineList"].split("\n"):
        if line == "":
            continue
        elif "," in line:
            name, val = line.split(" : ")
            val = val.split(",")
        else:
            name, val = line.split(" : ")
            val = [val]
        expectedElems[name] = val

    assert config.readMulitlineOption("Section3", "MultilineList", "List") == expectedElems


def test_ConfigReaderBase_multiline_exception(mocker, mockConfigAndExpectation):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    with pytest.raises(RuntimeError):
        config.readMulitlineOption("Section3", "MultilineList", "blubb")


@pytest.mark.parametrize("getter, expectation, option", [("float", 1.2, "FloatOption"),
                                                         ("int", 1, "IntOption"),
                                                         ("bool", False, "BoolOption"),
                                                         ("intlist", [1, 2, 3], "intlistOption"),
                                                         ("list", ["elem1", "elem2"], "listOption"),
                                                         ("str", None, "NoneOption"),
                                                         ("str", "Someoutput", "strOption")])
def test_ConfigReaderBase_setOptionWithDefault_present(mocker, mockConfigAndExpectation, getter, expectation, option):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    assert config.setOptionWithDefault("Section4", option, None, getter) == expectation


@pytest.mark.parametrize("getter, default, option", [("float", 2.1, "FloatOptionMiss"),
                                                     ("int", 2, "IntOptionMiss"),
                                                     ("bool", False, "BoolOptionMiss"),
                                                     ("intlist", [], "intlistOptionMiss"),
                                                     ("list", [], "listOptionMiss"),
                                                     ("str", "Hello", "strOptionMiss")])
def test_ConfigReaderBase_setOptionWithDefault_missing(mocker, mockConfigAndExpectation, getter, default, option):
    mockConfig, configExpectation = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = ConfigReaderBase("/path/to/config.cfg")

    assert config.setOptionWithDefault("Section4", option, default, getter) == default
