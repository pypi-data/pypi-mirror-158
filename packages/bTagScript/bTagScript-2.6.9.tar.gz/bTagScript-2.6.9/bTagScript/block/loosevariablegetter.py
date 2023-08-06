from typing import Optional

from ..adapter import StringAdapter
from ..interface import Block
from ..interpreter import Context


class LooseVariableGetterBlock(Block):
    """
    The loose variable block represents the adapters for any seeded or defined variables.
    This variable implementation is considered "loose" since it checks whether the variable is
    valid during :meth:`process`, rather than :meth:`will_accept`.

    **Usage:** ``{<variable_name>([parameter]):[payload]}``

    **Aliases:** This block is valid for any inputted declaration.

    **Payload:** Depends on the variable's underlying adapter.

    **Parameter:** Depends on the variable's underlying adapter.

    **Examples:**

    .. tagscript::

        {=(example):This is my variable.}
        {example}
        This is my variable.
    """

    def will_accept(self, ctx: Context) -> bool:
        return True

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration.startswith("$"):
            varname = ctx.verb.declaration.split("$", 1)[1]
            ctx.response.variables[varname] = StringAdapter(str(ctx.verb.payload))
            return ""
        elif ctx.verb.declaration in ctx.response.variables:
            return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
        else:
            return None
