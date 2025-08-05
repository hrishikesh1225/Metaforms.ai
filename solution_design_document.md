# Solution Design Document – Architecture, Major Design Choices, and Rationale

**Date:** 2025-08-04 (Updated 2025-08-05)

## Overview

This document outlines the architectural decisions, major design choices, and the rationale behind them for the implementation of the project. The primary focus was to build a streamlined, functional system using familiar and well-supported tools, while addressing the limitations and strengths of large language models.

---

## Architecture Summary

The system is now designed as a **two-stage transformation pipeline** that is schema-agnostic at first, and schema-conforming in the second phase. It comprises the following major components:

- **Frontend Interface**: Built using Streamlit for user interaction, file uploads, and displaying outputs.
- **Backend Logic**: Uses Python to process input, extract structured meaning, apply schema constraints, and validate outputs.
- **Two-Stage LLM Integration**:
  - Stage 1: Extracts structured intermediate JSON from free-form input
  - Stage 2: Converts structured data into a strict schema-compliant JSON object
- **Validation Layer**: Employs the `jsonschema` library to validate generated output against user-uploaded schemas.
- **Deployment**: Uses Streamlit sharing and GitHub for version control and secure deployment, with `.env` handling for API key management.

---

## Major Design Choices & Rationale

### 1. **Two-Stage Pipeline (Intermediate Representation → Schema Mapping)**

- **Rationale**: Simplifies the model's task by decoupling understanding from validation.
- **Benefits**:
  - Avoids hallucinated or invalid outputs
  - Ensures outputs are cleanly validated against schema
  - Enables debugging and inspection of intermediate output

### 2. **Explicit Prompt Engineering in Each Stage**

- **Stage 1**: Focused on semantic extraction of entities and fields without schema constraints.
- **Stage 2**: Focused on strict mapping to the user’s JSON schema.

This modularity allowed fine-grained control over model behavior and error resolution.

### 3. **Schema Validation with jsonschema**

- **Rationale**: Ensures that the final JSON output meets all structural and type constraints defined by the user.
- **Integration**: Validation failures trigger user-visible error messages and display the invalid output for debugging.

### 4. **Use of GPT-4o**

- **Rationale**: Selected for its higher context length and performance, while minimizing hallucinations.
- **Fallback Strategy**: Prompts are optimized to stay under the token limit, and manual fallbacks are added for common cases like missing required keys (e.g., `outputs.value`).

### 5. **Post-Processing Safeguards**

- **Example**: If outputs are missing `value` fields, the system inserts known defaults when appropriate (e.g., for `page-url`).

---

## Future Considerations

- Add token estimators for inputs and schemas
- Allow batch input processing for test cases
- Add visual schema explorer
- Introduce dynamic prompt tuning based on schema complexity
- Support multi-model fallback and optimization for cost vs performance

---
