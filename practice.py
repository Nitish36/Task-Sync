from database import NoteDatabase

note_db = NoteDatabase()  # Initialize the database class
notes = note_db.get_note()  # Call the method
print(f"Notes retrieved: {notes}")  # Confirm output