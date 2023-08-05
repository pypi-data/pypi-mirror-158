#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Functions for patching the configuration dictionary
"""
import os, sys
from meerschaum.config._paths import PATCH_DIR_PATH, PERMANENT_PATCH_DIR_PATH
from meerschaum.config._read_config import read_config
patch_config = None
if PATCH_DIR_PATH.exists():
    from meerschaum.utils.yaml import yaml, _yaml
    if _yaml is not None:
        patch_config = read_config(directory=PATCH_DIR_PATH)

permanent_patch_config = None
if PERMANENT_PATCH_DIR_PATH.exists():
    from meerschaum.utils.yaml import yaml, _yaml
    if _yaml is not None:
        permanent_patch_config = read_config(directory=PERMANENT_PATCH_DIR_PATH)
else:
    permanent_patch_config = None


def apply_patch_to_config(
        config: dict,
        patch: dict
    ):
    """Patch the config dict with a new dict (cascade patching).

    Parameters
    ----------
    config: dict :
        
    patch: dict :
        

    Returns
    -------

    """
    from meerschaum.utils.packages import cascadict
    base = cascadict.CascaDict(config)
    new = base.cascade(patch)
    return new.copy_flat()

def write_patch(
        patch: dict,
        debug: bool = False
    ):
    """Write patch dict to yaml

    Parameters
    ----------
    patch: dict :
        
    debug: bool :
         (Default value = False)

    Returns
    -------

    """
    from meerschaum.config._edit import write_config
    if debug:
        from meerschaum.utils.formatting import pprint
        print(f"Writing configuration to {PATCH_DIR_PATH}:", file=sys.stderr)
        pprint(patch, stream=sys.stderr)
    write_config(patch, directory=PATCH_DIR_PATH)
