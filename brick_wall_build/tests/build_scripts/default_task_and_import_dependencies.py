#!/usr/bin/python

from brick_wall_build import task

from brick_wall_build.tests.build_scripts.simple import *
from brick_wall_build.tests.build_scripts import build_with_params

tasks_run = []

@task()
def local_task(input_artifacts, output_artifact):
    tasks_run.append('local_task')
    

@task(clean, build_with_params.html, local_task)
def task_with_imported_dependencies(input_artifacts, output_artifact):
    tasks_run.append('task_with_imported_dependencies')

__DEFAULT__ = task_with_imported_dependencies