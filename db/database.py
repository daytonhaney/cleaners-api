from flask import Flask, render_template, request, redirect, url_for, jsonify
import os 
import psycopg2
from dotenv import load_dotenv

def customers_table():
    url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("""
        create table if not exists customers (
           id serial PRIMARY KEY,
           first_name varchar(100) NOT NULL,
           last_name varchar(100) NOT NULL,
           email varchar(100) NOT NULL,
           amound_paid decimal(10,2) NOT NULL,
           data DATE not NULL,
           address text NOT NULL       
           )
    """)
    conn.commit()
    cur.close()
    conn.close()
    return 0
