"""
Analytics and Reporting View for GearGuard Pro
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from helpers import (
    calculate_completion_rate,
    get_overdue_requests,
    get_requests_by_team,
    get_equipment_by_category
)

def render():
    """Render the analytics dashboard"""
    
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("*Comprehensive performance insights and reports*")
    st.markdown("---")
    
    # Key metrics
    render_key_metrics()
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_requests_by_type_chart()
        st.markdown("<br>", unsafe_allow_html=True)
        render_priority_distribution_chart()
    
    with col2:
        render_requests_by_stage_chart()
        st.markdown("<br>", unsafe_allow_html=True)
        render_team_performance_chart()
    
    st.markdown("---")
    
    # Time-based analysis
    col1, col2 = st.columns(2)
    
    with col1:
        render_requests_timeline()
    
    with col2:
        render_equipment_category_chart()
    
    st.markdown("---")
    
    # Detailed tables
    render_detailed_reports()

def render_key_metrics():
    """Render key performance metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    total_equipment = len(st.session_state.equipment)
    total_requests = len(st.session_state.requests)
    active_requests = len([r for r in st.session_state.requests 
                          if r['stage'] in ['New', 'In Progress']])
    completed_requests = len([r for r in st.session_state.requests 
                             if r['stage'] == 'Repaired'])
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="stat-card-title">Total Equipment</div>
            <div class="stat-card-number">{total_equipment}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-card-title">Total Requests</div>
            <div class="stat-card-number">{total_requests}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-card-title">Active</div>
            <div class="stat-card-number">{active_requests}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        completion_rate = calculate_completion_rate()
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stat-card-title">Completion Rate</div>
            <div class="stat-card-number">{completion_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics row
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    overdue = len(get_overdue_requests())
    preventive = len([r for r in st.session_state.requests if r['type'] == 'Preventive'])
    corrective = len([r for r in st.session_state.requests if r['type'] == 'Corrective'])
    avg_duration = round(sum(r.get('duration', 0) for r in st.session_state.requests 
                            if r['stage'] == 'Repaired') / max(completed_requests, 1), 1)
    
    with col1:
        st.metric("Overdue Requests", overdue, delta=f"-{overdue}" if overdue > 0 else "0", delta_color="inverse")
    
    with col2:
        st.metric("Preventive Maintenance", preventive)
    
    with col3:
        st.metric("Corrective Maintenance", corrective)
    
    with col4:
        st.metric("Avg Duration (hrs)", avg_duration)

def render_requests_by_type_chart():
    """Render requests by type pie chart"""
    st.markdown("### 🔧 Requests by Type")
    
    type_counts = {
        'Corrective': len([r for r in st.session_state.requests if r['type'] == 'Corrective']),
        'Preventive': len([r for r in st.session_state.requests if r['type'] == 'Preventive'])
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(type_counts.keys()),
        values=list(type_counts.values()),
        hole=0.4,
        marker=dict(colors=['#ff6b6b', '#51cf66']),
        textinfo='label+percent',
        textfont=dict(size=14, color='white', family='Outfit')
    )])
    
    fig.update_layout(
        showlegend=True,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#1a1a2e')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_requests_by_stage_chart():
    """Render requests by stage bar chart"""
    st.markdown("### 📈 Requests by Stage")
    
    stages = ['New', 'In Progress', 'Repaired', 'Scrap']
    stage_counts = [len([r for r in st.session_state.requests if r['stage'] == s]) for s in stages]
    
    colors = ['#ffd43b', '#4ecdc4', '#51cf66', '#ff6b6b']
    
    fig = go.Figure(data=[go.Bar(
        x=stages,
        y=stage_counts,
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=stage_counts,
        textposition='auto',
        textfont=dict(size=16, color='white', family='Space Mono', weight='bold')
    )])
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#1a1a2e')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#64748b')
        ),
        font=dict(family='Outfit')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_priority_distribution_chart():
    """Render priority distribution chart"""
    st.markdown("### ⚠️ Priority Distribution")
    
    priorities = ['High', 'Medium', 'Low']
    priority_counts = [len([r for r in st.session_state.requests if r['priority'] == p]) for p in priorities]
    
    colors = ['#fa5252', '#ffd43b', '#74c0fc']
    
    fig = go.Figure(data=[go.Bar(
        x=priorities,
        y=priority_counts,
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=priority_counts,
        textposition='auto',
        textfont=dict(size=16, color='white', family='Space Mono', weight='bold')
    )])
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#1a1a2e')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#64748b')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_team_performance_chart():
    """Render team performance chart"""
    st.markdown("### 👥 Team Performance")
    
    team_data = []
    for team in st.session_state.teams:
        team_requests = get_requests_by_team(team['name'])
        team_data.append({
            'Team': team['name'],
            'Total': len(team_requests),
            'Completed': len([r for r in team_requests if r['stage'] == 'Repaired']),
            'In Progress': len([r for r in team_requests if r['stage'] == 'In Progress']),
            'New': len([r for r in team_requests if r['stage'] == 'New'])
        })
    
    df = pd.DataFrame(team_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Completed',
        x=df['Team'],
        y=df['Completed'],
        marker=dict(color='#51cf66'),
        text=df['Completed'],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='In Progress',
        x=df['Team'],
        y=df['In Progress'],
        marker=dict(color='#4ecdc4'),
        text=df['In Progress'],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='New',
        x=df['Team'],
        y=df['New'],
        marker=dict(color='#ffd43b'),
        text=df['New'],
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='stack',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            title=None,
            tickfont=dict(family='Outfit', size=11, color='#1a1a2e')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#64748b')
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(family='Outfit', size=11)
        ),
        font=dict(family='Space Mono', size=11, color='white', weight='bold')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_requests_timeline():
    """Render requests timeline"""
    st.markdown("### 📅 Request Timeline (Last 30 Days)")
    
    # Get requests from last 30 days
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    timeline_data = []
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        count = len([r for r in st.session_state.requests 
                    if r.get('createdDate') == date_str])
        timeline_data.append({
            'Date': date.strftime('%b %d'),
            'Requests': count
        })
    
    df = pd.DataFrame(timeline_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Requests'],
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            title=None,
            tickfont=dict(family='Outfit', size=10, color='#1a1a2e'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title=None,
            tickfont=dict(family='Outfit', size=12, color='#64748b')
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_equipment_category_chart():
    """Render equipment by category chart"""
    st.markdown("### ⚙️ Equipment by Category")
    
    categories = get_equipment_by_category()
    cat_data = {cat: len(items) for cat, items in categories.items()}
    
    fig = go.Figure(data=[go.Pie(
        labels=list(cat_data.keys()),
        values=list(cat_data.values()),
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']),
        textinfo='label+value',
        textfont=dict(size=12, family='Outfit')
    )])
    
    fig.update_layout(
        showlegend=True,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05,
            font=dict(family='Outfit', size=11)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_detailed_reports():
    """Render detailed data tables"""
    st.markdown("### 📋 Detailed Reports")
    
    tab1, tab2, tab3 = st.tabs(["All Requests", "Equipment Status", "Team Workload"])
    
    with tab1:
        st.markdown("#### All Maintenance Requests")
        df_requests = pd.DataFrame(st.session_state.requests)
        if not df_requests.empty:
            df_display = df_requests[[
                'id', 'subject', 'equipmentName', 'type', 'stage', 
                'priority', 'scheduledDate', 'assignedTo', 'maintenanceTeam'
            ]].copy()
            df_display.columns = [
                'ID', 'Subject', 'Equipment', 'Type', 'Stage', 
                'Priority', 'Scheduled', 'Assigned To', 'Team'
            ]
            st.dataframe(df_display, use_container_width=True, height=400)
            
            # Download button
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv,
                file_name=f"maintenance_requests_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with tab2:
        st.markdown("#### Equipment Status Report")
        df_equipment = pd.DataFrame(st.session_state.equipment)
        if not df_equipment.empty:
            df_display = df_equipment[[
                'id', 'name', 'serialNumber', 'category', 'department', 
                'location', 'maintenanceTeam', 'status'
            ]].copy()
            df_display.columns = [
                'ID', 'Name', 'Serial Number', 'Category', 'Department',
                'Location', 'Team', 'Status'
            ]
            st.dataframe(df_display, use_container_width=True, height=400)
    
    with tab3:
        st.markdown("#### Team Workload Analysis")
        team_workload = []
        for team in st.session_state.teams:
            team_requests = get_requests_by_team(team['name'])
            team_workload.append({
                'Team': team['name'],
                'Members': len(team['members']),
                'Total Requests': len(team_requests),
                'Active': len([r for r in team_requests if r['stage'] in ['New', 'In Progress']]),
                'Completed': len([r for r in team_requests if r['stage'] == 'Repaired']),
                'Completion Rate': f"{round((len([r for r in team_requests if r['stage'] == 'Repaired']) / max(len(team_requests), 1)) * 100, 1)}%"
            })
        
        df_teams = pd.DataFrame(team_workload)
        st.dataframe(df_teams, use_container_width=True, height=300)
