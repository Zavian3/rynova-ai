import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Rynova AI - Client Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supabase configuration
SUPABASE_URL = "https://psfmytpqxvrblksgtuee.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZm15dHBxeHZyYmxrc2d0dWVlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE2NjQ4MjksImV4cCI6MjA2NzI0MDgyOX0.v8vaA37TCtEH-Okc9Aiy-MbpcPN-dlmo-6Jc5YfZ-uU"

# API headers
HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json"
}

# Custom CSS for AI-themed modern design
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global app styling with dark AI theme */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #2d1b69 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
        background: transparent;
    }
    
    /* Header styling - AI inspired */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Metric cards - AI themed */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Client cards */
    .client-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        color: #e2e8f0;
    }
    
    .client-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Text colors for better visibility */
    .stApp, .stApp p, .stApp span, .stApp div {
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-weight: 600;
    }
    
    /* Status indicators - AI themed */
    .status-active { 
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-pending { 
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }
    
    .status-inactive { 
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    .status-trial { 
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
    }
    
    /* Integration status */
    .integration-yes {
        color: #10b981 !important;
        font-weight: 600;
    }
    
    .integration-no {
        color: #94a3b8 !important;
        font-style: italic;
    }
    
    /* Success and error messages */
    .success-message {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981 !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2));
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444 !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(51, 65, 85, 0.6));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.8));
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 2rem;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(51, 65, 85, 0.9)) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1)) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #e2e8f0 !important;
        backdrop-filter: blur(10px);
    }
    
    /* Metric styling */
    .css-1r6slb0 {
        background: transparent !important;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="metric-container"] > div {
        color: #e2e8f0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }
    
    /* Labels and text */
    .stMarkdown, label {
        color: #e2e8f0 !important;
    }
    
    /* Charts background */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Warning and info boxes */
    .stWarning, .stInfo {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1)) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #f59e0b !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

class SupabaseClient:
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.headers = HEADERS
    
    def get_all_clients(self) -> List[Dict]:
        """Fetch all clients from Supabase"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/client?select=*",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching clients: {e}")
            return []
    
    def create_client(self, client_data: Dict) -> bool:
        """Create a new client"""
        try:
            response = requests.post(
                f"{self.base_url}/rest/v1/client",
                headers={**self.headers, "Prefer": "return=minimal"},
                json=client_data
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Error creating client: {e}")
            return False
    
    def update_client(self, client_id: str, update_data: Dict) -> bool:
        """Update an existing client"""
        try:
            response = requests.patch(
                f"{self.base_url}/rest/v1/client?client_id=eq.{client_id}",
                headers={**self.headers, "Prefer": "return=minimal"},
                json=update_data
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Error updating client: {e}")
            return False
    
    def delete_client(self, client_id: str) -> bool:
        """Delete a client"""
        try:
            response = requests.delete(
                f"{self.base_url}/rest/v1/client?client_id=eq.{client_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting client: {e}")
            return False

# Initialize Supabase client
@st.cache_resource
def get_supabase_client():
    return SupabaseClient()

supabase = get_supabase_client()

def render_header():
    """Render the main dashboard header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Rynova AI Client Dashboard</h1>
        <p>Manage AI Agent Appointments & Client Onboarding</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar navigation"""
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.title("🚀 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Dashboard Overview", "➕ Add New Client", "👥 Client Management", "📈 Analytics"]
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Quick stats in sidebar
    clients = supabase.get_all_clients()
    
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 📊 Quick Stats")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Total", len(clients))
    with col2:
        active_clients = len([c for c in clients if c.get('status') == 'active']) if clients else 0
        st.metric("Active", active_clients)
    
    if clients:
        # Integration stats
        setup_integrations = len([c for c in clients if c.get('calendar_type') or c.get('crm_type')])
        integration_rate = (setup_integrations / len(clients) * 100) if clients else 0
        
        st.metric("Setup Rate", f"{integration_rate:.0f}%")
        
        # Most common business type
        business_types = [c.get('business_type') for c in clients if c.get('business_type')]
        if business_types:
            most_common = max(set(business_types), key=business_types.count)
            st.write(f"**Top Type:** {most_common}")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return page

def render_dashboard_overview():
    """Render the main dashboard overview"""
    st.header("📊 Dashboard Overview")
    
    # Fetch client data
    clients = supabase.get_all_clients()
    
    if not clients:
        st.warning("No clients found. Add your first client to get started!")
        return
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Clients", len(clients))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        active_clients = len([c for c in clients if c.get('status') == 'active'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Clients", active_clients)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        business_types = len(set([c.get('business_type') for c in clients if c.get('business_type')]))
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Business Types", business_types)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        integrations = len([c for c in clients if c.get('calendar_type') or c.get('crm_type')])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Integrations Setup", integrations)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Business Types Distribution")
        business_types = [c.get('business_type') or 'Not specified' for c in clients]
        business_type_counts = pd.Series(business_types).value_counts()
        
        if not business_type_counts.empty:
            # AI-themed color palette
            ai_colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5a3c', '#6b7280']
            
            fig = px.pie(
                values=business_type_counts.values,
                names=business_type_counts.index,
                title="Client Business Types",
                color_discrete_sequence=ai_colors
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12,
                textfont_color='white'
            )
            fig.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                title_font=dict(color='#f1f5f9', size=16)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No business type data available")
    
    with col2:
        st.subheader("🔗 Integration Status")
        integration_data = []
        for client in clients:
            has_calendar = bool(client.get('calendar_type'))
            has_crm = bool(client.get('crm_type'))
            
            if has_calendar and has_crm:
                integration_data.append("Both")
            elif has_calendar:
                integration_data.append("Calendar Only")
            elif has_crm:
                integration_data.append("CRM Only")
            else:
                integration_data.append("None")
        
        integration_counts = pd.Series(integration_data).value_counts()
        
        if not integration_counts.empty:
            # Color mapping for different integration statuses
            colors = {
                'Both': '#28a745',      # Green
                'Calendar Only': '#17a2b8',  # Blue
                'CRM Only': '#ffc107',  # Yellow
                'None': '#dc3545'       # Red
            }
            
            fig = px.bar(
                x=integration_counts.index,
                y=integration_counts.values,
                title="Integration Setup Status",
                color=integration_counts.index,
                color_discrete_map=colors
            )
            fig.update_layout(
                xaxis_title="Integration Type", 
                yaxis_title="Number of Clients",
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                title_font=dict(color='#f1f5f9', size=16)
            )
            fig.update_xaxes(
                gridcolor='rgba(148,163,184,0.2)',
                title_font=dict(color='#e2e8f0'),
                tickfont=dict(color='#e2e8f0')
            )
            fig.update_yaxes(
                gridcolor='rgba(148,163,184,0.2)',
                title_font=dict(color='#e2e8f0'),
                tickfont=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No integration data available")
    
    # Recent clients
    st.subheader("👥 Recent Clients")
    recent_clients = clients[:5]  # Show first 5 clients
    
    for client in recent_clients:
        st.markdown('<div class="client-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 3, 2])
        
        with col1:
            business_name = client.get('business_name') or 'Unnamed Business'
            business_type = client.get('business_type') or 'Not specified'
            st.write(f"**{business_name}**")
            st.write(f"Type: {business_type}")
        
        with col2:
            email = client.get('email') or 'Not setup'
            phone = client.get('phone') or 'Not setup'
            st.write(f"Email: {email}")
            st.write(f"Phone: {phone}")
        
        with col3:
            status = client.get('status', 'unknown')
            if status == "active":
                st.markdown('<span class="status-active">🟢 Active</span>', unsafe_allow_html=True)
            elif status == "pending":
                st.markdown('<span class="status-pending">🟡 Pending</span>', unsafe_allow_html=True)
            elif status == "trial":
                st.markdown('<span class="status-trial">🔵 Trial</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-inactive">🔴 Inactive</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_add_client_form():
    """Render the add new client form"""
    st.header("➕ Add New Client")
    
    with st.form("add_client_form"):
        st.subheader("🏢 Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input("Client ID*", help="Unique identifier for the client")
            business_name = st.text_input("Business Name*")
            business_type = st.selectbox("Business Type*", [
                "salon", "spa", "clinic", "dental", "medical", "fitness", "restaurant", 
                "retail", "consulting", "other"
            ])
            phone = st.text_input("Phone Number*", placeholder="+1234567890")
            email = st.text_input("Email Address*", placeholder="contact@business.com")
        
        with col2:
            street_address = st.text_input("Street Address")
            city = st.text_input("City")
            state = st.text_input("State/Province")
            zip_code = st.text_input("ZIP/Postal Code")
            country = st.text_input("Country")
        
        st.subheader("🔗 Integrations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**CRM Integration**")
            crm_type = st.selectbox("CRM Type", ["", "squareup"], 
                                  help="Currently supporting SquareUp only. Leave empty if not using CRM.")
            
            # Show CRM API Key field only if SquareUp is selected
            crm_api_key = ""
            if crm_type == "squareup":
                crm_api_key = st.text_input("SquareUp API Key*", type="password", 
                                          help="Required when using SquareUp CRM")
            
            st.write("**Calendar Integration**")
            
            # Calendar logic based on CRM selection
            if crm_type == "squareup":
                # If SquareUp CRM is selected, calendar must also be SquareUp
                calendar_type = "squareup"
                st.info("📅 Calendar automatically set to SquareUp when using SquareUp CRM")
                calendar_api_key = st.text_input("SquareUp Calendar API Key*", type="password",
                                                help="Required for SquareUp calendar integration")
            else:
                # If no CRM or different CRM, can select Google Calendar
                calendar_type = st.selectbox("Calendar Type", ["", "google"], 
                                           help="Select Google Calendar if not using SquareUp CRM")
                calendar_api_key = ""
                if calendar_type == "google":
                    calendar_api_key = st.text_input("Google Calendar API Key*", type="password",
                                                   help="Required for Google Calendar integration")
        
        with col2:
            st.write("**Communication Setup**")
            twilio_number = st.text_input("Twilio Number", 
                                        help="Phone number for SMS notifications")
            front_desk_number = st.text_input("Front Desk Number", 
                                            help="Main contact number for the business")
            front_desk_email = st.text_input("Front Desk Email", 
                                           help="Main contact email for the business")
            google_review_link = st.text_input("Google Review Link", 
                                             help="Link to Google Reviews page")
        
        st.subheader("⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            status = st.selectbox("Status", ["active", "pending", "inactive", "trial"])
            subscription_plan = st.selectbox("Subscription Plan", [
                "", "basic", "professional", "enterprise", "custom"
            ])
        
        with col2:
            subscription_expires_at = st.date_input("Subscription Expires", value=None)
            business_hours = st.text_area("Business Hours (JSON format)", 
                                        placeholder='{"mon": "9:00-17:00", "tue": "9:00-17:00"}')
        
        st.subheader("🎯 AI Agent Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            reminder_offsets = st.text_input("Reminder Offsets (minutes)", 
                                           placeholder="60,1440", help="Comma-separated minutes before appointment")
            rating_offset_minutes = st.number_input("Rating Request Delay (minutes)", 
                                                   min_value=0, value=60)
        
        with col2:
            features = st.multiselect("Enabled Features", [
                "appointment_booking", "reminders", "follow_ups", "reviews", 
                "promotions", "analytics", "integrations"
            ])
        
        # Template fields
        st.subheader("📝 Message Templates")
        rating_template = st.text_area("Rating Request Template")
        rating_high_template = st.text_area("High Rating Follow-up Template")
        rating_low_template = st.text_area("Low Rating Follow-up Template")
        
        submitted = st.form_submit_button("🚀 Create Client", type="primary")
        
        if submitted:
            # Validate required fields
            if not all([client_id, business_name, business_type, phone, email]):
                st.error("Please fill in all required fields marked with *")
                return
            
            # Validate integration-specific required fields
            validation_errors = []
            
            if crm_type == "squareup" and not crm_api_key:
                validation_errors.append("SquareUp API Key is required when using SquareUp CRM")
            
            if calendar_type == "squareup" and not calendar_api_key:
                validation_errors.append("SquareUp Calendar API Key is required when using SquareUp Calendar")
            elif calendar_type == "google" and not calendar_api_key:
                validation_errors.append("Google Calendar API Key is required when using Google Calendar")
            
            if validation_errors:
                for error in validation_errors:
                    st.error(error)
                return
            
            # Prepare client data
            client_data = {
                "client_id": client_id,
                "business_name": business_name,
                "business_type": business_type,
                "phone": phone,
                "email": email,
                "street_address": street_address or None,
                "city": city or None,
                "state": state or None,
                "zip_code": zip_code or None,
                "country": country or None,
                "crm_type": crm_type or None,
                "crm_api_key": crm_api_key or None,
                "calendar_type": calendar_type or None,
                "calendar_id": calendar_api_key or None,  # Store API key in calendar_id field
                "twilio_number": twilio_number or None,
                "front_desk_number": front_desk_number or None,
                "front_desk_email": front_desk_email or None,
                "business_hours": business_hours or None,
                "features": json.dumps(features) if features else None,
                "status": status,
                "subscription_plan": subscription_plan or None,
                "subscription_expires_at": subscription_expires_at.isoformat() if subscription_expires_at else None,
                "google_review_link": google_review_link or None,
                "flags": "{}",
                "reminder_offsets": json.dumps([int(x.strip()) for x in reminder_offsets.split(",") if x.strip().isdigit()]) if reminder_offsets else "[]",
                "follow_up_rules": "[]",
                "rating_template": rating_template or None,
                "rating_high_template": rating_high_template or None,
                "rating_low_template": rating_low_template or None,
                "rating_offset_minutes": rating_offset_minutes,
                "promo_schedule": "{}",
                "reengage_rules": "[]",
                "locations": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Create client
            if supabase.create_client(client_data):
                st.markdown('<div class="success-message">✅ Client created successfully!</div>', 
                          unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown('<div class="error-message">❌ Failed to create client. Please try again.</div>', 
                          unsafe_allow_html=True)

def render_client_management():
    """Render the client management page"""
    st.header("👥 Client Management")
    
    # Fetch clients
    clients = supabase.get_all_clients()
    
    if not clients:
        st.warning("No clients found. Add your first client to get started!")
        return
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search clients...", placeholder="Search by name, email, or business type")
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "active", "pending", "inactive", "trial"])
    
    with col3:
        business_type_filter = st.selectbox("Filter by Business Type", 
                                          ["All"] + list(set([c.get('business_type', '') for c in clients if c.get('business_type')])))
    
    # Filter clients
    filtered_clients = clients
    
    if search_term:
        filtered_clients = [
            c for c in filtered_clients 
            if search_term.lower() in (c.get('business_name', '') + c.get('email', '') + c.get('business_type', '')).lower()
        ]
    
    if status_filter != "All":
        filtered_clients = [c for c in filtered_clients if c.get('status') == status_filter]
    
    if business_type_filter != "All":
        filtered_clients = [c for c in filtered_clients if c.get('business_type') == business_type_filter]
    
    st.write(f"Showing {len(filtered_clients)} of {len(clients)} clients")
    
    # Display clients
    for client in filtered_clients:
        business_name = client.get('business_name') or 'Unnamed Business'
        client_id = client.get('client_id') or 'No ID'
        
        with st.expander(f"🏢 {business_name} | ID: {client_id}"):
            col1, col2, col3 = st.columns([3, 3, 2])
            
            with col1:
                st.write("**📋 Basic Information**")
                business_type = client.get('business_type') or 'Not specified'
                email = client.get('email') or 'Not setup'
                phone = client.get('phone') or 'Not setup'
                address = client.get('street_address') or 'Not setup'
                
                st.write(f"• Business Type: {business_type}")
                st.write(f"• Email: {email}")
                st.write(f"• Phone: {phone}")
                st.write(f"• Address: {address}")
                
                city = client.get('city')
                state = client.get('state')
                if city or state:
                    location = f"{city or ''}, {state or ''}".strip(', ')
                    st.write(f"• Location: {location}")
                else:
                    st.write("• Location: Not setup")
            
            with col2:
                st.write("**🔗 Integration Status**")
                
                # CRM integration
                crm_type = client.get('crm_type')
                if crm_type:
                    crm_display = f"{crm_type.title()}"
                    if crm_type == "squareup":
                        crm_display = "SquareUp"
                    st.markdown(f'• CRM: <span class="integration-yes">✅ {crm_display}</span>', unsafe_allow_html=True)
                    if client.get('crm_api_key'):
                        st.markdown('• CRM API: <span class="integration-yes">✅ Configured</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('• CRM API: <span class="integration-no">❌ Not setup</span>', unsafe_allow_html=True)
                else:
                    st.markdown('• CRM: <span class="integration-no">❌ Not setup</span>', unsafe_allow_html=True)
                
                # Calendar integration
                calendar_type = client.get('calendar_type')
                if calendar_type:
                    calendar_display = f"{calendar_type.title()}"
                    if calendar_type == "squareup":
                        calendar_display = "SquareUp"
                    elif calendar_type == "google":
                        calendar_display = "Google Calendar"
                    st.markdown(f'• Calendar: <span class="integration-yes">✅ {calendar_display}</span>', unsafe_allow_html=True)
                    if client.get('calendar_id'):  # This stores the API key
                        st.markdown('• Calendar API: <span class="integration-yes">✅ Configured</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('• Calendar API: <span class="integration-no">❌ Not setup</span>', unsafe_allow_html=True)
                else:
                    st.markdown('• Calendar: <span class="integration-no">❌ Not setup</span>', unsafe_allow_html=True)
                
                # Twilio integration
                twilio_number = client.get('twilio_number')
                if twilio_number:
                    st.markdown('• Twilio: <span class="integration-yes">✅ Configured</span>', unsafe_allow_html=True)
                else:
                    st.markdown('• Twilio: <span class="integration-no">❌ Not setup</span>', unsafe_allow_html=True)
                
                # Subscription
                subscription_plan = client.get('subscription_plan') or 'Not setup'
                st.write(f"• Subscription: {subscription_plan}")
                
                subscription_expires = client.get('subscription_expires_at')
                if subscription_expires:
                    st.write(f"• Expires: {subscription_expires}")
            
            with col3:
                status = client.get('status', 'unknown')
                st.write("**📊 Status & Actions**")
                
                if status == "active":
                    st.markdown('<span class="status-active">🟢 Active</span>', unsafe_allow_html=True)
                elif status == "pending":
                    st.markdown('<span class="status-pending">🟡 Pending</span>', unsafe_allow_html=True)
                elif status == "trial":
                    st.markdown('<span class="status-trial">🔵 Trial</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-inactive">🔴 Inactive</span>', unsafe_allow_html=True)
                
                st.write("")  # Spacing
                
                # Action buttons
                if st.button(f"✏️ Edit", key=f"edit_{client_id}"):
                    st.session_state[f"edit_mode_{client_id}"] = True
                
                if st.button(f"🗑️ Delete", key=f"delete_{client_id}", type="secondary"):
                    if supabase.delete_client(client_id):
                        st.success("Client deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete client.")
            
            # Edit mode
            if st.session_state.get(f"edit_mode_{client_id}", False):
                st.markdown("---")
                st.write("**✏️ Edit Client Information**")
                st.write(f"**Client ID:** `{client_id}`")
                
                with st.form(f"edit_form_{client_id}"):
                    st.subheader("🏢 Basic Information")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_business_name = st.text_input("Business Name*", value=client.get('business_name', ''))
                        new_business_type = st.selectbox("Business Type*", 
                                                       ["salon", "spa", "clinic", "dental", "medical", "fitness", "restaurant", "retail", "consulting", "other"],
                                                       index=["salon", "spa", "clinic", "dental", "medical", "fitness", "restaurant", "retail", "consulting", "other"].index(client.get('business_type', 'salon')) if client.get('business_type') in ["salon", "spa", "clinic", "dental", "medical", "fitness", "restaurant", "retail", "consulting", "other"] else 0)
                        new_phone = st.text_input("Phone*", value=client.get('phone', ''))
                        new_email = st.text_input("Email*", value=client.get('email', ''))
                    
                    with col2:
                        new_street_address = st.text_input("Street Address", value=client.get('street_address', '') or '')
                        new_city = st.text_input("City", value=client.get('city', '') or '')
                        new_state = st.text_input("State", value=client.get('state', '') or '')
                        new_zip_code = st.text_input("ZIP Code", value=client.get('zip_code', '') or '')
                        new_country = st.text_input("Country", value=client.get('country', '') or '')
                    
                    st.subheader("🔗 Integrations")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # CRM Integration
                        current_crm = client.get('crm_type', '')
                        crm_options = ["", "squareup"]
                        crm_index = crm_options.index(current_crm) if current_crm in crm_options else 0
                        new_crm_type = st.selectbox("CRM Type", crm_options, index=crm_index)
                        
                        new_crm_api_key = ""
                        if new_crm_type == "squareup":
                            new_crm_api_key = st.text_input("SquareUp API Key", type="password", value=client.get('crm_api_key', '') or '')
                        
                        # Calendar Integration
                        if new_crm_type == "squareup":
                            new_calendar_type = "squareup"
                            st.info("📅 Calendar automatically set to SquareUp")
                            new_calendar_api_key = st.text_input("SquareUp Calendar API Key", type="password", value=client.get('calendar_id', '') or '')
                        else:
                            current_calendar = client.get('calendar_type', '')
                            calendar_options = ["", "google"]
                            calendar_index = calendar_options.index(current_calendar) if current_calendar in calendar_options else 0
                            new_calendar_type = st.selectbox("Calendar Type", calendar_options, index=calendar_index)
                            new_calendar_api_key = ""
                            if new_calendar_type == "google":
                                new_calendar_api_key = st.text_input("Google Calendar API Key", type="password", value=client.get('calendar_id', '') or '')
                    
                    with col2:
                        new_twilio_number = st.text_input("Twilio Number", value=client.get('twilio_number', '') or '')
                        new_front_desk_number = st.text_input("Front Desk Number", value=client.get('front_desk_number', '') or '')
                        new_front_desk_email = st.text_input("Front Desk Email", value=client.get('front_desk_email', '') or '')
                        new_google_review_link = st.text_input("Google Review Link", value=client.get('google_review_link', '') or '')
                    
                    st.subheader("⚙️ Settings")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Handle None status by defaulting to 'pending'
                        current_status = client.get('status') or 'pending'
                        status_options = ["active", "pending", "inactive", "trial"]
                        if current_status not in status_options:
                            current_status = 'pending'
                        new_status = st.selectbox("Status", status_options, index=status_options.index(current_status))
                        
                        subscription_options = ["", "basic", "professional", "enterprise", "custom"]
                        current_subscription = client.get('subscription_plan', '') or ''
                        sub_index = subscription_options.index(current_subscription) if current_subscription in subscription_options else 0
                        new_subscription_plan = st.selectbox("Subscription Plan", subscription_options, index=sub_index)
                    
                    with col2:
                        # Parse existing subscription expiry
                        current_expiry = None
                        if client.get('subscription_expires_at'):
                            try:
                                current_expiry = datetime.fromisoformat(client.get('subscription_expires_at').replace('Z', '+00:00')).date()
                            except:
                                current_expiry = None
                        
                        new_subscription_expires_at = st.date_input("Subscription Expires", value=current_expiry)
                        new_business_hours = st.text_area("Business Hours (JSON)", value=client.get('business_hours', '') or '', height=100)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.form_submit_button("💾 Update Client", type="primary"):
                            # Validate required fields
                            if not all([new_business_name, new_business_type, new_phone, new_email]):
                                st.error("Please fill in all required fields marked with *")
                            else:
                                # Validate integration-specific required fields
                                validation_errors = []
                                
                                if new_crm_type == "squareup" and not new_crm_api_key:
                                    validation_errors.append("SquareUp API Key is required when using SquareUp CRM")
                                
                                if new_calendar_type == "squareup" and not new_calendar_api_key:
                                    validation_errors.append("SquareUp Calendar API Key is required when using SquareUp Calendar")
                                elif new_calendar_type == "google" and not new_calendar_api_key:
                                    validation_errors.append("Google Calendar API Key is required when using Google Calendar")
                                
                                if validation_errors:
                                    for error in validation_errors:
                                        st.error(error)
                                else:
                                    # Prepare update data
                                    update_data = {
                                        "business_name": new_business_name,
                                        "business_type": new_business_type,
                                        "phone": new_phone,
                                        "email": new_email,
                                        "street_address": new_street_address or None,
                                        "city": new_city or None,
                                        "state": new_state or None,
                                        "zip_code": new_zip_code or None,
                                        "country": new_country or None,
                                        "crm_type": new_crm_type or None,
                                        "crm_api_key": new_crm_api_key or None,
                                        "calendar_type": new_calendar_type or None,
                                        "calendar_id": new_calendar_api_key or None,
                                        "twilio_number": new_twilio_number or None,
                                        "front_desk_number": new_front_desk_number or None,
                                        "front_desk_email": new_front_desk_email or None,
                                        "google_review_link": new_google_review_link or None,
                                        "status": new_status,
                                        "subscription_plan": new_subscription_plan or None,
                                        "subscription_expires_at": new_subscription_expires_at.isoformat() if new_subscription_expires_at else None,
                                        "business_hours": new_business_hours or None,
                                        "updated_at": datetime.now().isoformat()
                                    }
                                    
                                    if supabase.update_client(client_id, update_data):
                                        st.success("✅ Client updated successfully!")
                                        st.session_state[f"edit_mode_{client_id}"] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to update client.")
                    
                    with col2:
                        if st.form_submit_button("❌ Cancel"):
                            st.session_state[f"edit_mode_{client_id}"] = False
                            st.rerun()
                    
                    with col3:
                        if st.form_submit_button("🗑️ Delete Client", type="secondary"):
                            if supabase.delete_client(client_id):
                                st.success("Client deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete client.")

def render_analytics():
    """Render the analytics page"""
    st.header("📈 Analytics & Insights")
    
    clients = supabase.get_all_clients()
    
    if not clients:
        st.warning("No clients found. Add clients to view analytics!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_clients = len(clients)
        st.metric("Total Clients", total_clients)
    
    with col2:
        active_clients = len([c for c in clients if c.get('status') == 'active'])
        activation_rate = (active_clients / total_clients * 100) if total_clients > 0 else 0
        st.metric("Activation Rate", f"{activation_rate:.1f}%")
    
    with col3:
        clients_with_integrations = len([c for c in clients if c.get('calendar_type') or c.get('crm_type')])
        integration_rate = (clients_with_integrations / total_clients * 100) if total_clients > 0 else 0
        st.metric("Integration Rate", f"{integration_rate:.1f}%")
    
    with col4:
        subscription_plans = [c.get('subscription_plan') for c in clients if c.get('subscription_plan')]
        avg_plan_value = len(subscription_plans)
        st.metric("Subscribed Clients", avg_plan_value)
    
    # Detailed charts
    st.subheader("📊 Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Business type distribution
        business_types = [c.get('business_type') or 'Not specified' for c in clients]
        business_type_df = pd.DataFrame({'Business Type': business_types})
        business_type_counts = business_type_df['Business Type'].value_counts()
        
        fig = px.bar(
            x=business_type_counts.values,
            y=business_type_counts.index,
            orientation='h',
            title="Clients by Business Type",
            labels={'x': 'Number of Clients', 'y': 'Business Type'},
            color=business_type_counts.values,
            color_continuous_scale=[[0, '#1e293b'], [0.5, '#6366f1'], [1, '#06b6d4']]
        )
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            title_font=dict(color='#f1f5f9', size=16)
        )
        fig.update_xaxes(
            gridcolor='rgba(148,163,184,0.2)',
            title_font=dict(color='#e2e8f0'),
            tickfont=dict(color='#e2e8f0')
        )
        fig.update_yaxes(
            gridcolor='rgba(148,163,184,0.2)',
            title_font=dict(color='#e2e8f0'),
            tickfont=dict(color='#e2e8f0')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status distribution
        statuses = [c.get('status', 'unknown') for c in clients]
        status_df = pd.DataFrame({'Status': statuses})
        status_counts = status_df['Status'].value_counts()
        
        # Status color mapping
        status_colors = {
            'active': '#10b981',
            'pending': '#f59e0b', 
            'inactive': '#ef4444',
            'trial': '#06b6d4',
            'unknown': '#6b7280'
        }
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Client Status Distribution",
            color=status_counts.index,
            color_discrete_map=status_colors
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=12,
            textfont_color='white'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            title_font=dict(color='#f1f5f9', size=16)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Integration analysis
    st.subheader("🔗 Integration Analysis")
    
    integration_data = []
    for client in clients:
        integrations = []
        if client.get('calendar_type'):
            integrations.append(f"Calendar ({client.get('calendar_type')})")
        if client.get('crm_type'):
            integrations.append(f"CRM ({client.get('crm_type')})")
        if client.get('twilio_number'):
            integrations.append("Twilio")
        
        integration_data.append({
            'Client': client.get('business_name', 'N/A'),
            'Integrations': ', '.join(integrations) if integrations else 'None',
            'Count': len(integrations)
        })
    
    integration_df = pd.DataFrame(integration_data)
    
    if not integration_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Integration count distribution
            integration_counts = integration_df['Count'].value_counts().sort_index()
            fig = px.bar(
                x=integration_counts.index,
                y=integration_counts.values,
                title="Number of Integrations per Client",
                labels={'x': 'Number of Integrations', 'y': 'Number of Clients'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top integrations
            all_integrations = []
            for integrations in integration_df['Integrations']:
                if integrations != 'None':
                    all_integrations.extend(integrations.split(', '))
            
            if all_integrations:
                integration_popularity = pd.Series(all_integrations).value_counts()
                fig = px.bar(
                    x=integration_popularity.values,
                    y=integration_popularity.index,
                    orientation='h',
                    title="Most Popular Integrations",
                    labels={'x': 'Number of Clients', 'y': 'Integration Type'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Client insights table
    st.subheader("📋 Client Insights")
    
    insights_data = []
    for client in clients:
        insights_data.append({
            'Business Name': client.get('business_name') or 'Unnamed Business',
            'Type': client.get('business_type') or 'Not specified',
            'Status': client.get('status', 'unknown'),
            'Calendar': '✅' if client.get('calendar_type') else '❌',
            'CRM': '✅' if client.get('crm_type') else '❌',
            'Subscription': client.get('subscription_plan') or 'Not setup',
            'Email': client.get('email') or 'Not setup'
        })
    
    insights_df = pd.DataFrame(insights_data)
    st.dataframe(insights_df, use_container_width=True)

def main():
    """Main application function"""
    render_header()
    
    # Sidebar navigation
    page = render_sidebar()
    
    # Render selected page
    if page == "📊 Dashboard Overview":
        render_dashboard_overview()
    elif page == "➕ Add New Client":
        render_add_client_form()
    elif page == "👥 Client Management":
        render_client_management()
    elif page == "📈 Analytics":
        render_analytics()

if __name__ == "__main__":
    main()
