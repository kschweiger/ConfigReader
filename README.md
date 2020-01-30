# ConfigReader

Utility module for interfacing with configparser.

After writing very similar interfaces to work with config files that are intended to be processed with the configparser module multiple times, I decided to move this to a repository so I have a central place for it.

Implements utility to deal with formatting in config files:

```
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
```

1. Read lists: `section2`, `ListOption` interpret `,` in string as list elements
2. Multiple lines: Implements options that span over mutliple lines and are separate by a separationg char (default is ` : `)
3. Interpret lines in multiline options as lists (see 1.)

Additionally a function for getting option with default valuesis implemented.

## AutoConfigReader

Read a config file and saves a dict with all option for each section as class attributed with name section. Section can also be exlcuded (if a child class need to implement special behaviour for certain section) and a section can be specified for which the options will be set as class attributions directly, e.g. if all options in a `General` section should be direct class attributes instead of elements in a dict called `AutoConfigReader.General`.
