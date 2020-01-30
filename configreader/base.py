import configparser
import logging


class ConfigReaderBase:
    """
    Base class for configreader.

    Args:
      pathtoConfig (str) : Path to config file, that would be opened with the python configparser module

    Attributes:
      readConfig (configparser.ConfigParser)
      path (str) : Original path to the config
    """
    def __init__(self, pathtoConfig):
        logging.info("Loading config %s", pathtoConfig)
        thisconfig = self.readConfig(pathtoConfig)
        self.readConfig = thisconfig
        self.path = pathtoConfig

    def readConfig(self, pathtoConfig):
        """
        Create and load the configparser object.
        """
        thisconfig = configparser.ConfigParser()
        thisconfig.optionxform = str  # Use this so the section names keep Uppercase letters
        thisconfig.read(pathtoConfig)

        return thisconfig

    def readMulitlineOption(self, section, thisOption, optionType, sep=" : "):
        """
        Read option (thisOption) in a section (section) that has multiple lines where option and value are separated with sep

        Args:
          section (str) : Section
          thisOption (str) : Option
          optionType (str) : Single: Full line after sep is treated as value. List: Line will be split at ,
          sept (str) : Separator between option and value

        Raises:
          RuntimeError : Raised if optionType is not Single or List
        """
        ret = {}
        option = self.readConfig.get(section, thisOption)
        for elem in option.split("\n"):
            if elem == "":
                continue
            if optionType == "Single":
                name, value = elem.split(sep)
            elif optionType == "List":
                name, value = elem.split(sep)
                value = self.getList(value)
            else:
                raise RuntimeError
            logging.debug("Found: %s = %s", name, value)
            ret[name] = value

        return ret

    def setOptionWithDefault(self, section, option, default, getterType="str"):
        """
        Wrapper for configparser.ConfigParser.get() that inserts default value if option is not available.

        Args:
          section (str) : Section
          option (str) : Option
          default (any type) : Default value that will be returned of option is not available.
                               If None is passed and the option is present and is "None", None will be returned
          getterType (str) : What value is expected to be read (float, int, bool, intlist, list, str)
        """
        if self.readConfig.has_option(section, option):
            if getterType == "float":
                return self.readConfig.getfloat(section, option)
            elif getterType == "int":
                return self.readConfig.getint(section, option)
            elif getterType == "bool":
                return self.readConfig.getboolean(section, option)
            elif getterType == "intlist":
                return [int(x) for x in self.getList(self.readConfig.get(section, option))]
            elif getterType == "list":
                return self.getList(self.readConfig.get(section, option))
            else:
                if default is None and self.readConfig.get(section, option) == "None":
                    return None
                else:
                    return self.readConfig.get(section, option)
        else:
            return default

    def getListOption(self, section, option):
        """
        Interpret the option (option) in section (section) as komma separated list

        Args:
          section (str) : Section
          option (str) : Option
        """
        return self.getList(self.readConfig.get(section, option))

    @staticmethod
    def getList(value):
        value = value.replace(" ", "")
        return value.split(",")


class AutoConfigReader(ConfigReaderBase):
    """
    Configreader, that automatically set section as attributes of the ConfigReader object

    Args:
      pythtoConfig (str) : Path the config file
      multilineSep (str) : Separator for multiline option (see ConfigReaderBase.readMulitlineOption)
      toplevelSection (str) : If string is passed, the options in this section will become class attributes
      exclude (str, list) : Passed string and will be checked against section and if present excluded

    Raises:
      TypeError : Raised if passed exclude is not str or list
      RuntimeError : Raised if at least one element in exclude is no section
    """
    def __init__(self, pathtoConfig, multilineSep=" : ", toplevelSection=None, exclude=[]):
        if not (isinstance(exclude, str) or isinstance(exclude, list)):
            raise TypeError("exclusion is required to be str or list bit is %s"%(type(exclude)))

        if isinstance(exclude, str):
            exclude = [exclude]

        super().__init__(pathtoConfig)

        for excludeSection in exclude:
            if excludeSection not in self.readConfig.sections():
                raise RuntimeError("Section %s was passed for excludion but is not in config file"%(excludeSection))

        for section in self.readConfig.sections():
            if section in exclude:
                continue
            thisSection = {}
            for option in self.readConfig[section]:
                value = self.readConfig.get(section, option)
                if "\n" in value:
                    if "," in value:
                        optionType = "List"
                    else:
                        optionType = "Single"
                    thisSection[option] = self.readMulitlineOption(section,
                                                                   option,
                                                                   optionType,
                                                                   multilineSep)
                elif "," in value:
                    thisSection[option] = self.getList(value)
                else:
                    thisSection[option] = value
            if toplevelSection == section:
                for option in thisSection:
                    setattr(self, option, thisSection[option])
            else:
                setattr(self, section, thisSection)
