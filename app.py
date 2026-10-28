"""Optional Streamlit interface. Install with: python -m pip install -e '.[ui]'"""
import streamlit as st

from meetagent.agent import AgentOutputError, analyze_notes
from meetagent.provider import ModelError
from meetagent.render import to_markdown

st.set_page_config(page_title="Meeting Action Agent", page_icon="📋", layout="wide")
st.title("Meeting Action Agent")
st.caption("Turn messy meeting notes into an evidence-backed action plan. Missing details stay missing; they are not guessed.")
notes = st.text_area("Paste meeting notes", height=300, placeholder="Alex: I'll send the revised budget by Friday. Priya will book the room by Thursday...")
with st.expander("Model connection"):
    st.write("Uses an OpenAI-compatible model server. Defaults to Ollama at http://localhost:11434/v1.")
    st.code("MEETAGENT_BASE_URL=http://localhost:11434/v1\nMEETAGENT_MODEL=qwen2.5:3b\n# Optional for hosted providers: MEETAGENT_API_KEY=...")
if st.button("Create action plan", type="primary", disabled=not notes.strip()):
    with st.spinner("Reading notes and checking the extracted action items..."):
        try:
            result = analyze_notes(notes)
            st.success("Action plan generated. Review it before sharing.")
            c1, c2, c3 = st.columns(3)
            c1.metric("Action items", len(result["action_items"]))
            c2.metric("Need clarification", sum(x["status"] == "needs_clarification" for x in result["action_items"]))
            c3.metric("Open questions", len(result["open_questions"]))
            st.markdown(to_markdown(result))
            st.download_button("Download Markdown report", to_markdown(result), file_name="action_plan.md", mime="text/markdown")
        except (ValueError, ModelError, AgentOutputError) as exc:
            st.error(str(exc))
