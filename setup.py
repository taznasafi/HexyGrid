try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'name': 'HexyGridMaker',
	'description': 'This Tool creates H3 grids based on Roads',
	'author': "Murtaza NASAFI",
	'e-mail': "murtaza.nasafi@fcc.gov",
	'version': '0.1dev',
	'license': 'Creative Commons Attribution-Noncommercial-Share Alike license',
	'install_requires': ['nose', 'arcpy', 'pandas', 'numpy', 'zipfile',
						 'shutil', 'fnmatch', 'geopandas', 'contextily', 'cenpy',
						 'shapely', 'fiona', 'h3', 'setuptools', 'multiprocessing'],
	'packages': ['tests', 'Hexy', 'bin',]

}

setup(**config)