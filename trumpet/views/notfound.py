from formencode.htmlgen import html
from pyramid.httpexceptions import HTTPNotFound

from menus import BaseMenu

def error_menu(request):
    menu = BaseMenu(header='Error Menu', class_='errormenu')
    menu.append(html.tr(html.td(html.p('Explanation:  ${explanation}'))))
    menu.append(html.tr(html.td(html.p('Detail:  ${detail}'))))
    menu.append_new_entry('back', request.referrer)
    menu.append_new_entry('home', request.route_url('home'))
    return menu


def NotFound(request, detail):
            menu = error_menu(request)
            return HTTPNotFound(detail=detail,
                                body_template=unicode(menu))


