import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unitparsing-pkg-mtmonacelli",
    version="0.0.1",
    author="Taylor Monacelli",
    author_email="taylormonacelli@gmail.com",
    description="Find quantities in strings based off regex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taylormonacelli/unit-parsing-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
