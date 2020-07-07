import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=setuptools.find_packages('mat'),
    install_requires=[
        'Click',
        'confuse',
        'requests',
        'flask',
        'flask-cors',
    ],
     entry_points='''
        [console_scripts]
        mat=mat.app:cli
    ''',
    python_requires='>=3.6',
)
