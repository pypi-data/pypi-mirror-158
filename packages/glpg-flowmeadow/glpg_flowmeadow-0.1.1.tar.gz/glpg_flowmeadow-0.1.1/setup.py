import os

from setuptools import find_packages, setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="glpg_flowmeadow",
    version="0.1.1",
    license='MIT',
    packages=find_packages(include=["glpg_flowmeadow", "glpg_flowmeadow.*"]),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    description="pyglet OpenGL playground",
    author="Florian Wiese",
    author_email="florian-wiese93@outlook.de",
    url="https://github.com/flowmeadow/pygletPlayground",
    download_url="https://github.com/flowmeadow/pygletPlayground.git",
    keywords=["pyglet", "OpenGL"],
)
