def get_nested_value(obj, key):
    # Split the key by the '/' delimiter
    keys = key.split('/')
    
    # Iterate over the keys and navigate through the nested dictionary
    for k in keys:
        if k in obj:
            obj = obj[k]
        else:
            return None  # Return None if the key is not found at any level
    return obj

# Example usage:
object1 = {"a": {"b": {"c": "d"}}}
key1 = "a/b/c"
value1 = get_nested_value(object1, key1)
print(value1)  # Output: d

object2 = {"x": {"y": {"z": "a"}}}
key2 = "x/y/z"
value2 = get_nested_value(object2, key2)
print(value2)  # Output: a