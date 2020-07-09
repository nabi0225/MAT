import setuptools

setuptools.setup(
    name="MAT",
    version="0.0.1",
    url='https://github.com/nabi0225/MAT.git',
    packages=setuptools.find_packages('mat'),
    include_package_data=True,
    py_modules=['mat'],
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
