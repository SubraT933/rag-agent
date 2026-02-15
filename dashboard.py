import streamlit as st
import time
import graphviz

# --- Page Config ---
st.set_page_config(
    page_title="AI Agent Control Room",
    page_icon="🤖",
    layout="wide"
)

# --- Session State (Memory) ---
if "logs" not in st.session_state:
    st.session_state.logs = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "current_step" not in st.session_state:
    st.session_state.current_step = None

# --- Sidebar: The Controller ---
with st.sidebar:
    st.title("🎛️ Mission Control")
    st.divider()
    
    # Task Input
    task_input = st.text_area("Enter Administrative Task:", 
                             "Log into CRM and update Lead #105 status to 'Qualified'.")
    
    # Difficulty Selector (Simulates Policy Logic)
    mode = st.radio("Safety Mode", ["Standard", "High Security", "Audit Only"])
    
    start_btn = st.button("🚀 Launch Agent", type="primary", use_container_width=True)

# --- Helper Function: Simulate Agent Thinking ---
def add_log(step, message, status="Running", sleep_time=1.5):
    st.session_state.current_step = step
    
    # Create a log entry structure
    log_entry = {
        "step": step,
        "message": message,
        "status": status,
        "timestamp": time.strftime("%H:%M:%S")
    }
    st.session_state.logs.append(log_entry)
    time.sleep(sleep_time) # Simulate processing time

# --- Main Logic ---
if start_btn:
    st.session_state.logs = [] # Clear old logs
    st.session_state.processing = True
    
    # Phase 1: Ingestion
    add_log("Ingestion", "Receiving task request...", "Success")
    add_log("Ingestion", "Loading 'CRM_SOP.pdf' from Vector Store...", "Success")
    
    # Phase 2: Brain (Ollama)
    add_log("Brain", "Ollama (Llama 3) is analyzing request...", "Thinking")
    add_log("Brain", "Plan Generated: 4 Steps identified.", "Success")
    
    # Phase 3: Policy
    add_log("Policy", "Checking 'Role Permissions' for Update actions...", "Checked")
    
    # Phase 4: Execution
    add_log("Hands", "Playwright launching Chromium (Headless)...", "Running")
    add_log("Hands", "Navigating to crm.portal.com...", "Success")
    add_log("Hands", "Typing credentials...", "Success")
    add_log("Hands", "Clicking 'Update Status'...", "Success")
    
    # Phase 5: Audit
    add_log("Audit", "Writing execution trace to 'audit_log.jsonl'...", "Saved")
    
    st.session_state.processing = False
    st.session_state.current_step = "Done"

# --- Main Interface ---

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🧠 Live Architecture View")
    
    # Create the Architecture Diagram
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB')
    
    # Define Nodes based on current state
    def get_color(step_name):
        if st.session_state.current_step == step_name:
            return "orange" # Active
        elif st.session_state.current_step == "Done":
            return "green"  # Completed
        return "lightgrey" # Pending

    graph.node('A', 'User Request', shape='box', style='filled', fillcolor=get_color("Ingestion"))
    graph.node('B', 'Memory (RAG)', shape='cylinder', style='filled', fillcolor=get_color("Ingestion"))
    graph.node('C', 'Brain (Ollama)', shape='hexagon', style='filled', fillcolor=get_color("Brain"))
    graph.node('D', 'Policy Check', shape='diamond', style='filled', fillcolor=get_color("Policy"))
    graph.node('E', 'Hands (Playwright)', shape='component', style='filled', fillcolor=get_color("Hands"))
    graph.node('F', 'Audit Log', shape='folder', style='filled', fillcolor=get_color("Audit"))

    # Edges
    graph.edge('A', 'C', label='Task')
    graph.edge('B', 'C', label='SOP Context')
    graph.edge('C', 'D', label='JSON Plan')
    graph.edge('D', 'E', label='Approved')
    graph.edge('E', 'F', label='Trace')

    st.graphviz_chart(graph)
    
    st.info("The diagram highlights the active module in real-time as the agent works.")

with col2:
    st.subheader("📜 Live Execution Logs")
    
    log_container = st.container()
    
    # Display Logs
    if not st.session_state.logs:
        st.write("Waiting for mission start...")
    else:
        for log in st.session_state.logs:
            with st.expander(f"{log['timestamp']} | {log['step']}: {log['status']}", expanded=True):
                st.write(log['message'])
                if log['step'] == "Brain" and "Plan Generated" in log['message']:
                    st.code("""
{
  "action": "click",
  "target": "#login_btn",
  "confidence": 0.98
}
                    """, language="json")
                if log['step'] == "Hands" and "Navigating" in log['message']:
                    st.image("https://placehold.co/600x200?text=Browser+Simulation:+CRM+Login", caption="Agent View")

    if st.session_state.processing:
        with st.spinner("Agent is working..."):
            time.sleep(1) # Visual placeholder

    if st.session_state.current_step == "Done":
        st.success("✅ Mission Accomplished successfully.")