import pickle
import yaml


def deserialize_pickle(data):
    # Unsafe deserialization from untrusted source
    return pickle.loads(data)


def deserialize_yaml(data):
    # Unsafe deserialization using yaml.load which could execute arbitrary code
    return yaml.load(data, Loader=yaml.FullLoader)


# Simulate receiving data from an untrusted source
dangerous_pickle_data = b"cos(system('ls'))"  # This is a placeholder for dangerous pickle data
dangerous_yaml_data = "!!python/object/apply:os.system ['ls']"

if __name__ == "__main__":
    result_pickle = deserialize_pickle(dangerous_pickle_data)
    result_yaml = deserialize_yaml(dangerous_yaml_data)
    print(result_pickle, result_yaml)
