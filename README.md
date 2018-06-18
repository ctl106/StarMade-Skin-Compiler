# StarMade-Skin-Compiler
###### A Python 3 script for automatically compiling collections of skin textures into StarMade .smskin files.
------

### Flags
[Recursion: `-r/--recursive`](#recursive-usage)

[Specify Output Directory: `-o/--output OUTPUT`](#specify-output-directory)

[Calculate Execution Time: `-t/--time`](#time)

[Request Help: `-h/--help`](#help)

------


### Basic Usage
For basic usage of this script, have a body texture file and helmet texture file as well as an optional body emissions file and helmet emissions file.

These files must be named in the following convention:
`skin_name-skin_variation-texture.png`

##### Where:
`skin_name` - the constant part of the skin name

`skin_variation` - the variation of the texture

`texture` - identifies which of the texture files; this must be one of the below

##### texture:
`-body`

`-body_em`

`-helmet`

`-helmet_em`

Then, the program can be run in the directory containing the textures.
```bash
smsc
```
And a file with the name `skin_name.smskin` will be created.
###### Note: Depending on your OS, you may need to use `smsc.py` or `python3 smsc.py` if `.py` is not recognized as a runnable file format.


### Recursive Usage
Depending on your workflow, you may sometimes wish to run this from a parent directory to the one containing the texture or you may want to compile textures seperated in many different directories at once. To accomplish this, this script can also recursively search directories to find associated textures.
```bash
smsc -r
```

### Specify Output Directory
Additionally, it can be useful to store the resulting skin files in a seperate directory from the one in which the script is being run.
```bash
smsc -o OUTPUT
```
Where `OUTPUT` is an absolute or relative directory for the `.smskin` files to be stored.

###### Note: There is an issue in my current test environment where the directory willl be created if it does not already exist, but the .smskin files are not created and stored in this directory. It is recommended to make sure the directory `OUTPUT` already exists before running.

### MISC
##### Time
Another ability is to request execution time in seconds.
```bash
smsc -t
```
This will print out the time taken to search and compile the skins, as well as total execution time.

##### Help
This should go without saying, but help can be requested from the script.
```bash
smsc -h
```
