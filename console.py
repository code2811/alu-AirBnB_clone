#!/usr/bin/python3
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review

class_map = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "City": City,
    "State": State,
    "Amenity": Amenity,
    "Review": Review
}

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def emptyline(self):
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        print()
        return True

    def do_create(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in class_map:
            print("** class doesn't exist **")
            return
        instance = class_map[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        args = shlex.split(arg)
        objects = storage.all()
        if args and args[0] not in class_map:
            print("** class doesn't exist **")
            return
        result = []
        for obj in objects.values():
            if not args or obj.__class__.__name__ == args[0]:
                result.append(str(obj))
        print(result)

    def do_update(self, arg):
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3].strip('"'))
        obj.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()

