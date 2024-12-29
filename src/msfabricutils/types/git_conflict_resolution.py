from dataclasses import dataclass
from typing import Annotated, Literal
from .complex_type import ComplexType
from cyclopts import Parameter


@dataclass
class GitConflictResolution(ComplexType):
    conflict_resolution_type: Annotated[Literal["Workspace"], Parameter(help="The type of conflict resolution to apply.")] = None
    conflict_resolution_policy: Annotated[Literal["PreferRemote", "PreferWorkspace"], Parameter(help="The policy to apply for conflict resolution.")] = None

    def to_dict(self):
        payload = {}
        if self.conflict_resolution_type:
            payload["conflictResolutionType"] = self.conflict_resolution_type
        if self.conflict_resolution_policy:
            payload["conflictResolutionPolicy"] = self.conflict_resolution_policy
        return payload
