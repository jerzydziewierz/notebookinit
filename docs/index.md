# General

`Notebookinit` is a toolset to accelerate experimental code development, primarily intended for jupyter notebook and it's derivatives

**Warning**:
This package has **very** heavy dependencies, and this is intentional. 


## Objectives
* Requires all my favourite packages which I would normally install anyway, hence, when creating a new environment, I only need to specify THIS package and everything else is alread installed as dependency
* one-liner initializer for my new notebooks: `from notebookinit import *`  will do everything that I would normally do to ready my notebook for exploration


## Implemented features

### Imports

* `numpy`
* `pandas`
* `json`
* `jax` if available
* `chevron` if available
* `plotly.express as px`
* `plotly.graph_objects as go`
* `from warnings import warn`
* `from mict import mict`
* `from pathlib import Path`
* `from IPython.display import display, HTML`
* `from tqdm.auto import tqdm`
* `from math import tau`
* `os`
* `sys`
* `time`


### Helper constants


`nan` is `numpy.nan`

`folder_project_root` is current folder, 2 levels up
`folder_data` is current folder 1 level up + `\data\` 
	* e.g. `os.getcwd() +"/../data/""`


### Helper functions




## Usage

### Initialisation
Single line usage:

`from notebookinit import *`

if you additionally want a log:

`log=logging.getLogger('<your_region_name>')`

### Programming tools

`class Obsolete(Exception)`

`make_log(section_name="something",...)`

`run_with_shell(command)` - runs a shell command and pipes the output to the logger.

`add_path(new_lib_path, ...)` - robust path incrementer



### Data tools

`Timestamp()` shortcut to `pandas.Timestamp()` 

`px_show(hf, width, height, fname)` - show a plotly figure using a .png renderer. This makes the notebook to save the figure in the notebook body, and reduces the performance pentalty when scrolling across a figure that was generated using a lot of data. if `fname` is provided, the figure is not displayed but written to that file name instead. `hf` - handle to a plotly figure. This is probably the second most useful tool in this set.

`px_describe(hf, title, xlabel, ylabel, fontsize, xrange, yrange)` shortcut to make plotly more usable. `hf` - handle to a plotly figure. Returns the same handle, but with title, xlabel, ylabel, fontsize, xrange, yrange set as needed. This has to be the most useful tool in this toolset. 

`px_axis_equal(hf)` - set equal axis for plotly figure




### General notebook tools

`print_watermark()` watermarks the current notebook. Useful for reproducibilty.

`ipython` - shortcut to `import IPython; ipython=IPython.get_ipython()`

`save_notebook(notebook_name=None,  git_message="no message")` 
Asks the jupyter kernel to save the notebook, and then asks git to commit the changes to the local repository. leave `notebook_name` as `None` to use automatic name resolution. 


### Logging


`log.info(message)`

### Internal functions

`get_notebook_name()` 
`get_notebook_name2()` 



### Recommended but ommited

If you want to show off, you can add rich:

```python
try:
	import rich
	rich.load_ipython_extension(ipython)
	rich.traceback.install(show_locals=False)
	from rich import pretty
	pretty.install()
except ImportError:
	print(f"Couldn't load rich")
```

I do not normally use it; Rich works best for console apps, and for jupyter it's just not as good. It is pretty for demos, but not essential, and can produce conflicts with jupyter functionality.

## Installation

Install straight from github:

```bash
python -m pip \
install -U \
git+https://github.com/jerzydziewierz/notebookinit.git#egg=mict
```


To uninstall, a symmetric command is:

```bash
python -m pip uninstall notebookinit
```

For a development mode editable local installation, clone the files from the repo to your favourite folder, and then, from inside the root folder of the repo (where the `setup.py` is )

```bash
python -m pip -e .
```

