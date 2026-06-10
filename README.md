# 🧩 Snowflake DB Clone Tool (Streamlit)

## 📌 Project Overview
This repository contains a Streamlit-based web application designed to automate the process of cloning a Snowflake database and provisioning the correct access rights (Grants) for Development and Read-Only roles.

## 🛠 Tech Stack
* **Python**
* **Streamlit** (UI and interaction)
* **Snowflake SQL** (Data Definition and Access Control)

## 🚀 App Functionality
The application collects user inputs (Target DB name, Source DB, Owner Role, and Read-Only Role) and dynamically generates a valid Snowflake SQL script. 

The generated script:
1. Drops the target database if it already exists.
2. Clones the source database (`Zero-Copy Clone`).
3. Switches to the appropriate role.
4. Distributes access rights layer by layer.

## 🔐 Reasoning Behind the GRANTS
Snowflake's security model is built on a hierarchical structure (Database -> Schema -> Table). To ensure the correct permissions are set, the following grants were explicitly used:

1. **`GRANT OWNERSHIP ON DATABASE <db> TO ROLE <owner> REVOKE CURRENT GRANTS;`**
   * *Reasoning:* Transfers complete administrative control of the cloned database to the specified Developer role. The `REVOKE CURRENT GRANTS` clause is crucial here: it ensures that any legacy permissions copied from the original database are stripped, providing exclusive, clean ownership to the new role.
2. **`GRANT USAGE ON DATABASE <db> TO ROLE <read_only>;`**
   * *Reasoning:* This is the first essential layer of access. It allows the read-only role to "see" and enter the database.
3. **`GRANT USAGE ON ALL SCHEMAS IN DATABASE <db> TO ROLE <read_only>;`**
   * *Reasoning:* The second layer of access. Once inside the database, the role needs permission to navigate through the schemas.
4. **`GRANT SELECT ON ALL TABLES IN DATABASE <db> TO ROLE <read_only>;`**
   * *Reasoning:* The final layer. The `USAGE` privilege does not apply to tables; therefore, `SELECT` is explicitly granted to allow the read-only role to query and retrieve data without being able to modify or drop the tables.