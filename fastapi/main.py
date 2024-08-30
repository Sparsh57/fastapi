import fastapi
from typing import *
from pydantic import BaseModel
import sqlite3
from contextlib import closing


class Database:
    def __init__(self):
        self.db = sqlite3.connect('todolist.db', check_same_thread=False)

    def initialize_database(self):
        try:
            with closing(self.db.cursor()) as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS todolist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    status TEXT
                )""")
                self.db.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def add(self, text, status):
        try:
            with closing(self.db.cursor()) as cur:
                cur.execute("INSERT INTO todolist (text, status) VALUES (?, ?)", (text, status))
                self.db.commit()
        except sqlite3.Error as e:
            print(f"Error adding item: {e}")

    def extract(self):
        try:
            with closing(self.db.cursor()) as cur:
                results = cur.execute("SELECT id, text, status FROM todolist").fetchall()
                return [{'id': row[0], 'text': row[1], 'status': row[2]} for row in results]
        except sqlite3.Error as e:
            print(f"Error extracting items: {e}")
            return []

    def extract_status(self, value):
        try:
            with closing(self.db.cursor()) as cur:
                results = cur.execute("SELECT id, text, status FROM todolist WHERE status=?", (value,)).fetchall()
                return [{'id': str(row[0]), 'text': row[1], 'status': row[2]} for row in results] if results else []
        except sqlite3.Error as e:
            print(f"Error extracting items by status: {e}")
            return []

    def extract_id(self, id):
        try:
            with closing(self.db.cursor()) as cur:
                result = cur.execute("SELECT id, text, status FROM todolist WHERE id=?", (id,)).fetchone()
                if result:
                    return {'id': result[0], 'text': result[1], 'status': result[2]}
                return None
        except sqlite3.Error as e:
            print(f"Error extracting item by id: {e}")
            return None

    def last_id(self):
        try:
            with closing(self.db.cursor()) as cur:
                result = cur.execute("SELECT id FROM todolist ORDER BY id DESC LIMIT 1").fetchone()
                if result:
                    return result[0]
                return 0
        except sqlite3.Error as e:
            print(f"Error fetching last id: {e}")
            return 0

    def remove(self, id):
        try:
            with closing(self.db.cursor()) as cur:
                cur.execute("DELETE FROM todolist WHERE id=?", (id,))
                self.db.commit()
        except sqlite3.Error as e:
            print(f"Error removing item: {e}")

    def update(self, id, text, status):
        try:
            with closing(self.db.cursor()) as cur:
                cur.execute("UPDATE todolist SET text=(?), status=(?) WHERE id=(?)", (text, status, id))
                self.db.commit()
        except sqlite3.Error as e:
            print(f"Error updating item: {e}")


app = fastapi.FastAPI()
db = Database()
db.initialize_database()


@app.get("/todolist")
def todolist(filter: str = "all"):
    if filter == "completed":
        return db.extract_status("completed")
    if filter == "pending":
        return db.extract_status("pending")
    if filter == "all":
        return db.extract()
    raise fastapi.HTTPException(status_code=400, detail="Invalid filter name")


def get_item_by_id(id: int):
    item = db.extract_id(id)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Not found")
    return item


@app.get("/todolist/{id}")
def get_item(id: int):
    return get_item_by_id(id)


class TodoItem(BaseModel):
    text: str



def success(**kwargs):
    return {"status": "success", **kwargs}


@app.post("/todolist")
def new_item(item: TodoItem):
    item.text = TodoItem.validate_text(item.text)
    newid = db.last_id() + 1
    db.add(item.text, "pending")
    return success(url=f"/todolist/{newid}")


class ItemMods(BaseModel):
    text: Optional[str] = None
    done: Optional[str] = None

    def validate_and_update(self, item):
        self.text = self.text.strip() if self.text else item['text']
        self.text = TodoItem.validate_text(self.text)
        self.done = "completed" if self.done else "pending"


@app.put("/todolist/{id}")
def mod_item(id: int, mods: ItemMods):
    item = get_item_by_id(id)
    mods.validate_and_update(item)
    db.update(id, mods.text, mods.done)
    return success()


@app.delete("/todolist/{id}")
def del_item(id: int):
    db.remove(id)
    return success()