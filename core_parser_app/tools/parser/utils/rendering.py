"""Form rendering utils
"""
import re
import textwrap


def format_tooltip(text, width=80):
    """Format the tooltip to limit the size of the line

    Args:
        text:
        width:

    Returns:

    """
    return textwrap.fill(re.sub(r"\s+", " ", text.strip()), width)
