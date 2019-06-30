from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.path import AssetResolver


def static_asset_response(request, asset):
    resolver = AssetResolver()
    descriptor = resolver.resolve(asset)
    if not descriptor.exists():
        raise HTTPNotFound(request.url)
    path = descriptor.abspath()
    response = FileResponse(path, request)
    zip_response = False
    for ending in ['.css', '.js', '.coffee', '.html', '.ttf']:
        if path.endswith(ending):
            zip_response = True
    if zip_response:
        response.encode_content()
    for ending in ['.css', '.js']:
        # one day for css and js
        if path.endswith(ending):
            response.cache_expires(3600 * 24)
            response.cache_control.public = True
    if path.endswith('.ttf'):
        # one year for fonts
        response.cache_expires(3600 * 24 * 365)
        response.cache_control.public = True
    return response
