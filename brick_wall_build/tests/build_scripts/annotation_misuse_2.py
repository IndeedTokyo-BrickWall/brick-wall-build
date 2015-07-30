from brick_wall_build import task

@task()
def clean(input_artifacts, output_artifact):
    pass
    
# Should be marked as task.
def html(input_artifacts, output_artifact):
    pass

# References a non task.
@task(clean,html)
def android(input_artifacts, output_artifact):
    pass
