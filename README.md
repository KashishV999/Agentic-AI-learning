# AIP444

**Student:** Kashish Verma  
**Course:** AIP444 - AI Programming for Developers

## Overview

This repository is my course portfolio for AIP444. It contains the labs and assignments I completed while learning how to build practical LLM-powered software.

Across the repo, the work progresses from basic prompt-based CLI tools to structured output systems, tool-calling workflows, retrieval pipelines, multimodal apps, and full agent-based projects.

## Repository Structure

```text
aip444/
├── labs/          # weekly labs and smaller experiments
├── assignments/   # larger end-to-end projects
└── tools/         # shared utility scripts
```

## Labs

| # | Project | What I Built | Why This Lab Matters | LLM / AI Concepts Used |
| --- | --- | --- | --- | --- |
| 1 | [Lab 01](labs/lab-01/README.md) | A CLI that reads the staged Git diff and suggests a commit message. | It introduces the basic LLM app pattern: take real developer input, send it to a model, and turn the response into something immediately useful in a workflow. | Chat Completions API, system prompting, prompt conditioning, temperature control, conventional-commit formatting |
| 2 | [Lab 02](labs/lab-02/README.md) | A flashcard generator that converts notes into ACE-format study cards. | It focuses on getting reliable output through prompt design instead of complex code. | Prompt engineering, few-shot prompting, delimiter-based prompting, structured reasoning workflow, hallucination control, token/cost awareness |
| 3 | [Lab 03](labs/lab-03/README.md) | A PR explainer that reads a GitHub pull request diff and comment thread, then summarizes it like a senior engineer. | It shows how LLMs can help developers understand unfamiliar code changes by combining code and discussion context. | Role prompting, code-aware prompting, context framing, delimiter design, prompt synthesis across multiple input sources |
| 4 | [Lab 04](labs/lab-04/README.md) | A FastAPI service that generates flashcards and returns validated JSON. | It moves from plain text generation to application-ready structured data that other software can safely consume. | Structured outputs, schema-constrained generation, Pydantic validation, system prompt separation, API-oriented LLM design |
| 5 | [Lab 05](labs/lab-05/README.md) | An upgraded PR explainer that can fetch full files from GitHub when the diff alone is not enough. | It demonstrates that LLMs become more useful when they can request extra context instead of guessing. | Function calling, tool schema design, tool-use prompting, external context retrieval, context window management |
| 6 | [Lab 06](labs/lab-06/README.md) | A semantic search tool for products using vector embeddings and reranking. | It introduces the idea that meaning can be searched numerically, not just with keyword matching. | Text embeddings, vector similarity search, cosine similarity, reranking, semantic search |
| 7 | [Lab 07](labs/lab-07/README.md) | A Retrieval-Augmented Generation system over Node.js documentation. | It shows how to ground model answers in retrieved source documents to reduce hallucination and improve relevance. | Retrieval-Augmented Generation (RAG), document chunking, embedding-based retrieval, vector database indexing, reranking, grounded generation |
| 8 | [Lab 08](labs/lab-08/README.md) | A visual debugging assistant that inspects screenshots of errors and searches for likely fixes. | It expands beyond text-only apps and shows how multimodal models can support practical debugging tasks. | Multimodal prompting, vision-language models, image preprocessing, tool-augmented reasoning, web-grounded troubleshooting |
| 9 | [Lab 09](labs/lab09/README.md) | A source-credibility analyzer agent that investigates a URL and writes a structured credibility report. | It demonstrates autonomous multi-step problem solving, where the model chooses tools, gathers evidence, and forms a justified conclusion. | AI agents, agent loop orchestration, tool use, Think Tool pattern, structured evaluation schemas, evidence-based reasoning, web research |

## Assignments

| # | Project | What I Built | Why This Assignment Matters | LLM / AI Concepts Used |
| --- | --- | --- | --- | --- |
| 1 | [Assignment 01](assignments/assignment-01/README.md) | A multi-agent code review pipeline with two specialized reviewers and a final judge that produces an HTML report. | It brings together parallel review, structured findings, tool use, and synthesis into a realistic AI-assisted software engineering workflow. | Multi-agent orchestration, parallel LLM calls, structured outputs, function calling, schema-based findings, evaluator/judge pattern |
| 2 | [Assignment 02](assignments/assignment-02/README.md) | A 3-phase job search assistant that analyzes job postings, compares them to a resume, and generates targeted application advice. | It is the largest end-to-end project in the repo and combines extraction, analysis, external research, and agent-based report generation into one practical system. | Agentic workflows, structured information extraction, Pydantic schemas, web search tools, retrieval of external evidence, legitimacy assessment, report generation |

## What This Repo Demonstrates

- Prompt engineering for reliable and constrained generation
- Structured outputs backed by schemas and validation
- Tool calling for file access, search, and external context gathering
- Embeddings, semantic search, reranking, and RAG pipelines
- Multimodal workflows using image input
- Agentic systems that investigate, evaluate, and produce reports
- Practical AI software engineering with Python CLIs, APIs, and HTML/Markdown outputs
