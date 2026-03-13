import streamlit as st
import pandas as pd
import plotly.express as px

# Categories with keywords
categories = {
    'Academic': ['exam', 'marks', 'syllabus', 'assignment', 'faculty', 'teacher', 'professor', 'test', 'semester', 'grade', 'course', 'lecture'],
    'Hostel': ['wifi', 'room', 'mess', 'food', 'hostel', 'warden', 'water', 'filter', 'roommate', 'accommodation', 'stay', 'internet', 'network'],
    'Infrastructure': ['library', 'lab', 'classroom', 'bench', 'seat', 'chair', 'projector', 'computer', 'building', 'facility', 'equipment', 'ac', 'furniture', 'maintenance'],
    'Administration': ['fees', 'id card', 'scholarship', 'office', 'certificate', 'documents', 'admission', 'payment', 'billing', 'registration']
}

def categorize_complaint(text):
    text_lower = text.lower()
    
    # Count keyword matches for each category
    match_counts = {}
    for cat, kws in categories.items():
        count = sum(1 for kw in kws if kw in text_lower)
        match_counts[cat] = count
    
    # Find the category with maximum matches
    max_matches = max(match_counts.values())
    
    # Return the category if at least one keyword matched
    if max_matches > 0:
        for cat, cnt in match_counts.items():
            if cnt == max_matches:
                return cat
    
    return "Other"

def detect_priority(text):
    text_lower = text.lower()
    
    # Check for high priority keywords
    high_priority_keywords = ['urgent', 'emergency', 'immediately', 'critical', 'serious', 'asap', 'broken', 'not working', 'severe']
    for keyword in high_priority_keywords:
        if keyword in text_lower:
            return 'High'
    
    # Check for medium priority keywords
    medium_priority_keywords = ['soon', 'important', 'please', 'need', 'required', 'issue', 'problem']
    for keyword in medium_priority_keywords:
        if keyword in text_lower:
            return 'Medium'
    
    # Default to low priority
    return 'Low'

def generate_insights(df):
    cat_counts = df['Category'].value_counts()
    insights = []
    
    # Add top category insight
    top_category = cat_counts.idxmax()
    top_percentage = (cat_counts.max() / len(df)) * 100
    insights.append(f"Most complaints are related to **{top_category}** issues ({top_percentage:.1f}%).")
    
    # Add high priority insight if applicable
    high_priority = len(df[df['Priority'] == 'High'])
    if high_priority > 0:
        high_priority_percentage = (high_priority / len(df)) * 100
        insights.append(f"**{high_priority}** complaints ({high_priority_percentage:.1f}%) require immediate attention.")
    
    # Add category diversity insight
    total_categories = df['Category'].nunique()
    insights.append(f"Complaints span across **{total_categories}** different categories.")
    
    # Add second most common category if exists
    if len(cat_counts) > 1:
        second_category = cat_counts.index[1]
        second_percentage = (cat_counts.iloc[1] / len(df)) * 100
        insights.append(f"**{second_category}** is the second most reported issue ({second_percentage:.1f}%).")
    
    return insights

def initialize_filter_state(key, options):
    current = st.session_state.get(key)
    valid_values = set(options) | {'All'}

    if not current:
        st.session_state[key] = ['All']
        return

    cleaned = [value for value in current if value in valid_values]
    if not cleaned:
        st.session_state[key] = ['All']
        return

    actual_selected = [value for value in cleaned if value != 'All']
    if len(actual_selected) == len(options):
        st.session_state[key] = ['All']
    else:
        st.session_state[key] = cleaned

def normalize_filter_selection(key, options):
    selected = st.session_state.get(key, ['All'])
    actual_selected = [value for value in selected if value != 'All']

    if not selected or not actual_selected and 'All' not in selected:
        st.session_state[key] = ['All']
        return

    if 'All' in selected and actual_selected:
        st.session_state[key] = actual_selected
        return

    if len(actual_selected) == len(options):
        st.session_state[key] = ['All']

def resolve_filter_values(selected, options):
    return options if 'All' in selected else selected

st.set_page_config(page_title="CHRIST University Complaint Intelligence", page_icon="just_logo.png", layout="wide", initial_sidebar_state="auto")

# Initialize session state for storing complaints
if 'complaints_data' not in st.session_state:
    st.session_state.complaints_data = []

st.markdown("""<style>.sidebar-content{font-size:.9rem;line-height:1.6;color:#2c3e50}section[data-testid="stSidebar"]>div:first-child{background-color:transparent!important}section[data-testid="stSidebar"] img{image-rendering:-webkit-optimize-contrast;image-rendering:crisp-edges;image-rendering:pixelated}[data-testid="stMetricValue"]{color:#000000!important;font-size:1.8rem;font-weight:700}[data-testid="stMetricLabel"]{color:#5a6c7d;font-size:.9rem;font-weight:500}h3,.stMarkdown h3,.stMarkdown h2{color:#1f3c88!important}</style>""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;padding:1rem 0 1.5rem'><h1 style='font-size:2rem;font-weight:700;color:#1f3c88;margin-bottom:.8rem;letter-spacing:-.3px'>CHRIST University Complaint Intelligence System</h1><p style='font-size:1.05rem;color:#2c3e50;margin-bottom:.5rem;font-weight:500'>Rule-Based Intelligent Complaint Classification for Efficient Campus Management</p><p style='font-size:.88rem;color:#5a6c7d;font-weight:400'>Rule-Based NLP System | Real-Time Analytics | Smart Prioritization</p></div>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    _, col, _ = st.columns([1, 3, 1])
    with col: st.image("logo.png", width=220)
    st.markdown("<br><div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("### Categories\n**Academic** • Exams, Marks, Faculty  \n**Hostel** • Accommodation, Mess, WiFi  \n**Infrastructure** • Labs, Library, Equipment  \n**Administration** • Fees, Documents, Office\n\n---\n\n### Priority Scale")
    st.markdown("<div style='margin:.6rem 0'><span style='background-color:#3d5a80;color:white;padding:.25rem .7rem;border-radius:14px;font-size:.75rem;font-weight:600'>HIGH</span><span style='color:#2c3e50;font-size:.85rem;margin-left:.6rem'>Urgent</span></div><div style='margin:.6rem 0'><span style='background-color:#6c8cd5;color:white;padding:.25rem .7rem;border-radius:14px;font-size:.75rem;font-weight:600'>MEDIUM</span><span style='color:#2c3e50;font-size:.85rem;margin-left:.6rem'>Important</span></div><div style='margin:.6rem 0'><span style='background-color:#a8b3cf;color:white;padding:.25rem .7rem;border-radius:14px;font-size:.75rem;font-weight:600'>LOW</span><span style='color:#2c3e50;font-size:.85rem;margin-left:.6rem'>Regular</span></div>", unsafe_allow_html=True)
    st.markdown("---\n\n### Features\nReal-time analysis  \nPriority detection  \nBulk CSV processing  \nInteractive charts  \nExport reports\n</div><br>", unsafe_allow_html=True)
    if st.button("Reset Dashboard", use_container_width=True):
        st.session_state.complaints_data = []
        st.session_state.last_result = None
        st.rerun()

# Dashboard metrics
st.markdown("### System Overview")
col1, col2, col3 = st.columns(3)
if st.session_state.complaints_data:
    sdf = pd.DataFrame(st.session_state.complaints_data)
    total, most_common, high_count = len(sdf), sdf['Category'].value_counts().idxmax(), len(sdf[sdf['Priority'] == 'High'])
else:
    total, most_common, high_count = 0, "—", 0
col1.metric("Total Processed", total)
col2.metric("Most Common Category", most_common)
col3.metric("High Priority Cases", high_count)
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Single Complaint Analysis", "Bulk Upload & Analytics"])

with tab1:
    st.markdown("### Enter Your Complaint")
    st.write("Type your complaint below and get instant categorization")
    with st.form("complaint_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        complaint_input = c1.text_area("Complaint Text:", placeholder="Example: The hostel wifi is not working and room maintenance is pending...", height=150, label_visibility="collapsed")
        c2.write(""); c2.write("")
        submit_btn = c2.form_submit_button("Categorize", use_container_width=True, type="primary")
        clear_btn = c2.form_submit_button("Clear", use_container_width=True)
    
    if submit_btn and complaint_input.strip():
        cat, pri = categorize_complaint(complaint_input), detect_priority(complaint_input)
        st.session_state.complaints_data.append({'Complaint_Text': complaint_input, 'Category': cat, 'Priority': pri})
        st.session_state.last_result = {'category': cat, 'priority': pri, 'text': complaint_input}
        st.rerun()
    elif submit_btn: st.warning("Please enter a complaint to categorize!")
    
    if 'last_result' in st.session_state and st.session_state.last_result:
        r = st.session_state.last_result
        st.markdown("---")
        st.subheader("Results")
        st.info(f"### Category: {r['category']}")
        ca, cb = st.columns(2)
        ca.write(f"**Priority:** {r['priority']}")
        cb.write(f"**Total Analyzed This Session:** {len(st.session_state.complaints_data)}")
        with st.expander("View Original Complaint"): st.write(r['text'])

with tab2:
    st.subheader("Bulk Complaint Processing")
    st.write("Upload CSV file for comprehensive complaint analysis and categorization")
    with st.expander("CSV Format Requirements"):
        st.code("Complaint_Text\nMy exam marks are not updated\nHostel wifi is not working urgently\nLibrary computers are slow", language="csv")
        st.info("Your CSV must have a column named exactly: **Complaint_Text**")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'], help="CSV file must contain a column named 'Complaint_Text'")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Complaint_Text' not in df.columns:
                st.error("Error: CSV file must contain a column named 'Complaint_Text'")
            else:
                with st.spinner('Processing complaints...'):
                    df['Category'] = df['Complaint_Text'].apply(categorize_complaint)
                    df['Priority'] = df['Complaint_Text'].apply(detect_priority)
                for _, row in df.iterrows():
                    st.session_state.complaints_data.append({'Complaint_Text': row['Complaint_Text'], 'Category': row['Category'], 'Priority': row['Priority']})
                st.success(f"Successfully processed {len(df)} complaints!")
                
                st.markdown("---\n### Key Performance Indicators")
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Total Complaints", len(df))
                c2.metric("Top Category", df['Category'].value_counts().idxmax())
                c3.metric("Categories", df['Category'].nunique())
                c4.metric("High Priority", len(df[df['Priority']=='High']), delta="Urgent")
                c5.metric("Success Rate", f"{len(df[df['Category']!='Other'])/len(df)*100:.1f}%")
                
                st.markdown("---\n### Complaint Insights")
                
                # Generate and display insights
                insights = generate_insights(df)
                insight_columns = st.columns(len(insights))
                for i, col in enumerate(insight_columns):
                    col.info(insights[i])
                
                st.markdown("---")
                
                dtab1, dtab2, dtab3 = st.tabs(["Data View", "Analytics Dashboard", "Priority Analysis"])
                
                with dtab1:
                    st.subheader("Categorized Complaints")
                    fc1, fc2 = st.columns(2)
                    category_options = sorted(df['Category'].unique().tolist())
                    priority_options = sorted(df['Priority'].unique().tolist())

                    initialize_filter_state("bulk_filter_category", category_options)
                    initialize_filter_state("bulk_filter_priority", priority_options)

                    filter_cat = fc1.multiselect(
                        "Filter by Category:",
                        ['All'] + category_options,
                        key="bulk_filter_category",
                        on_change=normalize_filter_selection,
                        args=("bulk_filter_category", category_options)
                    )
                    filter_pri = fc2.multiselect(
                        "Filter by Priority:",
                        ['All'] + priority_options,
                        key="bulk_filter_priority",
                        on_change=normalize_filter_selection,
                        args=("bulk_filter_priority", priority_options)
                    )

                    selected_categories = resolve_filter_values(filter_cat, category_options)
                    selected_priorities = resolve_filter_values(filter_pri, priority_options)
                    filtered = df[
                        df['Category'].isin(selected_categories)
                        & df['Priority'].isin(selected_priorities)
                    ]
                    st.dataframe(filtered, use_container_width=True, hide_index=True)
                    st.caption(f"Showing {len(filtered)} of {len(df)} complaints")
                
                with dtab2:
                    st.subheader("Analytics Dashboard")
                    cc1, cc2 = st.columns(2)
                    cat_counts = df['Category'].value_counts()
                    colors = ["#1f3c88", "#4b7bec", "#6c8cd5", "#a8b3cf", "#7a8699"]
                    with cc1:
                        st.markdown("**Category Distribution**")
                        fig_pie = px.pie(values=cat_counts.values, names=cat_counts.index, color_discrete_sequence=colors, hole=0.4)
                        fig_pie.update_layout(showlegend=True, height=400, margin=dict(t=30, b=30, l=30, r=30))
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    with cc2:
                        st.markdown("**Complaint Volume by Category**")
                        fig_bar = px.bar(x=cat_counts.index, y=cat_counts.values, color=cat_counts.index, color_discrete_sequence=colors, labels={'x':'Category','y':'Number of Complaints'})
                        fig_bar.update_layout(showlegend=False, height=400, margin=dict(t=30, b=30, l=30, r=30))
                        st.plotly_chart(fig_bar, use_container_width=True)
                    st.markdown("---")
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        st.markdown("<h4 style='color:#1f3c88;margin-bottom:1rem'>Category Breakdown</h4>", unsafe_allow_html=True)
                        for cat, cnt in cat_counts.items():
                            st.markdown(f"<p style='color:#2c3e50;margin:.4rem 0'><strong style='color:#1f3c88'>{cat}</strong>: {cnt} complaints ({cnt/len(df)*100:.1f}%)</p>", unsafe_allow_html=True)
                    with sc2:
                        st.markdown("<h4 style='color:#1f3c88;margin-bottom:1rem'>Priority Distribution</h4>", unsafe_allow_html=True)
                        for pri, cnt in df['Priority'].value_counts().items():
                            st.markdown(f"<p style='color:#2c3e50;margin:.4rem 0'><strong style='color:#1f3c88'>{pri}</strong>: {cnt} ({cnt/len(df)*100:.1f}%)</p>", unsafe_allow_html=True)
                
                with dtab3:
                    st.subheader("Priority Analysis")
                    fig_heat = px.imshow(pd.crosstab(df['Priority'], df['Category']), labels=dict(x="Category", y="Priority", color="Count"), color_continuous_scale="Blues", aspect="auto")
                    fig_heat.update_layout(title="Priority vs Category Heatmap", height=400)
                    st.plotly_chart(fig_heat, use_container_width=True)
                    st.markdown("---")
                    if len(high_df := df[df['Priority']=='High']) > 0:
                        st.markdown("**High Priority Complaints Requiring Immediate Attention**")
                        st.dataframe(high_df[['Complaint_Text', 'Category', 'Priority']], use_container_width=True, hide_index=True)
                    else: st.info("No high priority complaints found.")
                
                st.markdown("---\n### Export Results")
                st.columns([1, 1, 1])[1].download_button("Download Processed Data", df.to_csv(index=False), "complaint_intelligence_report.csv", "text/csv", use_container_width=True, type="primary")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

st.markdown("---")
st.markdown("<div style='text-align:center;padding:1rem 0;background-color:#e8ecf1;border-radius:10px;margin-top:1rem'><p style='font-size:1.1rem;font-weight:600;color:#1f3c88;margin-bottom:.5rem'>CHRIST University Complaint Intelligence System</p><p style='font-size:.9rem;color:#2c3e50;margin-bottom:.5rem'>Powered by Rule-Based NLP | Real-Time Analytics | Smart Categorization</p><p style='font-size:.85rem;color:#5a6c7d'>Developed by: <strong style='color:#1f3c88'>Kuheli Begum</strong> | MCA519A-3 Advanced Python Programming</p></div>", unsafe_allow_html=True)
