from brick_wall_build import task

tasks_run = []

@task()
def clean(input_artifacts, output_artifact):
    tasks_run.append("clean")

@task(clean)
def html(input_artifacts, output_artifact):
    'Generate HTML.'
    tasks_run.append("html")

@task(clean, ignore=True)
def images(input_artifacts, output_artifact):
    """Prepare images.

    Should be ignored."""

    raise Exception("This task should have been ignored.")

@task(clean,html,images)
def android(input_artifacts, output_artifact):
    "Package Android app."

    tasks_run.append('android')

