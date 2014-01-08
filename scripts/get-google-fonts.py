import os, sys
import subprocess
import json


import requests

prefix = 'https://googlefontdirectory.googlecode.com/hg'

cabin_files = [
    'Cabin-BoldItalic.ttf',
    'Cabin-MediumItalic.ttf',
    'Cabin-SemiBoldItalic.ttf',
    'Cabin-Bold.ttf',
    'Cabin-Medium.ttf',
    'Cabin-SemiBold.ttf',
    'Cabin-Italic.ttf',
    'Cabin-Regular.ttf',
    'OFL.txt',]

droid_sans_files = [
    'DroidSans-Bold.ttf',
    'DroidSans.ttf',
    'LICENSE.txt',]

droid_serif_files = [
    'DroidSerif-BoldItalic.ttf',
    'DroidSerif-Italic.ttf',
    'LICENSE.txt',
    'DroidSerif-Bold.ttf',
    'DroidSerif.ttf',]

nunito_files = [
    'Nunito-Bold.ttf',
    'Nunito-Light.ttf',
    'Nunito-Regular.ttf',
    'OFL.txt',]

open_sans_files = [
    'LICENSE.txt',
    'OpenSans-LightItalic.ttf',
    'OpenSans-BoldItalic.ttf',
    'OpenSans-Light.ttf',
    'OpenSans-Bold.ttf',
    'OpenSans-Regular.ttf',
    'OpenSans-ExtraBoldItalic.ttf',
    'OpenSans-SemiboldItalic.ttf',
    'OpenSans-ExtraBold.ttf',
    'OpenSans-Semibold.ttf',
    'OpenSans-Italic.ttf',]


play_files = [
    'OFL.txt',
    'Play-Bold.ttf',
    'Play-Regular.ttf',]


questrial_files = [
    'OFL.txt',
    'Questrial-Regular.ttf',]


rambla_files = [
    'OFL.txt',
    'Rambla-Bold.ttf',
    'Rambla-Regular.ttf',
    'Rambla-BoldItalic.ttf',
    'Rambla-Italic.ttf',]

rumraisin_files = [
    'OFL.txt',
    'RumRaisin-Regular.ttf',]

sacramento_files = [
    'OFL.txt',
    'Sacramento-Regular.ttf',]

source_sans_pro_files = [
    'OFL.txt',
    'SourceSansPro-Italic.ttf',
    'SourceSansPro-BlackItalic.ttf',
    'SourceSansPro-LightItalic.ttf',
    'SourceSansPro-Black.ttf',
    'SourceSansPro-Light.ttf',
    'SourceSansPro-BoldItalic.ttf',
    'SourceSansPro-Regular.ttf',
    'SourceSansPro-Bold.ttf',
    'SourceSansPro-SemiboldItalic.ttf',
    'SourceSansPro-ExtraLightItalic.ttf',
    'SourceSansPro-Semibold.ttf',
    'SourceSansPro-ExtraLight.ttf',]

LOCALPATHS = dict(Cabin=cabin_files,
                  Droid_Sans=droid_sans_files,
                  Droid_Serif=droid_serif_files,
                  Nunito=nunito_files,
                  Open_Sans=open_sans_files,
                  Play=play_files,
                  Questrial=questrial_files,
                  Rambla=rambla_files,
                  Rum_Raisin=rumraisin_files,
                  Sacramento=sacramento_files,
                  Source_Sans_Pro=source_sans_pro_files)

UPSTREAM_DIRS = dict(Cabin='ofl/cabin',
                     Droid_Sans='apache/droidsans',
                     Droid_Serif='apache/droidserif',
                     Nunito='ofl/nunito',
                     Open_Sans='apache/opensans',
                     Play='ofl/play',
                     Questrial='ofl/questrial',
                     Rambla='ofl/rambla',
                     Rum_Raisin='ofl/rumraisin',
                     Sacramento='ofl/sacramento',
                     Source_Sans_Pro='ofl/sourcesanspro',)


def get_font(name, fontpath='trumpet/static/fonts'):
    fontdir = os.path.join(fontpath, name)
    if not os.path.isdir(fontdir):
        os.makedirs(fontdir)
    upstream_dir = os.path.join(prefix, UPSTREAM_DIRS[name])
    for basename in LOCALPATHS[name]:
        filename = os.path.join(fontdir, basename)
        if not os.path.isfile(filename):
            url = os.path.join(upstream_dir, basename)
            print "downloading", url
            r = requests.get(url)
            with file(filename, 'w') as outfile:
                outfile.write(r.content)
                
    
    
def update_fonts():
    for name in LOCALPATHS:
        get_font(name)
        

if __name__ == '__main__':
    update_fonts()
    
    
