from __future__ import with_statement
import re
import os
import sys
from contextlib import contextmanager


def activate_virtualenv(path):
    at = os.path.join(path, "bin", "activate_this.py")
    execfile(at, dict(__file__=at))

@contextmanager
def activated_virtualenv(venv_path=None):
    if venv_path:
        old_path = list(sys.path)
        activate_virtualenv(venv_path)
        try:
            yield
        finally:
            sys.path = old_path
    else:
        yield


class ModuleSearcher(object):
    def __init__(self, proj_path=None, venv_path=None):
        sp = [proj_path]

        with activated_virtualenv(venv_path):
            sp += sys.path

        self.search_path = filter(lambda x: x, sp)

    def possible_files(self, module, can_have_name=False):
        c = module.split(".")

        pf = [
            os.path.join(*c) + ".py",
            os.path.join(*(c + ["__init__"])) + ".py"
        ]

        if can_have_name and len(c) > 1:
            c = c[:-1]
            pf += [
                os.path.join(*c) + ".py",
                os.path.join(*(c + ["__init__"])) + ".py"
            ]

        return pf

    def search(self, module, can_be_name=False, local_path=None):
        fns = self.possible_files(module, can_be_name)
        sp = self.search_path

        if local_path:
            sp = [local_path] + sp

        for p in sp:
            for f in fns:
                fn = os.path.join(p, f)
                if os.path.isfile(fn):
                    return fn

        return None


class PySourceFinder(object):

    def __init__(self):
        venv_path = self.get_virtualenv_from_env_var()
        proj_path = os.getcwd()

        self.searcher = ModuleSearcher(proj_path=proj_path, venv_path=venv_path)

        self.import_re = re.compile(
            r"^\s*(from (?P<from>{module}) )?import (?P<module>{module})( as {module})?$".format(
                module=r"\w+(\.\w+)*"
            )
        )

    def get_virtualenv_from_env_var(self):
        return os.environ.get("VIRTUAL_ENV", None)

    def get_module_from_import_line(self, line):
        m = self.import_re.match(line)

        if not m:
            return (None, False)

        g = m.groupdict()

        mod = g["module"]

        can_have_name = False

        if g["from"]:
            mod = g["from"] + "." + mod
            can_have_name = True

        return (mod, can_have_name)

    def find_module(self, module, can_have_name=False, curr_file=None):
        local_path = None
        if curr_file:
            local_path = os.path.split(curr_file)[0]

        return self.searcher.search(module, can_have_name, local_path)

    def find_module_from_import_line(self, line, curr_file=None):
        module, can_have_name = self.get_module_from_import_line(line)

        if module:
            return self.find_module(module, can_have_name, curr_file)

        return None

    @classmethod
    def plugin_loaded(cls):
        cls._instance = cls()

    @classmethod
    def search(cls, line, curr_file):
        return cls._instance.find_module_from_import_line(line, curr_file)



