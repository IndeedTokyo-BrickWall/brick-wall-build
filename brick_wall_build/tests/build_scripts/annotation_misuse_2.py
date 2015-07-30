from brick_wall_build import task

@task()
def clean():
    pass
    
# Should be marked as task.
def html():
    pass

# References a non task.
@task(clean,html)
def android():
    pass
