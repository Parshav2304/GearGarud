"""
Calendar View for GearGuard Pro - Preventive Maintenance Scheduling
"""
import streamlit as st
from datetime import datetime, timedelta
import calendar
from helpers import get_equipment_by_id, generate_next_id, get_all_technicians

def render():
    """Render the calendar view"""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 📅 Preventive Maintenance Calendar")
        st.markdown("*Schedule and track preventive maintenance tasks*")
    with col2:
        if st.button("➕ Schedule", use_container_width=True):
            st.session_state.show_calendar_form = True
    
    st.markdown("---")
    
    # Show form if requested
    if st.session_state.get('show_calendar_form', False):
        render_schedule_form()
        return
    
    # Month/Year selector
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
    
    today = datetime.now()
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = today.month
    if 'calendar_year' not in st.session_state:
        st.session_state.calendar_year = today.year
    
    with col2:
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        selected_month = st.selectbox(
            "Month",
            options=range(1, 13),
            index=st.session_state.calendar_month - 1,
            format_func=lambda x: months[x-1],
            key="month_selector"
        )
        st.session_state.calendar_month = selected_month
    
    with col4:
        selected_year = st.selectbox(
            "Year",
            options=range(today.year - 1, today.year + 3),
            index=1,
            key="year_selector"
        )
        st.session_state.calendar_year = selected_year
    
    # Quick navigation buttons
    with col1:
        if st.button("◀️ Prev", use_container_width=True):
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
            st.rerun()
    
    with col5:
        if st.button("Next ▶️", use_container_width=True):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
            st.rerun()
    
    with col3:
        if st.button("📍 Today", use_container_width=True):
            st.session_state.calendar_month = today.month
            st.session_state.calendar_year = today.year
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats for the month
    month_start = datetime(st.session_state.calendar_year, st.session_state.calendar_month, 1)
    month_end = datetime(st.session_state.calendar_year, st.session_state.calendar_month, 
                        calendar.monthrange(st.session_state.calendar_year, st.session_state.calendar_month)[1])
    
    month_requests = [r for r in st.session_state.requests 
                     if r.get('scheduledDate') and r['type'] == 'Preventive']
    month_requests = [r for r in month_requests 
                     if month_start <= datetime.strptime(r['scheduledDate'], '%Y-%m-%d') <= month_end]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scheduled", len(month_requests))
    with col2:
        completed = len([r for r in month_requests if r['stage'] == 'Repaired'])
        st.metric("Completed", completed)
    with col3:
        in_progress = len([r for r in month_requests if r['stage'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    with col4:
        pending = len([r for r in month_requests if r['stage'] == 'New'])
        st.metric("Pending", pending)
    
    st.markdown("---")
    
    # Render calendar
    render_calendar_grid(st.session_state.calendar_year, st.session_state.calendar_month)
    
    # Upcoming schedule
    st.markdown("### 📋 Upcoming Preventive Maintenance")
    upcoming = get_upcoming_preventive_requests()
    
    if upcoming:
        for request in upcoming[:5]:  # Show next 5
            render_upcoming_card(request)
    else:
        st.info("No upcoming preventive maintenance scheduled for the next 30 days.")

def render_calendar_grid(year, month):
    """Render the calendar grid"""
    
    # Get calendar data
    cal = calendar.monthcalendar(year, month)
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # Header row
    cols = st.columns(7)
    for idx, day in enumerate(days_of_week):
        with cols[idx]:
            st.markdown(f"<div style='text-align: center; font-weight: 700; color: #667eea; padding: 10px; background: #f8f9fa; border-radius: 8px;'>{day}</div>", 
                       unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Calendar rows
    for week in cal:
        cols = st.columns(7)
        for idx, day in enumerate(week):
            with cols[idx]:
                if day == 0:
                    st.markdown("<div style='min-height: 120px;'></div>", unsafe_allow_html=True)
                else:
                    render_calendar_day(year, month, day)

def render_calendar_day(year, month, day):
    """Render a single calendar day"""
    date = datetime(year, month, day)
    date_str = date.strftime('%Y-%m-%d')
    today = datetime.now().date()
    
    # Get requests for this day
    day_requests = [r for r in st.session_state.requests 
                   if r.get('scheduledDate') == date_str and r['type'] == 'Preventive']
    
    # Determine day styling
    is_today = date.date() == today
    is_past = date.date() < today
    
    bg_color = "#e0e7ff" if is_today else "#ffffff" if not is_past else "#f8f9fa"
    border_color = "#667eea" if is_today else "#e2e8f0"
    
    st.markdown(f"""
    <div style='
        background: {bg_color}; 
        border: 2px solid {border_color}; 
        border-radius: 10px; 
        padding: 10px; 
        min-height: 120px;
        position: relative;
    '>
        <div style='
            font-weight: 700; 
            font-size: 1.2rem; 
            color: {"#667eea" if is_today else "#1a1a2e"};
            margin-bottom: 8px;
        '>{day}</div>
    """, unsafe_allow_html=True)
    
    # Display requests
    for request in day_requests:
        status_color = {
            'New': '#ffd43b',
            'In Progress': '#4ecdc4',
            'Repaired': '#51cf66',
            'Scrap': '#ff6b6b'
        }.get(request['stage'], '#667eea')
        
        st.markdown(f"""
        <div style='
            background: {status_color}; 
            color: white; 
            padding: 6px 8px; 
            border-radius: 6px; 
            font-size: 0.75rem; 
            margin-bottom: 4px;
            font-weight: 600;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        ' title='{request["subject"]} - {request["equipmentName"]}'>
            {request['subject'][:20]}{"..." if len(request['subject']) > 20 else ""}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_upcoming_card(request):
    """Render an upcoming request card"""
    days_until = (datetime.strptime(request['scheduledDate'], '%Y-%m-%d') - datetime.now()).days
    
    urgency_color = "#ff6b6b" if days_until <= 3 else "#ffd43b" if days_until <= 7 else "#51cf66"
    
    st.markdown(f"""
    <div style='
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {urgency_color};
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    '>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div>
                <h4 style='margin: 0; color: #1a1a2e;'>{request['subject']}</h4>
                <p style='color: #64748b; margin: 0.5rem 0;'>🔧 {request['equipmentName']}</p>
                <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                    📅 {format_date_display(request['scheduledDate'])}
                </p>
            </div>
            <div style='text-align: right;'>
                <div style='
                    background: {urgency_color};
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 0.85rem;
                '>
                    {f"In {days_until} days" if days_until > 0 else "Today" if days_until == 0 else "Overdue"}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_schedule_form():
    """Render the scheduling form"""
    st.markdown("## 📅 Schedule Preventive Maintenance")
    
    with st.form("schedule_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Maintenance Task *", placeholder="e.g., Monthly Oil Change")
            
            equipment_options = {eq['id']: f"{eq['name']} ({eq['category']})" 
                               for eq in st.session_state.equipment}
            selected_eq_id = st.selectbox(
                "Equipment *",
                options=list(equipment_options.keys()),
                format_func=lambda x: equipment_options[x]
            )
            
            scheduled_date = st.date_input(
                "Scheduled Date *",
                min_value=datetime.now().date()
            )
        
        with col2:
            priority = st.selectbox("Priority", ["Medium", "High", "Low"])
            
            # Auto-fill from equipment
            selected_eq = get_equipment_by_id(selected_eq_id)
            
            if selected_eq:
                st.text_input("Category", value=selected_eq['category'], disabled=True)
                st.text_input("Team", value=selected_eq['maintenanceTeam'], disabled=True)
                
                # Technician assignment
                team_members = []
                for team in st.session_state.teams:
                    if team['name'] == selected_eq['maintenanceTeam']:
                        team_members = team['members']
                        break
                
                assign_now = st.checkbox("Assign technician?", value=False)
                assigned_tech = None
                if assign_now and team_members:
                    assigned_tech = st.selectbox("Technician", options=team_members)
        
        description = st.text_area(
            "Description",
            placeholder="Describe the preventive maintenance tasks to be performed...",
            height=100
        )
        
        # Recurrence options (future enhancement placeholder)
        st.markdown("**🔄 Recurrence** *(Coming Soon)*")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Repeat", ["Does not repeat", "Daily", "Weekly", "Monthly", "Yearly"], disabled=True)
        with col2:
            st.number_input("Every", value=1, min_value=1, disabled=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit = st.form_submit_button("✅ Schedule", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit and subject and selected_eq_id:
            selected_eq = get_equipment_by_id(selected_eq_id)
            new_request = {
                'id': generate_next_id(st.session_state.requests),
                'subject': subject,
                'equipmentId': selected_eq_id,
                'equipmentName': selected_eq['name'],
                'type': 'Preventive',
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
            st.session_state.show_calendar_form = False
            st.success(f"✅ Maintenance scheduled for {format_date_display(scheduled_date.strftime('%Y-%m-%d'))}")
            st.rerun()
        
        if cancel:
            st.session_state.show_calendar_form = False
            st.rerun()

def get_upcoming_preventive_requests():
    """Get upcoming preventive maintenance requests"""
    from datetime import timedelta
    today = datetime.now()
    future_date = today + timedelta(days=30)
    
    upcoming = []
    for r in st.session_state.requests:
        if r['type'] == 'Preventive' and r.get('scheduledDate') and r['stage'] not in ['Repaired', 'Scrap']:
            scheduled = datetime.strptime(r['scheduledDate'], '%Y-%m-%d')
            if today <= scheduled <= future_date:
                upcoming.append(r)
    
    return sorted(upcoming, key=lambda x: x['scheduledDate'])

def format_date_display(date_str):
    """Format date for display"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_str
