import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="MAT",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'confuse',
        'requests',
        'flask',
        'flask-cors',
        'shutil',
        'yaml',
        'os',
    ],
     entry_points='''
        [console_scripts]
        mat=app:cli
    ''',
    python_requires='>=3.6',
)
