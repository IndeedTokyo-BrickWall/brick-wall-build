#!/usr/bin/python

from brick_wall_build import task


@task()
def clean(input_artifacts, output_artifact):
    """Clean build directory."""

    print("clean")

@task()
def html(input_artifacts, output_artifact):
    """Generate HTML."""
    
    print("html")

@task()
def images(input_artifacts, output_artifact):
    """Prepare images."""

    print("images")

@task()
def android(input_artifacts, output_artifact):
    """Package Android app."""

    print("android")

@task()
def ios(input_artifacts, output_artifact):
    """Package iOS app."""

    print("ios")
    
def some_utility_method(input_artifacts, output_artifact):
    """Some utility method."""

    print("some utility method")

__DEFAULT__ = ios