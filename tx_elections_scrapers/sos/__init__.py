from . import interpret_county
from . import interpret_statewide
from . import serialize_county
from . import serialize_statewide


def statewide(input):
    """
    Serialize input as statewide election results.

    Input can be text or a file-like object.
    """
    return interpret_statewide.interpret(serialize_statewide.serialize(input))


def county(input):
    """
    Serialize input as county by county election results.

    Input can be text or a file-like object.
    """
    return interpret_county.interpret(serialize_county.serialize(input))
