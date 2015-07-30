#!/usr/bin/python

from brick_wall_build import task

tasks_run = []
    
@task()
def clean(input_artifacts, output_artifact,directory='/tmp'):
    tasks_run.append('clean[%s]' % directory)

    
@task(clean)
def html(input_artifacts, output_artifact):
    tasks_run.append('html')


@task()
def tests(input_artifacts, output_artifact, *test_names):
    tasks_run.append('tests[%s]' % ','.join(test_names))


@task(clean)
def copy_file(input_artifacts, output_artifact, from_, to, fail_on_error='True'):
    tasks_run.append('copy_file[%s,%s,%s]' % (from_, to, fail_on_error))


@task(clean)
def start_server(input_artifacts, output_artifact, port='80', debug='True'):
    tasks_run.append('start_server[%s,%s]' % (port, debug))

@task(ignore=True)
def ignored(input_artifacts, output_artifact, file, contents):
    tasks_run.append('append_to_file[%s,%s]' % (file, contents))

@task(clean, ignored)
def append_to_file(input_artifacts, output_artifact, file, contents):
    tasks_run.append('append_to_file[%s,%s]' % (file, contents))

    
@task(ignored)
def echo(input_artifacts, output_artifact, *args,**kwargs):
    args_str = []
    if args:
        args_str.append(','.join(args))
    if kwargs:
        args_str.append(','.join("%s=%s" %  (kw, kwargs[kw]) for kw in sorted(kwargs)))

    tasks_run.append('echo[%s]' % ','.join(args_str))
