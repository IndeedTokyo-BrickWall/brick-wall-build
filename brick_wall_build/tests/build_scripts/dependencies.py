from brick_wall_build import task


@task()
def clean(input_artifacts, output_artifact):
    """Clean build directory."""

    print("clean")

@task(clean)
def html(input_artifacts, output_artifact):
    """Generate HTML."""
    
    print("html")

@task(clean)
def images(input_artifacts, output_artifact):
    """Prepare images."""

    print("images")

@task(clean,html,images)
def android(input_artifacts, output_artifact):
    """Package Android app."""

    print("android")

@task(clean,html,images)
def ios(input_artifacts, output_artifact):
    """Package iOS app."""

    print("ios")
    
def some_utility_method(input_artifacts, output_artifact):
    """Some utility method."""

    print("some utility method")
