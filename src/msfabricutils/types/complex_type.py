from abc import ABC, abstractmethod


class ComplexType(ABC):
    @abstractmethod
    def to_dict(self):
        pass


def load_json_payload(payload: str):
    import json

    if payload.endswith(".json") or payload.endswith(".jsonl"):
        with open(payload, "r") as f:
            return json.load(f)
    else:
        return json.loads(payload)
