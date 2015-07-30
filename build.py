#!/usr/bin/python

# example and test
#
import subprocess
from brick_wall_build import task

    
@task()
def test(*args):
    """
    Run unit tests.
    """
    print("yo")
