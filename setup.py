from setuptools import setup, Command
import brick_wall_build

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name="brick_wall_build",
    version= brick_wall_build.__version__,
    author="Artem Onuchin",
    author_email="onuchinart@gmail.com",
    url= brick_wall_build.__contact__, 
    cmdclass = {'test': PyTest},
    packages=["brick_wall_build"],
    entry_points =  {'console_scripts': ['brick_wall_build=brick_wall_build:main']}, 
    license="MIT License",
    description="Lightweight Python Build Tool.",
    long_description="A hack of Pynt for https://github.com/IndeedTokyo-BrickWall/BrickWall project",
    install_requires=['cuisine'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7'],

)
