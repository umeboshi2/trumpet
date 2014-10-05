import os

def add_static_views(config, settings):
    #config.add_static_view(name='client',
    #                       path=settings['static_assets_path'])
    assets_path = settings['static_assets_path']
    assets = settings['static_assets'].strip().split('\n')
    for asset in assets:
        config.add_static_view(name=asset,
                               path=os.path.join(assets_path, asset))
    
