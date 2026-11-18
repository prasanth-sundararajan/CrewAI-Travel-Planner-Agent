# Wanderlust: CrewAI Travel Planner Agent

> Type a city and an AI travel-guide agent suggests the top 3 places to visit.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![CrewAI](https://img.shields.io/badge/CrewAI-multi--agent-FF5A50) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white) ![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

A single-agent [CrewAI](https://www.crewai.com/) app. An *Expert Local Travel Guide* agent receives a city and returns exactly 3 must-visit places with short descriptions. The output is parsed and shown as attraction cards in a travel-site style Streamlit UI.

## Features

- CrewAI agent + task with a strict expected output (3 places)
- Output parsing into structured cards
- Polished Streamlit UI with hero banner and animations
- Works for any city worldwide

## Demo

![App screenshot](Traveler_agent.png)

## How it works

```mermaid
flowchart LR
    C["City input"] --> A["Agent: Expert Local Travel Guide"] --> T["Task: 3 must-visit places"]
    T --> P["parse_places()"] --> UI["Attraction cards"]
```

## Tech stack

| Layer | Technology |
|---|---|
| Agents | CrewAI |
| LLM | OpenAI |
| UI | Streamlit |

## Project structure

```text
.
├── travel-planner.py
├── requirements.txt
├── .env.example
└── Traveler_agent.png
```

## Getting started

**Prerequisites:** Python 3.10+

```bash
git clone https://github.com/prasanth-sundararajan/CrewAI-Travel-Planner-Agent.git
cd CrewAI-Travel-Planner-Agent
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

## Usage

```bash
streamlit run travel-planner.py
```
Enter a city (e.g. *Jaipur*, *Tokyo*) and click **Generate Itinerary**.

## Configuration

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key used for chat and embeddings |

## License

Released under the [MIT License](LICENSE).

## Author

**Prasanth Sundararajan**, Senior SRE and AI Engineer  
[LinkedIn](https://www.linkedin.com/in/prasanth-s-a093a7109/) · [GitHub](https://github.com/prasanth-sundararajan)
