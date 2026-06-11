import streamlit as st
st.title("🧩 Snowflake DB Clone Tool")
target_db = st.text_input("Target DB name", "Streamlit_Sergey")
source_db = st.text_input("Clone from DB", "DEV")
owner_role = st.selectbox("Owner role", ["DEVELOPMENT", "SYSADMIN", "ACCOUNTADMIN"])
readonly_role = st.text_input("Read-only role", "read_only_role")
st.warning(f"⚠️ {target_db} already exists (owner: {owner_role}). It will be dropped and recreated if you proceed.")
if st.button("Refresh SQL"):
    sql_script = f"""
DROP DATABASE IF EXISTS {target_db};
CREATE OR REPLACE DATABASE {target_db} CLONE {source_db};
USE ROLE {owner_role};
GRANT OWNERSHIP ON DATABASE {target_db} TO ROLE {owner_role} REVOKE CURRENT GRANTS;
GRANT OWNERSHIP ON ALL SCHEMAS IN DATABASE {target_db} TO ROLE {owner_role} REVOKE CURRENT GRANTS;
GRANT OWNERSHIP ON ALL TABLES IN DATABASE {target_db} TO ROLE {owner_role} REVOKE CURRENT GRANTS;
GRANT OWNERSHIP ON ALL VIEWS IN DATABASE {target_db} TO ROLE {owner_role} REVOKE CURRENT GRANTS;
GRANT USAGE ON DATABASE {target_db} TO ROLE {readonly_role};
GRANT USAGE ON ALL SCHEMAS IN DATABASE {target_db} TO ROLE {readonly_role};
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {target_db} TO ROLE {readonly_role};
GRANT SELECT ON ALL TABLES IN DATABASE {target_db} TO ROLE {readonly_role};
GRANT SELECT ON FUTURE TABLES IN DATABASE {target_db} TO ROLE {readonly_role};
GRANT SELECT ON ALL VIEWS IN DATABASE {target_db} TO ROLE {readonly_role};
GRANT SELECT ON FUTURE VIEWS IN DATABASE {target_db} TO ROLE {readonly_role};"""
    st.subheader("Generated SQL")
    st.markdown("### Please, always check db names you set up!")
    st.code(sql_script, language="sql")
    st.button("🚀 Execute SQL")
