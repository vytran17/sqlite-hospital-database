# SQLite Hospital Database

## 1. Introduction

This project includes a set of tools for managing a hospital database. 

- It consists of a set of SQL queries (`hospital.sql`) to populate a hospital database from CSV files.
- It also contains a Python application (`hospital.py`) that does the same thing as the former set of SQL commands but using Python sqlalchemy APIs. 

## 2. Requirements

- Python 3.x
- SQLite3
- Additional Python libraries (please check `hospital.py` file for details)

## 3. Installation Instructions

No additional installation is required if the above prerequisites are met. 
Ensure that Python and SQLite3 are installed on your system.

## 4. How to Use the SQL Queries (`hospital.sql`)

To import and use the SQL queries from `hospital.sql`:

1. Open SQLite command-line tool in your command prompt.
2. And run the commands from `hospital.sql` as needed. You can also run: `$ sqlite3 < hospital.sql`

## 5. How to Run the Application Program (`hospital.py`)

To execute the `hospital.py` script:

1. Open a terminal or command prompt.
2. Navigate to the directory containing `hospital.py`.
3. Run the script: `python hospital.py`
