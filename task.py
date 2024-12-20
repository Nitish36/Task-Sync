from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from database import Database,NoteDatabase
from kivy.core.window import Window

Window.size = (500, 600)

db = Database()
db1 = NoteDatabase()


class Home(MDScreen):
    pass


class Workspace(MDScreen):
    pass

class NoteTaking(MDScreen):
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
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)



class ListItemWithCheckbox(TwoLineAvatarIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database
        # primary keys
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

class ListItemWithCheckboxNote(TwoLineAvatarIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database
        # primary keys
        self.pk = pk


    def delete_note(self,the_note_item):
        self.parent.remove_widget(the_note_item)
        db1.delete_note(the_note_item.pk)


class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

class NoteDialogContent(MDBoxLayout):
    """def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")"""
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


class TaskManager(MDApp):
    task_list_dialog = None
    note_list_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snackbar = None
        self._interval = 0
        self.screen = Builder.load_file("task.kv")

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent()
            )
        self.task_list_dialog.open()

    def add_task(self, task_text_widget, task_date):
        task_text = task_text_widget.text
        # Create the task in the database
        created_task = db.create_task(task_text, task_date)
        # Access the Task screen
        task_screen = self.root.get_screen('Task')
        container = task_screen.ids.container
        # Add the created task as a widget in the container
        container.add_widget(
            ListItemWithCheckbox(
                pk=created_task[0],  # Primary key from the database
                text=f"[b]{created_task[1]}[/b]",  # Task text
                secondary_text=created_task[2]  # Task date
            )
        )

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
                    text=f"[s]{task[1]}[/s]",
                    secondary_text=task[2]  # Task date
                )
                add_task.ids.check.active = True
                container.add_widget(add_task)
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def set_error_message(self, instance_textfield):
        instance_textfield.error = True

    def build(self):
        return self.screen

    def show_note_dialog(self):
        if not self.note_list_dialog:
            self.note_list_dialog = MDDialog(
                title="Create Note",
                type="custom",
                content_cls=NoteDialogContent()
            )
        self.note_list_dialog.open()

    def add_note(self, note_text_widget, note_date):
        note_text = note_text_widget.text
        # Create the task in the database
        created_note = db1.create_note(note_text, note_date)
        # Access the Task screen
        task_screen = self.root.get_screen('NoteTaking')
        container = task_screen.ids.container
        # Add the created task as a widget in the container
        container.add_widget(
            ListItemWithCheckboxNote(
                pk=created_note[0],  # Primary key from the database
                text=f"[b]{created_note[1]}[/b]",  # Task text
                secondary_text=created_note[2]  # Task date
            )
        )

    def close_note_dialog(self,**kwargs):
        if self.note_list_dialog:
            self.note_list_dialog.dismiss()

    def on_note_start(self):
        try:
            # Fetch notes from the database
            completed_notes = db1.get_note()

            # Access the NoteTaking screen container
            note_screen = self.root.get_screen('NoteTaking')

            # Ensure the container exists and is accessible
            container = getattr(note_screen.ids, 'container', None)
            if container is None:
                raise AttributeError("Container with id 'container' not found in NoteTaking screen.")

            # Clear existing notes (if needed)
            container.clear_widgets()

            # Add notes to the UI
            for note in completed_notes:
                add_note = ListItemWithCheckboxNote(
                    pk=note[0],  # Note ID from the database
                    text=f"[b]{note[1]}[/b]",  # Note text
                    secondary_text=note[2]  # Note date
                )
                container.add_widget(add_note)

            print(f"Notes loaded into UI: {completed_notes}")
        except Exception as e:
            print(f"Error loading tasks: {e}")




if __name__ == "__main__":
    TaskManager().run()