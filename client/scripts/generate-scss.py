import os, sys

jquery_ui_template = """\
@import "partials/basecolors/%(basecolor)s";
@import "partials/jq-ui-theme";
@include jquery-ui-base-theme;
"""

bootstrap_template = """\
@import "partials/basecolors/%(basecolor)s";
@import "partials/bootstrap-variables";
@import "partials/bootstrap-custom";
@import "partials/bootstrap-widgets";
"""

screen_template = """\
@import "partials/basecolors/%(basecolor)s";
@import "partials/base";
@import "partials/misc";
@import "partials/page";
"""

TEMPLATES = dict(jqueryui=jquery_ui_template,
                 bootstrap=bootstrap_template,
                 screen=screen_template)


BASECOLORS = ['darkseagreen', 'light-plum', 'lightskyblue',
              'deep-pink', 'azure3', 'light-steel-blue',
              'white-smoke', 'darkkhaki', 'mistyrose3',
              'wheat4', 'easter']

def generate_scss(basecolor, name, template):
    filename = '%s-%s.scss' % (name, basecolor)
    path = os.path.join('sass', filename)
    env = dict(basecolor=basecolor)
    with file(path, 'w') as o:
        o.write(template % env)
        
        

def generate_all_scss(basecolors):
    for basecolor in basecolors:
        for name, template in TEMPLATES.items():
            generate_scss(basecolor, name, template)

    # prepare font-awesome
    with file('sass/font-awesome.scss', 'w') as o:
        o.write('@import "partials/fontawesome/font-awesome";\n')
        
            
if __name__ == '__main__':
    generate_all_scss(BASECOLORS)
    
    
    
