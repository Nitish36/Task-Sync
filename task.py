from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem,ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from database import Database
import re

db = Database()



class Home(MDScreen):
    pass


class Task(MDScreen):
    pass


class RegLog(MDScreen):
    pass


class Register(MDScreen):
    pass


class Login(MDScreen):
    pass

 

  
class DialogContent(MDBoxLayout):
    """def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")"""
   

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
 
        date_dialog.open()
  
   

    def on_save(self,instance,value,date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)
 

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk
        
    def mark(self,check,the_list_item):
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_completed(the_list_item.pk)
        
        else:
            the_list_item.text = str(db.mark_task_as_incompleted(the_list_item.pk))
    
    def delete_item(self,the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBody,MDCheckbox):
    pass



  
class TaskManager(MDApp):
    task_list_dialog = None
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = None

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title = "Create Task",
                type = "custom",
                content_cls = DialogContent()
            )
        self.task_list_dialog.open()

 
    def add_task(self, task_text_widget, task_date):
        try:
            # Extract the text from the TextInput widget
            task_text = task_text_widget.text  # Get the actual string from the widget
            
            # Create the task in the database
            created_task = db.create_task(task_text, task_date)
            
            # Access the Task screen
            task_screen = self.root.get_screen('Task')  # Ensure the screen name matches the .kv file
            container = task_screen.ids.container  # Access the container inside the Task screen
            
            # Add the created task as a widget in the container
            container.add_widget(
                ListItemWithCheckbox(
                    pk=created_task[0],  # Primary key from the database
                    text=f"[b]{created_task[1]}[/b]",  # Task text
                    secondary_text=created_task[2]  # Task date
                )
            )
        except KeyError as e:
            print(f"KeyError: {e}. Ensure the 'container' ID is correctly defined in the .kv file.")
        except Exception as e:
            print(f"Unexpected error: {e}")


        

    def close_dialog(self,**kwargs):
        if self.task_list_dialog:
            self.task_list_dialog.dismiss()

  
    def on_start(self):
        try:
            # Fetch incompleted and completed tasks from the database
            incompleted_tasks, completed_tasks = db.get_tasks()

            # Access the Task screen container
            task_screen = self.root.get_screen('Task')
            container = task_screen.ids.container

            # Add incompleted tasks
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(
                    pk=task[0],  # Task ID from the database
                    text=f"[b]{task[1]}[/b]",  # Task name
                    secondary_text=task[2]  # Task date
                )
                container.add_widget(add_task)

            # Add completed tasks
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(
                    pk=task[0],  # Task ID from the database
                    text=f"[s]{task[1]}[/s]",  # Strikethrough for completed tasks
                    secondary_text=task[2]  # Task date
                )
                add_task.ids.check.active = True  # Check the checkbox for completed tasks
                container.add_widget(add_task)
        except Exception as e:
            print(f"Error loading tasks: {e}")





   
    def set_error_message(self, instance_textfield):
        instance_textfield.error = True

    def build(self):
        self.screen = Builder.load_file("task.kv")
        return self.screen

    def on_kv_post(self, base_widget):
        # Bind the events after the kv file is fully loaded
        if hasattr(self.screen.ids, "text_field_error"):
            self.screen.ids.username_text.bind(
                on_text_validate=self.set_error_message,
                on_focus=self.set_error_message,
            )
        else:
            print("Warning: 'text_field_error' ID not found in practice.kv")

    def validate_email(self, instance, value):
        # Regular expression for validating email
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, value):
            instance.error = False
        else:
            instance.error = True

    def toggle_password_visibility(self):
        password_field = self.root.ids.password_field
        password_field.password = not password_field.password


if __name__ == "__main__":
    TaskManager().run()