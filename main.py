import streamlit as st
import openai
import json
import os
from PyPDF2 import PdfReader
from io import StringIO
from jsonschema import validate, ValidationError

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(file_obj):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = PdfReader(file_obj)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def convert_to_json(text_input, schema_content):
    """Calls OpenAI API to convert text to the specified JSON schema."""
    if not openai.api_key:
        st.error("OPENAI_API_KEY is not set. Please add it to your environment or Streamlit secrets.")
        st.stop()
    try:
        json.loads(schema_content)
    except json.JSONDecodeError:
        st.error("The provided schema is not valid JSON. Please check the format.")
        st.text_area("Invalid Schema:", value=schema_content, height=200)
        return None

    system_prompt = f"""
You are an expert data extraction tool. Your task is to convert the user's text into a valid JSON object
that strictly adheres to the following JSON schema. Do not add or make up any fields that are not in the JSON schema given to you below.
Ensure all required fields are present. Output ONLY the JSON object, with no additional text or explanations.

JSON Schema:
{schema_content}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": text_input}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        json_output = response.choices[0].message.content

        parsed_output = json.loads(json_output)
        schema_dict = json.loads(schema_content)
        try:
            validate(instance=parsed_output, schema=schema_dict)
        except ValidationError as ve:
            st.error(f"The output JSON does not match the schema: {ve.message}")
            st.text_area("Invalid Output:", value=json_output, height=200)
            return None

        return json_output

        # json.loads(json_output)
        # return json_output
    except openai.OpenAIError as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
    except json.JSONDecodeError:
        st.error("The model returned an invalid JSON. Please try again or refine your input.")
        st.text_area("Model's Raw Output:", value=json_output, height=200)
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None



# Streamlit App Layout
st.set_page_config(page_title="Universal JSON Converter", page_icon="⚙️")
st.title("Metaforms.ai Assignment")
st.write(
    "Upload your data (text or PDF) and a JSON schema, and the AI will perform the conversion. "
    "File uploads take priority over pasted text."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Provide Input Data")
    input_file = st.file_uploader(
        "Upload a data file (.txt or .pdf)",
        type=['txt', 'pdf']
    )
    input_text_area = st.text_area(
        "Or paste raw text here:",
        height=300,
        placeholder="John Doe\nSoftware Engineer at Acme Inc..."
    )

with col2:
    st.subheader("2. Provide JSON Schema")
    schema_file = st.file_uploader(
        "Upload a schema file (.json or .txt)",
        type=['json', 'txt']
    )
    schema_text_area = st.text_area(
        "Or paste schema here:",
        height=300,
        placeholder='{\n  "name": "string",\n  "company": "string"\n}'
    )

if st.button("Convert to JSON", type="primary"):
    final_input_text = ""
    if input_file:
        if input_file.type == "application/pdf":
            final_input_text = extract_text_from_pdf(input_file)
        else: 
            final_input_text = input_file.getvalue().decode("utf-8")
            # stringio = StringIO(input_file.getvalue().decode("utf-8"))
            # final_input_text = stringio.read()
    elif input_text_area.strip():
        final_input_text = input_text_area
    else:
        st.warning("Please upload or paste your input data.")

    final_schema_content = ""
    if schema_file:
        stringio = StringIO(schema_file.getvalue().decode("utf-8"))
        final_schema_content = stringio.read()
    elif schema_text_area.strip():
        final_schema_content = schema_text_area
    else:
        st.warning("Please upload or paste a target JSON schema.")

    if final_input_text and final_schema_content:
        with st.spinner("Converting... Please wait."):
            json_result = convert_to_json(final_input_text, final_schema_content)
            if json_result:
                st.json(json_result)
    else:
        pass
