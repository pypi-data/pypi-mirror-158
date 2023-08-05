"""
**parse**: YAML and JSON input handler
--------------------------------------

.. codeauthor:: 
    Peter Kraus
    
"""
import os
import yaml
import json
from typing import Any
from dgbowl_schemas.dgpost import to_recipe


def parse(fn: str) -> dict[str, Any]:
    """
    Input file parsing function.

    Supports loading ``yaml`` and ``json`` files using the `recipe`-parsing
    function and schema provided in the :mod:`dgbowl_schemas.dgpost..recipe_1_1`
    module.

    Parameters
    ----------
    fn
        Path to the filename to be parsed

    Returns
    -------
    ret: dict[str, Any]
        A dictionary representing the recipe.

    """
    assert os.path.exists(fn) and os.path.isfile(fn), (
        f"provided file name '{fn}' does not exist " f"or is not a valid file"
    )

    with open(fn, "r") as infile:
        if fn.endswith("yml") or fn.endswith("yaml"):
            indict = yaml.safe_load(infile)
        elif fn.endswith("json"):
            indict = json.load(infile)
    ret = to_recipe(**indict).dict(by_alias=True, exclude_none=True)
    return ret
