
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from missing_records import find_missing_records
from duplicate_checker import find_duplicate_records
from schema_validator import validate_schema
from null_checker import find_null_values
from extra_records import find_extra_records
from llm_analyzer import chat_with_ai


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILE = PROJECT_ROOT / "data" / "source_data.csv"
TARGET_FILE = PROJECT_ROOT / "data" / "target_data.csv"


# Streamlit page configuration
st.set_page_config(
    page_title="AI Data Quality Dashboard",
    page_icon="📊",
    layout="wide"
)


# Dashboard title
st.title("📊 AI Data Quality Dashboard")

st.caption(
    "Automated Source-to-Target Data Quality Validation"
)


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Load data
@st.cache_data
def load_data():

    source_df = pd.read_csv(SOURCE_FILE)
    target_df = pd.read_csv(TARGET_FILE)

    return source_df, target_df


try:

    source_df, target_df = load_data()

except Exception as e:

    st.error(f"Unable to load input files: {e}")
    st.stop()


# Run validations
if st.button("Run Data Quality Validation"):

    with st.spinner("Running data quality checks..."):

        missing_df = find_missing_records(
            source_df,
            target_df,
            "TRX_ID"
        )

        duplicate_df = find_duplicate_records(
            target_df,
            "TRX_ID"
        )

        schema_result = validate_schema(
            source_df,
            target_df
        )

        null_df = find_null_values(target_df)

        extra_df = find_extra_records(
            source_df,
            target_df,
            "TRX_ID"
        )

        # Store validation results
        st.session_state["results"] = {
            "missing": missing_df,
            "duplicate": duplicate_df,
            "null": null_df,
            "extra": extra_df,
            "schema": schema_result
        }

        # Clear previous chat history
        st.session_state["chat_history"] = []

    st.success("Data Quality Validation Completed!")


# Display dashboard
if "results" in st.session_state:

    results = st.session_state["results"]

    missing_df = results["missing"]
    duplicate_df = results["duplicate"]
    null_df = results["null"]
    extra_df = results["extra"]

    st.subheader("Data Quality Overview")

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Missing Records",
        len(missing_df)
    )

    col2.metric(
        "Duplicate Records",
        len(duplicate_df)
    )

    col3.metric(
        "Null Records",
        len(null_df)
    )

    col4.metric(
        "Extra Records",
        len(extra_df)
    )

    # Record comparison
    st.subheader("Source vs Target Records")

    comparison_df = pd.DataFrame({
        "Dataset": ["Source", "Target"],
        "Records": [
            len(source_df),
            len(target_df)
        ]
    })

    fig = px.bar(
        comparison_df,
        x="Dataset",
        y="Records",
        color="Dataset",
        title="Source and Target Record Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Validation charts
    st.subheader("Data Quality Findings")

    quality_df = pd.DataFrame({
        "Validation": [
            "Missing",
            "Duplicate",
            "Null",
            "Extra"
        ],
        "Count": [
            len(missing_df),
            len(duplicate_df),
            len(null_df),
            len(extra_df)
        ]
    })

    fig = px.pie(
        quality_df,
        names="Validation",
        values="Count",
        hole=0.5,
        title="Data Quality Issues Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Detailed validation results
    st.subheader("Detailed Validation Results")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Missing Records",
        "Duplicate Records",
        "Null Records",
        "Extra Records"
    ])

    with tab1:
        st.dataframe(
            missing_df,
            use_container_width=True
        )

    with tab2:
        st.dataframe(
            duplicate_df,
            use_container_width=True
        )

    with tab3:
        st.dataframe(
            null_df,
            use_container_width=True
        )

    with tab4:
        st.dataframe(
            extra_df,
            use_container_width=True
        )

    # AI Chatbot
    st.divider()

    st.subheader("🤖 AI Data Quality Assistant")

    st.caption(
        "Ask questions about missing records, duplicates, "
        "null values, extra records and schema validation."
    )

    # Display previous conversations
    for message in st.session_state["chat_history"]:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_question = st.chat_input(
        "Ask AI about your data quality issues..."
    )

    if user_question:

        # Store user question
        st.session_state["chat_history"].append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("AI is analysing your data..."):

                ai_response = chat_with_ai(
                    user_question,
                    st.session_state["results"],
                    st.session_state["chat_history"][:-1]
                )

                st.markdown(ai_response)

        # Store AI response
        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": ai_response
        })

else:

    st.info(
        "Click 'Run Data Quality Validation' "
        "to generate the dashboard and enable AI chatbot."
    )
