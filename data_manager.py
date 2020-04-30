from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_data_by_table(cursor: RealDictCursor, table: str) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    table name for inquery
    :return:
    all data from specified table
    """
    query = f"""
        SELECT *
        FROM {table}
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def delete_from_table_by_id(cursor: RealDictCursor, table: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    enter table for deleting data
    :param id:
    select the id for the delete
    :return:
    deletes line for chosen id
    """
    query=f"""
        DELETE FROM {table}
        WHERE id={id}
    """
    cursor.execute(query)
    return "Id deleted"

@database_common.connection_handler
def get_data_by_id(cursor: RealDictCursor, table: str,column:str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    table name for inquery
    :param id:
    enter id for desired data
    :return:
    data form selected table by selected id
    """
    query = f"""
            SELECT *
            FROM {table}
            WHERE {column} = {id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_question(cursor: RealDictCursor, submission_time: str, view_number: int,
                   vote_number:int, title:str, message: str, image: str) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    enter a table for inserting data
    :param column:
    May be one or many columns name for which the values are sent to database
    :param value:
    May be one or many values name for which the columns were chosen to be sent to database
    :return:
    inserts values for columns indicated
    """

    query = f"""
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES ('{submission_time}',{view_number},{vote_number},'{title}','{message}','{image}')
            """
    cursor.execute(query)
    return "New value added"


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id: int) -> list:
    query=f"""
        DELETE FROM comment
        WHERE id={comment_id}
    """
    cursor.execute(query)
    return "Comment deleted"

@database_common.connection_handler
def write_answer(cursor: RealDictCursor, submission_time: str, vote_number: int,
                 question_id: int, message: str, image: str) -> list:
    """
    :param cursor:
    RealDictCursor
    :param submission_time:
    timestamp
    :param vote_number:
    the votes number
    :param question_id:
    the question id for which this answer is for (Foreign Key)
    :param message:
    The message for the answer
    :param image:
    link for the image associated with this answer
    :return:
    inserts values for columns indicated
    """

    query = f"""
            INSERT INTO answer (submission_time, vote_number,question_id,message,image)
            VALUES ('{submission_time}',{vote_number},{question_id},'{message}','{image}')
            """
    cursor.execute(query)
    return "New value added"


@database_common.connection_handler
def update_data(cursor: RealDictCursor, table: str, column: str, value: str, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    select table for the updates
    :param value:
    value for the update
    :param column:
    enter a column name to be updated with the above value
    :param id:
    :return:
    """
    query = f"""
            UPDATE {table}
            SET {column} = '{value}'
            WHERE id = {id}
            """

    cursor.execute(query)
    updated_query = f"""
            SELECT *
            FROM {table}
            WHERE id = {id}
            """
    cursor.execute(updated_query)
    return cursor.fetchall()

@database_common.connection_handler
def update_edit_number(cursor: RealDictCursor, value:int,id: int) -> list:
    query=f"""
        UPDATE comment 
        SET edited_count={value}+1
        WHERE id={id}
    """
    cursor.execute(query)
    return "DONE"

@database_common.connection_handler
def get_edit_number(cursor: RealDictCursor,id: int) -> list:
    query=f"""
        SELECT edited_count
        FROM comment
        WHERE id={id}
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def update_number(cursor: RealDictCursor, table: str, column: str, value: int, id: int) -> list:
    """
    :param cursor:
    RealDictCursor
    :param table:
    select table for the updates
    :param value:
    value for the update
    :param column:
    enter a column name to be updated with the above value
    :param id:
    :return:
    """
    query = f"""
            UPDATE {table}
            SET {column} = {value}
            WHERE id = {id}
            """

    cursor.execute(query)
    updated_query = f"""
            SELECT *
            FROM {table}
            WHERE id = {id}
            """

    cursor.execute(updated_query)
    return cursor.fetchall()


@database_common.connection_handler
def write_comment(cursor: RealDictCursor, question_id: int, message: str,
                  submission_time: str, edited_count: int) -> list:

    query = f"""
            INSERT INTO comment (question_id, message, submission_time, edited_count)
            VALUES ({question_id},'{message}','{submission_time}',{edited_count})
            """
    cursor.execute(query)
    return "New value added"


@database_common.connection_handler
def search(cursor: RealDictCursor, phrase: str) -> list:
    query = """
            SELECT DISTINCT question.id AS id, question.submission_time AS submission_time , 
question.view_number AS view_number, question.vote_number AS vote_number, question.title AS title, 
question.message AS message, question.image AS image, answer.id AS answer_id,
answer.question_id AS answer_question_id, answer.submission_time AS answer_submission_time, 
answer.vote_number AS answer_vote_number, answer.message AS answer_message, answer.image AS answer_image
            FROM question
            LEFT OUTER JOIN answer
            ON question.id = answer.question_id
            WHERE question.title LIKE %(phrase)s
            OR question.message LIKE %(phrase)s
            OR answer.message LIKE %(phrase)s;
            """
    args = ({'phrase': '%' + phrase + '%'})
    cursor.execute(query, args)
    return cursor.fetchall()


@database_common.connection_handler
def comment_answer(cursor: RealDictCursor, answer_id: int, message: str, submission_time: str, edited_count: int) -> list:
    query = f"""
            INSERT INTO comment (answer_id, message,submission_time,edited_count)
            VALUES ({answer_id},'{message}','{submission_time}',{edited_count})
            """
    cursor.execute(query)
    return "New value added"


@database_common.connection_handler
def get_latest_questions(cursor: RealDictCursor) -> list:
    query = """SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_question_tags(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = f"""
        INSERT INTO question_tag
        VALUES ({question_id},{tag_id})
    """
    cursor.execute(query)
    return "Tags Updated"


@database_common.connection_handler
def tags(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
            SELECT question_tag.question_id,question_tag.tag_id,tag.name
            FROM question_tag JOIN tag
            ON question_tag.tag_id=tag.id
            WHERE question_tag.question_id={question_id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = f"""
        DELETE FROM question_tag
        WHERE question_id={question_id} AND tag_id={tag_id}
    """
    cursor.execute(query)
    return "Tag deleted"


@database_common.connection_handler
def add_new_tag(cursor: RealDictCursor,new_tag:str) -> list:
    query = f"""
        INSERT INTO tag (name)
        VALUES ('{new_tag}')
    """
    cursor.execute(query)
    return "DONE"