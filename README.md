# ConfigReader

Utility module for interfacing with configparser.

After writing very similar interfaces to work with config files that are intended to be processed with the configparser module, I decided to move this to a repository so I have a central place for it.


Implements utility for advanced formatiing of config files:

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
2. Multiple lines: Implements otpions that spans over mutliple lines and is separate by a separationg char (default is `:`)
3. Interpret lines in multiline options as lists (see 1.)

Additionally a function for option calls with default value is implemented
