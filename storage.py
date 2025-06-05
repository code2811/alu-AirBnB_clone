#!/usr/bin/python3
"""
FileStorage module for AirBnB Clone
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to JSON file and deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    # Dictionary mapping class names to class objects
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def all(self):
        """Return the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)"""
        serialized_objects = {}
        
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()
        
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserialize the JSON file to __objects (if the JSON file exists)"""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                for key, obj_dict in data.items():
                    class_name = obj_dict['__class__']
                    
                    if class_name in self.classes:
                        # Create instance of the appropriate class
                        cls = self.classes[class_name]
                        obj = cls(**obj_dict)
                        FileStorage.__objects[key] = obj
                        
        except FileNotFoundError:
            # File doesn't exist yet, which is fine
            pass
        except (json.JSONDecodeError, KeyError):
            # Invalid JSON or missing required keys
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it exists"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()

    def get(self, cls, id):
        """Retrieve an object by class and id"""
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return FileStorage.__objects.get(key, None)
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is None:
            return len(FileStorage.__objects)
        else:
            count = 0
            for key in FileStorage.__objects.keys():
                if key.startswith(cls.__name__ + "."):
                    count += 1
            return count
