from __future__ import annotations

import ast
import typing


class Utils:
    def add_returns(self, body: typing.Any) -> None:
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.add_returns(body[-1].body)
            self.add_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.add_returns(body[-1].body)

    async def f_eval(self, *, code: str, renv: dict[str, typing.Any]) -> typing.Any:
        """Evaluates the code in the bot's namespace.

        Parameters
        ----------

        code : str
            The code to evaluate.
        renv: dict[str, typing.Any]
            Environment to evaluate code in.

        Returns
        -------
        
        typing.Any
            The result of the code.

        """
        _fn_name = "__wyvern_eval"
        code = "\n".join(f"    {i}" for i in code.strip().splitlines())
        parsed: typing.Any = ast.parse(f"async def {_fn_name}:\n{code}")
        self.add_returns(parsed.body[0].body)
        exec(compile(parsed, filename="<ast>", mode="exec"), renv)
        fn = renv[_fn_name]
        return await fn()
