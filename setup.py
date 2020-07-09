import setuptools

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=['mat'],
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
        mat=app:cli
    ''',
    python_requires='>=3.6',
)
