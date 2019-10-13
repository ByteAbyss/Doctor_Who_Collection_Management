import logging
import sqlite3
from .Connector import DatabaseConnection

# Time, Level (-# = min char length) , File, Line of error in file , Message
# Date Format D-M-Y H:M:S
# Debugging Level
# Name of file to write log to.
logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s: %(lineno)d] %(message)s',
                    datefmt='%d-%-m-%y %H:%M:%S',
                    level=logging.INFO,
                    filename='Doctor_Who_Episode_logger.txt')

# Adjust Level as you develop -- lowest level --> Production
logger = logging.getLogger('DW')
logger.info('Logger Starting')
error = 0


def add_record(Title: str, Series_Run: str, Season: int, Story_Aired: int, Season_URL: str, Episodes: int,
               Doctor_Incarnation: int, Actor: str, Companions: str, Monster: str, Setting: str, Synopsis: str,
               Collected='No'):
    """Append Records to the database."""
    TABLE = 'Who'
    global logger
    with DatabaseConnection() as conn:

        # Insert Values into the table
        try:
            sql_insert = f'Insert into {TABLE} values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

            md_ins = conn.cursor()  # Executes SQL Code
            md_ins.execute(sql_insert, (Title, Series_Run, Season, Story_Aired, Season_URL, Episodes, Doctor_Incarnation,
                                        Actor, Companions, Monster, Setting, Synopsis, Collected))
        except sqlite3.IntegrityError:  # Duplication of Primary Key
                global error
                error += 1
                logger.info(f'Duplicate -->\n {Title}, {Series_Run}, {Story_Aired}, {Season_URL}, {Episodes}, '
                            f'{Doctor_Incarnation},  {Actor}, {Companions}, {Monster}, {Setting}, {Synopsis} \n\n')
                print(f'{Title} --> {Series_Run} exists already. --> Error # {error}')


def acquired(aired, title, change):
    TABLE = 'Who'
    with DatabaseConnection() as conn:
        dml = conn.cursor()

        # Change by index:  ['Acquired', 'Partial Acquisition', 'On Order', 'Removed']

        acquired = f"""update {TABLE}
                     set Collected = 'Yes'
                     where Title like ? and Story_Aired = ? """

        partial = f"""update {TABLE}
                      set Collected = 'Partial'
                      where Title like ? and Story_Aired = ? """

        on_order = f"""update {TABLE}
                       set Collected = 'Ordered'
                       where Title like ? and Story_Aired = ? """

        removed =  f""" update {TABLE}
                        set Collected = 'No' 
                        where Title like ? and Story_Aired = ? """

        if change == 0:
            dml.execute(acquired, (title, aired))
        elif change == 1:
            dml.execute(partial, (title, aired ))
        elif change == 2:
            dml.execute(on_order, (title, aired))
        elif change == 3:
            dml.execute(removed, (title,aired))
