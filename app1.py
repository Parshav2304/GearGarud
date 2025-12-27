import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="GearGuard - Maintenance Tracker",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'equipment' not in st.session_state:
    st.session_state.equipment = [
        {
            'id': 1,
            'name': 'CNC Machine 01',
            'serialNumber': 'CNC-2024-001',
            'category': 'Production',
            'department': 'Production',
            'owner': 'Factory Floor',
            'purchaseDate': '2023-05-15',
            'warranty': '2025-05-15',
            'location': 'Building A, Floor 2',
            'maintenanceTeam': 'Mechanics',
            'defaultTechnician': 'John Doe'
        },
        {
            'id': 2,
            'name': 'Laptop Dell XPS',
            'serialNumber': 'DELL-2024-042',
            'category': 'IT Equipment',
            'department': 'Engineering',
            'owner': 'Alice Johnson',
            'purchaseDate': '2024-01-10',
            'warranty': '2027-01-10',
            'location': 'Office 301',
            'maintenanceTeam': 'IT Support',
            'defaultTechnician': 'Tom Brown'
        }
    ]

if 'teams' not in st.session_state:
    st.session_state.teams = [
        {'id': 1, 'name': 'Mechanics', 'members': ['John Doe', 'Jane Smith']},
        {'id': 2, 'name': 'Electricians', 'members': ['Mike Johnson', 'Sarah Wilson']},
        {'id': 3, 'name': 'IT Support', 'members': ['Tom Brown', 'Lisa Garcia']}
    ]

if 'requests' not in st.session_state:
    st.session_state.requests = [
        {
            'id': 1,
            'subject': 'Leaking Oil',
            'equipmentId': 1,
            'equipmentName': 'CNC Machine 01',
            'type': 'Corrective',
            'stage': 'New',
            'scheduledDate': '2024-12-28',
            'duration': 0,
            'assignedTo': None,
            'createdDate': '2024-12-27',
            'priority': 'High',
            'category': 'Production',
            'maintenanceTeam': 'Mechanics'
        },
        {
            'id': 2,
            'subject': 'Monthly Maintenance Check',
            'equipmentId': 1,
            'equipmentName': 'CNC Machine 01',
            'type': 'Preventive',
            'stage': 'In Progress',
            'scheduledDate': '2024-12-30',
            'duration': 2,
            'assignedTo': 'John Doe',
            'createdDate': '2024-12-20',
            'priority': 'Medium',
            'category': 'Production',
            'maintenanceTeam': 'Mechanics'
        }
    ]

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .kanban-card {
        background: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .overdue {
        border-left: 4px solid #ef4444 !important;
        background: #fef2f2 !important;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px;
    }
    .badge-corrective {
        background: #fee2e2;
        color: #dc2626;
    }
    .badge-preventive {
        background: #dcfce7;
        color: #16a34a;
    }
    .badge-high {
        background: #fef2f2;
        color: #dc2626;
    }
    .badge-medium {
        background: #fef3c7;
        color: #d97706;
    }
    .badge-low {
        background: #dbeafe;
        color: #2563eb;
    }
    .equipment-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-top: 4px solid #3b82f6;
    }
    .team-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 4px solid #8b5cf6;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #1e3a8a 100%);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_equipment_by_id(eq_id):
    for eq in st.session_state.equipment:
        if eq['id'] == eq_id:
            return eq
    return None

def is_overdue(request):
    if not request.get('scheduledDate'):
        return False
    scheduled = datetime.strptime(request['scheduledDate'], '%Y-%m-%d')
    return scheduled < datetime.now() and request['stage'] != 'Repaired'

def get_requests_by_equipment(eq_id):
    return [r for r in st.session_state.requests if r['equipmentId'] == eq_id and r['stage'] != 'Scrap']

# Header
st.markdown("""
<div class="main-header">
    <h1>🔧 GearGuard - Maintenance Tracker</h1>
    <p>Ultimate Equipment and Maintenance Management System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/maintenance.png", width=100)
    st.title("Navigation")
    view = st.radio("Select View", 
                    ["🎯 Kanban Board", "📅 Calendar", "⚙️ Equipment", "👥 Teams", "📊 Analytics"],
                    label_visibility="collapsed")

# Main Content
if view == "🎯 Kanban Board":
    st.header("Maintenance Kanban Board")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ New Request"):
            st.session_state.show_request_form = True
    
    # Show request form
    if st.session_state.get('show_request_form', False):
        with st.form("new_request_form"):
            st.subheader("Create New Maintenance Request")
            subject = st.text_input("Subject *")
            equipment_options = {eq['id']: eq['name'] for eq in st.session_state.equipment}
            selected_eq_id = st.selectbox("Equipment *", options=list(equipment_options.keys()), 
                                         format_func=lambda x: equipment_options[x])
            request_type = st.selectbox("Type *", ["Corrective", "Preventive"])
            priority = st.selectbox("Priority *", ["High", "Medium", "Low"])
            scheduled_date = st.date_input("Scheduled Date *")
            description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Create Request")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                selected_eq = get_equipment_by_id(selected_eq_id)
                new_request = {
                    'id': len(st.session_state.requests) + 1,
                    'subject': subject,
                    'equipmentId': selected_eq_id,
                    'equipmentName': selected_eq['name'],
                    'type': request_type,
                    'stage': 'New',
                    'scheduledDate': scheduled_date.strftime('%Y-%m-%d'),
                    'duration': 0,
                    'assignedTo': None,
                    'createdDate': datetime.now().strftime('%Y-%m-%d'),
                    'priority': priority,
                    'category': selected_eq['category'],
                    'maintenanceTeam': selected_eq['maintenanceTeam'],
                    'description': description
                }
                st.session_state.requests.append(new_request)
                st.session_state.show_request_form = False
                st.success("✅ Request created successfully!")
                st.rerun()
            
            if cancel:
                st.session_state.show_request_form = False
                st.rerun()
    
    # Kanban columns
    stages = ['New', 'In Progress', 'Repaired', 'Scrap']
    cols = st.columns(4)
    
    for idx, stage in enumerate(stages):
        with cols[idx]:
            stage_requests = [r for r in st.session_state.requests if r['stage'] == stage]
            st.markdown(f"### {stage} ({len(stage_requests)})")
            
            for request in stage_requests:
                overdue = is_overdue(request)
                card_class = "kanban-card overdue" if overdue else "kanban-card"
                
                st.markdown(f"""
                <div class="{card_class}">
                    {"<p style='color: #dc2626; font-weight: bold; font-size: 12px;'>⚠️ OVERDUE</p>" if overdue else ""}
                    <h4 style='margin: 0; color: #1f2937;'>{request['subject']}</h4>
                    <p style='color: #6b7280; font-size: 14px; margin: 5px 0;'>{request['equipmentName']}</p>
                    <span class="badge badge-{request['type'].lower()}">{request['type']}</span>
                    <span class="badge badge-{request['priority'].lower()}">{request['priority']}</span>
                    <p style='color: #6b7280; font-size: 12px; margin-top: 10px;'>📅 {request['scheduledDate']}</p>
                    {f"<p style='color: #2563eb; font-size: 12px;'>👤 {request['assignedTo']}</p>" if request['assignedTo'] else "<p style='color: #9ca3af; font-size: 12px;'>👤 Unassigned</p>"}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                with st.expander("Actions"):
                    if not request['assignedTo']:
                        all_members = []
                        for team in st.session_state.teams:
                            all_members.extend([(m, team['name']) for m in team['members']])
                        
                        selected_tech = st.selectbox(
                            "Assign to:", 
                            options=[m[0] for m in all_members],
                            format_func=lambda x: f"{x} ({[t[1] for t in all_members if t[0] == x][0]})",
                            key=f"assign_{request['id']}"
                        )
                        if st.button("Assign", key=f"assign_btn_{request['id']}"):
                            request['assignedTo'] = selected_tech
                            request['stage'] = 'In Progress'
                            st.success(f"Assigned to {selected_tech}")
                            st.rerun()
                    
                    if stage == 'New':
                        if st.button("▶️ Start Work", key=f"start_{request['id']}"):
                            request['stage'] = 'In Progress'
                            st.rerun()
                    
                    if stage == 'In Progress':
                        if st.button("✅ Mark as Repaired", key=f"repair_{request['id']}"):
                            request['stage'] = 'Repaired'
                            st.rerun()
                    
                    if st.button("🗑️ Move to Scrap", key=f"scrap_{request['id']}"):
                        request['stage'] = 'Scrap'
                        st.warning("Equipment marked for scrap")
                        st.rerun()

elif view == "📅 Calendar":
    st.header("Preventive Maintenance Schedule")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Schedule Maintenance"):
            st.session_state.show_request_form = True
    
    # Calendar view
    st.subheader("December 2024")
    
    # Create calendar grid
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    cols = st.columns(7)
    
    for idx, day in enumerate(days):
        with cols[idx]:
            st.markdown(f"**{day}**")
    
    # Display dates with requests
    start_date = datetime(2024, 12, 1)
    for week in range(5):
        cols = st.columns(7)
        for day in range(7):
            date = start_date + timedelta(days=week*7 + day)
            if date.month == 12:
                with cols[day]:
                    date_str = date.strftime('%Y-%m-%d')
                    day_requests = [r for r in st.session_state.requests 
                                   if r['scheduledDate'] == date_str and r['type'] == 'Preventive']
                    
                    st.markdown(f"**{date.day}**")
                    for req in day_requests:
                        st.markdown(f"<div style='background: #dbeafe; padding: 5px; border-radius: 5px; font-size: 11px; margin: 2px 0;'>{req['subject']}</div>", 
                                  unsafe_allow_html=True)

elif view == "⚙️ Equipment":
    st.header("Equipment Database")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Equipment"):
            st.session_state.show_equipment_form = True
    
    # Show equipment form
    if st.session_state.get('show_equipment_form', False):
        with st.form("new_equipment_form"):
            st.subheader("Add New Equipment")
            name = st.text_input("Equipment Name *")
            serial = st.text_input("Serial Number *")
            category = st.text_input("Category *")
            department = st.text_input("Department *")
            owner = st.text_input("Owner *")
            purchase_date = st.date_input("Purchase Date *")
            warranty = st.date_input("Warranty End Date *")
            location = st.text_input("Location *")
            team_options = [t['name'] for t in st.session_state.teams]
            maintenance_team = st.selectbox("Maintenance Team *", team_options)
            default_tech = st.text_input("Default Technician *")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Add Equipment")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                new_equipment = {
                    'id': len(st.session_state.equipment) + 1,
                    'name': name,
                    'serialNumber': serial,
                    'category': category,
                    'department': department,
                    'owner': owner,
                    'purchaseDate': purchase_date.strftime('%Y-%m-%d'),
                    'warranty': warranty.strftime('%Y-%m-%d'),
                    'location': location,
                    'maintenanceTeam': maintenance_team,
                    'defaultTechnician': default_tech
                }
                st.session_state.equipment.append(new_equipment)
                st.session_state.show_equipment_form = False
                st.success("✅ Equipment added successfully!")
                st.rerun()
            
            if cancel:
                st.session_state.show_equipment_form = False
                st.rerun()
    
    # Display equipment
    cols = st.columns(2)
    for idx, eq in enumerate(st.session_state.equipment):
        with cols[idx % 2]:
            req_count = len(get_requests_by_equipment(eq['id']))
            st.markdown(f"""
            <div class="equipment-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin: 0; color: #1f2937;">{eq['name']}</h3>
                        <p style="color: #6b7280; font-size: 14px;">{eq['serialNumber']}</p>
                    </div>
                    <span style="background: #dbeafe; color: #2563eb; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                        🔧 {req_count} Requests
                    </span>
                </div>
                <hr style="margin: 15px 0;">
                <div style="font-size: 14px;">
                    <p><strong>Category:</strong> {eq['category']}</p>
                    <p><strong>Department:</strong> {eq['department']}</p>
                    <p><strong>Location:</strong> {eq['location']}</p>
                    <p><strong>Owner:</strong> {eq['owner']}</p>
                    <p><strong>Warranty:</strong> {eq['warranty']}</p>
                    <p><strong>Team:</strong> {eq['maintenanceTeam']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Maintenance History"):
                history = get_requests_by_equipment(eq['id'])
                if history:
                    for req in history:
                        st.markdown(f"**{req['subject']}** - {req['stage']}")
                        st.caption(f"{req['type']} | Scheduled: {req['scheduledDate']}")
                else:
                    st.info("No maintenance requests found")

elif view == "👥 Teams":
    st.header("Maintenance Teams")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Team"):
            st.session_state.show_team_form = True
    
    # Show team form
    if st.session_state.get('show_team_form', False):
        with st.form("new_team_form"):
            st.subheader("Add New Team")
            team_name = st.text_input("Team Name *")
            members = st.text_area("Team Members (one per line) *")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Add Team")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                member_list = [m.strip() for m in members.split('\n') if m.strip()]
                new_team = {
                    'id': len(st.session_state.teams) + 1,
                    'name': team_name,
                    'members': member_list
                }
                st.session_state.teams.append(new_team)
                st.session_state.show_team_form = False
                st.success("✅ Team added successfully!")
                st.rerun()
            
            if cancel:
                st.session_state.show_team_form = False
                st.rerun()
    
    # Display teams
    cols = st.columns(3)
    for idx, team in enumerate(st.session_state.teams):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="team-card">
                <h3 style="margin: 0; color: #1f2937;">👥 {team['name']}</h3>
                <hr style="margin: 15px 0;">
                <p style="font-weight: 600; color: #6b7280; font-size: 14px;">Team Members:</p>
            </div>
            """, unsafe_allow_html=True)
            
            for member in team['members']:
                st.markdown(f"• {member}")

elif view == "📊 Analytics":
    st.header("Analytics Dashboard")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div>Total Equipment</div>
            <div class="stat-number">{len(st.session_state.equipment)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div>Total Requests</div>
            <div class="stat-number">{len(st.session_state.requests)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        in_progress = len([r for r in st.session_state.requests if r['stage'] == 'In Progress'])
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div>In Progress</div>
            <div class="stat-number">{in_progress}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        completed = len([r for r in st.session_state.requests if r['stage'] == 'Repaired'])
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div>Completed</div>
            <div class="stat-number">{completed}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests by Type")
        type_data = pd.DataFrame({
            'Type': ['Corrective', 'Preventive'],
            'Count': [
                len([r for r in st.session_state.requests if r['type'] == 'Corrective']),
                len([r for r in st.session_state.requests if r['type'] == 'Preventive'])
            ]
        })
        st.bar_chart(type_data.set_index('Type'))
    
    with col2:
        st.subheader("Requests by Stage")
        stage_data = pd.DataFrame({
            'Stage': stages,
            'Count': [len([r for r in st.session_state.requests if r['stage'] == s]) for s in stages]
        })
        st.bar_chart(stage_data.set_index('Stage'))
    
    # Team performance
    st.subheader("Requests by Team")
    team_data = {}
    for team in st.session_state.teams:
        team_data[team['name']] = len([r for r in st.session_state.requests if r.get('maintenanceTeam') == team['name']])
    
    team_df = pd.DataFrame(list(team_data.items()), columns=['Team', 'Requests'])
    st.bar_chart(team_df.set_index('Team'))
    
    # Detailed table
    st.subheader("All Maintenance Requests")
    df = pd.DataFrame(st.session_state.requests)
    if not df.empty:
        st.dataframe(df[['subject', 'equipmentName', 'type', 'stage', 'priority', 'scheduledDate', 'assignedTo']], 
                    use_container_width=True)
