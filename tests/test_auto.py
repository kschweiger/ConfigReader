import configparser
from configreader.base import ConfigReaderBase, AutoConfigReader

import pytest

@pytest.fixture(scope="module")
def mockConfigAndExpectation():
    config = configparser.ConfigParser()
    config.optionxform = str

    """
    [Section1]
    Option1 : Value1
    Option2 : Value2

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
    expectation["Section1"] = { "Option1" : "Value1",
                                "Option2" : "Value2" }
    expectation["Section2"] = { "ListOption" : "elem1,elem2" }
    expectation["Section3"] = { "Multiline" : "\noption1 : line1\noption2 : line2",
                                "MultilineList" : "\noption3 : elem3,elem4\noption4 : elem5"}

    config['Section1'] = expectation["Section1"]
    config['Section2'] = expectation["Section2"]
    config['Section3'] = expectation["Section3"]

    expectationformatted = {}
    expectationformatted['Section1'] = expectation["Section1"]
    expectationformatted['Section2'] = {}
    expectationformatted['Section2']["ListOption"] = expectation["Section2"]["ListOption"].split(",")
    expectationformatted["Section3"] = {}
    expectationformatted["Section3"]["Multiline"] = { "option1" : "line1",
                                                      "option2" : "line2" }
    expectationformatted["Section3"]["MultilineList"] = { "option3" : ["elem3","elem4"],
                                                          "option4" : ["elem5"] }
    return config, expectation, expectationformatted


def test_AutoConfigReader_init(mocker, mockConfigAndExpectation):
    mockConfig, configExpectation, configExpectationFormatted = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = AutoConfigReader("/path/to/config.cfg")


    for key in configExpectationFormatted:
        assert getattr(config, key) == configExpectationFormatted[key]

@pytest.mark.parametrize("section", ["Section1", "Section2"])
def test_AutoConfigReader_init_toplevelSection(mocker, mockConfigAndExpectation, section):
    mockConfig, configExpectation, configExpectationFormatted = mockConfigAndExpectation
    mocker.patch.object(ConfigReaderBase, "readConfig", return_value=mockConfig)

    config = AutoConfigReader("/path/to/config.cfg", toplevelSection=section)
   
    
    for key in configExpectationFormatted:
        if key == section:
            for option in configExpectationFormatted[key]:
                assert getattr(config, option) == configExpectationFormatted[key][option]
        else:
            assert getattr(config, key) == configExpectationFormatted[key]
