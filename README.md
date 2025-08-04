# Metaforms.ai

**Assessment: AI Solution Design**

---

## Overview

Metaforms.ai is a project focused on designing and prototyping a system that transforms unstructured plain text into a structured format, strictly following a specified JSON schema.

---

## Goal

Design and implement a solution that:

- Converts unstructured plain text into a structured output.
- Enforces adherence to a given JSON schema.

---

## Assignment Scope

- The solution **can be exposed via CLI or web application**—implement whichever interface is more convenient.
- **Any closed-source LLM API, framework, or library** may be used.
- **No constraints on cost or latency per request** (do not optimize for efficiency, expense, or tokens).
- **No need for production bells and whistles** (e.g., streaming, high-throughput, retry logic). Focus on core functionality.

---

## Evaluation Criteria

- **P1. Decision & Experimentation Log**
  - Maintain a log of key decisions, experiments, and insights throughout your process.
- **P2. Functional Correctness**
  - The system must process these [sample test cases](https://drive.google.com/drive/folders/1npk4DAvFNu3GofVJrsAKfa5Tu1R9lBOy) and produce outputs that adhere to their schema ([validate here](https://www.jsonschemavalidator.net)).
- **P3. Input & Schema Complexity**
  - Large input and schema support:
    - Text input: **up to 50,000 tokens**
    - Schema file: **up to 100,000 tokens**
    - Deep nesting: **7+ levels**
    - Large schema: **1,000+ literals**

---

## Submission Guidelines

- **Solution Design Document** – Architecture, major design choices, and rationale.
- **Implementation Log** – Steps taken, challenges faced, insights gained.
- **GitHub Repo** (required) and/or **Deployed UI** (optional).
- **Constraints you enforced** in your solution.
- **Trade-offs** made (and how you would address them with more time or resources).

---

## Notes

- Focus on **core functionality** and **schema validation**.
- Mockups/placeholders are acceptable in place of full production features.
- Full productionization (streaming, retries, high throughput) is *not* required.

---

## Usage

- Use the link provided as it contains the api-key and has been deployed for easy access. https://metaformsai-assignment.streamlit.app
- For local usage you will be required to add your own openai api key. 