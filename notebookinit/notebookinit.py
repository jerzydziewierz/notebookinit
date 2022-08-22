"""
notebookinit.py
does all the standard tools import
imports logging, numpy, pandas, e.t.c.

usage:

from std_init import *
log=logging.getLogger('<your_region_name>')

# then at the end (to be ran after "run all")

print_watermark()
save_notebook()

"""

"""
# install requirements:

conda install -y mamba 
alias mambao="mamba install --use-index-cache -y --channel conda-forge"
python -m pip install -U git+https://github.com/jerzydziewierz/mict.git#egg=mict
mambao jupyter ipython plotly numpy pandas cryptography jax python-kaleido tqdm watermark pymc3
python -m pip install kaleido chevron
# multiprocessing: 
python -m pip install pqdm bounded-pool-executor

"""
_available_functions = ""
_available_modules = ""
# do all the imports here to keep the dev file clean


def import_module_to_parent(import_from = None, module_name=None, import_as=None, _available_modules="",  verbose=False):
    """
    import_module_to_parent() - import a module and return it.
    :param import_from: if not None, uses "from X import Y" semantics. Otherwise, it uses "Import X" semantics
    :param module_name: name of the module to import.
    :param import_as: if not None, adds "as Z" semantics. Otherwise, does nothing.
    :param _available_modules: running list of available modules, string.
    :param verbose: if True, print the module name and the imported module.
    :return: incremented _available_modules string. if "import_as" is used, the input _available_modules is incremented with "import_as" name; otherwise, it is incremented with `module_name` name.
    """
    import inspect
    parent_locals = inspect.currentframe().f_back.f_locals
    parent_globals = inspect.currentframe().f_back.f_globals
    if import_from is None:
        code_to_exec = f'import {module_name}'
    else:
        code_to_exec = f'from {import_from} import {module_name}'
    if import_as is not None:
        code_to_exec += f' as {import_as}'
    success = False
    try:
        exec(code_to_exec, parent_globals, parent_locals)
        success = True
    except Exception as e:
        if verbose:
            print(f'failed to import {module_name}')
            print(e)
        else:
            pass
    if import_as is not None:
        _available_modules += f'{import_as} '
    else:
        _available_modules += f'{module_name} '

    return _available_modules


# ==================================== start with the logger
import logging
import IPython

ipython = IPython.get_ipython()

from pandas import Timestamp
now = Timestamp.now()
_available_functions += "now "

# %(created)f - # that makes an unix epoch time
log_fmt = '%(asctime)s | %(name)-6s | %(levelname)-5s | > %(message)s'

logging.basicConfig(level=logging.INFO, format=log_fmt, filename=f'log_{Timestamp.utcnow().isoformat()[0:13]}.log',
                    filemode='a')  # ,datefmt="%Y-%m-%dT%H:%M:%S%z"

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-5s| %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def make_log(section_name='unknown', verbose=False):
    """ shortcut to get global program logger with local section name.
    Make the section name 6 characters or less, please.
    :param section_name:
    :return:
    """
    _log = logging.getLogger(section_name)
    try:
        if verbose:
            print(f'logging to {_log.parent.handlers[0].stream.name}')
    except:
        pass
    return _log


_available_functions += "nnlog "


def nnlog(message='message unset', section=None, log=None, level=None):
    """
    Shortcut: conditional logging
    :param message: message to log. If None, will say "message unset"
    :param section: section to log to. if None, will get the caller's name.
    :param log: log to this logger. if None, will make new logger.
    :param level: log level. if None, will use logging.DEBUG (which is quite low)
    :return: nothing.
    """

    if section is None:
        import inspect
        section = inspect.stack()[1][3]

    if log is None:
        _log = make_log(section_name=section)
    else:
        _log = log

    if _log is not None:
        if level is None:
            level = logging.DEBUG
        _log.log(level, message)


del console
del formatter
del log_fmt

_available_functions += "Obsolete "


class Obsolete(Exception):
    def __init__(self, use_instead=None):
        import inspect
        caller = inspect.stack()[1]
        caller_fn_name = caller.function
        caller_file = caller.filename
        # print(caller)
        if use_instead is not None:
            message = f"function >>{caller_fn_name}<< from {caller_file} is obsolete. Use {use_instead} instead."
        else:
            message = f">{caller_fn_name}< from {caller_file} is obsolete."
        super().__init__(message)

    pass


_available_functions += "print_watermark "


def print_watermark():
    """ Display "watermark" in the jupyter notebook,
    :return: nothing.
    """
    # ipython.magic('load_ext watermark')
    # ipython.magic('watermark -d -t -v -h -m -g -iv -u')

    import watermark
    log.info(watermark.watermark(
        python=True, hostname=True,
        machine=True, githash=True,
        updated=True, current_time=True, current_date=True, timezone=True, iso8601=True))


_available_functions += "make_log  "


# auxiliary tools
_available_functions += "run_with_shell "


def run_with_shell(command):
    """
    run_with_shell(str) -  runs a shell command and pipes the output to logger
    :param command:  string of shell command to run.
    :return: nothing??
    """
    return log.info(command + ' :says: ' + os.popen(command).read())


_available_functions += "add_path "

def add_path(new_lib_path=None, verbose=False):
    """
    add_path(str) - robust path incrementer, also, avoids adding it multiple times
    """
    if new_lib_path is not None:
        if new_lib_path not in sys.path:
            sys.path.append(new_lib_path)
    if verbose:
        print(sys.path)


_available_functions += "px_show "


def px_show(hf, width=980, height=360, fname=None, file=None):
    """ show plotly figure using a .png renderer. This makes the notebook to save the figure in the notbook body, and increases browser performance in general.
    :param width: default 400 [px]
    :param height: default 1800 [px]
    :param filename: None -> show. string-> save to this file name.
    :param hf: plotly.figure

    """
    hf.layout.font.size = 14
    if file is not None and fname is None:
        raise Obsolete('use fname instead of file in px_show(fname=...)')
    if fname is None:
        hf.show(renderer='png', width=width, height=height)
    else:
        Path(fname).parent.mkdir(parents=True, exist_ok=True)
        hf.write_image(file=fname, width=width, height=height)


_available_functions += "px_describe "


def px_describe(hf=None,
                title='long title',
                xlabel='xlabel[units]',
                ylabel='ylabel[units]',
                fontsize=14,
                xrange=None,
                yrange=None):
    """
    px_describe(hf, title, xaxis, yaxis, fontsize, xrange, yrange) -
    add a description to the plotly figure.
    """
    # handle errors:
    if hf.layout.xaxis.title.text == '':
        hf.layout.xaxis.title.text = 'x'
    if hf.layout.yaxis.title.text == '':
        hf.layout.yaxis.title.text = 'y'
    if hf.layout.title.text == '':
        hf.layout.title.text = 'title'  # default title

    if hf is None:
        raise ValueError('please provide a plotly figure in hf=...')
    hf.layout.title.text = title
    hf.layout.xaxis.title.text = xlabel
    hf.layout.yaxis.title.text = ylabel
    hf.layout.yaxis.title.font.size = fontsize
    hf.layout.xaxis.title.font.size = fontsize
    hf.layout.title.font.size = fontsize
    hf.layout.legend.title.font.size = fontsize
    hf.layout.margin.autoexpand = True
    hf.layout.margin.t = 2 * fontsize
    hf.layout.margin.b = fontsize
    hf.layout.margin.l = fontsize
    hf.layout.margin.r = fontsize
    hf.layout.margin.pad = 0

    if xrange is not None:
        hf.layout.xaxis.range = xrange
    if yrange is not None:
        hf.layout.yaxis.range = yrange

    return hf


_available_functions += "px_axis_equal "


def px_axis_equal(hf):
    """"
    px_axis_equal(hf) - set equal axis for plotly figure
    """
    hf.update_yaxes(scaleanchor="x", scaleratio=1)
    return hf


# grab notebook name for displaying later
def get_notebook_name():
    """
    This asks the jupyter core to send a javascript to the browser
    to ask the jupyter core (again!) to load the javascript-side notebook name.

    Note that this will not get executed by the kernel until the cell exits.

    Hence, one cannot ask for the same value before all the automation code has exited.

    In fact, not until the entire thing ends.

    In other words, it is kindof useless for automation. bad luck :-(

    There really should be a better way -- how come that the ipython/jupyter core does not know the notebook name?
    """
    raise Obsolete
    import IPython
    # this will be executed in the browser
    jscript = """   
    IPython.notebook.kernel.execute('notebook_name = "' + IPython.notebook.notebook_name + '" ');        
    """
    IPython.display.display(IPython.display.Javascript(jscript))


# ========== Get notebook name 2


def get_notebook_name2():
    """
    Return the full path of the jupyter notebook.
    """
    import json
    import os.path
    import re
    import ipykernel
    import requests

    from urllib.parse import urljoin
    from notebook.notebookapp import list_running_servers
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)


def save_notebook(notebook_name=None,
                  git_message='no message'):
    import time
    import IPython
    import hashlib
    import os
    nb_full_path = None

    if notebook_name is None:
        nb_full_path = get_notebook_name2()
    else:
        nb_full_path = os.path.join(os.getcwd(), notebook_name)

    if nb_full_path is not None:
        print(f'saving as {nb_full_path}')
        print_watermark()
        start_md5 = hashlib.md5(open(nb_full_path, 'rb').read()).hexdigest()
        IPython.display.display(IPython.display.Javascript('IPython.notebook.save_checkpoint();'))
        current_md5 = start_md5

        while start_md5 == current_md5:
            time.sleep(1)
            current_md5 = hashlib.md5(open(nb_full_path, 'rb').read()).hexdigest()
    else:
        print('save and pray...')
        IPython.display.display(IPython.display.Javascript('IPython.notebook.save_checkpoint();'))

    run_with_shell('git add .')
    run_with_shell(f'git commit -a -m "{git_message}"')
    run_with_shell('git push')


log = make_log('notebookinit')

# ====================================  add project root to path
_available_functions += "Path "
from pathlib import Path

import os
import sys
import warnings

_available_functions += "warn "
from warnings import warn

_available_functions += "mict "
from mict import mict

# log.info(f'NOT adding {folder_project_root=} to path')
# sys.path.insert(0,folder_project_root)

# ====================================  database access
# import urllib3

# urllib3.disable_warnings()
# import dotenv
#
# dotenv.load_dotenv()  # take environment variables from .env.
# passwords = mict(dotenv.dotenv_values())

# ====================================  data science tools
_available_modules = import_module_to_parent(module_name='numpy', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='plotly', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='plotly.express', import_as='px', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='plotly.graph_objects', import_as='go', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='pandas', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='json', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='pint', _available_modules=_available_modules)
_available_modules = import_module_to_parent(module_name='uncertanities', _available_modules=_available_modules)


try:
    import jax
    jax.config.update('jax_platform_name', 'cpu')
    jax.config.update('jax_platforms', 'cpu')
    jax.config.update('jax_enable_x64', True)
    jax.config.update('jax_default_dtype_bits', 32)
    jax.numpy.arange(10)
    _available_modules += "jax, "
except ImportError:
    pass

try:
    import chevron
    _available_modules += "chevron, "
except ImportError:
    pass

from IPython.display import display, HTML


_available_functions += "tqdm "
from tqdm.auto import tqdm
import time

_available_modules += "tau, nan, inf "
from math import tau
from numpy import nan
from numpy import inf

ipython.magic('load_ext autoreload')

# ====================================  project folders setup

folder_project_root = str(Path(os.getcwd()).joinpath('../').resolve())
folder_data = Path(os.getcwd() + '/../data/').resolve().__str__()
# folder_reports = Path(os.getcwd() + '/../reports/raw/').resolve().__str__()
# folder_cache = Path(os.getcwd() + '/../data/cache/').resolve().__str__()
#
#
Path(folder_data).mkdir(parents=True, exist_ok=True)
# Path(folder_reports).mkdir(parents=True, exist_ok=True)
# Path(folder_cache).mkdir(parents=True, exist_ok=True)

welcome_text = f''
welcome_text += f''
# welcome_text += f'{folder_project_root=}\n{folder_data=}\n{folder_reports=}\n{folder_cache=}\n'
welcome_text += f'{folder_project_root=}\n'
welcome_text += f'{_available_functions} {_available_modules}\n'
welcome_text += f'Have a productive day!'
log.info(welcome_text)

del welcome_text
del _available_modules
del _available_functions



# disabled because: it's nice, but can slow down the notebook by a lot. use it only when needed.
# try:
#     import rich
#     _available_modules += "rich, "
#     rich.load_ipython_extension(ipython)
#     rich.traceback.install(show_locals=True)  # note that this gets very slow when in interactive notebook.
# except ImportError:
#     pass
