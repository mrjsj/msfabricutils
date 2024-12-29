
from dataclasses import dataclass
from typing import Annotated
from .complex_type import ComplexType
from cyclopts import Parameter


@dataclass
class Principal(ComplexType):
    id: Annotated[str, Parameter(help="The ID of the principal.")]
    type: Annotated[str, Parameter(help="The type of the principal.")]

    def to_dict(self):
        payload = {}
        if self.id:
            payload["id"] = self.id
        if self.type:
            payload["type"] = self.type
        return payload
