from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AnimeIA",
    version="0.1",
    author="Rafael Guevara",
    packages=find_packages(),
    install_requires = requirements,
)