from dataclasses import dataclass
from typing import Annotated, Literal
from .complex_type import ComplexType
from cyclopts import Parameter


@dataclass
class GitUpdateCredentials(ComplexType):
    source: Annotated[Literal["Automatic", "ConfiguredConnection", "None"], Parameter(help="The Git credentials source.")]
    connection_id: Annotated[str, Parameter(help="The object ID of the connection. Only used if source is ConfiguredConnection.")] = None

    def to_dict(self):
        payload = {}
        if self.source:
            payload["source"] = self.source
        if self.connection_id:
            payload["connectionId"] = self.connection_id
        return payload
