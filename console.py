#!/usr/bin/python3
"""
Console for AirBnB Clone - Command Interpreter
"""
import cmd
import re
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""

    prompt = '(hbnb) '
    
    # Dictionary of all available classes
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing when empty line is entered"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class
        Usage: create <class_name>
        """
        if not arg:
            print("** class name missing **")
            return
        
        if arg not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show string representation of an instance
        Usage: show <class_name> <id>
        """
        args = arg.split()
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
            
        print(objects[key])

    def do_destroy(self, arg):
        """Delete an instance based on class name and id
        Usage: destroy <class_name> <id>
        """
        args = arg.split()
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
            
        del objects[key]
        storage.save()

    def do_all(self, arg):
        """Print all string representations of instances
        Usage: all [class_name]
        """
        objects = storage.all()
        result = []
        
        if not arg:
            # Show all instances
            for obj in objects.values():
                result.append(str(obj))
        else:
            # Show instances of specific class
            if arg not in self.classes:
                print("** class doesn't exist **")
                return
            
            for key, obj in objects.items():
                if key.startswith(arg + "."):
                    result.append(str(obj))
        
        print(result)

    def do_update(self, arg):
        """Update an instance by adding or updating attribute
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        args = self.parse_args(arg)
        
        if not args:
            print("** class name missing **")
            return
            
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
            
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
            
        if len(args) < 3:
            print("** attribute name missing **")
            return
            
        if len(args) < 4:
            print("** value missing **")
            return

        obj = objects[key]
        attr_name = args[2]
        attr_value = args[3]
        
        # Convert value to appropriate type
        if hasattr(obj, attr_name):
            current_type = type(getattr(obj, attr_name))
            try:
                if current_type == int:
                    attr_value = int(attr_value)
                elif current_type == float:
                    attr_value = float(attr_value)
            except ValueError:
                pass
        
        setattr(obj, attr_name, attr_value)
        obj.save()

    def parse_args(self, arg):
        """Parse arguments handling quoted strings"""
        args = []
        current_arg = ""
        in_quotes = False
        
        for char in arg:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
            else:
                current_arg += char
        
        if current_arg:
            args.append(current_arg)
        
        return args

    def default(self, line):
        """Handle advanced command syntax: <class>.<command>()"""
        match = re.match(r"(\w+)\.(\w+)\((.*)\)", line)
        if match:
            class_name = match.group(1)
            command = match.group(2)
            args_str = match.group(3)
            
            if class_name in self.classes:
                if command == "all":
                    self.do_all(class_name)
                elif command == "count":
                    self.do_count(class_name)  
                elif command == "show":
                    args = args_str.strip('"')
                    self.do_show("{} {}".format(class_name, args))
                elif command == "destroy":
                    args = args_str.strip('"')
                    self.do_destroy("{} {}".format(class_name, args))
                elif command == "update":
                    # Handle update with dictionary or individual attributes
                    if "{" in args_str and "}" in args_str:
                        # Dictionary update format
                        self.handle_dict_update(class_name, args_str)
                    else:
                        # Individual attribute update
                        args = re.findall(r'"([^"]*)"', args_str)
                        if len(args) >= 3:
                            self.do_update("{} {} {} \"{}\"".format(
                                class_name, args[0], args[1], args[2]))
                else:
                    print("*** Unknown syntax: {}".format(line))
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_count(self, arg):
        """Count instances of a class
        Usage: count <class_name> or <class_name>.count()
        """
        if not arg:
            print("** class name missing **")
            return
            
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        
        objects = storage.all()
        count = 0
        
        for key in objects.keys():
            if key.startswith(arg + "."):
                count += 1
        
        print(count)

    def handle_dict_update(self, class_name, args_str):
        """Handle update with dictionary format"""
        try:
            # Extract ID and dictionary
            parts = args_str.split(", {", 1)
            obj_id = parts[0].strip('"')
            dict_str = "{" + parts[1]
            
            # Parse dictionary
            update_dict = json.loads(dict_str.replace("'", '"'))
            
            # Apply updates
            for attr_name, attr_value in update_dict.items():
                self.do_update("{} {} {} \"{}\"".format(
                    class_name, obj_id, attr_name, attr_value))
        except (ValueError, IndexError, json.JSONDecodeError):
            print("** invalid dictionary format **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
