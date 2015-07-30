from brick_wall_build import task

@task()
def clean(input_artifacts, output_artifact):
    pass
    
# Referring to clean by name rather than reference.
@task(1234)
def html(input_artifacts, output_artifact):
    pass
