import re
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import streamlit as st

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Wanderlust | Explore The World",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for rich tourist website decorations & animations
st.markdown("""
<style>
    /* Global Reset & Styling */
    .stApp {
        background: linear-gradient(180deg, #f0f4f8 0%, #e2e8f0 100%);
    }
    
    /* Hero Banner Container */
    .hero-container {
        position: relative;
        background: linear-gradient(rgba(15, 23, 42, 0.55), rgba(15, 23, 42, 0.75)), 
                    url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 60px 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 10px;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.5);
    }
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.95;
        max-width: 700px;
        margin: 0 auto 20px auto;
    }
    
    /* Search Box Container */
    .search-box-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 40px;
    }
    
    /* Custom Styling for Streamlit Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
    
    /* Individual Attraction Cards */
    .attraction-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .attraction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    .card-badge {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 10px;
    }
    .card-body {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        color: #64748b;
        font-size: 0.9rem;
        border-top: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# 1. Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌍 EXPLORE THE UNEXPLORED</div>
    <div class="hero-subtitle">Let our AI Agent craft your perfect 3-spot itinerary in seconds. Destination discovery made effortlessly beautiful.</div>
</div>
""", unsafe_allow_html=True)

# 2. Search Controls Section
with st.container():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div class="search-box-card">', unsafe_allow_html=True)
        city = st.text_input("📍 Destination City", placeholder="e.g. Jaipur, Tokyo, Paris, Rome, Sydney")
        generate_btn = st.button("✈️ Generate Itinerary")
        st.markdown('</div>', unsafe_allow_html=True)

# Function to parse CrewAI plain output into clean items for card layouts
def parse_places(output_text):
    # Regex split on numbered items (e.g. "1. **Name**", "1. Name")
    items = re.split(r'\n(?=\d+\.\s)', output_text.strip())
    parsed = []
    for item in items:
        clean_item = item.strip()
        if clean_item:
            lines = clean_item.split('\n', 1)
            title = lines[0]
            # Clean Markdown bold indicators
            title = re.sub(r'^\d+\.\s*', '', title).replace('**', '')
            body = lines[1].replace('**', '').strip() if len(lines) > 1 else ""
            parsed.append((title, body))
    return parsed

# 3. Agent Execution & Results Display
if generate_btn:
    if not city.strip():
        st.warning("⚠️ Please enter a city name to begin your journey.")
    else:
        with st.spinner(f"✨ Our AI Travel Agent is mapping out {city.title()}..."):
            try:
                # CrewAI Agent & Task Setup
                planner = Agent(
                    role="Expert Local Travel Guide",
                    goal="Provide the top 3 must-visit places for any given city with concise and inspiring details.",
                    backstory="You are a seasoned globetrotter and expert local guide who has explored every corner of the world. You know the history, culture, and best sights of every city, and you always give practical, authentic recommendations.",
                    verbose=True
                )

                task = Task(
                    description="Find and suggest exactly 3 must-visit places in {city}.",
                    expected_output="A clean numbered list of exactly 3 places to visit in the city, each with a brief name and a short description.",
                    agent=planner
                )

                crew = Crew(agents=[planner], tasks=[task])
                raw_result = str(crew.kickoff(inputs={"city": city}))

                # Visual Results Section
                st.markdown("---")
                st.markdown(f"<h2 style='text-align: center; color: #0f172a; margin-bottom: 30px;'>🌟 Top 3 Destinations in {city.title()}</h2>", unsafe_allow_html=True)

                places = parse_places(raw_result)

                if len(places) >= 3:
                    col1, col2, col3 = st.columns(3)
                    cols = [col1, col2, col3]

                    for idx, (title, desc) in enumerate(places[:3]):
                        with cols[idx]:
                            st.markdown(f"""
                            <div class="attraction-card">
                                <span class="card-badge">MUST VISIT #{idx+1}</span>
                                <div class="card-title">📍 {title}</div>
                                <div class="card-body">{desc}</div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    # Fallback standard card if regex format differed
                    st.markdown(f'<div class="attraction-card"><div class="card-body">{raw_result}</div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred while generating the plan: {e}")

# 4. Website Footer Decoration
st.markdown("""
<div class="footer">
    🌴 <b>Wanderlust AI Travel Services</b> • Built with CrewAI & Streamlit • Powered by OpenAI
</div>
""", unsafe_allow_html=True)