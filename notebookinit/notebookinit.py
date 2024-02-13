"""
notebookinit.py
does all the standard tools import
imports logging, numpy, pandas, e.t.c.

usage:

from notebookinit import *
log=logging.getLogger('<your_region_name>')

# then at the end (to be run after "run all")

print_watermark()
save_notebook()

"""


help_msg = ""
# do all the imports here to keep the dev file clean

# ====================================  project folders setup
help_msg += "Path "
from pathlib import Path
import os
import sys
import warnings


# version with root folder being above the current folder:
# folder_project_root = str(Path(os.getcwd()).joinpath('../').resolve())
# version with root folder being the current folder:
folder_project_root = str(Path(os.getcwd()).resolve())
folder_data = Path(os.getcwd() + '/../data/').resolve().__str__()
folder_log = str(Path(folder_project_root).joinpath('log').resolve())
Path(folder_log).mkdir(parents=True, exist_ok=True)
# folder_reports = Path(os.getcwd() + '/../reports/raw/').resolve().__str__()
# folder_cache = Path(os.getcwd() + '/../data/cache/').resolve().__str__()
#
#
Path(folder_data).mkdir(parents=True, exist_ok=True)
# Path(folder_reports).mkdir(parents=True, exist_ok=True)
# Path(folder_cache).mkdir(parents=True, exist_ok=True)

from .bring import bring


# ==================================== start with the logger
import logging
import IPython

ipython = IPython.get_ipython()

from pandas import Timestamp
now = Timestamp.now
help_msg += "now "

# %(created)f - # that makes an unix epoch time
log_fmt = '%(asctime)s | %(name)-6s | %(levelname)-5s | > %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt, filename=f'{folder_log}/log_{Timestamp.utcnow().isoformat()[0:13]}.log',
                    filemode='a')  # ,datefmt="%Y-%m-%dT%H:%M:%S%z"

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-5s| %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def make_log(section_name='unknown', verbose=False):
    """ shortcut to get global program logger with local section name.
    Make the section name 6 characters or fewer, please.
    :param section_name:
    :param verbose: if True, print the section name.
    :return:
    """
    _log = logging.getLogger(section_name)
    try:
        if verbose:
            print(f'logging to {_log.parent.handlers[0].stream.name}')
    except:
        pass
    return _log.info


help_msg += "nnlog "


def nnlog(message='message unset', section=None, log=None, level=None, execute=True):
    """
    Shortcut: conditional logging
    :param message: message to log. If None, will say "message unset"
    :param section: section to log to. if None, will get the caller's name.
    :param log: log to this logger. if None, will make new logger.
    :param level: log level. if None, will use logging.DEBUG (which is quite low)
    :param execute: if false, do nothing. default true.
    :return: nothing.
    """
    if execute:
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

bring(import_from='notebookinit.obsolete', module_name='Obsolete', help_msg=help_msg, verbose=False)


help_msg += "print_watermark "


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


help_msg += "make_log  "


# auxiliary tools
help_msg += "run_with_shell "


def run_with_shell(command):
    """
    run_with_shell(str) -  runs a shell command and pipes the output to logger
    :param command:  string of shell command to run.
    :return: nothing??
    """
    result = os.popen(command).read()
    # log.info(command + ' :says: ' + result)
    return result


help_msg += "add_path "


def add_path(new_lib_path=None, verbose=False):
    """
    add_path(str) - robust path incrementer, also, avoids adding it multiple times
    """
    if new_lib_path is not None:
        if new_lib_path not in sys.path:
            sys.path.append(str(new_lib_path))
    if verbose:
        print(sys.path)


help_msg += "px_show "


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


help_msg += "px_describe "


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


help_msg += "px_axis_equal "


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
    try:
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
    except RuntimeError as e:
        warnings.warn(e.args[0])
        return None


def save_notebook(notebook_name=None,
                  git_message=None):
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

    if git_message is not None:
        log.info(f'commiting with git...')
        run_with_shell(f'nbdev_clean --clear_all --fname {nb_full_path}')
        run_with_shell('git add .')
        run_with_shell(f'git commit -a -m "{git_message}"')
        run_with_shell('git push')
        log.info('git push done')


# ====================================  add project root to path

Path('log').mkdir(parents=True, exist_ok=True)
log = make_log('notebookinit')

help_msg += "warn "
from warnings import warn

help_msg += "mict "
from mict import mict

# log.info(f'NOT adding {folder_project_root=} to path')
# sys.path.insert(0,folder_project_root)

# ====================================  database access
# import urllib3

# urllib3.disable_warnings()

# ====================================  data science tools
help_msg = bring(module_name='numpy', help_msg=help_msg)
help_msg = bring(module_name='plotly', help_msg=help_msg)
help_msg = bring(module_name='plotly.express', import_as='px', help_msg=help_msg)
help_msg = bring(module_name='plotly.graph_objects', import_as='go', help_msg=help_msg)
help_msg = bring(module_name='pandas', help_msg=help_msg)
help_msg = bring(module_name='json', help_msg=help_msg)
help_msg = bring(module_name='pint', help_msg=help_msg)
help_msg = bring(module_name='uncertanities', help_msg=help_msg)
help_msg = bring(module_name='pydantic', help_msg=help_msg)
help_msg = bring(import_from='retry', module_name='retry', help_msg=help_msg)


try:
    import jax
    jax.config.update('jax_platform_name', 'cpu')
    jax.config.update('jax_platforms', 'cpu')
    jax.config.update('jax_enable_x64', True)
    jax.config.update('jax_default_dtype_bits', 32)
    jax.numpy.arange(10)
    help_msg += "jax, "
except ImportError:
    pass
except AttributeError:
    print('could not import jax')

try:
    import chevron
    help_msg += "chevron, "
except ImportError:
    pass

from IPython.display import display, HTML


help_msg = bring(import_from='tqdm.auto', module_name='tqdm', help_msg=help_msg)
help_msg = bring(module_name='time', help_msg=help_msg)
help_msg = bring(import_from='math', module_name='tau', help_msg=help_msg)
help_msg = bring(import_from='numpy', module_name='nan', help_msg=help_msg)
help_msg = bring(import_from='numpy', module_name='inf', help_msg=help_msg)
help_msg = bring(import_from='numpy', module_name='pi', help_msg=help_msg)

# note that this will not work when not-in-jupyter
try:
    ipython.magic('load_ext autoreload')
except Exception:
    print('possibly non-jupyter env detected.')



import dotenv
#
dotenv.load_dotenv()  # take environment variables from .env.
passwords = mict(dotenv.dotenv_values())
if len(passwords) > 0:
    help_msg += f"passwords={len(passwords)}; "

welcome_text = f''
welcome_text += f''
# welcome_text += f'{folder_project_root=}\n{folder_data=}\n{folder_reports=}\n{folder_cache=}\n'
welcome_text += f'folder_project_root={folder_project_root}\n'
welcome_text += f'{help_msg}\n'
welcome_text += f'Have a productive day!'
log(welcome_text)

del welcome_text
del help_msg



# disabled because: it's nice, but can slow down the notebook by a lot. use it only when needed.
# try:
#     import rich
#     _available_modules += "rich, "
#     rich.load_ipython_extension(ipython)
#     rich.traceback.install(show_locals=True)  # note that this gets very slow when in interactive notebook.
# except ImportError:
#     pass
