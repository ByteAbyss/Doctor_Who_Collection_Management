import sqlite3
import os

fileDir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(fileDir, 'time_vortex.db')

class DatabaseConnection:

    def __init__(self):
        self.conn = None

    def __enter__(self):   # Enter the Context Manager --> Do this ...
        self.conn = sqlite3.connect(filename)
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):   #  Exit the Context Manager --> Do this ...
        if exc_tb or exc_type or exc_val:       # If it throws an error close the connection so it does not commit.
            self.conn.close()
        else:       # No errors -- commit & close.
            self.conn.commit()
            self.conn.close()


# If table object is null create one
with DatabaseConnection() as conn:
        TABLE = 'Who'

        sql_create = f"""
          CREATE TABLE IF NOT Exists {TABLE}
          (Title nvarchar(75),
          Series_Run nvarchar(25),
          Season nvarchar(25),
          Story_Aired nvarchar(25),
          Season_URL nvarchar(500),
          Episodes nvarchar(25),
          Doctor_Incarnation nvarchar(25),
          Actor nvarchar(75),
          Companions nvarchar(255),
          Monster nvarchar(75),
          Setting nvarchar(75),
          Synopsis nvarchar(500),
          Collected nvarchar(10),
          PRIMARY KEY (Title, Series_Run));  """

        md_create = conn.cursor()
        md_create.execute(sql_create)

