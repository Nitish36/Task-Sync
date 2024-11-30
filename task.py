from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.dialog import MDDialog
import re

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

    def on_save(self,instance,value,date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)
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

    def close_dialog(self,**kwargs):
        self.task_list_dialog.dismiss()


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

TaskManager().run()