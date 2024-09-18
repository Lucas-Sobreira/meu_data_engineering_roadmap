import streamlit as st 
import psycopg2
import os 

# Função para conectar ao banco de dados
def connect_db(): 
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASS')
        )

def create_table(): 
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages(message TEXT)
                """)
    conn.commit()
    cur.close()
    conn.close()

def add_message(message): 
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", (message))
    conn.commit()
    cur.close()
    conn.close()

def get_messages(): 
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""SELECT message FROM messages""")
    messages = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

def main(): 
    st.title("Message Board")
    create_table()

    message = st.text_input("Add a new message: ")
    if st.button("Submit"): 
        add_message(message)
        st.sucess("Message added!")
    
    st.subheader("Messages")
    messages = get_messages()
    for message in messages: 
        st.write(message[0])

if __name__ == "__main__": 
    main()