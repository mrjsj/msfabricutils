from dataclasses import dataclass
from typing import Annotated

from cyclopts import Parameter

from .complex_type import ComplexType


@dataclass
class GitUpdateOptions(ComplexType):
    allow_override_items: Annotated[bool, Parameter(help="Whether to allow override items.")] = None

    def to_dict(self):
        payload = {}
        if self.allow_override_items:
            payload["allowOverrideItems"] = self.allow_override_items
        return payload
