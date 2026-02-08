import os
import json
import sqlite3
import streamlit as st

from sqlalchemy import create_engine, inspect
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



db_url = "sqlite:///amazon.db"


def extract_Schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)

    schema = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col["name"] for col in columns]

    return json.dumps(schema)


def get_sql_query_from_text(schema, user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
You are an expert in converting English questions into SQL queries.

Below is the database schema.
You must use ONLY the tables and columns provided.

Schema:
{schema}

Instructions:
- If the user question can be answered using the given tables and columns,
  generate a valid SQLite SQL query.
- If the question is NOT related to the database schema or cannot be answered
  using the tables, return exactly this text:
  NOT_RELEVANT

Rules:
- Do NOT include ``` or the word sql.
- Do NOT add explanations.
- Return ONLY the SQL query or NOT_RELEVANT.

User Question:
{user_query}
""")

    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    chain = groq_sys_prompt | llm | StrOutputParser()

    return chain.invoke({
        "schema": schema,
        "user_query": user_query
    })


def get_data_from_database(sql_query):
    with sqlite3.connect("amazon.db") as conn:
        return conn.execute(sql_query).fetchall()


def main():
    st.set_page_config(page_title="text-to-sql")
    st.header("Talk to your Database")

    schema = extract_Schema(db_url)

    user_query = st.text_input("input:")
    submit = st.button("enter")

    if submit:
        sql_query = get_sql_query_from_text(schema, user_query)
        retrieve_database = get_data_from_database(sql_query)

        for row in retrieve_database:
            st.header(row)


if __name__ == "__main__":
    main()
