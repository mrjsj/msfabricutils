from typing import Annotated, List, Optional
from cyclopts import Parameter
from dataclasses import dataclass
from .complex_type import ComplexType

@dataclass
class ExecutionData(ComplexType):
    table_name: Annotated[str, Parameter(help="Table name")]
    schema_name: Optional[Annotated[str, Parameter(help="Schema name. Only applicable for schema enabled lakehouses.")]] = None
    v_order: Optional[Annotated[bool, Parameter(negative="", help="Whether to enable v-order")]] = None
    z_order_by: Optional[Annotated[List[str], Parameter(consume_multiple=True, negative="", help="List of columns to z-order by")]] = None
    retention_period: Optional[Annotated[str, Parameter(help="Retention period in format d:hh:mm:ss")]] = None
    

    def to_dict(self):
        payload = {}
        if self.table_name:
            payload["tableName"] = self.table_name
        if self.schema_name:
            payload["schemaName"] = self.schema_name
        if self.v_order or self.z_order_by:
            payload["optimizeSettings"] = {}
        if self.v_order:
            payload["optimizeSettings"]["vOrder"] = self.v_order
        if self.z_order_by:
            payload["optimizeSettings"]["zOrderBy"] = self.z_order_by
        if self.retention_period:
            payload["vacuumSettings"] = {}
            payload["vacuumSettings"]["retentionPeriod"] = self.retention_period
        return payload
