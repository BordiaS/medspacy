import spacy

from db_connect import DbConnect
from db_reader import DbReader
from db_writer import DbWriter
from doc_consumer import DocConsumer
from pipeline import Pipeline

# sql config
driver = "SQL_Server"
server = "test_server"
db = "test_db"
user = ""
pwd = ""

# destination settings
destination_table = "table_name"
create_table = True
drop_existing = True
write_batch_size = 25
row_type = "ent"  # 'ents' or 'sections'

# column specifier, not fully fleshed out
if row_type == "ent":
    cols = ["id", "text_", "start_char", "end_char", "label", "label_"]
    col_types = ["bigint", "varchar(50)", "int", "int", "varchar(50)"]
elif row_type == "section":
    cols = [
        "id",
        "section_title",
        "section_title_text",
        "section_title_start_char",
        "section_title_end_char",
        "section_text",
        "section_text_start_char",
        "section_text_end_char",
        "section_parent",
    ]
    col_types = ["bigint", "varchar(200)", "varchar(max)", "int", "int", "varchar(max)", "int", "int", "varchar(200)"]


# read settings
read_query = "select docid, text from read_table where rowid between {0} and {1}"
start = 0
end = 100
read_batch_size = 10

# make an NLP pipeline with doc_consumer component
nlp = spacy.load("en_core_web_sm")
consumer = DocConsumer(nlp)
nlp.add_pipe(consumer)

# make db connection
db_read_conn = DbConnect(driver, server, db, user, pwd)
db_write_conn = DbConnect(driver, server, db, user, pwd)

# make db read/write
db_reader = DbReader(db_read_conn, read_query, start, end, read_batch_size)
db_writer = DbWriter(db_write_conn, destination_table, create_table, drop_existing, write_batch_size, cols, col_types)

# make final pipeline
pipeline = Pipeline(db_reader, db_writer, nlp, row_type)
