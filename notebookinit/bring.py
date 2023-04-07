"""bring.py

This module contains the bring() function, which is used to import modules into the caller's frame.

"""


def bring(import_from=None, module_name=None, import_as=None, help_msg="", verbose=False, levels=1):
    """
    Import a module or a function from a module, to the caller's frame.

    :param import_from: if not None, uses "from X import Y" semantics. Otherwise, it uses "Import X" semantics
    :param module_name: name of the module to import.
    :param import_as: if not None, adds "as Z" semantics. Otherwise, does nothing.
    :param help_msg: running list of available modules, string.
    :param verbose: if True, print the module name and the imported module.
    :param levels: how many levels up to go to find the caller's frame. Default 1. Note that it is not always obvious how many levels up you need to go.
    :return: incremented _available_modules string. if "import_as" is used, the input _available_modules is incremented with "import_as" name; otherwise, it is incremented with `module_name` name.
    """
    import inspect
    #     parent_locals = inspect.currentframe().f_back.f_locals
    #     parent_globals = inspect.currentframe().f_back.f_globals
    frame = inspect.currentframe()
    for i in range(levels):
        frame = frame.f_back
        if verbose:
            print(f"frame {i}: {frame}")
    parent_locals = frame.f_locals
    parent_globals = frame.f_globals

    if import_from is None:
        code_to_exec = f'import {module_name}'
    else:
        code_to_exec = f'from {import_from} import {module_name}'
    if import_as is not None:
        code_to_exec += f' as {import_as}'
    success = False
    try:
        if verbose:
            print(f'running: {code_to_exec}')
        exec(code_to_exec, parent_globals, parent_locals)
        success = True
    except Exception as e:
        if verbose:
            print(f'failed to import {module_name}')
            print(e)
        else:
            return help_msg  # on fail, return with no change to help_msg
    if import_as is not None:
        help_msg += f'{import_as} '
    else:
        help_msg += f'{module_name} '

    return help_msg
