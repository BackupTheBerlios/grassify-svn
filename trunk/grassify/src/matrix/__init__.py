def name():
    return "grassify plugin"

def description():
    return "archeological stratigraphy in qgis"

def version():
    return "Version 0.1"

def classFactory(iface):
    # load parser class from file GrassifyPlugin.py
    from GrassifyPlugin import *

    return GrassifyPlugin(iface)
