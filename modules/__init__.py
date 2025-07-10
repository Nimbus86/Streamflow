import os
from importlib import import_module

def register_modules(app):
    modules_dir = os.path.dirname(__file__)
    for name in os.listdir(modules_dir):
        mod_path = os.path.join(modules_dir, name)
        # pak alleen echte module-mappen, geen __pycache__ enz.
        if os.path.isdir(mod_path) and name not in ['__pycache__']:
            try:
                routes = import_module(f'modules.{name}.routes')
                bp = getattr(routes, 'bp', None)
                if bp:
                    app.register_blueprint(bp, url_prefix=f'/{name}')
                    print(f'Registered module: {name}')
            except ImportError as e:
                print(f'Failed to register {name}:', e)
