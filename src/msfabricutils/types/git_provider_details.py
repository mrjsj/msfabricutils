from dataclasses import dataclass
from typing import Annotated, Literal

from cyclopts import Parameter

from .complex_type import ComplexType


@dataclass
class GitProviderDetails(ComplexType):
    branch_name: Annotated[str, Parameter(help="The name of the branch.")]
    directory_name: Annotated[str, Parameter(help="The name of the directory.")]
    git_provider_type: Annotated[Literal["GitHub", "AzureDevOps"], Parameter(help="The type of git provider.")]
    repository_name: Annotated[str, Parameter(help="The name of the repository.")]
    organization_name: Annotated[str, Parameter(help="The name of the organization. Only used for AzureDevOps.")] = None
    project_name: Annotated[str, Parameter(help="The name of the project. Only used for AzureDevOps.")] = None
    owner_name: Annotated[str, Parameter(help="The name of the owner. Only used for GitHub.")] = None

    def to_dict(self):
        payload = {}
        if self.branch_name:
            payload["branchName"] = self.branch_name
        if self.directory_name:
            payload["directoryName"] = self.directory_name
        if self.git_provider_type:
            payload["gitProviderType"] = self.git_provider_type
        if self.organization_name:
            payload["organizationName"] = self.organization_name
        if self.project_name:
            payload["projectName"] = self.project_name
        if self.repository_name:
            payload["repositoryName"] = self.repository_name
        if self.owner_name:
            payload["ownerName"] = self.owner_name
        return payload
