"""
Configuration settings for GearGuard Pro
"""

PAGE_CONFIG = {
    "page_title": "GearGuard Pro - Maintenance Tracker",
    "page_icon": "🔧",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Enhanced Custom CSS with modern, distinctive design
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-icon {
        font-size: 4rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #fff 0%, #a8edea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .header-stats {
        display: flex;
        gap: 1rem;
    }
    
    .stat-pill {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        transition: all 0.3s ease;
    }
    
    .stat-pill:hover {
        background: rgba(255,255,255,0.15);
        transform: translateY(-2px);
    }
    
    .stat-label {
        font-size: 0.75rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .sidebar-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a2e;
        letter-spacing: 1px;
    }
    
    .sidebar-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
    }
    
    .sidebar-stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .sidebar-stat-item:last-child {
        margin-bottom: 0;
    }
    
    .sidebar-stat-label {
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    .sidebar-stat-value {
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .overdue-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
    }
    
    .today-badge {
        background: #4ecdc4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
    }
    
    .kanban-column {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        min-height: 500px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .kanban-header {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #1a1a2e;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .kanban-count {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-family: 'Space Mono', monospace;
    }
    
    .kanban-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .kanban-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .kanban-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .kanban-card.overdue {
        border-left: 4px solid #ff6b6b;
        background: linear-gradient(135deg, #fff 0%, #ffe5e5 100%);
    }
    
    .kanban-card-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: #1a1a2e;
    }
    
    .kanban-card-equipment {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 0.5rem;
    }
    
    .badge-corrective {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
    }
    
    .badge-preventive {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(81, 207, 102, 0.3);
    }
    
    .badge-high {
        background: linear-gradient(135deg, #fa5252 0%, #e03131 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(250, 82, 82, 0.3);
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(255, 212, 59, 0.3);
    }
    
    .badge-low {
        background: linear-gradient(135deg, #74c0fc 0%, #4c6ef5 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(116, 192, 252, 0.3);
    }
    
    .equipment-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-top: 5px solid;
        border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .equipment-card::after {
        content: '⚙️';
        position: absolute;
        right: -20px;
        bottom: -20px;
        font-size: 8rem;
        opacity: 0.05;
    }
    
    .equipment-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .equipment-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1.5rem;
    }
    
    .equipment-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a1a2e;
        margin: 0;
    }
    
    .equipment-serial {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-family: 'Space Mono', monospace;
    }
    
    .equipment-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.85rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .equipment-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .equipment-detail-item {
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 10px;
        border-left: 3px solid #667eea;
    }
    
    .equipment-detail-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .equipment-detail-value {
        font-size: 1rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    
    .team-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 6px solid #8b5cf6;
        transition: all 0.3s ease;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.2);
    }
    
    .team-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .team-icon {
        font-size: 2.5rem;
    }
    
    .team-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a1a2e;
        margin: 0;
    }
    
    .team-members {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
    }
    
    .member-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
        transition: all 0.3s ease;
    }
    
    .member-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stat-card-title {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .stat-card-number {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Space Mono', monospace;
        position: relative;
    }
    
    .overdue-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        animation: alertPulse 2s ease-in-out infinite;
    }
    
    @keyframes alertPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid #e2e8f0;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
"""

# Stage colors for visual consistency
STAGE_COLORS = {
    'New': '#667eea',
    'In Progress': '#ffd43b',
    'Repaired': '#51cf66',
    'Scrap': '#ff6b6b'
}

# Priority colors
PRIORITY_COLORS = {
    'High': '#fa5252',
    'Medium': '#ffd43b',
    'Low': '#74c0fc'
}

# Type colors
TYPE_COLORS = {
    'Corrective': '#ff6b6b',
    'Preventive': '#51cf66'
}
