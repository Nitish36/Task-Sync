from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
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
class TaskManager(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = None

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
