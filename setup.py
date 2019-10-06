import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="straw",
    version="0.0.1",
    author="Meng-Hsin Tung",
    author_email="itswindtw@gmail.com",
    description="Object mapping at ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itswindtw/straw",
    packages=setuptools.find_packages(exclude=('tests')),
    install_requires=['dateutil']
)
