import os
import json
import openai
import streamlit as st
from io import StringIO
from PyPDF2 import PdfReader
from jsonschema import validate, ValidationError

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(file_obj):
    try:
        pdf_reader = PdfReader(file_obj)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None


def convert_to_intermediate(text_input):
    system_prompt_stage1 = """
    You are a data structuring assistant. Your task is to convert the user's instructions into a structured JSON object
    without applying any schema or formatting constraints. Focus on capturing all meaningful information in a normalized structure.

    Output only a JSON object with keys like:
    - name
    - author
    - description
    - inputs (with name, description, required, default)
    - outputs (with description AND value)
    - steps (name, type, run/uses, shell, if, with, etc.)
    - branding (color, icon)

    If an output is described as referencing a step's output (e.g., "from deploy step"), use the syntax `${{ steps.step_id.outputs.output_name }}` for the value.
    Do not validate against any schema. Just structure the meaning.
    """
    response = openai.chat.completions.create(
        model="gpt-4o", #Upgrade to turbo models for larger token limits
        messages=[
            {"role": "system", "content": system_prompt_stage1},
            {"role": "user", "content": text_input}
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def convert_structured_to_json(intermediate_data, schema_content):
    system_prompt_stage2 = f"""
    You are a schema application assistant. Your task is to take structured data and map it to a JSON object that strictly follows this schema:

    {schema_content}

    - Only include properties defined in the schema.
    - Ensure all required fields are present.
    - If 'runs.using' is 'composite', then each output entry MUST contain both 'description' and 'value'.
    - If an output references a step, use ${{ steps.step_id.outputs.output_name }} syntax.

    Output only the final JSON object.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt_stage2},
                {"role": "user", "content": json.dumps(intermediate_data)}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        output = json.loads(response.choices[0].message.content)

        return output
    except openai.RateLimitError as e:
        st.error("Token limit exceeded.")
        st.stop()
    except Exception as e:
        st.error("Unexpected error during schema mapping.")
        raise


# Streamlit App Layout
st.set_page_config(page_title="JSON Converter")
st.title("Metaforms.ai Assignment")
st.write(
    "Upload your data (text or PDF) and a JSON schema, and the AI will convert it to a valid JSON structure."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Provide Input Data")
    input_file = st.file_uploader("Upload a data file (.txt or .pdf)", type=['txt', 'pdf'])
    input_text_area = st.text_area("Or paste raw text here:", height=300)

with col2:
    st.subheader("2. Provide JSON Schema")
    schema_file = st.file_uploader("Upload a schema file (.json or .txt)", type=['json', 'txt'])
    schema_text_area = st.text_area("Or paste schema here:", height=300)

if st.button("Convert to JSON", type="primary"):
    final_input_text = ""
    if input_file:
        if input_file.type == "application/pdf":
            final_input_text = extract_text_from_pdf(input_file)
        else:
            final_input_text = input_file.getvalue().decode("utf-8")
    elif input_text_area.strip():
        final_input_text = input_text_area
    else:
        st.warning("Please upload or paste your input data.")

    final_schema_content = ""
    if schema_file:
        final_schema_content = schema_file.getvalue().decode("utf-8")
    elif schema_text_area.strip():
        final_schema_content = schema_text_area
    else:
        st.warning("Please upload or paste a target JSON schema.")

    if final_input_text and final_schema_content:
        with st.spinner("Extracting structured data..."):
            try:
                intermediate = convert_to_intermediate(final_input_text)
                st.success("Intermediate data extracted successfully.")
                with st.expander("Show Intermediate JSON"):
                    st.json(intermediate)
            except Exception as e:
                st.error("Failed to extract intermediate data.")
                st.exception(e)
                st.stop()

        with st.spinner("Converting to schema-compliant JSON..."):
            try:
                final_json = convert_structured_to_json(intermediate, final_schema_content)
                validate(instance=final_json, schema=json.loads(final_schema_content))
                st.success("Conversion complete and schema is valid.")
                st.json(final_json)
            except ValidationError as ve:
                st.error(f"The output JSON does not match the schema: {ve.message}")
                st.text_area("Invalid Output:", value=json.dumps(final_json, indent=2), height=200)
            except Exception as e:
                st.error("Unexpected error during schema mapping.")
                st.exception(e)