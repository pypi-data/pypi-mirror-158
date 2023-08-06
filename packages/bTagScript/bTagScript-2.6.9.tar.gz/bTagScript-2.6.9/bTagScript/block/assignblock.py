from typing import Optional

from ..adapter import StringAdapter
from ..interface import verb_required_block
from ..interpreter import Context


class AssignmentBlock(verb_required_block(False, parameter=True)):
    """
    Variables are useful for choosing a value and referencing it later in a tag.
    Variables can be referenced using brackets as any other block.
    Note that if the variable's name is being "used" by any other block the variable
    will be ignored.

    **Usage:** ``{=(<name>):<value>}``

    **Aliases:** ``assign, let, var, =``

    **Payload:** value

    **Parameter:** name

    **Examples:**

    .. tagscript::

        {=(prefix):!}
        The prefix here is `{prefix}`.
        The prefix here is `!`.

        {assign(day):Monday}
        {if({day}==Wednesday):It's Wednesday my dudes!|The day is {day}.}
        The day is Monday.
    """

    ACCEPTED_NAMES = ("=", "assign", "let", "var")

    def process(self, ctx: Context) -> Optional[str]:
        if not ctx.verb.parameter:
            return None
        elif ctx.verb.parameter in ctx.interpreter._blocknames:
            return None
        ctx.response.variables[ctx.verb.parameter] = StringAdapter(str(ctx.verb.payload))
        return ""
