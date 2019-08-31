from yaht import Auto, TypedBytes, unserialize, serialize, Schema

a = TypedBytes('application/json', b'{"x": 5}') | Auto
assert str(a) == 'Auto {\'x\': 5}'

print(Schema)
