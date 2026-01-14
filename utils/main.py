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


import random


def generate_otp():
    otp = random.randint(100000, 999999)
    return otp


def add_tag_groups(result, generator, request, public):
    result['x-tagGroups'] = [
        {
            'name': 'User Management',
            'tags': ['Auth', 'User']
        },
        {
            'name': 'Event Management',
            'tags': ['Reservations', 'Events', 'Speakers', 'File Upload']
        },
        {
            'name': 'Projects',
            'tags': ['Projects']
        },
        {
            'name': 'Blog Management',
            'tags': ['Blog', 'Posts', 'Comments']
        }
    ]
    return result
