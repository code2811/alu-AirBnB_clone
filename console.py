#!/usr/bin/python3
"""Console module for AirBnB clone."""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone."""
    
    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel."""
        if not arg:
            print("** class name missing **")
            return
        
        if arg not in self.__classes:
            print("** class doesn't exist **")
            return
            
        new_instance = self.__classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show string representation of an instance."""
        args = arg.split()
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return
            
        print(models.storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on class name and id."""
        args = arg.split()
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return
            
        del models.storage.all()[key]
        models.storage.save()

    def do_all(self, arg):
        """Print all string representations of instances."""
        obj_list = []
        
        if not arg:
            for obj in models.storage.all().values():
                obj_list.append(str(obj))
        else:
            if arg not in self.__classes:
                print("** class doesn't exist **")
                return
            for key, obj in models.storage.all().items():
                if key.startswith(arg):
                    obj_list.append(str(obj))
                    
        print(obj_list)

    def do_update(self, arg):
        """Update an instance based on class name and id."""
        args = arg.split()
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return
            
        if len(args) < 3:
            print("** attribute name missing **")
            return
            
        if len(args) < 4:
            print("** value missing **")
            return
            
        obj = models.storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip('"')
        
        # Try to cast the value to the correct type
        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                attr_value = attr_type(attr_value)
            except ValueError:
                pass
        
        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
