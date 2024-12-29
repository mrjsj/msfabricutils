from typing import Annotated, Literal

from cyclopts import Parameter
from dataclasses import dataclass
from .complex_type import ComplexType

@dataclass
class FileFormatOptions(ComplexType):
    delimiter: Annotated[str, Parameter(help="The delimiter of the data file. Only applicable for CSV files.")] = None
    format: Annotated[Literal["Csv", "Parquet"], Parameter(help="Data file format name.")] = None
    header: Annotated[bool, Parameter(help="Whether the data file has a header. Only applicable for CSV files.")] = None

    def to_dict(self):
        payload = {}

        if self.delimiter:
            payload["delimiter"] = self.delimiter
        if self.format:
            payload["format"] = self.format
        if self.header:
            payload["header"] = self.header

        return payload

