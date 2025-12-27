"""
Session state management for GearGuard Pro
"""
import streamlit as st
from datetime import datetime, timedelta

def initialize_session_state():
    """Initialize session state with sample data if not exists"""
    
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
                'defaultTechnician': 'John Doe',
                'status': 'Operational'
            },
            {
                'id': 2,
                'name': 'Laptop Dell XPS 15',
                'serialNumber': 'DELL-2024-042',
                'category': 'IT Equipment',
                'department': 'Engineering',
                'owner': 'Alice Johnson',
                'purchaseDate': '2024-01-10',
                'warranty': '2027-01-10',
                'location': 'Office 301',
                'maintenanceTeam': 'IT Support',
                'defaultTechnician': 'Tom Brown',
                'status': 'Operational'
            },
            {
                'id': 3,
                'name': 'Forklift FL-200',
                'serialNumber': 'FLT-2023-089',
                'category': 'Logistics',
                'department': 'Warehouse',
                'owner': 'Warehouse Manager',
                'purchaseDate': '2023-03-20',
                'warranty': '2026-03-20',
                'location': 'Warehouse B',
                'maintenanceTeam': 'Mechanics',
                'defaultTechnician': 'Jane Smith',
                'status': 'Operational'
            },
            {
                'id': 4,
                'name': 'Server Rack SR-01',
                'serialNumber': 'SRV-2024-012',
                'category': 'IT Equipment',
                'department': 'IT',
                'owner': 'IT Department',
                'purchaseDate': '2024-02-01',
                'warranty': '2029-02-01',
                'location': 'Server Room A',
                'maintenanceTeam': 'IT Support',
                'defaultTechnician': 'Lisa Garcia',
                'status': 'Operational'
            },
            {
                'id': 5,
                'name': '3D Printer ProMax',
                'serialNumber': '3DP-2024-033',
                'category': 'Production',
                'department': 'R&D',
                'owner': 'Research Team',
                'purchaseDate': '2024-06-15',
                'warranty': '2027-06-15',
                'location': 'Lab 3',
                'maintenanceTeam': 'Mechanics',
                'defaultTechnician': 'John Doe',
                'status': 'Operational'
            }
        ]
    
    if 'teams' not in st.session_state:
        st.session_state.teams = [
            {
                'id': 1,
                'name': 'Mechanics',
                'members': ['John Doe', 'Jane Smith', 'Robert Wilson']
            },
            {
                'id': 2,
                'name': 'Electricians',
                'members': ['Mike Johnson', 'Sarah Wilson', 'David Lee']
            },
            {
                'id': 3,
                'name': 'IT Support',
                'members': ['Tom Brown', 'Lisa Garcia', 'Chris Martinez']
            },
            {
                'id': 4,
                'name': 'HVAC Specialists',
                'members': ['Andrew Davis', 'Emily Taylor']
            }
        ]
    
    if 'requests' not in st.session_state:
        today = datetime.now()
        st.session_state.requests = [
            {
                'id': 1,
                'subject': 'Oil Leak Detected',
                'equipmentId': 1,
                'equipmentName': 'CNC Machine 01',
                'type': 'Corrective',
                'stage': 'New',
                'scheduledDate': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
                'duration': 0,
                'assignedTo': None,
                'createdDate': (today - timedelta(days=2)).strftime('%Y-%m-%d'),
                'priority': 'High',
                'category': 'Production',
                'maintenanceTeam': 'Mechanics',
                'description': 'Hydraulic oil leak observed near the main cylinder. Requires immediate attention to prevent production downtime.'
            },
            {
                'id': 2,
                'subject': 'Monthly Maintenance Check',
                'equipmentId': 1,
                'equipmentName': 'CNC Machine 01',
                'type': 'Preventive',
                'stage': 'In Progress',
                'scheduledDate': today.strftime('%Y-%m-%d'),
                'duration': 2,
                'assignedTo': 'John Doe',
                'createdDate': (today - timedelta(days=7)).strftime('%Y-%m-%d'),
                'priority': 'Medium',
                'category': 'Production',
                'maintenanceTeam': 'Mechanics',
                'description': 'Routine monthly maintenance including lubrication, calibration, and safety checks.'
            },
            {
                'id': 3,
                'subject': 'Software Update Required',
                'equipmentId': 2,
                'equipmentName': 'Laptop Dell XPS 15',
                'type': 'Preventive',
                'stage': 'New',
                'scheduledDate': (today + timedelta(days=2)).strftime('%Y-%m-%d'),
                'duration': 0,
                'assignedTo': None,
                'createdDate': today.strftime('%Y-%m-%d'),
                'priority': 'Low',
                'category': 'IT Equipment',
                'maintenanceTeam': 'IT Support',
                'description': 'Security updates and system optimization needed for Dell laptop.'
            },
            {
                'id': 4,
                'subject': 'Battery Replacement',
                'equipmentId': 3,
                'equipmentName': 'Forklift FL-200',
                'type': 'Corrective',
                'stage': 'In Progress',
                'scheduledDate': today.strftime('%Y-%m-%d'),
                'duration': 3,
                'assignedTo': 'Jane Smith',
                'createdDate': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
                'priority': 'High',
                'category': 'Logistics',
                'maintenanceTeam': 'Mechanics',
                'description': 'Forklift battery showing signs of failure. Replacement required to maintain operational capacity.'
            },
            {
                'id': 5,
                'subject': 'Quarterly Inspection',
                'equipmentId': 4,
                'equipmentName': 'Server Rack SR-01',
                'type': 'Preventive',
                'stage': 'Repaired',
                'scheduledDate': (today - timedelta(days=5)).strftime('%Y-%m-%d'),
                'duration': 4,
                'assignedTo': 'Tom Brown',
                'createdDate': (today - timedelta(days=10)).strftime('%Y-%m-%d'),
                'priority': 'Medium',
                'category': 'IT Equipment',
                'maintenanceTeam': 'IT Support',
                'description': 'Quarterly server maintenance completed including cooling system check, dust cleaning, and performance monitoring.'
            },
            {
                'id': 6,
                'subject': 'Nozzle Calibration',
                'equipmentId': 5,
                'equipmentName': '3D Printer ProMax',
                'type': 'Preventive',
                'stage': 'New',
                'scheduledDate': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
                'duration': 0,
                'assignedTo': None,
                'createdDate': today.strftime('%Y-%m-%d'),
                'priority': 'Medium',
                'category': 'Production',
                'maintenanceTeam': 'Mechanics',
                'description': 'Regular nozzle calibration and bed leveling required for optimal print quality.'
            },
            {
                'id': 7,
                'subject': 'Brake System Check',
                'equipmentId': 3,
                'equipmentName': 'Forklift FL-200',
                'type': 'Preventive',
                'stage': 'Repaired',
                'scheduledDate': (today - timedelta(days=15)).strftime('%Y-%m-%d'),
                'duration': 2,
                'assignedTo': 'Robert Wilson',
                'createdDate': (today - timedelta(days=20)).strftime('%Y-%m-%d'),
                'priority': 'High',
                'category': 'Logistics',
                'maintenanceTeam': 'Mechanics',
                'description': 'Regular brake system inspection and maintenance completed successfully.'
            }
        ]
    
    # Initialize view state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'kanban'
    
    # Initialize form states
    if 'show_request_form' not in st.session_state:
        st.session_state.show_request_form = False
    
    if 'show_equipment_form' not in st.session_state:
        st.session_state.show_equipment_form = False
    
    if 'show_team_form' not in st.session_state:
        st.session_state.show_team_form = False
