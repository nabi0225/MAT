import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MAT",
    version="0.0.1",
    #  py_modules=['MAT'],
    # author="Marco",
    # author_email="marco_li@paradise-soft.com.tw",
    # description="MAT",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
    ],
     entry_points='''
        [console_scripts]
        mat=app:cli
    ''',
    python_requires='>=3.6',
)