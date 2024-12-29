from dataclasses import dataclass
from .complex_type import ComplexType, load_json_payload
from typing import Annotated, Literal
from cyclopts import Parameter

@dataclass
class PoolProperties(ComplexType):
    customize_compute_enabled: Annotated[bool, Parameter(help="Whether to customize the compute pool")] = None
    default_pool_id: Annotated[str, Parameter(help="The default pool ID")] = None
    default_pool_name: Annotated[str, Parameter(help="The default pool name")] = None
    default_pool_type: Annotated[Literal["Capacity", "Workspace"], Parameter(help="The default pool type")] = None
    starter_pool_max_node_count: Annotated[int, Parameter(help="The maximum number of nodes to start")] = None
    starter_pool_max_executors: Annotated[int, Parameter(help="The maximum number of executors to start")] = None

    def to_dict(self):
        payload = {}

        # Customize compute
        if self.customize_compute_enabled:
            payload["customizeComputeEnabled"] = self.customize_compute_enabled

        # Default pool
        if self.default_pool_id or self.default_pool_name or self.default_pool_type:
            payload["defaultPool"] = {}
            if self.default_pool_id:
                payload["defaultPool"]["id"] = self.default_pool_id
            if self.default_pool_name:
                payload["defaultPool"]["name"] = self.default_pool_name
            if self.default_pool_type:
                payload["defaultPool"]["type"] = self.default_pool_type

        # Starter pool
        if self.starter_pool_max_node_count or self.starter_pool_max_executors:
            payload["starterPool"] = {}
            if self.starter_pool_max_node_count:
                payload["starterPool"]["maxNodeCount"] = self.starter_pool_max_node_count
            if self.starter_pool_max_executors:
                payload["starterPool"]["maxExecutors"] = self.starter_pool_max_executors
        
        return payload

