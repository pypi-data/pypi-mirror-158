#
# File:    ./src/vutils/yaml/__init__.pyi
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-23 10:01:39 +0200
# Project: vutils-yaml: Working with YAML format
#
# SPDX-License-Identifier: MIT
#

from collections.abc import Callable
from typing import Protocol, TypeVar

import yaml
from _typeshed import SupportsRead
from typing_extensions import TypeAlias

_T = TypeVar("_T")

PyList: TypeAlias = list[object]
PySet: TypeAlias = set[object]
PyDict: TypeAlias = dict[object, object]

_MarkType: TypeAlias = yaml.error.Mark
_NodeType: TypeAlias = yaml.nodes.Node
_CtorType: TypeAlias = yaml.constructor.BaseConstructor
_CtorSpecType: TypeAlias = tuple[str, str | None, bool]
_CtorDecorType: TypeAlias = Callable[[type[_CtorType]], type[_CtorType]]
_StreamType: TypeAlias = str | bytes | SupportsRead[str] | SupportsRead[bytes]

def _new_date(cls: type[_T], *args: object) -> _T: ...
def _new_datetime(cls: type[_T], *args: object, **kwargs: object) -> _T: ...

class _CtorFuncType(Protocol):
    def __call__(
        self, inst: _CtorType, node: _NodeType, *args: object, **kwargs: object
    ) -> object: ...
