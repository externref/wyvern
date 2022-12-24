# type: ignore

# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
wyvern 🚀
--------

A feature rich library which allows you to interact with the discord API using 
bots.

"""


from . import commands, extensions, utils  # noqa: 401
from .aliases import *  # noqa: F403
from .clients import *  # noqa: F403
from .components import *  # noqa: F403
from .constructors import *  # noqa: F403
from .events import *  # noqa: F403
from .exceptions import *  # noqa: F403
from .files import *  # noqa: F403
from .intents import *  # noqa: F403
from .interactions import *  # noqa: F403
from .models import *  # noqa: F403
from .permissions import *  # noqa: F403
from .plugins import *  # noqa: F403
from .presences import *  # noqa: F403
from .rest import *  # noqa: F403

__version__: str = "0.1.0"
