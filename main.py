import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# GRADEGLOW - STUDENT ANALYTICS
# ==========================================

st.set_page_config(
    page_title="GradeGlow | Student Analytics",
    page_icon="🎓",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "students.csv"

subjects = [
    "Python",
    "Mathematics",
    "English",
    "Computer Networks",
    "Data Science"
]


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    if not CSV_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(CSV_FILE)


df = load_data()


# ==========================================
# CALCULATE MARKS
# ==========================================

if not df.empty:

    required_columns = [
        "Name",
        "Department",
        *subjects
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            "Missing CSV columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    for subject in subjects:
        df[subject] = pd.to_numeric(
            df[subject],
            errors="coerce"
        )

    df[subjects] = df[subjects].fillna(0)

    df["Total"] = df[subjects].sum(axis=1)

    df["Average"] = (
        df[subjects].mean(axis=1).round(2)
    )


# ==========================================
# GRADE CALCULATION
# ==========================================

def calculate_grade(average):

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


if not df.empty:

    df["Grade"] = df["Average"].apply(
        calculate_grade
    )

    df["Result"] = df[subjects].apply(
        lambda row:
        "PASS" if (row >= 35).all()
        else "FAIL",
        axis=1
    )


# ==========================================
# PREMIUM CSS DESIGN
# ==========================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(
        135deg,
        #080D1C,
        #11152B,
        #191438
    );
    color: #F8FAFF;
}

/* HEADER */

[data-testid="stHeader"] {
    background: transparent;
}

/* MAIN CONTENT */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10172B,
        #17132F
    );
    border-right: 1px solid #34365B;
}

/* SIDEBAR TITLE */

[data-testid="stSidebar"] h1 {
    color: #FFFFFF !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* SIDEBAR TEXT */

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #E5E9FF !important;
}

/* NAVIGATION */

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #E6E9FF !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* HEADINGS */

h1 {
    color: #FFFFFF !important;
    font-size: 42px !important;
    font-weight: 850 !important;
}

h2 {
    color: #F3F0FF !important;
    font-size: 28px !important;
    font-weight: 750 !important;
}

h3 {
    color: #E6DEFF !important;
    font-size: 21px !important;
    font-weight: 700 !important;
}

/* GENERAL TEXT */

p, li {
    color: #DCE3F7 !important;
}

/* KPI CARDS */

.metric-card {
    background: linear-gradient(
        145deg,
        #28204F,
        #382765
    );

    padding: 22px;
    border-radius: 20px;
    border: 1px solid #6D55B8;

    box-shadow:
        0 8px 28px rgba(0, 0, 0, 0.30);

    min-height: 130px;
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border: 1px solid #B69CFF;

    box-shadow:
        0 12px 35px rgba(124, 92, 255, 0.25);
}

/* KPI TITLE */

.metric-title {
    color: #E0D5FF !important;
    font-size: 15px !important;
    font-weight: 650 !important;
}

/* KPI VALUE */

.metric-value {
    color: #FFFFFF !important;
    font-size: 32px !important;
    font-weight: 850 !important;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

/* DATA TABLE */

[data-testid="stDataFrame"] {
    border: 1px solid #7057C9;
    border-radius: 14px;
    overflow: hidden;
}

/* BUTTONS */

.stDownloadButton button,
.stFormSubmitButton button {
    background: linear-gradient(
        90deg,
        #7657FF,
        #A66BFF
    );

    color: #FFFFFF !important;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;
}

.stDownloadButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(
        90deg,
        #987CFF,
        #C18BFF
    );
}

/* INPUTS */

input, textarea {
    color: #FFFFFF !important;
}

/* DIVIDER */

hr {
    border-color: #45436B !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("## 🎓 GradeGlow")

st.sidebar.caption(
    "Student Performance Analytics"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Student Records",
        "Top Performers",
        "Add Student"
    ]
)

st.sidebar.markdown("---")


# ==========================================
# SIDEBAR GROWTH CARD
# ==========================================

sidebar_card = (
    '<div style="'
    'background:#11182F;'
    'border:1px solid #6C5CE7;'
    'border-radius:18px;'
    'padding:20px 16px;'
    'margin-top:18px;'
    'box-shadow:0 5px 18px rgba(0,0,0,0.3);'
    '">'

    '<div style="'
    'color:#AFA0FF;'
    'font-size:12px;'
    'font-weight:700;'
    'letter-spacing:1.5px;'
    'margin-bottom:12px;'
    '">'
    'YOUR LEARNING JOURNEY'
    '</div>'

    '<div style="'
    'color:#FFFFFF;'
    'font-size:20px;'
    'font-weight:800;'
    'margin-bottom:14px;'
    '">'
    '🚀 Track Your Growth'
    '</div>'

    '<div style="'
    'color:#E1E7FF;'
    'font-size:15px;'
    'font-weight:500;'
    'line-height:1.8;'
    '">'
    'Analyze performance.<br>'
    'Improve every day.'
    '</div>'

    '</div>'
)

st.sidebar.markdown(
    sidebar_card,
    unsafe_allow_html=True
)


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown("# ✨ GradeGlow")

st.markdown(
    "Smart Student Performance Analytics Dashboard"
)

st.markdown("---")


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    if df.empty:

        st.warning(
            "No student data found. "
            "Please add records to students.csv."
        )

    else:

        total_students = len(df)

        average_marks = df["Average"].mean()

        pass_count = (
            df["Result"] == "PASS"
        ).sum()

        pass_percentage = (
            pass_count / total_students
        ) * 100

        topper = df.loc[
            df["Average"].idxmax(),
            "Name"
        ]


        # ==================================
        # KPI CARDS
        # ==================================

        col1, col2, col3, col4 = st.columns(4)

        def display_card(
            column,
            title,
            value,
            icon
        ):

            html = (
                '<div class="metric-card">'
                f'<div class="metric-title">'
                f'{icon} {title}</div>'
                f'<div class="metric-value">'
                f'{value}</div>'
                '</div>'
            )

            with column:
                st.markdown(
                    html,
                    unsafe_allow_html=True
                )


        display_card(
            col1,
            "Total Students",
            total_students,
            "🎓"
        )

        display_card(
            col2,
            "Average Marks",
            f"{average_marks:.1f}",
            "📊"
        )

        display_card(
            col3,
            "Pass Percentage",
            f"{pass_percentage:.0f}%",
            "✅"
        )

        display_card(
            col4,
            "Top Performer",
            topper,
            "🏆"
        )


        st.markdown("<br>", unsafe_allow_html=True)


        # ==================================
        # CHARTS
        # ==================================

        left, right = st.columns(2)


        # SUBJECT PERFORMANCE

        with left:

            st.subheader(
                "📈 Subject Performance"
            )

            subject_average = (
                df[subjects]
                .mean()
                .reset_index()
            )

            subject_average.columns = [
                "Subject",
                "Average"
            ]

            fig = px.bar(
                subject_average,
                x="Subject",
                y="Average",
                color="Average",

                color_continuous_scale=[
                    "#6C4CFF",
                    "#B38AFF"
                ],

                template="plotly_dark",
                text="Average"
            )

            fig.update_traces(
                texttemplate="%{y:.1f}",
                textposition="outside"
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Arial",
                    size=14,
                    color="#F1F3FF"
                ),

                xaxis=dict(
                    title="Subject",
                    title_font=dict(
                        color="#FFFFFF"
                    ),
                    tickfont=dict(
                        color="#F1F3FF",
                        size=12
                    ),
                    gridcolor="#343451"
                ),

                yaxis=dict(
                    title="Average Marks",
                    title_font=dict(
                        color="#FFFFFF"
                    ),
                    tickfont=dict(
                        color="#F1F3FF"
                    ),
                    gridcolor="#45436B",
                    range=[0, 110]
                ),

                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # GRADE DISTRIBUTION

        with right:

            st.subheader(
                "🎯 Grade Distribution"
            )

            grade_order = [
                "A+",
                "A",
                "B",
                "C",
                "D",
                "F"
            ]

            grade_counts = (
                df["Grade"]
                .value_counts()
                .reindex(
                    grade_order,
                    fill_value=0
                )
                .reset_index()
            )

            grade_counts.columns = [
                "Grade",
                "Students"
            ]

            grade_counts = grade_counts[
                grade_counts["Students"] > 0
            ]

            fig2 = px.pie(
                grade_counts,
                names="Grade",
                values="Students",
                hole=0.55,

                color_discrete_sequence=[
                    "#7C5CFF",
                    "#A78BFA",
                    "#C4B5FD",
                    "#6366F1",
                    "#818CF8",
                    "#F472B6"
                ],

                template="plotly_dark"
            )

            fig2.update_traces(
                textposition="inside",
                textinfo="percent+label",

                textfont=dict(
                    color="#FFFFFF",
                    size=15
                )
            )

            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Arial",
                    size=15,
                    color="#FFFFFF"
                ),

                legend=dict(
                    font=dict(
                        color="#F1F3FF",
                        size=14
                    )
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


        # ==================================
        # STUDENT OVERVIEW
        # ==================================

        # Clean centered heading card.
        # No separate HTML tags displayed as code.

        overview_heading = (
            '<div style="'
            'background:linear-gradient(135deg,#211947,#30245E);'
            'border:1px solid #8065E8;'
            'border-radius:18px;'
            'padding:22px;'
            'margin-top:20px;'
            'margin-bottom:18px;'
            'text-align:center;'
            'box-shadow:0 8px 25px rgba(0,0,0,0.25);'
            '">'

            '<h2 style="'
            'color:#FFFFFF;'
            'font-size:28px;'
            'font-weight:800;'
            'margin:0;'
            '">'
            '📋 Student Overview'
            '</h2>'

            '<p style="'
            'color:#CFC4FF;'
            'font-size:15px;'
            'margin-top:10px;'
            'margin-bottom:0;'
            '">'
            'Academic performance at a glance'
            '</p>'

            '</div>'
        )

        st.markdown(
            overview_heading,
            unsafe_allow_html=True
        )


        # ==================================
        # STUDENT TABLE
        # ==================================

        overview = df[
            [
                "Name",
                "Department",
                "Total",
                "Average",
                "Grade",
                "Result"
            ]
        ].sort_values(
            by="Average",
            ascending=False
        )


        # Table styling

        styled_overview = (
            overview.style

            .set_properties(
                **{
                    "background-color": "#17152F",
                    "color": "#F5F3FF",
                    "border-color": "#51447F",
                    "text-align": "center",
                    "font-size": "15px",
                    "padding": "12px"
                }
            )

            .set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                            (
                                "background-color",
                                "#493080"
                            ),
                            (
                                "color",
                                "#FFFFFF"
                            ),
                            (
                                "font-weight",
                                "bold"
                            ),
                            (
                                "text-align",
                                "center"
                            ),
                            (
                                "border",
                                "1px solid #8065E8"
                            )
                        ]
                    },
                    {
                        "selector": "td",
                        "props": [
                            (
                                "border",
                                "1px solid #51447F"
                            )
                        ]
                    },
                    {
                        "selector": "table",
                        "props": [
                            (
                                "border-collapse",
                                "collapse"
                            ),
                            (
                                "width",
                                "100%"
                            )
                        ]
                    }
                ]
            )
        )

        st.dataframe(
            styled_overview,
            use_container_width=True,
            hide_index=True
        )


        # ==================================
        # DOWNLOAD REPORT
        # ==================================

        st.download_button(
            label="⬇️ Download Student Report",

            data=overview.to_csv(index=False),

            file_name="gradeglow_report.csv",

            mime="text/csv"
        )


# ==========================================
# STUDENT RECORDS
# ==========================================

elif page == "Student Records":

    st.subheader("📚 Student Records")

    if df.empty:

        st.info("No student records available.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="⬇️ Download Student Report",
            data=df.to_csv(index=False),
            file_name="gradeglow_report.csv",
            mime="text/csv"
        )


# ==========================================
# TOP PERFORMERS
# ==========================================

elif page == "Top Performers":

    st.subheader("🏆 Top Performers")

    if df.empty:

        st.info("No student records available.")

    else:

        top_students = df.sort_values(
            by="Average",
            ascending=False
        ).head(5)

        for rank, (_, student) in enumerate(
            top_students.iterrows(),
            start=1
        ):

            html = (
                '<div class="metric-card" '
                'style="margin-bottom:15px;">'

                f'<div class="metric-title">'
                f'🏅 Rank #{rank}</div>'

                f'<div class="metric-value">'
                f'{student["Name"]}</div>'

                f'<p style="color:#E0D5FF;">'
                f'Average: {student["Average"]} '
                f'| Grade: {student["Grade"]}'
                '</p>'

                '</div>'
            )

            st.markdown(
                html,
                unsafe_allow_html=True
            )


# ==========================================
# ADD STUDENT
# ==========================================

elif page == "Add Student":

    st.subheader("➕ Add New Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        department = st.text_input(
            "Department",
            value="CSE"
        )

        marks = {}

        for subject in subjects:

            marks[subject] = st.number_input(
                subject,
                min_value=0,
                max_value=100,
                value=0
            )

        submitted = st.form_submit_button(
            "Save Student"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter student name."
                )

            else:

                new_student = {
                    "Name": name.strip(),
                    "Department": department.strip(),
                    **marks
                }

                new_df = pd.DataFrame(
                    [new_student]
                )

                new_df.to_csv(
                    CSV_FILE,
                    mode="a",
                    header=not CSV_FILE.exists(),
                    index=False
                )

                st.success(
                    f"{name} added successfully!"
                )

                st.cache_data.clear()

                st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <p style="
        text-align:center;
        color:#B8B4D8 !important;
        font-size:14px !important;
    ">
        GradeGlow | Student Analytics
        <br>
        Built with Python coding
    </p>
    """,
    unsafe_allow_html=True
)