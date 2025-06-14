import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="CrisisTriage AI Dashboard",
    page_icon="🚀",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000"

def fetch_data():
    try:
        response = requests.get(f"{API_BASE_URL}/incidents/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

st.title("🚀 Live Incident Dashboard")

incidents = fetch_data()

if incidents is None:
    st.error("Could not connect to the backend API. Please ensure the server is running.")
else:
    if not incidents:
        st.info("No incidents reported yet. The dashboard is standing by.")
    else:
        df = pd.DataFrame(incidents)

        # --- Metrics Row ---
        st.write("### 🚨 Mission Overview")
        total_incidents = len(df)
        needs_dispatch = len(df[df['status'] == 'Needs Dispatch'])
        acknowledged = len(df[df['status'] == 'Acknowledged'])
        dispatched = total_incidents - needs_dispatch - acknowledged

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Incidents", total_incidents)
        col2.metric("Pending Dispatch", needs_dispatch, delta=None if needs_dispatch == 0 else -needs_dispatch, delta_color="inverse")
        col3.metric("Teams Dispatched", dispatched)

        # --- Main Incident Table ---
        st.write("### Triage Queue")
        df_display = df[['id', 'priority_score', 'status', 'message']].copy()
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # --- Incident Detail View & Actions ---
        st.write("---")
        st.write("### 🛠️ Incident Management")
        selected_id = st.selectbox("Select Incident ID for Details & Actions:", options=df['id'])
        
        selected_incident_response = requests.get(f"{API_BASE_URL}/incidents/{selected_id}")
        if selected_incident_response.status_code == 200:
            incident = selected_incident_response.json()
            details = json.loads(incident['details']) if isinstance(incident['details'], str) else incident['details']

            st.subheader(f"Details for Incident #{incident['id']}")
            
            # Action Buttons
            action_cols = st.columns(2)
            with action_cols[0]:
                if st.button("Acknowledge", use_container_width=True, disabled=(incident['status'] != 'Needs Dispatch')):
                    requests.post(f"{API_BASE_URL}/incidents/{selected_id}/acknowledge")
                    st.success("Incident Acknowledged!")
                    st.rerun()
            with action_cols[1]:
                if st.button("Simulate Dispatch", use_container_width=True, disabled=(incident['status'] == 'Needs Dispatch' or not details.get('latitude'))):
                    res = requests.post(f"{API_BASE_URL}/incidents/{selected_id}/dispatch")
                    st.success("Dispatch simulation complete!")
                    st.rerun()
            
            # Display Details in a clean format
            st.code(json.dumps(details, indent=2), language="json")

        else:
            st.error("Could not fetch incident details.")