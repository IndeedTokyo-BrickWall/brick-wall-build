#!/usr/bin/python

import subprocess
from brick_wall_build import task

    
@task()
def test(*args):
    """
    Run unit tests.
    """
    subprocess.call(["py.test-2.7"] + list(args))
