# Implementation Log – Steps Taken, Challenges Faced, Insights Gained

**Date:** 2025-08-04

## Overview
Given the time constraints, my primary goal was to build a functional product. The log below outlines the steps I took, the problems I encountered, how I resolved them, and possible areas for future improvement.

## Step-by-Step Breakdown

1. **Initial CLI Implementation**  
   - Started by building a structure that worked via the command line interface.  
   - Used OpenAI's GPT-4 model through API keys.  
   - Ran into issues due to token limitations when processing large input files.

2. **Token Constraint Workaround**  
   - Implemented chunking strategies with overlapping windows to summarize inputs.  
   - Explored use of agentic AI theoretically for better structuring by providing tools to decompose and reassemble information. Could not implement due to complexity and time.

3. **Prompt Engineering & Model Upgrade**  
   - Iterated over different prompt formulations for optimal performance.  
   - Switched to the `gpt-4-1106-preview` (GPT-4 Turbo) model after discovering it allowed more tokens.

4. **Web Application via Streamlit**  
   - Chose Streamlit due to its speed and Python compatibility.  
   - Built a user-friendly UI for uploading or pasting files and schemas.  
   - Supported input via `.txt` and `.pdf` files for text, and `.json`/`.txt` for schemas.

5. **Output Formatting Issues**  
   - Noticed model-specific formatting issues.  
   - Switched temporarily to `gpt-3.5-turbo` which handled output formatting better.  
   - Eventually resolved the issue and reverted to GPT-4 Turbo.

6. **Deployment & Secrets Management**  
   - Successfully deployed a local working web app.  
   - Attempted to push code to GitHub but ran into issues with `.env` secrets being tracked.  
   - Used Streamlit’s community deployment tools to securely manage API keys without exposing them.

## Insights Gained

- Chunking and summarization are critical when dealing with token-limited LLMs.  
- Prompt structure plays a significant role in the quality of outputs.  
- Formatting and parsing issues can vary widely across models.  
- Managing secrets during deployment is essential to avoid compromising security.

## Future Improvements

- Refine prompt design and dynamic structuring techniques.  
- Explore agentic AI capabilities for chunking and file parsing.  
- Experiment with RAG (Retrieval-Augmented Generation) architecture to manage and search large text corpora.  
- Implement similarity-based chunk retrieval and answer aggregation.  
- Add more robust input validation and error handling.  
- Extend file support to additional formats (e.g., docx, csv, yaml).

## Conclusion

This was a rewarding and insightful project. Despite the time constraints, I was able to produce a functional and deployable product while learning about handling LLM token limits, prompt engineering, and secure deployments.
