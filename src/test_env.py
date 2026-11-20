
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, APIError

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: API key not found.")
else:
    try:
        client = OpenAI(api_key=api_key)

        print("OpenAI client initialized successfully.")

        response = client.responses.create(
            model="gpt-5.5",
            input="Explain what a Data Quality Report is in simple terms."
        )

        print("\nAI Response:")
        print(response.output_text)

    except APIError as e:
        print("\nOpenAI API Error:")
        print("Status:", e.status_code)
        print("Details:", str(e))

    except Exception as e:
        print("\nUnexpected Error:", str(e))
