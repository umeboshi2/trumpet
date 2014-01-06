#!/usr/bin/env python
import os, sys

from chert.path import path

skippable_suffixes = ['pyc', '~', '#',
                      '.gz', '.bz2',
                      '.ico', '.png', '.jpg',
                      '.sqlite']

skippable_directories = ['.git']

def tmpl_name(filename):
    basename = filename.basename()
    return '%s_tmpl' % basename

def is_skippable(fullpath):
    if 'sass/partials' in fullpath:
        return True
    for dirname in skippable_directories:
        if fullpath.startswith(dirname):
            return True
    for suffix in skippable_suffixes:
        if fullpath.endswith(suffix):
            return True
    return False



def main():
    here = path.getcwd()

    for fullpath in here.walkfiles():
        if is_skippable(fullpath):
            continue
        
        relpath = fullpath.relpath()
        tmpl = path(tmpl_name(relpath))
        tname = fullpath.dirname() / tmpl
        if not tname.exists():
            fullpath.symlink(tname)
        
    
