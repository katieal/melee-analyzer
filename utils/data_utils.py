# Import packages
import json

# File for data utility methods

def stringify_id(id_) -> str:
    """
    Convert a pattern-matching ID dict to a string. Mostly used to link labels to
    input fields with html_for.
    :param id_: the ID dict to convert
    :return: string
    """
    if isinstance(id_, dict):
        return json.dumps(id_, sort_keys=True, separators=(",", ":"))
    return id_