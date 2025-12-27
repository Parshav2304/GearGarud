import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from config.settings import PAGE_CONFIG, CUSTOM_CSS
from utils.session_state import initialize_session_state
from utils.helpers import get_equipment_by_id, is_overdue, get_requests_by_equipment
from views import kanban, calendar_view, equipment, teams, analytics

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Initialize session state
initialize_session_state()

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header with animated gradient
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <div class="logo-section">
            <span class="logo-icon">🔧</span>
            <div>
                <h1>GearGuard Pro</h1>
                <p>Ultimate Equipment & Maintenance Management</p>
            </div>
        </div>
        <div class="header-stats">
            <div class="stat-pill">
                <span class="stat-label">Equipment</span>
                <span class="stat-value">{}</span>
            </div>
            <div class="stat-pill">
                <span class="stat-label">Active Tasks</span>
                <span class="stat-value">{}</span>
            </div>
        </div>
    </div>
</div>
""".format(
    len(st.session_state.equipment),
    len([r for r in st.session_state.requests if r['stage'] in ['New', 'In Progress']])
), unsafe_allow_html=True)

# Sidebar Navigation with enhanced design
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">⚙️</div>
        <div class="sidebar-title">Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    view_options = [
        ("🎯 Kanban Board", "kanban", "Drag & drop maintenance workflow"),
        ("📅 Calendar", "calendar", "Schedule preventive maintenance"),
        ("⚙️ Equipment", "equipment", "Asset database & tracking"),
        ("👥 Teams", "teams", "Maintenance team management"),
        ("📊 Analytics", "analytics", "Performance insights & reports")
    ]
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'kanban'
    
    for label, key, description in view_options:
        is_active = st.session_state.current_view == key
        button_class = "nav-button-active" if is_active else "nav-button"
        
        col1, col2 = st.columns([1, 5])
        with col2:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_view = key
                st.rerun()
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("""
    <div class="sidebar-stats">
        <div class="sidebar-stat-item">
            <span class="sidebar-stat-label">Overdue</span>
            <span class="sidebar-stat-value overdue-badge">{}</span>
        </div>
        <div class="sidebar-stat-item">
            <span class="sidebar-stat-label">Today</span>
            <span class="sidebar-stat-value today-badge">{}</span>
        </div>
    </div>
    """.format(
        len([r for r in st.session_state.requests if is_overdue(r)]),
        len([r for r in st.session_state.requests if r['scheduledDate'] == datetime.now().strftime('%Y-%m-%d')])
    ), unsafe_allow_html=True)

# Main Content Router
current_view = st.session_state.current_view

if current_view == 'kanban':
    kanban.render()
elif current_view == 'calendar':
    calendar_view.render()
elif current_view == 'equipment':
    equipment.render()
elif current_view == 'teams':
    teams.render()
elif current_view == 'analytics':
    analytics.render()

# Footer
st.markdown("""
<div class="footer">
    <p>GearGuard Pro v1.0 | Built for Excellence | © 2024</p>
</div>
""", unsafe_allow_html=True)
