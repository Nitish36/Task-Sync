import sqlite3


class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("""Create Table If Not Exists tasks 
                            (
                                ID integer PRIMARY KEY AUTOINCREMENT,
                                task varchar(50) NOT NULL,due_date VARCHAR(50),
                                completed BOOLEAN NOT NULL CHECK (completed IN (0,1))
                            )""")
        self.con.commit()

    def create_task(self, task, due_date=None):
        self.cursor.execute("Insert Into tasks(task,due_date,completed) VALUES(?,?,?)", (task, due_date, 0))
        self.con.commit()

        created_task = self.cursor.execute("Select id,task,due_date FROM tasks WHERE task=? and completed=0",
                                           (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        try:
            # Fetch incompleted tasks
            self.cursor.execute("SELECT * FROM tasks WHERE completed=0")
            incompleted_tasks = self.cursor.fetchall()

            # Fetch completed tasks
            self.cursor.execute("SELECT * FROM tasks WHERE completed=1")
            completed_tasks = self.cursor.fetchall()

            return incompleted_tasks, completed_tasks
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return [], []

    def mark_task_as_completed(self, taskid):
        self.cursor.execute("Update tasks SET completed=1 WHERE id = ?", (taskid,))
        self.con.commit()

    def mark_task_as_incompleted(self, taskid):
        self.cursor.execute("Update tasks SET completed=0 WHERE id = ?", (taskid,))
        self.con.commit()

        task_text = self.cursor.execute("SELECT task from tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()