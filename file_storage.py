#!/usr/bin/python3
"""This module defines the FileStorage class."""

import json
import os


class FileStorage:
    """FileStorage serializes instances to JSON file and deserializes back.

    Attributes:
        __file_path (str): path to the JSON file
        __objects (dict): dictionary to store all objects by <class name>.id
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects.

        Returns:
            dict: Dictionary containing all stored objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id.

        Args:
            obj: Object to be stored
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)."""
        json_dict = {}
        for key, obj in FileStorage.__objects.items():
            json_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_dict, f)

    def reload(self):
        """Deserialize JSON file to __objects (only if JSON file exists)."""
        if os.path.exists(FileStorage.__file_path):
            try:
                with open(FileStorage.__file_path, 'r') as f:
                    json_dict = json.load(f)

                 
                from models.base_model import BaseModel
                from models.user import User
                from models.state import State
                from models.city import City
                from models.amenity import Amenity
                from models.place import Place
                from models.review import Review

                classes = {
                    'BaseModel': BaseModel,
                    'User': User,
                    'State': State,
                    'City': City,
                    'Amenity': Amenity,
                    'Place': Place,
                    'Review': Review
                }

                for key, value in json_dict.items():
                    class_name = value['__class__']
                    del value['__class__']
                    cls = classes[class_name]
                    FileStorage.__objects[key] = cls(**value)
            except (IOError, ValueError, KeyError):
                pass
