from dataclasses import dataclass
from typing import Annotated

from cyclopts import Parameter

from .complex_type import ComplexType, load_json_payload


@dataclass
class ConnectionRequest(ComplexType):
    connection_request: Annotated[str, Parameter(help="The connection request")] = None

    def to_dict(self):
        return load_json_payload(self.connection_request)
