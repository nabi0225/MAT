import setuptools

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=setuptools.find_packages(exclude=['config.yaml', 'data']),
    package_data={'mat': ['config.yaml', 'data']},
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
