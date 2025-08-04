
# Solution Design Document – Architecture, Major Design Choices, and Rationale

**Date:** 2025-08-04

## Overview

This document outlines the architectural decisions, major design choices, and the rationale behind them for the implementation of the project. The primary focus was to build a streamlined, functional system using familiar and well-supported tools, while addressing the limitations and strengths of large language models.

---

## Architecture Summary

The system architecture is designed with simplicity and rapid deployment in mind. It comprises the following major components:

- **Frontend Interface**: Built using Streamlit for user interaction, file uploads, and displaying outputs.
- **Backend Logic**: Powered by Python to handle input processing, prompt generation, schema validation, and communication with OpenAI's API.
- **LLM Integration**: Utilizes OpenAI’s `gpt-4-1106-preview` model for its higher token limits and better performance with complex inputs.
- **Deployment**: Uses Streamlit sharing and GitHub for version control and secure deployment, with `.env` handling for API key management.

---

## Major Design Choices & Rationale

### 1. **Use of OpenAI's API**

- **Rationale**: Chosen due to the wide variety of powerful models, prior familiarity, and consistently strong performance across use cases.
- **Benefits**: Quick integration, reliable results, good support and documentation.

### 2. **Prompt Engineering & Schema Focus**

- **Rationale**: Prompt engineering was essential to reduce hallucinations and increase schema compliance, which is often a challenge with LLMs.
- **Focus**: Iteratively refined prompts to ensure outputs aligned with user-provided schemas.
- **Later Emphasis**: Shifted focus toward validation techniques to catch hallucinations and ensure output quality.

### 3. **High Token Limit Model Selection**

- **Rationale**: Larger token context in GPT-4 Turbo allowed for processing longer inputs without aggressive chunking.
- **Trade-Off Avoided**: This reduced the need for complex chunking strategies and avoided the implementation of agentic decomposition logic under time constraints.

### 4. **Streamlit for Frontend and Deployment**

- **Rationale**: Streamlit offers a fast, simple, Python-native way to create UIs and deploy web applications.
- **Benefits**: Rapid prototyping, ease of integration with GitHub, built-in support for deploying apps, and minimal setup time.

---

## Future Considerations

- Introduce chunking and agentic pipelines if using lower-token models.
- Add real-time schema validation feedback to improve trust and reliability.
- Explore alternative LLM providers or models for cost-performance trade-offs.

---

