from jsonschema import RefResolver, Draft7Validator
import json
import os.path
import os

META_DIR = os.path.abspath("meta")
SCHEMA_DIR = os.path.abspath("schema")
VALID_DATA_DIR = os.path.abspath("data")


def get_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


def get_schema(name):
    schema = get_json(f"schema/{name}.json")
    return schema


def validate(instance, schema):
    resolver = RefResolver(base_uri=f'file://{SCHEMA_DIR}/', referrer=schema)
    v = Draft7Validator(schema, resolver=resolver)
    return v.iter_errors(instance)


def main():
    errors = []

    # validate schema
    meta_json = get_json(os.path.join(META_DIR, "schema.json"))
    for schema_name in os.listdir(SCHEMA_DIR):
        full_name = os.path.join(SCHEMA_DIR, schema_name)
        schema_json = get_json(full_name)
        for e in validate(schema_json, meta_json):
            errors.append(f"{schema_name}: {e.message}")

    if errors:
        print("Invalid schema")
        for e in errors:
            print(e)
        exit(1)

    # validate data
    for schema_name in os.listdir(VALID_DATA_DIR):
        schema = get_schema(schema_name)

        examples_dir = os.path.join(VALID_DATA_DIR, schema_name)
        for file_name in os.listdir(examples_dir):
            full_name = os.path.join(examples_dir, file_name)
            data = get_json(full_name)
            for e in validate(instance=data, schema=schema):
                errors.append(f"{file_name}: {e.message}")

    if errors:
        print("Invalid data")
        for e in errors:
            print(e)
        exit(1)


if __name__ == "__main__":
    main()

