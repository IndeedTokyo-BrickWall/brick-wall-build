from setuptools import setup
import brick_wall_build
setup(
    name="brick_wall_build",
    version= brick_wall_build.__version__,
    author="Artem Onuchin",
    author_email="onuchinart@gmail.com",
    url= brick_wall_build.__contact__, 
    packages=["brick_wall_build"],
    entry_points =  {'console_scripts': ['brick_wall_build=brick_wall_build:main']}, 
    license="MIT License",
    description="Lightweight Python Build Tool.",
    long_description="A hack of Pynt for https://github.com/IndeedTokyo-BrickWall/BrickWall project"
)
