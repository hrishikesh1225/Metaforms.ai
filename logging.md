# Implementation Log – Steps Taken, Challenges Faced, Insights Gained

**Date:** 2025-08-04 (Updated 2025-08-05)

## Overview  
Given the time constraints, my primary goal was to build a functional product. The log below outlines the steps I took, the problems I encountered, how I resolved them, and possible areas for future improvement.

## Step-by-Step Breakdown

1. **Initial CLI Implementation**  
   - Started by building a structure that worked via the command line interface.  
   - Used OpenAI's GPT-4 model through API keys.  
   - Ran into issues due to token limitations when processing large input files.

2. **Token Constraint Workaround**  
   - Initially explored chunking strategies and overlapping windows for input summarization.  
   - Also researched agentic AI approaches for decomposition but couldn’t implement them due to time.

3. **Prompt Engineering and Model Upgrade**  
   - Refined multiple prompt templates to reduce hallucinations and improve alignment with user schemas.  
   - Originally switched to `gpt-3.5-turbo` for faster output and fewer hallucinations.  
   - Ultimately migrated to `gpt-4o` for more consistent results, better token efficiency, and extended context window.

4. **Shift to Two-Stage Transformation Pipeline**  
   - Introduced an intermediate structured format extracted from raw input (Stage 1).  
   - Created a second stage that maps the structured JSON into a schema-compliant format.  
   - This separation greatly improved both accuracy and debuggability.

5. **Web Application via Streamlit**  
   - Built a clean and interactive Streamlit UI.  
   - Supported file upload (.txt, .pdf) and schema upload (.json, .txt).  
   - Used columns and text areas for dual input modes.

6. **Schema Validation Using `jsonschema`**  
   - Integrated Python’s `jsonschema` package to validate the final model output.  
   - Captured and displayed validation errors to help users debug non-conforming outputs.

7. **Post-Processing Safeguards**  
   - For edge cases where the LLM missed required fields (e.g., missing `value` for `outputs`), added fallback rules manually.  
   - This prevented unnecessary failures due to predictable omissions.

8. **Deployment and Secrets Management**  
   - Deployed locally and on Streamlit Cloud.  
   - Used environment variables and Streamlit Secrets for secure API key handling.

## Insights Gained

- Two-stage pipelines work better than single prompts when schema compliance is critical.  
- Token-efficient models (like GPT-4o) handle longer documents without chunking.  
- Breaking down the problem into semantic extraction and schema application makes debugging easier.  
- Validating early with `jsonschema` improves reliability and user trust.  
- Model outputs can be made safer with simple post-processing rules.

## Future Improvements

- Support multiple test case uploads for bulk validation.  
- Improve prompt dynamicity based on schema complexity.  
- Add a real-time token estimator in the UI.  
- Build a visual schema explorer to help users understand their schema structure.  
- Explore LLM fine-tuning or custom function calling for high-accuracy schema conformance.

## Conclusion

This was a rewarding and insightful project. Despite the time constraints, I was able to produce a functional and deployable product while learning about structured LLM output, schema enforcement, and how modular prompt architectures lead to more reliable and debuggable systems.
