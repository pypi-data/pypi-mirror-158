import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name="GPSDO",
    version="0.1.0",
    url="https://www.qsl.net/zl3dw/",
    author="Andrew Barron",
    author_email="zl3dw@outlook.co.nz",
    description="A GPSDO experiment",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)