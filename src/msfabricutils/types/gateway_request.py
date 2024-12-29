from typing import Annotated
from cyclopts import Parameter
from .complex_type import ComplexType, load_json_payload
from dataclasses import dataclass


@dataclass
class GatewayRequest(ComplexType):
    gateway_request: Annotated[str, Parameter(help="The gateway request")] = None

    def to_dict(self):
        return load_json_payload(self.gateway_request)

