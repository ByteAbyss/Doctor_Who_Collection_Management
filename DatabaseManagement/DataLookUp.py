from DatabaseManagement.Connector import DatabaseConnection

datasource = 'Who'

def doctors(table=datasource):
    """ Grab # & Actor Name for all the doctors in the table
    :param table: Source Table
    :return: Tuple #) Actor ( Years Portrayed )  """

    with DatabaseConnection() as conn:
        doctor = conn.cursor()
        doc_list = f"""select distinct Actor, Doctor_Incarnation from {table}"""
        docs = [(f' {x[1].zfill(2)}) {x[0]}') for x in doctor.execute(doc_list) if x[0] != 'Not Listed']
        docs.sort()
        return docs


def last_episode(table=datasource):
    with DatabaseConnection() as conn:
        epi = conn.cursor()
        last = f"""select max(cast(Story_Aired as int)) from Who"""
        last_aired_db = [x for x in epi.execute(last,)]
        return last_aired_db[0][0]


# look_up(title=name, aired=aired)
def look_up(all=0, doctor=0, title=None, acquired='Yes', aired=None,  table=datasource):
    """  --  Database Look Up tool based on common search criteria in parameters. --
    :param all:  True 1 : False  0 -- Return all
    :param doctor:  Doctor Incarnation #
    :param title: Name of Story -- Matches "Like" terms.
    :param acquired: In Collection / Status : Yes , No , Ordered , Partial
    :param table: Data Source
    :return: namedtuple of table elements  """

    with DatabaseConnection() as conn:
        search = conn.cursor()

        all_search = F"""select * from {table} order by   cast(Story_Aired as int) """

        doc_search = F"""select * from {table} 
                         where Doctor_Incarnation != 'N/A'  
                         and Doctor_Incarnation = ? 
                         order by  cast(Story_Aired as int) """

        name_search = f"""select * from {table}
                          where Title like ?
                          order by cast(Story_Aired as int)"""

        uid_search = f"""select * from {table}
                         where Title like ? and Story_Aired = ? """

        pending = f"""select * from {table} where Collected != 'Yes' order by  cast(Story_Aired as int) """

        collected = f"""select * from {table} where Collected = 'Yes' order by  cast(Story_Aired as int) """


        if doctor:
            return [x for x in search.execute(doc_search, (doctor,))]

        if all:
            return [x for x in search.execute(all_search)]

        if aired and title:
            return [x for x in search.execute(uid_search, (f'%{title}%', aired))]

        if title:
            return [x for x in search.execute(name_search, (f'%{title}%',))]

        if acquired != 'Yes':
            return [x for x in search.execute(pending, )]

        if acquired == 'Yes':
            return [x for x in search.execute(collected, )]