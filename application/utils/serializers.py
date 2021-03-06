import json

def serialize_one(result):
    return json.dumps(result.to_dict())

def serialize_many(results):
    serialized = [res.to_dict() for res in results]
    return json.dumps(serialized)

# input result as dictionary 
def serialize_dictionary(result):
    return json.dumps(result)