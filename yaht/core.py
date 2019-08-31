from dataclasses import dataclass


@dataclass
class TypedBytes:
	type: str
	value: bytes
