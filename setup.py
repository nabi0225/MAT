import setuptools

setuptools.setup(
    name="MAT",
    version="0.0.1",
    url='https://github.com/nabi0225/MAT.git',
    packages=setuptools.find_packages(),
    package_data = {
        '': ['*.yaml','data'],
    },
    py_modules=['app'],
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
