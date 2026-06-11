# Snowflake DB Clone Tool (Streamlit)

## Project Overview
This repository contains a Streamlit-based web application designed to automate the process of cloning a Snowflake database and provisioning the correct, production-ready access rights for Owner and Read-Only roles.

## Tech Stack
* **Python & Streamlit** (UI and user interaction)
* **Snowflake SQL** (Data Definition and Role-Based Access Control)

## App Functionality
The application collects user inputs and dynamically generates a valid Snowflake SQL script. 
The generated script:
1. Drops the target database if it already exists.
2. Clones the source database (`Zero-Copy Clone`).
3. Distributes explicit, cascading access rights for both the Owner and Read-Only roles, accounting for Snowflake's lack of automatic downward privilege inheritance.

## Reasoning Behind the GRANTS
Snowflake's security model is built on a strict hierarchy (Database ➔ Schema ➔ Object). A crucial architectural feature is that **owning a container (Database) does not automatically grant permissions on the objects inside it** after a clone. Therefore, privileges must be explicitly granted at every level.

### 1. Developer Role (Owner)
* **`GRANT OWNERSHIP ON DATABASE / SCHEMAS / TABLES / VIEWS...`**
  * *Reasoning:* When a database is cloned, the role executing the clone becomes the owner of the new database, but the ownership of the underlying schemas and tables is not automatically transferred to the new target role. If we only grant ownership on the database level, the `DEV` role would be "locked out" of modifying existing tables. We must cascade the `OWNERSHIP` down to all schemas, tables, and views. 
  * `REVOKE CURRENT GRANTS` is used to strip any legacy permissions copied from the original database, ensuring exclusive control.

### 2. Read-Only Role
* **`GRANT USAGE ON DATABASE / SCHEMAS...`**
  * *Reasoning:* `USAGE` is the fundamental permission that allows a role to "enter" the database and navigate through its schemas.
* **`GRANT SELECT ON ALL TABLES / VIEWS...`**
  * *Reasoning:* `USAGE` does not apply to data objects. `SELECT` is explicitly required to allow the role to query the data without modifying it.
* **`GRANT ... ON FUTURE SCHEMAS / TABLES / VIEWS...`**
  * *Reasoning:* This is essential for a sustainable read-only role. Without `FUTURE` grants, if the `DEV` role creates a new table tomorrow, the Read-Only role will not see it. Future grants ensure that access permissions are automatically applied to any new objects created within the cloned database.