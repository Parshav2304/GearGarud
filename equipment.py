"""
Equipment Management View for GearGuard Pro
"""
import streamlit as st
from datetime import datetime
from helpers import (
    get_requests_by_equipment, 
    get_warranty_status, 
    format_date,
    generate_next_id,
    is_overdue
)

def render():
    """Render the equipment management view"""
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## ⚙️ Equipment Database")
        st.markdown("*Centralized asset tracking and management*")
    with col2:
        search_term = st.text_input("🔍 Search", placeholder="Search equipment...", label_visibility="collapsed")
    with col3:
        if st.button("➕ Add Equipment", use_container_width=True):
            st.session_state.show_equipment_form = True
    
    st.markdown("---")
    
    # Show form if requested
    if st.session_state.get('show_equipment_form', False):
        render_equipment_form()
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = ["All"] + list(set([eq['category'] for eq in st.session_state.equipment]))
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        departments = ["All"] + list(set([eq['department'] for eq in st.session_state.equipment]))
        selected_department = st.selectbox("Filter by Department", departments)
    
    with col3:
        teams = ["All"] + list(set([eq['maintenanceTeam'] for eq in st.session_state.equipment]))
        selected_team = st.selectbox("Filter by Team", teams)
    
    # Filter equipment
    filtered_equipment = st.session_state.equipment
    
    if search_term:
        filtered_equipment = [eq for eq in filtered_equipment 
                             if search_term.lower() in eq['name'].lower() 
                             or search_term.lower() in eq['serialNumber'].lower()]
    
    if selected_category != "All":
        filtered_equipment = [eq for eq in filtered_equipment if eq['category'] == selected_category]
    
    if selected_department != "All":
        filtered_equipment = [eq for eq in filtered_equipment if eq['department'] == selected_department]
    
    if selected_team != "All":
        filtered_equipment = [eq for eq in filtered_equipment if eq['maintenanceTeam'] == selected_team]
    
    # Summary stats
    st.markdown("### 📊 Equipment Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Equipment", len(filtered_equipment))
    
    with col2:
        operational = len([eq for eq in filtered_equipment if eq.get('status') == 'Operational'])
        st.metric("Operational", operational)
    
    with col3:
        with_requests = len([eq for eq in filtered_equipment 
                           if any(r['equipmentId'] == eq['id'] and r['stage'] in ['New', 'In Progress'] 
                                 for r in st.session_state.requests)])
        st.metric("With Pending Tasks", with_requests)
    
    with col4:
        scrapped = len([eq for eq in filtered_equipment if eq.get('status') == 'Scrapped'])
        st.metric("Scrapped", scrapped)
    
    st.markdown("---")
    
    # Display equipment cards
    if not filtered_equipment:
        st.info("No equipment found matching the filters.")
    else:
        # Display in a 2-column grid
        cols = st.columns(2)
        for idx, eq in enumerate(filtered_equipment):
            with cols[idx % 2]:
                render_equipment_card(eq)

def render_equipment_card(eq):
    """Render a single equipment card with smart button"""
    
    # Get maintenance requests for this equipment
    requests = get_requests_by_equipment(eq['id'])
    pending_requests = [r for r in requests if r['stage'] in ['New', 'In Progress']]
    overdue_requests = [r for r in pending_requests if is_overdue(r)]
    
    # Warranty status
    warranty_status = get_warranty_status(eq['warranty'])
    warranty_color = "#ff6b6b" if "Expired" in warranty_status or "Expiring" in warranty_status else "#51cf66"
    
    # Equipment status color
    status_color = {
        'Operational': '#51cf66',
        'Under Maintenance': '#ffd43b',
        'Scrapped': '#ff6b6b'
    }.get(eq.get('status', 'Operational'), '#51cf66')
    
    st.markdown(f"""
    <div class="equipment-card">
        <div class="equipment-header">
            <div>
                <h3 class="equipment-name">{eq['name']}</h3>
                <p class="equipment-serial">SN: {eq['serialNumber']}</p>
            </div>
            <div class="equipment-badge">
                🔧 {len(requests)} Request(s)
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Status badges
    if overdue_requests:
        st.markdown(f"""
        <div style='
            background: #ff6b6b;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-weight: 600;
        '>
            ⚠️ {len(overdue_requests)} Overdue Request(s)
        </div>
        """, unsafe_allow_html=True)
    
    # Equipment details grid
    st.markdown(f"""
        <div class="equipment-details">
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Category</div>
                <div class="equipment-detail-value">{eq['category']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Department</div>
                <div class="equipment-detail-value">{eq['department']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Location</div>
                <div class="equipment-detail-value">{eq['location']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Owner</div>
                <div class="equipment-detail-value">{eq['owner']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Purchase Date</div>
                <div class="equipment-detail-value">{format_date(eq['purchaseDate'])}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Warranty</div>
                <div class="equipment-detail-value" style="color: {warranty_color};">{warranty_status}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Maintenance Team</div>
                <div class="equipment-detail-value">{eq['maintenanceTeam']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Default Technician</div>
                <div class="equipment-detail-value">{eq['defaultTechnician']}</div>
            </div>
            <div class="equipment-detail-item">
                <div class="equipment-detail-label">Status</div>
                <div class="equipment-detail-value" style="color: {status_color};">
                    {eq.get('status', 'Operational')}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Smart button - View maintenance history
    with st.expander(f"📋 View Maintenance History ({len(requests)} records)", expanded=False):
        if requests:
            # Summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", len(requests))
            with col2:
                completed = len([r for r in requests if r['stage'] == 'Repaired'])
                st.metric("Completed", completed)
            with col3:
                st.metric("Pending", len(pending_requests))
            
            st.markdown("---")
            
            # List all requests
            for request in sorted(requests, key=lambda x: x['scheduledDate'], reverse=True):
                stage_color = {
                    'New': '#ffd43b',
                    'In Progress': '#4ecdc4',
                    'Repaired': '#51cf66',
                    'Scrap': '#ff6b6b'
                }.get(request['stage'], '#667eea')
                
                overdue_tag = ""
                if is_overdue(request):
                    overdue_tag = "<span style='background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 8px;'>OVERDUE</span>"
                
                st.markdown(f"""
                <div style='
                    background: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid {stage_color};
                    margin-bottom: 0.8rem;
                '>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <strong style='color: #1a1a2e;'>{request['subject']}</strong>
                            {overdue_tag}
                            <p style='color: #64748b; font-size: 0.85rem; margin: 0.3rem 0;'>
                                {request['type']} | Priority: {request['priority']}
                            </p>
                            <p style='color: #64748b; font-size: 0.85rem; margin: 0.3rem 0;'>
                                📅 Scheduled: {format_date(request['scheduledDate'])}
                            </p>
                            {f"<p style='color: #64748b; font-size: 0.85rem; margin: 0.3rem 0;'>👤 Assigned to: {request['assignedTo']}</p>" if request['assignedTo'] else ""}
                        </div>
                        <div style='
                            background: {stage_color};
                            color: white;
                            padding: 0.4rem 1rem;
                            border-radius: 20px;
                            font-size: 0.8rem;
                            font-weight: 600;
                        '>
                            {request['stage']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No maintenance history available for this equipment.")

def render_equipment_form():
    """Render the add equipment form"""
    st.markdown("## ➕ Add New Equipment")
    
    with st.form("equipment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Equipment Name *", placeholder="e.g., CNC Machine 02")
            serial = st.text_input("Serial Number *", placeholder="e.g., CNC-2024-002")
            category = st.text_input("Category *", placeholder="e.g., Production, IT Equipment")
            department = st.text_input("Department *", placeholder="e.g., Production, Engineering")
            owner = st.text_input("Owner *", placeholder="e.g., Factory Floor, John Smith")
        
        with col2:
            purchase_date = st.date_input("Purchase Date *", max_value=datetime.now().date())
            warranty = st.date_input("Warranty End Date *", min_value=datetime.now().date())
            location = st.text_input("Location *", placeholder="e.g., Building A, Floor 2")
            
            team_options = [t['name'] for t in st.session_state.teams]
            maintenance_team = st.selectbox("Maintenance Team *", team_options)
            
            # Get team members for default technician
            selected_team = next((t for t in st.session_state.teams if t['name'] == maintenance_team), None)
            tech_options = selected_team['members'] if selected_team else []
            
            default_tech = st.selectbox("Default Technician *", tech_options if tech_options else ["No team members"])
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit = st.form_submit_button("✅ Add Equipment", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit and all([name, serial, category, department, owner, location, default_tech]):
            new_equipment = {
                'id': generate_next_id(st.session_state.equipment),
                'name': name,
                'serialNumber': serial,
                'category': category,
                'department': department,
                'owner': owner,
                'purchaseDate': purchase_date.strftime('%Y-%m-%d'),
                'warranty': warranty.strftime('%Y-%m-%d'),
                'location': location,
                'maintenanceTeam': maintenance_team,
                'defaultTechnician': default_tech,
                'status': 'Operational'
            }
            st.session_state.equipment.append(new_equipment)
            st.session_state.show_equipment_form = False
            st.success(f"✅ Equipment '{name}' added successfully!")
            st.rerun()
        
        if cancel:
            st.session_state.show_equipment_form = False
            st.rerun()
