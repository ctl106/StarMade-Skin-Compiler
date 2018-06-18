#!/usr/bin/env python3

import argparse
import os       # for getcwd() and path
import sys      # for stderr
import time
import __main__

import smsctext
import starmade.Skin

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = []
        items.extend(values)
        setattr(namespace, self.dest, items)


def starts_with(s, start):
    return (start is None) or (s.startswith(start))

def ends_with(s, end):
    return (end is None) or (s.endswith(end))


def build_skins(bodies, body_ems, helmets, helmet_ems):
    textures = match_textures(bodies, body_ems, helmets, helmet_ems)
    output = {}
    
    for texture in textures:
        # body_em and helmet_em textures are optional
        if not texture[1]:
            texture[1] = get_default_body_em()
        if not texture[3]:
            texture[3] = get_default_helmet_em()
        
        # body and helmet textures are required
        if texture[0] and texture[2]:
            name = generate_name(texture)
            output[name] = starmade.Skin(
                texture[0],
                texture[1],
                texture[2],
                texture[3]
                )
            
    return output

def catch_bad_args(args):
    for path in args.paths:
        if not os.path.isdir(path):
            perror("No such directory \"" + path + "\".")
            exit()
    if args.dest and not os.path.isdir(args.dest[-1]):
        #perror("No such directory \"" + os.path.abspath(args.dest[-1]) + "\".")
        os.makedirs(args.dest[-1])
        exit()

def compile_skins(output, skins): 
    if len(skins):
        dir = None
        if output:
            dir = output[-1]
        else:
            dir = os.getcwd()
        
        for name in skins:
            path = os.path.join(dir, name)
            skins[name].compile(path)
    else:
        perror("No correctly named combinations of skins were found.")

def do_names_match(lst):
    output = True

    if len(lst[1:]):
        name = os.path.split(lst[0])[1].split("-")[0]

        i=1
        while(i<len(lst) and lst[i] is None):
            i+=1

        if not (lst[i] is None or starts_with(os.path.split(lst[i])[1], name)):
            output = False
            
    return output

def find_matching_files(location, begin=None, end=None):
    files = []
    for item in os.listdir(location):
        path = os.path.join(location, item)
        if os.path.isfile(path) and \
                starts_with(item, begin) and \
                ends_with(item, end):
            files.append(path)
    
    return files

def generate_variation(var1, var2):
    words = var1.split("_") + var2.split("_")
    unique_words = list(dict.fromkeys(words))
    combo_var = "_".join(unique_words)
    if combo_var[0] == "_": combo_var = combo_var[1:]
    return combo_var

def generate_name(texture):
    body = os.path.split(texture[0])[1]
    helmet = os.path.split(texture[2])[1]
    
    base_index = body.find("-")+1
    body_var_index = body.rfind(smsctext.body_end)
    helm_var_index = helmet.rfind(smsctext.helmet_end)
    
    name_base = body[:base_index]
    body_variation = body[base_index:body_var_index]
    helm_variation = helmet[base_index:helm_var_index]
    name_variation = generate_variation(body_variation, helm_variation)
    return name_base + name_variation + smsctext.ext

def get_default_body_em():
    module_dir = os.path.split(__main__.__file__)[0]
    defaults_dir = "defaults"
    body_em = "default-body_em.png"
    return os.path.join(module_dir, defaults_dir, body_em)

def get_default_helmet_em():
    module_dir = os.path.split(__main__.__file__)[0]
    defaults_dir = "defaults"
    helmet_em = "default-helmet_em.png"
    return os.path.join(module_dir, defaults_dir, helmet_em)

def make_parser():
    parser = argparse.ArgumentParser(
        description = smsctext.help,
        epilog = smsctext.subhelp,
        prefix_chars = smsctext.prefixchars,
        formatter_class = argparse.RawTextHelpFormatter
        )

    parser.register('action', 'list', ListAction)

    parser.add_argument(    # support windows-style flags
        smsctext.help_win_short,
        smsctext.help_win_long,
        action = "help",
        help = argparse.SUPPRESS
        )

    parser.add_argument(
        "paths",
        metavar = "source",
        nargs = "*",
        action = "list",
        default = [os.getcwd()],
        help = smsctext.paths_arg
        )

    parser.add_argument(
        smsctext.recursive_short,
        smsctext.recursive_long,
        dest = "recursive",
        action = "store_true",
        help = smsctext.recursive_arg
        )

    parser.add_argument(    # support windows-style flags
        smsctext.recursive_win_short,
        smsctext.recursive_win_long,
        dest = "recursive",
        action = "store_true",
        help = argparse.SUPPRESS
        )
    
    parser.add_argument(
        smsctext.time_short,
        smsctext.time_long,
        dest = "time",
        action = "store_true",
        help = smsctext.time_arg
        )

    parser.add_argument(    # support windows-style flags
        smsctext.time_win_short,
        smsctext.time_win_long,
        dest = "time",
        action = "store_true",
        help = argparse.SUPPRESS
        )

    parser.add_argument(
        smsctext.output_short,
        smsctext.output_long,
        nargs = 1,
        dest = "dest",
        help = smsctext.output_arg
        )

    parser.add_argument(    # support windows-style flags
        smsctext.output_win_short,
        smsctext.output_win_long,
        nargs = 1,
        dest = "dest",
        help = argparse.SUPPRESS
        )

    return parser

def match_textures(*args):
    output = []
    
    if len(args):
        matches = match_textures(*args[1:])
        matches_c = matches.copy()
        for item in args[0]:
            temp_output = []
            
            for match in matches:
                if do_names_match([item]+match):
                    temp_output.append([item]+match)
                    if match in matches_c: matches_c.remove(match)
            
            if not len(temp_output):
                output.append([item]+[None]*len(args[1:]))
            else:
                output += temp_output

        # ungrouped matches should be grouped with None
        output += [[None]+match for match in matches_c]

    return output

def perror(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

def search_for_skins(paths, recursive=False):
    skins = {}
    for path in paths: skins.update(skins_from_path(path, recursive))
    return skins

def skins_from_path(path, recursive=False):
    bodies = find_matching_files(path, end=smsctext.body_end)
    body_ems = find_matching_files(path, end=smsctext.body_em_end)
    helmets = find_matching_files(path, end=smsctext.helmet_end)
    helmet_ems = find_matching_files(path, end=smsctext.helmet_em_end)

    skins = build_skins(bodies, body_ems, helmets, helmet_ems) 
    
    if recursive:
        for name in os.listdir(path):
            branch = os.path.join(path, name)
            if os.path.isdir(branch):
                 skins.update(skins_from_path(branch, recursive))
                 
    return skins


def main():
    args = make_parser().parse_args()
    catch_bad_args(args)

    if args.time: begin_search = time.time()
    skins = search_for_skins(args.paths, args.recursive)
    
    if args.time: begin_compile = time.time()
    compile_skins(args.dest, skins)

    if args.time:
        finish = time.time()
        print("Search time:\t" + str(begin_compile-begin_search) + " s")
        print("Compile time:\t" + str(finish-begin_compile) + " s")
        print("Total time elapsed:\t" + str(finish-begin_search) + " s")

if __name__ == "__main__":
    main()
