"""
Helper functions for GearGuard Pro
"""
import streamlit as st
from datetime import datetime

def get_equipment_by_id(eq_id):
    """Get equipment by ID"""
    for eq in st.session_state.equipment:
        if eq['id'] == eq_id:
            return eq
    return None

def is_overdue(request):
    """Check if a request is overdue"""
    if not request.get('scheduledDate'):
        return False
    scheduled = datetime.strptime(request['scheduledDate'], '%Y-%m-%d')
    return scheduled < datetime.now() and request['stage'] not in ['Repaired', 'Scrap']

def get_requests_by_equipment(eq_id):
    """Get all requests for a specific equipment"""
    return [r for r in st.session_state.requests 
            if r['equipmentId'] == eq_id and r['stage'] != 'Scrap']

def get_team_by_name(team_name):
    """Get team by name"""
    for team in st.session_state.teams:
        if team['name'] == team_name:
            return team
    return None

def get_all_technicians():
    """Get all technicians from all teams"""
    technicians = []
    for team in st.session_state.teams:
        for member in team['members']:
            technicians.append({
                'name': member,
                'team': team['name']
            })
    return technicians

def get_requests_by_technician(technician_name):
    """Get all requests assigned to a specific technician"""
    return [r for r in st.session_state.requests 
            if r.get('assignedTo') == technician_name and r['stage'] != 'Scrap']

def get_requests_by_team(team_name):
    """Get all requests for a specific team"""
    return [r for r in st.session_state.requests 
            if r.get('maintenanceTeam') == team_name and r['stage'] != 'Scrap']

def calculate_completion_rate():
    """Calculate completion rate for requests"""
    total = len(st.session_state.requests)
    if total == 0:
        return 0
    completed = len([r for r in st.session_state.requests if r['stage'] == 'Repaired'])
    return round((completed / total) * 100, 1)

def get_overdue_requests():
    """Get all overdue requests"""
    return [r for r in st.session_state.requests if is_overdue(r)]

def get_upcoming_requests(days=7):
    """Get requests scheduled within the next N days"""
    from datetime import timedelta
    today = datetime.now()
    future_date = today + timedelta(days=days)
    
    upcoming = []
    for r in st.session_state.requests:
        if r.get('scheduledDate') and r['stage'] not in ['Repaired', 'Scrap']:
            scheduled = datetime.strptime(r['scheduledDate'], '%Y-%m-%d')
            if today <= scheduled <= future_date:
                upcoming.append(r)
    
    return sorted(upcoming, key=lambda x: x['scheduledDate'])

def get_equipment_by_category():
    """Group equipment by category"""
    categories = {}
    for eq in st.session_state.equipment:
        cat = eq['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(eq)
    return categories

def get_equipment_with_pending_requests():
    """Get equipment that has pending requests"""
    equipment_with_requests = []
    for eq in st.session_state.equipment:
        pending = [r for r in st.session_state.requests 
                  if r['equipmentId'] == eq['id'] and r['stage'] in ['New', 'In Progress']]
        if pending:
            equipment_with_requests.append({
                'equipment': eq,
                'pending_count': len(pending),
                'overdue_count': len([r for r in pending if is_overdue(r)])
            })
    return equipment_with_requests

def format_date(date_str):
    """Format date string for display"""
    if not date_str:
        return "N/A"
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_str

def get_warranty_status(warranty_date):
    """Check warranty status"""
    if not warranty_date:
        return "Unknown"
    
    try:
        warranty = datetime.strptime(warranty_date, '%Y-%m-%d')
        today = datetime.now()
        
        if warranty < today:
            return "Expired"
        
        days_left = (warranty - today).days
        
        if days_left <= 30:
            return f"Expiring Soon ({days_left} days)"
        elif days_left <= 90:
            return f"Valid ({days_left} days left)"
        else:
            return "Valid"
    except:
        return "Unknown"

def generate_next_id(items):
    """Generate next available ID"""
    if not items:
        return 1
    return max(item['id'] for item in items) + 1
