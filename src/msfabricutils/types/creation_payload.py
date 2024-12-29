from typing import Literal

from .complex_type import ComplexType


class CreationPayload(ComplexType):
    database_type: Literal["ReadWrite", "Shortcut"]
    parent_eventhouse_item_id: str
    invitation_token: str
    parent_eventhouse_item_id: str
    source_cluster_uri: str
    source_database_name: str


    def to_dict(self):
        payload = {}
        if self.database_type:
            payload["databaseType"] = self.database_type
        if self.parent_eventhouse_item_id:
            payload["parentEventhouseItemId"] = self.parent_eventhouse_item_id
        if self.invitation_token:
            payload["invitationToken"] = self.invitation_token
        if self.parent_eventhouse_item_id:
            payload["parentEventhouseItemId"] = self.parent_eventhouse_item_id
        if self.source_cluster_uri:
            payload["sourceClusterUri"] = self.source_cluster_uri
        if self.source_database_name:
            payload["sourceDatabaseName"] = self.source_database_name
        return payload
