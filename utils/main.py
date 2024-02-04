import os
import uuid

documentation_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "documentation/")


def generate_uuid() -> str:
    """
    Generate a unique identifier

    :return: A unique identifier
    """
    return str(uuid.uuid4())


def load_documentation(filename) -> str:
    """
    Load documentation from a file

    :param filename: The name of the file to load
    :return: The content of the file
    """
    with open(os.path.join(documentation_path, filename), "r") as doc:
        return doc.read()
