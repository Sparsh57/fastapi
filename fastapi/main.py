import fastapi
from typing import *
from pydantic import BaseModel
import sqlite3
from contextlib import closing


class Database:
    def __init__(self):
        self.db = sqlite3.connect('todolist.db', check_same_thread=False)

    def initialize_database(self):
        with closing(self.db.cursor()) as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS todolist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                status TEXT
            )""")

    def add(self, text, status):
        with closing(self.db.cursor()) as cur:
            cur.execute("INSERT INTO todolist (text, status) VALUES (?, ?)", (text, status))
            self.db.commit()

    def extract(self):
        with closing(self.db.cursor()) as cur:
            results = cur.execute("SELECT id, text, status FROM todolist").fetchall()
            result_dict = [{'id': row[0], 'text': row[1], 'status': row[2]} for row in results]
            return result_dict

    def extract_status(self, value):
        with closing(self.db.cursor()) as cur:
            results = cur.execute("SELECT id, text, status FROM todolist WHERE status=?", (value,)).fetchall()
            result_dict = None
            if results is not None:
                result_dict = [{'id': str(row[0]), 'text': row[1], 'status': row[2]} for row in results]
            return result_dict

    def extract_id(self, id):
        with closing(self.db.cursor()) as cur:
            result = cur.execute("SELECT id, text, status FROM todolist WHERE id=?", (id,)).fetchone()
            if result is not None:
                return {'id': result[0], 'text': result[1], 'status': result[2]}
            return None

    def last_id(self):
        with closing(self.db.cursor()) as cur:
            result = cur.execute("SELECT id FROM todolist ORDER BY id DESC LIMIT 1").fetchone()
            if result is not None:
                return result[0]
            return 0

    def remove(self, id):
        with closing(self.db.cursor()) as cur:
            cur.execute("DELETE FROM todolist WHERE id=?", (id,))
            self.db.commit()

    def update(self, id, text, status):
        with closing(self.db.cursor()) as cur:
            cur.execute("UPDATE todolist SET text=(?), status=(?) WHERE id=(?)", (text, status, id))
            self.db.commit()


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
    newid = db.last_id() + 1
    db.add(item.text, "pending")
    return success(url=f"/todolist/{newid}")


class ItemMods(BaseModel):
    text: Optional[str] = None
    done: Optional[str] = None


@app.put("/todolist/{id}")
def mod_item(id: int, mods: ItemMods):
    item = get_item_by_id(id)
    updated_text = mods.text if mods.text is not None else item['text']
    updated_status = "completed" if mods.done else "pending"
    db.update(id, updated_text, updated_status)
    return success()


@app.delete("/todolist/{id}")
def del_item(id: int):
    db.remove(id)
    return success()
