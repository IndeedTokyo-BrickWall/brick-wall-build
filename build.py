#!/usr/bin/python

# example and test
#
import subprocess
from brick_wall_build import task
  
@task()
def test(input_artifacts, output_artifact, ry):
    """
    Run unit tests.
    """
    print("a_variable")
