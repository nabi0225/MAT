import setuptools
from glob import glob

data = glob('data')
config = glob('config.yaml')

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'confuse',
        'requests',
        'flask',
        'flask_cors',
    ],
    entry_points='''
        [console_scripts]
        mat=mat.app:cli
    ''',
)
