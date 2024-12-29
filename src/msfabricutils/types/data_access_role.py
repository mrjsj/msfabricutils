from dataclasses import dataclass
from typing import Annotated

from cyclopts import Parameter

from .complex_type import ComplexType, load_json_payload


@dataclass
class DataAccessRole(ComplexType):
    data_access_roles: Annotated[str, Parameter(help="The data access roles")] = None

    def to_dict(self):
        return load_json_payload(self.data_access_roles)
