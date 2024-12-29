import base64
import os
from typing import Annotated
from cyclopts import Parameter
from dataclasses import dataclass
from msfabricpysdkcore.item import Item


@dataclass
class ItemDefinitionPart():
    path: Annotated[str, Parameter(help="The path of the item definition part.")]
    payload: Annotated[str, Parameter(help="The payload of the item definition part.")]
    payload_type: Annotated[str, Parameter(help="The type of the payload.")]

    def to_dict(self):
        payload = {}
        if self.path:
            payload["path"] = self.path
        if self.payload:
            payload["payload"] = self.payload
        if self.payload_type:
            payload["payloadType"] = self.payload_type
        return payload


@dataclass
class ItemDefinition():
    item_path: Annotated[str, Parameter(help="The file or folder path of the item definition.")]
    format: Annotated[str, Parameter(help="The format of the item definition.", show=False)] = None
    parts: Annotated[list[ItemDefinitionPart], Parameter(help="The parts of the item definition.", show=False)] = None

    def to_dict(self):
        payload = {}
        if self.format:
            payload["format"] = self.format
        if self.parts:
            payload["parts"] = [part.to_dict() for part in self.parts]
        return payload

    # @classmethod
    def load_from_path(self, format: str = None, payload_type: str = "InlineBase64") -> "ItemDefinition":
        
        self.format = format
        path = self.in_file
        parts = []
        if os.path.isfile(path):
            dirs = [(os.path.dirname(path), None, [os.path.basename(path)])]

        if os.path.isdir(path):
            dirs = os.walk(path)

        for root, _, files in dirs:
            for file in files:
                file_path = os.path.join(root, file)
                if file_path == path:
                    rel_path = file
                else:
                    rel_path = os.path.relpath(file_path, path)
                with open(file_path, "r") as f:
                    endoded_payload = base64.b64encode(f.read().encode()).decode()
                parts.append(ItemDefinitionPart(path=rel_path, payload=endoded_payload, payload_type=payload_type))
        return ItemDefinition(in_file=path, format=format, parts=parts)

@dataclass
class OutFile():
    item_path: Annotated[str, Parameter(help="The path to save the item definition.")]


def save_item_to_path(item: Item, path: str):
    item_definition = item.get("definition")
    os.makedirs(path, exist_ok=False)
    if item_definition:
        for part in item_definition.get("parts", []):
            file_path = os.path.join(path, part.get("path"))
            with open(file_path, "w") as f:
                f.write(base64.b64decode(part.get("payload")).decode())
