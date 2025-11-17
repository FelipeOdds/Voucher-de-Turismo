import reflex as rx
from app.models import init_db
from app.db import get_session


class InitState(rx.State):
    db_initialized: bool = False

    @rx.event
    async def initialize_database(self):
        if self.db_initialized:
            return
        print("Initializing database...")
        await init_db()
        self.db_initialized = True
        print("Database initialized successfully.")