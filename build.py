#!/usr/bin/python

# example and test
#
import subprocess
from brick_wall_build import task, set_artifact_path, run

set_artifact_path("/usr/local/var/tst")


def other_function():
	print "other_function"
	other_function2("ere")


def other_function2(param):
	print "other_function2 " + param

@task(watched_sources = ['brick_wall_build', 'LICENSE.txt'])
def test1(input_artifacts, output_artifact):
    run("echo test")



@task(test1, watched_sources = ['README.md'])
def test2(input_artifacts, output_artifact, param=''):
    run("echo test2 param=" + param)
    other_function()


@task()
def test(input_artifacts, output_artifact, *args):
    """
    Run unit tests.
    """
    run("py.test-2.7")

