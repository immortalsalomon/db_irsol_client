# libraries dependencies
import hashlib


def get_file_md5(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()


# Remove string variable not needed (empty, all whitespace, with placeholder(<, >) )
def filter_string_parameters(parameters):
    to_remove_keys = []

    for key, value in parameters.items():
        if isinstance(value, str) and (len(value) == 0 or value.isspace() or '>' in value or '<' in value):
            to_remove_keys.append(key)

    for to_remove_key in to_remove_keys:
        parameters.pop(to_remove_key)

    return parameters
