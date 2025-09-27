import os
import time
import pandas as pd
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
import streamlit as st
from sqlalchemy import create_engine, event, text

st.header(body="Lakebase data editor", divider=True)
st.subheader("Edit in real time OLTP transactions")
st.write(
    "Use this recipe to read, edit a postgres database to OLTP transactions"
    "with [Databricks SQL Connector]"
    "(https://www.databricks.com/blog/how-use-lakebase-transactional-data-layer-databricks-apps)."
)

cfg = Config()
workspace_client = WorkspaceClient()

postgres_username = cfg.client_id
postgres_host = os.getenv("PGHOST")
postgres_port = 5432
postgres_database = os.getenv("PGDATABASE", "lakebase-bpt-prt-int-ingroc-dev-use-001")

postgres_pool = create_engine(f"postgresql+psycopg://{postgres_username}:@{postgres_host}:{postgres_port}/{postgres_database}")

@event.listens_for(postgres_pool, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    """Provide the App's OAuth token. Caching is managed by WorkspaceClient"""
    cparams["password"] = workspace_client.config.oauth_token().access_token

def get_engine():
    """Return the PostgreSQL database engine."""
    return postgres_pool

def get_holiday_requests(table_name):
    """Fetch all holiday requests from the database."""
    engine = get_engine()
    df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY request_id DESC;", engine)
    return df

def update_request_status(request_id, status, comment, table_name):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                UPDATE {table_name}
                SET status = :status, manager_note = :comment
                WHERE request_id = :request_id
                """
            ),
            {"status": status, "comment": comment or "", "request_id": request_id}
        )

def display_requests(table_name):
    """Display requests with approve/reject functionality - Streamlit version of Dash callback"""
    
    try:
        df = get_holiday_requests(table_name)
    except Exception as e:
        st.error(f"Error reading DB: {e}")
        return

    if df.empty:
        st.info("No requests yet!")
        return

    # Display each row with buttons
    for _, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            # Mostrar según el status
            if row['status'] == 'approved':
                st.success(f"✅ {row['employee_name']} | {row['start_date']} → {row['end_date']}")
            elif row['status'] == 'rejected':
                st.error(f"❌ {row['employee_name']} | {row['start_date']} → {row['end_date']}")
            else:
                st.info(f"⏳ {row['employee_name']} | {row['start_date']} → {row['end_date']}")
        
        with col2:
            # Botones en una sola columna, más juntos
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            with btn_col1:
                if st.button("✅", key=f"approve_{row['request_id']}"):
                    update_request_status(row['request_id'], "approved", "Approved via app", table_name)
                    st.rerun()
            
            with btn_col2:
                if st.button("⏳", key=f"pending_{row['request_id']}"):
                    update_request_status(row['request_id'], "pending", "pending via app", table_name)
                    st.rerun()
            
            with btn_col3:
                if st.button("❌", key=f"reject_{row['request_id']}"):
                    update_request_status(row['request_id'], "rejected", "Rejected via app", table_name)
                    st.rerun()


tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

with tab_a:
    table_name = st.text_input(
        "Specify the Lakebase table name:",
        placeholder="schema.table_name",
        value="holidays_leo.holiday_requests"
    )

    if table_name:
        display_requests(table_name)
        st.subheader("Data Editor - Real Time OLTP")
        df = get_holiday_requests(table_name)
        edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True)

        df_diff = pd.concat([df, edited_df]).drop_duplicates(keep=False)
        if not df_diff.empty:
            if st.button("Save changes"):
                for _, row in df_diff.iterrows():
                    update_request_status(row["request_id"], row["status"], row["manager_note"])
    else:
        st.warning("Provide a table name to load data.")

with tab_b:
    st.code(
        """
        import os
        import time
        import pandas as pd
        from databricks.sdk import WorkspaceClient
        from databricks.sdk.core import Config
        import streamlit as st
        from sqlalchemy import create_engine, event, text

        cfg = Config() # Set the DATABRICKS_HOST environment variable when running locally

        """
    )

with tab_c:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **Permissions (app service principal)**
            * `SELECT`, `INSERT`, `UPDATE`, `DELETE` on Lakebase table
            * OAuth token access to Databricks workspace
            * Access to Lakebase PostgreSQL instance
            """
        )
    with col2:
        st.markdown(
            """
            **Databricks resources**
            * Lakebase PostgreSQL database
            * Databricks workspace with OAuth
            * App service principal with database permissions
            """
        )
    with col3:
        st.markdown(
            """
            **Dependencies**
            * [Databricks SDK](https://pypi.org/project/databricks-sdk/) - `databricks-sdk`
            * [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) - `sqlalchemy`
            * [Psycopg](https://pypi.org/project/psycopg/) - `psycopg`
            * [Pandas](https://pypi.org/project/pandas/) - `pandas`
            * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
            """
        )

    
