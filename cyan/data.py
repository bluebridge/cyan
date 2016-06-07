"""
    ---------------------------------------------------------------------

    This module contains functions that related to manipulate data.

    Note:
        *To see what options (providers) available with Faker, please refer to:*
        `fake-factory <http://fake-factory.readthedocs.org/en/latest/providers/base.html>`_

    ---------------------------------------------------------------------
"""

import string

from faker import Faker
import pypyodbc

from . import common, security

fake = Faker()


def sql_execute(sql: string):
    """
    Execute a SQL statement into the DB

    :param sql: The SQL statement to be executed.
    """
    security.check_self()
    conn = pypyodbc.connect(common.connection_string)
    cur = conn.cursor()
    cur.execute(sql)
    cur.commit()
    cur.close()
    conn.close()


def sql_select(sql: string) -> string:
    """
    Fetch a record set from DB by executing a SQL statement

    :param sql: The SQL statement that contain the select
    :return: string type
    """
    security.check_self()

    conn = pypyodbc.connect(common.connection_string)
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()
    cur.commit()
    cur.close()
    conn.close()
    return row


def sql_execute_file(path: string):
    """
    Execute a SQL statement from a file system into the DB

    :param path: The path the file that contains the sql statement/s
    """
    security.check_self()

    f = open(path, 'r')

    sql = f.read()
    sql_execute(sql)

    f.close()


def sql_execute_files(files, fetch_type: common.CursorFetchType = common.CursorFetchType.All):
    conn = pypyodbc.connect(common.connection_string)
    cur = conn.cursor()

    for file in files:
        sql = read_file_text(file)
        cur.execute(sql)

    print(fetch_type)
    data = {
        0: lambda x: None,
        1: lambda x: x.fetchone(),
        2: lambda x: x.fetchall(),
        3: lambda x: x.fetchmany()
    }[fetch_type.value](cur)

    # data = cur.fetchall()
    conn.commit()

    cur.close()
    conn.close()

    return data


def convert_rows_to_array(rows):
    """
    Convert rows to an array

    :param rows: The input row

    :return: (array) The convert rows
    """
    result = []
    count = len(rows)
    for x in range(0, count):
        result.append(rows[x][0])
    result.sort()
    return result


def read_file_text(path):
    f = open(path, 'r')

    return f.read()


def get_random_text(prefix: string) -> string:
    """
    Get a random word post-fixed with a random number

    :param prefix: The prefix for the random text
    :return: A random word post-fixed with a random number within the range of (0-9999)
    """
    return '%s%d' % (prefix, fake.random_int(min=0, max=9999))  # (prefix, random.random() * 100)
