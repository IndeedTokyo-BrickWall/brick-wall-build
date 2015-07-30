import pytest
import re
from brick_wall_build import _brick_wall_build, main, set_tmp_path, set_artifact_path
import sys
if sys.version.startswith("3."):
    from io import StringIO as SOut
else:
    from StringIO import StringIO as SOut

import os
from os import path
import imp
import cuisine
cuisine.mode_local()
cuisine.dir_remove('datasets')
cuisine.dir_ensure('datasets')
set_tmp_path("/tmp")
set_artifact_path("./datasets")


def fpath(mod):
    return path.splitext(mod.__file__)[0] + '.py'

    
def simulate_dynamic_module_load(mod):
    file_path = fpath(mod)
    dynamically_loaded_mod = imp.load_source(path.splitext(path.basename(file_path))[0], file_path)
    return dynamically_loaded_mod

def reset_build_file(mod):
    mod.tasks_run = []
def build(mod, params=None, init_mod = reset_build_file):
    dynamically_loaded_mod = simulate_dynamic_module_load(mod)
    dynamically_loaded_mod.tasks_run = []
    sys.argv = ['brick_wall_build', '-f', fpath(mod)] + (params or [])
    main()
    return dynamically_loaded_mod

class TestParseArgs:

    def test_parsing_commandline(self):
        cuisine.dir_remove('datasets')

        args = _brick_wall_build._create_parser().parse_args(['-f', "foo.py", "task1", "task2"])
        assert "foo.py" == args.file
        assert not args.list_tasks
        assert ['task1', 'task2'] == args.tasks

    def test_parsing_commandline_help(self):
        cuisine.dir_remove('datasets')
        assert _brick_wall_build._create_parser().parse_args(["-l"]).list_tasks
        assert _brick_wall_build._create_parser().parse_args([ "--list-tasks"]).list_tasks

    def test_parsing_commandline_build_file(self):
        cuisine.dir_remove('datasets')
        assert "some_file" == _brick_wall_build._create_parser().parse_args(["-f", "some_file"]).file
        assert "build.py" == _brick_wall_build._create_parser().parse_args([]).file
        assert "/foo/bar" == _brick_wall_build._create_parser().parse_args(
            ["--file", "/foo/bar"]).file
        
        
        with pytest.raises(SystemExit):
            _brick_wall_build._create_parser().parse_args(["--file"])
        with pytest.raises(SystemExit):
            _brick_wall_build._create_parser().parse_args(["-f"])

class TestBuildSimple:
        
    def test_get_tasks(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import simple
        ts = _brick_wall_build._get_tasks(simple)
        assert len(ts) == 5
        
class TestBuildWithDependencies:
        
    def test_get_tasks(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import dependencies
        tasks = _brick_wall_build._get_tasks(dependencies)
        assert len(tasks) == 5
        assert 3 == len([task for task in tasks if task.name == 'android'][0].dependencies)
        assert 3 == len([task for task in tasks if task.name == 'ios'][0].dependencies)

    def test_dependencies_for_imported(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import default_task_and_import_dependencies
        tasks = _brick_wall_build._get_tasks(default_task_and_import_dependencies)
        assert 7 == len(tasks)
        assert [task for task in tasks if task.name == 'clean']
        assert [task for task in tasks if task.name == 'local_task']
        assert [task for task in tasks if task.name == 'android']
        assert 3 == len([task for task in tasks
                         if task.name == 'task_with_imported_dependencies'][0].dependencies)
        

    def test_dependencies_that_are_imported_e2e(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import default_task_and_import_dependencies
        def mod_init(mod):
            mod.tasks_run = []
            mod.build_with_params.tasks_run = []
        module = build(default_task_and_import_dependencies,
                       ["task_with_imported_dependencies"], init_mod = mod_init)
        assert module.tasks_run == ['local_task', 'task_with_imported_dependencies']
        assert module.build_with_params.tasks_run == ['clean[/tmp]', 'html']

        
class TestDecorationValidation:

    def test_task_without_braces(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(Exception) as exc:
            from .build_scripts import annotation_misuse_1
        assert 'Replace use of @task with @task().' in str(exc.value)

    def test_dependency_not_a_task(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(Exception) as exc:
            from .build_scripts import annotation_misuse_2
        assert re.findall('function html.* is not a task.', str(exc.value))

    def test_dependency_not_a_function(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(Exception) as exc:
            from .build_scripts import annotation_misuse_3
        assert '1234 is not a task.' in str(exc.value)


import contextlib
@contextlib.contextmanager
def mock_stdout():
    oldout, olderr =  sys.stdout,  sys.stderr
    try:
        out = [SOut(),  SOut()]
        sys.stdout, sys.stderr =  out
        yield out
    finally:
        sys.stdout, sys.stderr =  oldout,  olderr
        out[0] =  out[0].getvalue()
        out[1] =  out[1].getvalue()
                                                                                
        
class TestOptions:

    @pytest.fixture
    def module(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import options as module
        self.docs = {'clean': '', 'html': 'Generate HTML.',
                     'images': '''Prepare images.\n\nShould be ignored.''',
                     'android': 'Package Android app.'}
        return module
        
    def test_ignore_tasks(self, module):
        cuisine.dir_remove('datasets')
        module = build(module,["android"])
        assert ['clean', 'html', 'android'] == module.tasks_run

    def test_docs(self, module):
        cuisine.dir_remove('datasets')
        tasks = _brick_wall_build._get_tasks(module)
        assert 4 == len(tasks)
        
        for task_ in tasks:
            assert task_.name in self.docs
            assert self.docs[task_.name] == task_.doc

    @pytest.mark.parametrize('args', [['-l'], ['--list-tasks'], []])
    def test_list_docs(self, module, args):
        cuisine.dir_remove('datasets')
        with mock_stdout() as out: 
            build(module,args)
        stdout = out[0]
        tasks = _brick_wall_build._get_tasks(module)
        for task in tasks:
            if task.ignored:
                assert re.findall('%s\s+%s\s+%s' % (task.name,"\[Ignored\]", task.doc), stdout)
            else:
                assert re.findall('%s\s+%s' % (task.name, task.doc), stdout)
            

            
class TestRuntimeError:

    def test_stop_on_exception(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import runtime_error as re
        with pytest.raises(IOError):
            build(re,["android"])
        mod = simulate_dynamic_module_load(re)
        assert mod.ran_images
        assert not hasattr(mod, 'ran_android')
        
    def test_exception_on_invalid_task_name(self):
        cuisine.dir_remove('datasets')
        from .build_scripts import build_with_params
        with pytest.raises(Exception) as exc:
            build(build_with_params,["doesnt_exist"])
            
            assert 'task should be one of append_to_file, clean' \
                ', copy_file, echo, html, start_server, tests' in str(exc.value)


class TestPartialTaskNames:
    def setup_method(self,method):
        cuisine.dir_remove('datasets')
        from .build_scripts import build_with_params
        self._mod = build_with_params

        
    def test_with_partial_name(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ["cl"])
        assert ['clean[/tmp]'] ==  mod.tasks_run
        
    def test_with_partial_name_and_dependencies(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ["htm"])
        assert ['clean[/tmp]','html'] ==  mod.tasks_run

    def test_exception_on_conflicting_partial_names(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(Exception) as exc:
            build(self._mod, ["c"])
        assert ('Conflicting matches clean, copy_file for task c' in str(exc.value) or
                'Conflicting matches copy_file, clean for task c' in str(exc.value))



class TestDefaultTask:
        def test_simple_default_task(self):
            cuisine.dir_remove('datasets')
            from .build_scripts import simple
            assert _brick_wall_build._run_default_task(simple) #returns false if no default task

        def test_module_with_defaults_which_imports_other_files_with_defaults(self):
            cuisine.dir_remove('datasets')
            from .build_scripts import default_task_and_import_dependencies
            mod = build(default_task_and_import_dependencies)
            assert 'task_with_imported_dependencies' in mod.tasks_run



class TestMultipleTasks:
    def setup_method(self,method):
        cuisine.dir_remove('datasets')
        from .build_scripts import build_with_params
        self._mod = build_with_params
  
    def test_multiple_partial_names(self):
        cuisine.dir_remove('datasets')
        assert ['clean[/tmp]', "html"] == build(self._mod, ["cl", "htm"]).tasks_run



class TesttaskArguments:
    def setup_method(self,method):
        cuisine.dir_remove('datasets')
        from .build_scripts import build_with_params
        self._mod = build_with_params
        self._mod.tasks_run = []

    def test_passing_optional_params_with_dependencies(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ["clean[~/project/foo]",
                                     'append_to_file[/foo/bar,ABCDEF]',
                                     "copy_file[/foo/bar,/foo/blah,False]",
                                     'start_server[8080]'])
        assert ["clean[~/project/foo]",  'append_to_file[/foo/bar,ABCDEF]', 
                "copy_file[/foo/bar,/foo/blah,False]", 'start_server[8080,True]'
            ] == mod.tasks_run
        
    def test_invoking_varargs_task(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ['tests[test1,test2,test3]'])
        assert ['tests[test1,test2,test3]'] == mod.tasks_run

    def test_partial_name_with_args(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ['co[foo,bar]','star'])
        assert ['clean[/tmp]','copy_file[foo,bar,True]', 'start_server[80,True]'
            ] == mod.tasks_run


    def test_passing_keyword_args(self):
        cuisine.dir_remove('datasets')
        mod = build(self._mod, ['co[to=bar,from_=foo]','star[80,debug=False]', 'echo[foo=bar,blah=123]'])

        assert ['copy_file[foo,bar,True]',
                'start_server[80,False]',
                'echo[blah=123,foo=bar]'] == mod.tasks_run



    def test_passing_varargs_and_keyword_args(self):
        cuisine.dir_remove('datasets')
        assert (['echo[1,2,3,some_str,111=333,bar=123.3,foo=xyz]']
                ==  
                build(self._mod,
                      ['echo[1,2,3,some_str,111=333,foo=xyz,bar=123.3]']
                  ).tasks_run)

    def test_validate_keyword_arguments_always_after_args(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(Exception) as exc:
            build(self._mod, ['echo[bar=123.3,foo]'])
        assert "Non keyword arg foo cannot follows" \
            " a keyword arg bar=123.3" in str(exc.value)
        
        with pytest.raises(Exception) as exc:
            build(self._mod, ['copy[from_=/foo,/foo1]'])

        assert "Non keyword arg /foo1 cannot follows" \
            " a keyword arg from_=/foo" in str(exc.value)


            
    def test_invalid_number_of_args(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(TypeError) as exc: 
             build(self._mod, ['append[1,2,3]'])
        print(str(exc.value))
        assert re.findall('takes .*4 .*arguments', str(exc.value))

             
    def test_invalid_names_for_kwargs(self):
        cuisine.dir_remove('datasets')
        with pytest.raises(TypeError) as exc: 
            build(self._mod, ['copy[1=2,to=bar]'])
        assert "got an unexpected keyword argument '1'" in str(exc.value)
        
        with pytest.raises(TypeError) as exc: 
            build(self._mod, ['copy[bar123=2]'])
        assert "got an unexpected keyword argument 'bar123'" in str(exc.value)

