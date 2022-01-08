from setuptools import setup, find_packages

with open("requirements.txt", "r") as infile:
    requirements = [i.strip() for i in infile.readlines()]

with open("VERSION", "r") as infile:
    version = infile.read().strip()

with open("README.md", "r") as infile:
    long_description = infile.read()

setup(
    name="eero-adguard-sync",
    version=version,
    author="Andrew Mickael",
    author_email="andrew.mickael@gmail.com",
    description="Sync Eero DHCP client list to AdGuard Home",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amickael/eero-adguard-sync",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["eag-sync=eero_adguard_sync.__main__:cli"],
    },
    python_requires=">=3.7",
    include_package_data=True,
)
