#!/usr/bin/python

# example and test
#
import subprocess
from brick_wall_build import task, set_artifact_path, run, artifact_path

set_artifact_path("/usr/local/var/tst")


def other_function():
	print artifact_path("test1", "test-dir", "test1.tsv")
	print artifact_path("test2", "test-dir", "test2.tsv")
	print artifact_path("test1")
	print artifact_path("test2")

	other_function2("ere")


def other_function2(param):
	print "other_function2 " + param


@task(watched_sources = ['brick_wall_build', 'LICENSE.txt'])
def test1():
    run("echo test")

@task(test1)
def test3():
    run("echo test3")

@task(test1, watched_sources = ['README.md'])
def test2(param=''):
    run("echo test2 param=" + param)
    other_function()

