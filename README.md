# pyfinder.vim

Jump to source file for python import statements.

## What it does

```python
from django.contrib.admin.models import User
```

Place the cursor on the above line, type `<leader>gf`,  
vim opens a new buffer with  
`.venv/lib/python2.7/site-packages/django/contrib/admin/models.py`

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
