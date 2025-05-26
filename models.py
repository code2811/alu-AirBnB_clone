#!/usr/bin/python3
"""This module defines the BaseModel class."""

import uuid
from datetime import datetime
import models


class BaseModel:
    """BaseModel class defines common attributes/methods for other classes.

    Attributes:
        id (str): unique id for each BaseModel instance
        created_at (datetime): datetime when instance is created
        updated_at (datetime): datetime when instance is last updated
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: Variable length argument list (unused)
            **kwargs: Arbitrary keyword arguments for instance attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return string representation of BaseModel instance.

        Returns:
            str: String representation in format [ClassName] (id) {attributes}
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at attribute with current datetime and save."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation of BaseModel instance.

        Returns:
            dict: Dictionary containing all keys/values of instance
        """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
