import setuptools

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=setuptools.find_packages(),
    package_data={
        'data': ['data/*.json'],
        '': ['*.yaml'],
    },
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
