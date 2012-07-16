# pyfinder.vim

#### Version 0.1

Jump to source file for python import statements.

## What it does

```python
from django.contrib.admin.models import User
```

Place the cursor on the above line, type
`<leader>gs`

vim opens a new buffer with  
`.venv/lib/python2.7/site-packages/django/contrib/admin/models.py`

## Installation

To install the plugin, just drop the plugin folder to your `dotvim` directory.

There are currently no configuration options available, so no need to edit your config file.

You can now use `<leader>gs` to jump to the source of your import statement.

### Using pathogen

Just clone the project in your bundles directory.

`git clone git://github.com/tudorprodan/pyfinder.vim.git /path/to/.vim/bundle/`


## Implementation

This plugin DOES NOT run any of the python modules it searches for.

Instead it searches by hand in the python paths.

It doesn't use `imp`, `pkgutil`, or anything else, as all of them import either the target module or their parents when fetching paths.

## Supported paths

Currently, the plugin finds python modules in the following order:

1. as a relative path to the current file
2. as a relative path to the project root (current directory)
3. as an absolute path to any of the virtualenv packages (if `$VIRTUAL_ENV` is set, by the activate script)
4. as an absolute path to any system module

## Limitations

The plugin currently uses Vim's `Python` bindings, and doesn't work without them.

However, the only real piece of python code that needs to be ran is at plugin-load to determine all system package paths. So it can be rewritten in full `VimL` in order to be usable on versions compiled with `-python`.

## Plans for the future

I plan to implement the following features, but I just haven't had time to yet.

* customizable bindings, `CtrlP` style. `let g:pyfinder_map`
* more commands to open in: new tab, split, vertical split
* `VimL` reimplementation. I have implemented it in `Python` to make sure it's useful and usable. There are no limitations why it could not be rewritten in `VimL`
* command to refresh with a new project root
* command to add a virtualenv
* project config file to be read, to allow more custom python package setups

## Contributing

Please feel free to contribute.

I'm quite new to writing Vim plugins, I'm sure there's a lot of stuff that can be improved.

If you find an issue, please post it in the [issue tracker](https://github.com/tudorprodan/pyfinder.vim/issues).

Thanks!
