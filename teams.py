"""
Teams Management View for GearGuard Pro
"""
import streamlit as st
from helpers import get_requests_by_team, generate_next_id

def render():
    """Render the teams management view"""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 👥 Maintenance Teams")
        st.markdown("*Manage teams and track their workload*")
    with col2:
        if st.button("➕ Add Team", use_container_width=True):
            st.session_state.show_team_form = True
    
    st.markdown("---")
    
    # Show form if requested
    if st.session_state.get('show_team_form', False):
        render_team_form()
        return
    
    # Team overview stats
    st.markdown("### 📊 Team Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Teams", len(st.session_state.teams))
    
    with col2:
        total_members = sum(len(team['members']) for team in st.session_state.teams)
        st.metric("Total Technicians", total_members)
    
    with col3:
        active_requests = len([r for r in st.session_state.requests 
                              if r['stage'] in ['New', 'In Progress']])
        st.metric("Active Requests", active_requests)
    
    with col4:
        avg_per_team = round(active_requests / len(st.session_state.teams), 1) if st.session_state.teams else 0
        st.metric("Avg Requests/Team", avg_per_team)
    
    st.markdown("---")
    
    # Display teams in a grid
    cols = st.columns(3)
    for idx, team in enumerate(st.session_state.teams):
        with cols[idx % 3]:
            render_team_card(team)

def render_team_card(team):
    """Render a single team card"""
    
    # Get team workload
    team_requests = get_requests_by_team(team['name'])
    active_requests = [r for r in team_requests if r['stage'] in ['New', 'In Progress']]
    completed_requests = [r for r in team_requests if r['stage'] == 'Repaired']
    
    # Calculate completion rate
    completion_rate = 0
    if team_requests:
        completion_rate = round((len(completed_requests) / len(team_requests)) * 100, 1)
    
    # Workload indicator
    workload_color = "#51cf66"  # Green - Low
    if len(active_requests) > 5:
        workload_color = "#ff6b6b"  # Red - High
    elif len(active_requests) > 2:
        workload_color = "#ffd43b"  # Yellow - Medium
    
    st.markdown(f"""
    <div class="team-card">
        <div class="team-header">
            <span class="team-icon">👥</span>
            <div>
                <h3 class="team-name">{team['name']}</h3>
                <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
                    {len(team['members'])} Member{"s" if len(team['members']) != 1 else ""}
                </p>
            </div>
        </div>
        
        <div style="
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #64748b; font-size: 0.85rem;">Active Tasks</span>
                <span style="
                    background: {workload_color};
                    color: white;
                    padding: 0.2rem 0.8rem;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 0.85rem;
                ">{len(active_requests)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #64748b; font-size: 0.85rem;">Completed</span>
                <span style="font-weight: 600; color: #1a1a2e;">{len(completed_requests)}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748b; font-size: 0.85rem;">Completion Rate</span>
                <span style="font-weight: 600; color: #51cf66;">{completion_rate}%</span>
            </div>
        </div>
        
        <div style="margin-top: 1rem;">
            <p style="
                color: #64748b;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">Team Members</p>
            <div class="team-members">
    """, unsafe_allow_html=True)
    
    for member in team['members']:
        # Count member's active tasks
        member_tasks = [r for r in st.session_state.requests 
                       if r.get('assignedTo') == member and r['stage'] in ['New', 'In Progress']]
        
        st.markdown(f"""
        <div class="member-badge" title="{len(member_tasks)} active task(s)">
            {member}
            {f" ({len(member_tasks)})" if member_tasks else ""}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expandable section for detailed workload
    with st.expander(f"📋 View Team Workload", expanded=False):
        if active_requests:
            st.markdown("**Active Requests:**")
            for request in active_requests:
                status_color = {
                    'New': '#ffd43b',
                    'In Progress': '#4ecdc4'
                }.get(request['stage'], '#667eea')
                
                st.markdown(f"""
                <div style='
                    background: #f8f9fa;
                    padding: 0.8rem;
                    border-radius: 8px;
                    border-left: 4px solid {status_color};
                    margin-bottom: 0.5rem;
                '>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <strong>{request['subject']}</strong>
                            <p style='color: #64748b; font-size: 0.85rem; margin: 0.2rem 0;'>
                                🔧 {request['equipmentName']}
                            </p>
                            <p style='color: #64748b; font-size: 0.8rem; margin: 0.2rem 0;'>
                                👤 {request.get('assignedTo', 'Unassigned')}
                            </p>
                        </div>
                        <div style='
                            background: {status_color};
                            color: white;
                            padding: 0.3rem 0.8rem;
                            border-radius: 15px;
                            font-size: 0.75rem;
                            font-weight: 600;
                            height: fit-content;
                        '>
                            {request['stage']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active requests for this team.")
        
        if completed_requests:
            st.markdown("---")
            st.markdown(f"**Recently Completed:** (Last {min(3, len(completed_requests))})")
            for request in sorted(completed_requests, key=lambda x: x.get('scheduledDate', ''), reverse=True)[:3]:
                st.markdown(f"""
                <div style='
                    background: #f0fdf4;
                    padding: 0.8rem;
                    border-radius: 8px;
                    border-left: 4px solid #51cf66;
                    margin-bottom: 0.5rem;
                '>
                    <strong>{request['subject']}</strong>
                    <p style='color: #64748b; font-size: 0.85rem; margin: 0.2rem 0;'>
                        🔧 {request['equipmentName']} | ⏱️ {request.get('duration', 0)} hours
                    </p>
                </div>
                """, unsafe_allow_html=True)

def render_team_form():
    """Render the add team form"""
    st.markdown("## ➕ Add New Team")
    
    with st.form("team_form", clear_on_submit=True):
        team_name = st.text_input(
            "Team Name *",
            placeholder="e.g., Mechanics, Electricians, IT Support"
        )
        
        st.markdown("**Team Members** *(one per line)*")
        members = st.text_area(
            "Members *",
            placeholder="John Doe\nJane Smith\nRobert Wilson",
            height=150,
            label_visibility="collapsed"
        )
        
        st.info("💡 Tip: Each team member should be on a new line. These technicians will be available for assignment to maintenance requests.")
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit = st.form_submit_button("✅ Add Team", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit and team_name and members:
            # Parse members
            member_list = [m.strip() for m in members.split('\n') if m.strip()]
            
            if not member_list:
                st.error("Please add at least one team member.")
                return
            
            # Check for duplicate team name
            if any(t['name'].lower() == team_name.lower() for t in st.session_state.teams):
                st.error(f"A team with the name '{team_name}' already exists.")
                return
            
            new_team = {
                'id': generate_next_id(st.session_state.teams),
                'name': team_name,
                'members': member_list
            }
            st.session_state.teams.append(new_team)
            st.session_state.show_team_form = False
            st.success(f"✅ Team '{team_name}' added with {len(member_list)} member(s)!")
            st.rerun()
        
        if cancel:
            st.session_state.show_team_form = False
            st.rerun()
