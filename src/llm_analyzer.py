
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, APIError


def generate_ai_report(
    missing_count,
    duplicate_count,
    null_count,
    extra_count,
    source_count,
    target_count
):

    project_root = Path(__file__).resolve().parent.parent

    load_dotenv(project_root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OpenAI API key not found.")
        return "AI analysis unavailable: API key not found."

    try:

        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are a Data Quality Analyst.

        Analyze the following data quality validation results.

        Source Records: {source_count}
        Target Records: {target_count}

        Missing Records: {missing_count}
        Duplicate Rows: {duplicate_count}
        Null Records: {null_count}
        Extra Records: {extra_count}

        Please provide:

        1. Overall Data Quality Assessment
        2. Identified Data Quality Issues
        3. Possible Root Causes
        4. Priority of Issues (High, Medium, Low)
        5. Recommended Corrective Actions

        Explain the findings in simple business language.

        Important:
        Do not invent validation results.
        Use only the supplied counts.
        """

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt
        )

        ai_report = response.output_text

        print("\nAI DATA QUALITY ANALYSIS")
        print("=" * 55)
        print(ai_report)

        return ai_report

    except APIError as e:

        print("\nOpenAI API Error:", str(e))

        return f"AI analysis unavailable: {str(e)}"

    except Exception as e:

        print("\nUnexpected AI Error:", str(e))

        return f"AI analysis unavailable: {str(e)}"


def chat_with_ai(question, quality_results, chat_history=None):

    project_root = Path(__file__).resolve().parent.parent

    load_dotenv(project_root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "AI chatbot unavailable: API key not found."

    try:

        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are an expert Data Quality and Data Engineering AI Assistant.

        Analyze the following actual validation results:

        Missing Records: {len(quality_results['missing'])}
        Duplicate Records: {len(quality_results['duplicate'])}
        Null Records: {len(quality_results['null'])}
        Extra Records: {len(quality_results['extra'])}

        Schema Validation:
        {quality_results['schema']}

        User Question:
        {question}

        Instructions:
        1. Answer based on the supplied validation results.
        2. Explain possible root causes.
        3. Suggest corrective actions.
        4. Provide SQL or Python examples when requested.
        5. Do not invent findings.
        """

        messages = [
            {
                "role": "system",
                "content": "You are a professional Data Quality AI Assistant."
            }
        ]

        if chat_history:
            messages.extend(chat_history[-10:])

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = client.responses.create(
            model="gpt-5.5",
            input=messages
        )

        return response.output_text

    except APIError as e:

        return f"OpenAI API Error: {str(e)}"

    except Exception as e:

        return f"Unexpected AI Error: {str(e)}"
