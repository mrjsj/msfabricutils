from dataclasses import dataclass
from typing import Annotated

from cyclopts import Parameter

from .complex_type import ComplexType, load_json_payload


@dataclass
class SparkProperties(ComplexType):
    spark_properties: Annotated[str, Parameter(help="The spark properties")] = None

    def to_dict(self):
        return load_json_payload(self.spark_properties)
