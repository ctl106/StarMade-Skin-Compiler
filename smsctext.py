import textwrap

prefixchars = "-/"

# texture files

body_end = "-body.png"
body_em_end = "-body_em.png"
helmet_end = "-helmet.png"
helmet_em_end = "-helmet_em.png"

ext = ".smskin"

# flags
help_win_short = "/h"
help_win_long = "/help"
recursive_short = "-r"
recursive_win_short = "/r"
recursive_long = "--recursive"
recursive_win_long = "/recursive"
output_short = "-o"
output_win_short = "/o"
output_long = "--out"
output_win_long = "/out"
time_short = "-t"
time_win_short = "/t"
time_long = "--time"
time_win_long = "/time"


# help strings

help = "Automatically compile textures into StarMade skin (.smskin) files."

subhelp = (textwrap.fill(
    "This application searches for a required body and helmet textures and "
    "optional body emissions and helmet emissions textures."
    , width = 79)
    + "\n\n" +
    textwrap.fill(
    "In order for this application to correctly identify and associate "
    "the textures with each other, the associated textures must be in the "
    "same directory and be named with the following convention:"
    , width = 79)
    + ("\n"
    "\tskin_name-skin_variation-texture.png\n\n"
    "Where:\n"
    "\tskin_name\t-\tthe constant part of the skin name\n"
    "\tskin_variation\t-\tthe variation of the texture\n"
    "\ttexture\t-\tidentifies which of the texture files:\n"
    "\t\t" + body_end[1:] + ", " + body_em_end[1:] + ", "
    + helmet_end[1:] + ", " + helmet_em_end[1:] +
    "\n\n") +
    textwrap.fill(
    "When "
    +recursive_short+
    "/"
    +recursive_long+
    " is enabled, textures will only be matched within the same directory "
    "and not across different directories."
    , width = 79)
    )


# arguments help messages

paths_arg = "where to search for texture files to compile"

recursive_arg = (
    "recursively search for textures"
    )

output_arg = "where to store the resulting StarMade skin file(s)"

time_arg = "calculate time elapsed searching and compiling skins"
