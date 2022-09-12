# Copyright (c) 2022 laurence mark

from sqlite3 import connect


class mark_Database():
    """
    Database of Database Of Mark AI
        This database won't be used if you're hosting this on heroku
    """

    def __init__(self) -> None:
        self.mark_db = connect("mark-x.db")
        self.curs = self.mark_db.cursor()
        # Creates a table for storing ai engine details
        self.curs.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            engine (engine_name text)
            """
        )

    async def set_engine(self, engine_name):
        is_exists = await self.get_engine()
        if not is_exists:
            self.curs.execute(
                """
                INSERT INTO engine(engine_name)
                VALUES (?)
                """, (engine_name,)
            )
        else:
            self.curs.execute(
                """
                UPDATE engine
                SET engine_name=?
                """, (engine_name,)
            )
        return self.mark_db.commit()
    
    async def get_engine(self):
        selct = self.curs.execute(
            """
            SELECT engine_name
            FROM engine
            """
        ).fetchone()
        if selct:
            return selct[0]
        else:
            return None