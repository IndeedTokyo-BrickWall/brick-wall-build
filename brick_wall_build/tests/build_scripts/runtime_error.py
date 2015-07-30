"""
Build script with a runtime error.
"""
from brick_wall_build import task


@task()
def images(input_artifacts, output_artifact):
    """Prepare images. Raises IOError."""
    global ran_images
    ran_images = True
    raise IOError

@task(images)
def android(input_artifacts, output_artifact):
    """Package Android app."""
    global ran_android
    print("android")
    ran_android = True

