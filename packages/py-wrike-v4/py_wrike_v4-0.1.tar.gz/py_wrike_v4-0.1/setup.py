from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="py_wrike_v4",
    version="0.1",
    license="MIT",
    author="Govinda Hosein",
    author_email="raziel619dev@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/Raziel619/py_wrike_v4",
    keywords="wrike",
    install_requires=required,
)
