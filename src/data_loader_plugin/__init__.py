from .base import DataLoaderBase

try:
    import importlib.metadata as mtd
    # Change here if project is renamed and does not equal the package name
    dist_name = 'data-loader-plugin'
    __version__ = mtd.version(dist_name)

except DistributionNotFound:
    __version__ = 'unknown'

