"""
Kanban Board View for GearGuard Pro
"""
import streamlit as st
from datetime import datetime
from helpers import get_equipment_by_id, is_overdue, get_all_technicians, generate_next_id

def render():
    """Render the Kanban board view"""
    
    # Header with action button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 🎯 Maintenance Kanban Board")
        st.markdown("*Drag & drop workflow for maintenance requests*")
    with col2:
        if st.button("➕ New Request", use_container_width=True):
            st.session_state.show_request_form = True
    
    st.markdown("---")
    
    # Show request form
    if st.session_state.get('show_request_form', False):
        render_request_form()
        return
    
    # Display overdue alert
    overdue_requests = [r for r in st.session_state.requests if is_overdue(r)]
    if overdue_requests:
        st.markdown(f"""
        <div class="overdue-alert">
            <span style="font-size: 1.5rem;">⚠️</span>
            <span><strong>{len(overdue_requests)} Overdue Request(s)</strong> - Immediate attention required!</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Kanban columns
    stages = ['New', 'In Progress', 'Repaired', 'Scrap']
    stage_emojis = {'New': '🆕', 'In Progress': '⚙️', 'Repaired': '✅', 'Scrap': '🗑️'}
    cols = st.columns(4)
    
    for idx, stage in enumerate(stages):
        with cols[idx]:
            stage_requests = [r for r in st.session_state.requests if r['stage'] == stage]
            
            # Column header
            st.markdown(f"""
            <div class="kanban-column">
                <div class="kanban-header">
                    <span>{stage_emojis[stage]} {stage}</span>
                    <span class="kanban-count">{len(stage_requests)}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Display cards
            for request in stage_requests:
                render_request_card(request, stage)
            
            st.markdown("</div>", unsafe_allow_html=True)

def render_request_card(request, stage):
    """Render a single request card"""
    overdue = is_overdue(request)
    card_class = "kanban-card overdue" if overdue else "kanban-card"
    
    # Card content
    st.markdown(f"""
    <div class="{card_class}">
        {f'<div class="overdue-alert" style="padding: 0.5rem; margin-bottom: 0.8rem;">⚠️ OVERDUE</div>' if overdue else ''}
        <h4 class="kanban-card-title">{request['subject']}</h4>
        <p class="kanban-card-equipment">🔧 {request['equipmentName']}</p>
        <div style="margin: 1rem 0;">
            <span class="badge badge-{request['type'].lower()}">{request['type']}</span>
            <span class="badge badge-{request['priority'].lower()}">{request['priority']}</span>
        </div>
        <p style="color: #64748b; font-size: 0.85rem; margin: 0.5rem 0;">
            📅 Scheduled: {format_date_display(request['scheduledDate'])}
        </p>
        <p style="color: #64748b; font-size: 0.85rem; margin: 0.5rem 0;">
            👤 {request['assignedTo'] if request['assignedTo'] else '<em>Unassigned</em>'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons in expander
    with st.expander("🔧 Actions & Details", expanded=False):
        # Show description if available
        if request.get('description'):
            st.markdown(f"**Description:** {request['description']}")
            st.markdown("---")
        
        # Assignment section
        if not request['assignedTo']:
            st.markdown("**Assign Technician:**")
            technicians = get_all_technicians()
            
            if technicians:
                tech_options = {f"{t['name']} ({t['team']})": t['name'] for t in technicians}
                selected = st.selectbox(
                    "Select technician:",
                    options=list(tech_options.keys()),
                    key=f"assign_select_{request['id']}",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Assign", key=f"assign_btn_{request['id']}", use_container_width=True):
                        request['assignedTo'] = tech_options[selected]
                        if request['stage'] == 'New':
                            request['stage'] = 'In Progress'
                        st.success(f"Assigned to {tech_options[selected]}")
                        st.rerun()
        else:
            st.info(f"Currently assigned to: **{request['assignedTo']}**")
            if st.button("🔄 Reassign", key=f"reassign_{request['id']}", use_container_width=True):
                request['assignedTo'] = None
                st.rerun()
        
        st.markdown("---")
        
        # Stage transition buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if stage == 'New' and st.button("▶️ Start Work", key=f"start_{request['id']}", use_container_width=True):
                request['stage'] = 'In Progress'
                st.rerun()
            
            if stage == 'In Progress':
                if st.button("✅ Mark Repaired", key=f"repair_{request['id']}", use_container_width=True):
                    request['stage'] = 'Repaired'
                    if request['duration'] == 0:
                        request['duration'] = 1  # Default duration
                    st.success("Request completed!")
                    st.rerun()
        
        with col2:
            if stage != 'Scrap':
                if st.button("🗑️ Move to Scrap", key=f"scrap_{request['id']}", use_container_width=True):
                    request['stage'] = 'Scrap'
                    # Update equipment status
                    equipment = get_equipment_by_id(request['equipmentId'])
                    if equipment:
                        equipment['status'] = 'Scrapped'
                    st.warning("Equipment marked for scrap")
                    st.rerun()
        
        # Duration input for completed work
        if stage == 'In Progress' or stage == 'Repaired':
            st.markdown("---")
            duration = st.number_input(
                "Work Duration (hours):",
                min_value=0.0,
                value=float(request.get('duration', 0)),
                step=0.5,
                key=f"duration_{request['id']}"
            )
            if st.button("💾 Save Duration", key=f"save_duration_{request['id']}", use_container_width=True):
                request['duration'] = duration
                st.success("Duration saved!")
                st.rerun()

def render_request_form():
    """Render the new request form"""
    st.markdown("## ➕ Create New Maintenance Request")
    
    with st.form("new_request_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Subject *", placeholder="e.g., Oil Leak Detected")
            
            equipment_options = {eq['id']: f"{eq['name']} ({eq['serialNumber']})" 
                               for eq in st.session_state.equipment}
            selected_eq_id = st.selectbox(
                "Equipment *",
                options=list(equipment_options.keys()),
                format_func=lambda x: equipment_options[x]
            )
            
            request_type = st.selectbox("Type *", ["Corrective", "Preventive"])
            priority = st.selectbox("Priority *", ["High", "Medium", "Low"])
        
        with col2:
            scheduled_date = st.date_input(
                "Scheduled Date *",
                min_value=datetime.now().date()
            )
            
            # Get equipment details to auto-fill
            selected_eq = get_equipment_by_id(selected_eq_id)
            
            if selected_eq:
                st.text_input("Category", value=selected_eq['category'], disabled=True)
                st.text_input("Maintenance Team", value=selected_eq['maintenanceTeam'], disabled=True)
                
                # Option to assign technician
                team_members = []
                for team in st.session_state.teams:
                    if team['name'] == selected_eq['maintenanceTeam']:
                        team_members = team['members']
                        break
                
                assign_now = st.checkbox("Assign technician now?")
                assigned_tech = None
                if assign_now and team_members:
                    assigned_tech = st.selectbox("Technician", options=team_members)
        
        description = st.text_area(
            "Description",
            placeholder="Detailed description of the maintenance request...",
            height=100
        )
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit = st.form_submit_button("✅ Create Request", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit and subject and selected_eq_id:
            selected_eq = get_equipment_by_id(selected_eq_id)
            new_request = {
                'id': generate_next_id(st.session_state.requests),
                'subject': subject,
                'equipmentId': selected_eq_id,
                'equipmentName': selected_eq['name'],
                'type': request_type,
                'stage': 'In Progress' if assigned_tech else 'New',
                'scheduledDate': scheduled_date.strftime('%Y-%m-%d'),
                'duration': 0,
                'assignedTo': assigned_tech,
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

def format_date_display(date_str):
    """Format date for display"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_str
