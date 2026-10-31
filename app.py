import os
import joblib
import pandas as pd
from datetime import datetime
import streamlit as st
st.write("Streamlit version:", st.__version__)
import plotly.express as px

from database import (
    create_table,
    add_expense,
    view_expenses,
    delete_expense,
    save_budget,
    get_budget,
    register_user,
    verify_user,
)
# Page setup
st.set_page_config(
    page_title="Verdant | Expense Tracker",
    page_icon="🌿",
    layout="wide"
)

# File paths
ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL = joblib.load(os.path.join(ROOT, "expense_model.pkl"))
VECTORIZER = joblib.load(os.path.join(ROOT, "tfidf_vectorizer.pkl"))



create_table()

# User login session
if "user" not in st.session_state:
    st.session_state.user = None

# Login and Signup screen
if st.session_state.user is None:

    st.title("🌿 Welcome to Verdant")
    st.caption("Your personal finance space")

    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        st.subheader("Welcome Back")

        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password",
                type="password"
            )
            login_button = st.form_submit_button("Login")

        if login_button:
            user = verify_user(login_username, login_password)

            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with signup_tab:
        st.subheader("Create Your Account")

        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            username = st.text_input("Choose Username")
            password = st.text_input(
                "Create Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            signup_button = st.form_submit_button("Create Account")

        if signup_button:
            if not all([name, email, username, password]):
                st.error("Please fill all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")
            else:
                success, message = register_user(
                    name, email, username, password
                )

                if success:
                    st.success(message)
                    st.info("Please login using your new account.")
                else:
                    st.error(message)

    st.stop()

# Logged-in user's information
user_id = st.session_state.user["id"]
saved_budget = get_budget(user_id)
budget = float(saved_budget)

CATEGORIES = [
    "Shopping", "Food", "Travel",
    "Entertainment", "Bills", "Education"
]
COLUMNS = ["Description", "Category", "Amount"]

# ===== VERDANT PREMIUM FINTECH THEME =====
st.markdown("""
<style>

/* Main application background */
.stApp,
[data-testid="stHeader"] {
    background: #F5F8F5 !important;
}

.block-container {
    max-width: 1450px !important;
    padding: 2rem 2.5rem 3rem !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #EDF3EE !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #DCE7DE;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #234432 !important;
}

/* Headings */
h1, h2, h3 {
    color: #1F3D2E !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

p, label,
[data-testid="stCaptionContainer"] {
    color: #52675A;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7DE !important;
    border-radius: 18px !important;
    padding: 22px !important;
    box-shadow: 0 4px 14px rgba(31,61,46,0.045);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #A9C5B0 !important;
    box-shadow: 0 9px 22px rgba(31,61,46,0.09);
}

[data-testid="stMetricLabel"] {
    color: #617568 !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    color: #1F3D2E !important;
    font-weight: 750 !important;
}

/* Dashboard containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7DE !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 14px rgba(31,61,46,0.045);
    transition: box-shadow 0.2s ease,
                border-color 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #B5CDBB !important;
    box-shadow: 0 8px 22px rgba(31,61,46,0.075);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #1F3D2E !important;
    border-color: #D0DFD3 !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button,
.stDownloadButton button {
    background: #315B45 !important;
    color: #FFFFFF !important;
    border: 1px solid #315B45 !important;
    border-radius: 11px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover,
.stDownloadButton button:hover {
    background: #244832 !important;
    border-color: #244832 !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 14px rgba(31,61,46,0.16);
}

/* Progress bar */
[data-testid="stProgress"] > div {
    background: #E5EEE7 !important;
    border-radius: 20px;
}

[data-testid="stProgress"] [data-testid="stProgressBar"] {
    background: #679477 !important;
    border-radius: 20px;
}

/* Transaction dataframe */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7DE !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    margin-top: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(31,61,46,0.045);
}

/* Category filter */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #DCE7DE !important;
    border-radius: 11px !important;
}

div[data-baseweb="tag"] {
    background: #E2EEE5 !important;
    border: 1px solid #C6D9CB !important;
    border-radius: 7px !important;
}

div[data-baseweb="tag"] *,
div[data-baseweb="tag"] span {
    color: #24543D !important;
}

/* Dividers */
hr {
    border-color: #E1EAE3 !important;
}

/* Smooth transitions */
button, input, [data-baseweb="select"] {
    transition: all 0.2s ease;
}

</style>
""", unsafe_allow_html=True)


def load_data():
    records = view_expenses(user_id)

    df = pd.DataFrame(
    records,
    columns=[
        "ID",
        "Description",
        "Category",
        "Amount",
        "Date",
        "User ID"
    ]
)
    if df.empty:
        return pd.DataFrame(
            columns=["ID", "Description", "Category", "Amount", "Date"]
        )

    df["Description"] = df["Description"].fillna("").astype(str)
    df["Category"] = df["Category"].fillna("Other").astype(str)
    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    ).fillna(0.0)

    return df


def save_expense(description, amount):
    if not description.strip():
        return False, "Please enter a description."

    if amount <= 0:
        return False, "Amount must be greater than zero."

    category = MODEL.predict(
        VECTORIZER.transform([description.strip()])
    )[0]

    add_expense(
    description.strip(),
    category,
    float(amount),
    user_id
)

    return True, category

# Sidebar: four option groups

with st.sidebar:

    st.write(f"Welcome, {st.session_state.user['name']}!")

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.pop("budget", None)
        st.rerun()

    st.title("🌿 Verdant")
    st.caption("YOUR PERSONAL FINANCE SPACE")
    st.divider()

    st.subheader("01 · Budget")

    if "budget" not in st.session_state:
        st.session_state.budget = float(saved_budget)

    budget = st.number_input(
        "Spending limit (₹)",
        min_value=0.0,
        step=100.0,
        key="budget"
    )

    if budget != saved_budget:
        save_budget(budget, user_id)
        saved_budget = budget

    st.divider()
    st.subheader("02 · Quick Add")

    with st.form("expense_form", clear_on_submit=True):
        description = st.text_input(
            "Description", placeholder="e.g. College lunch"
        )
        amount = st.number_input(
            "Amount (₹)", min_value=0.0, step=10.0
        )
        submitted = st.form_submit_button(
            "Predict & Save", use_container_width=True
        )

    if submitted:
        try:
            success, result = save_expense(description, amount)
            if success:
                st.session_state.message = (
                    f"Saved! AI predicted: {result}"
                )
                st.rerun()
            st.error(result)
        except Exception as error:
            st.error(f"Could not save expense: {error}")

    st.markdown("**Delete a mistaken expense**")

    current_expenses = load_data()

    if current_expenses.empty:
        st.caption("No expenses available to delete.")
    else:
        expense_options = {
            (
                f"ID {int(row['ID'])} | {row['Description']} | "
                f"{row['Category']} | ₹{row['Amount']:,.2f}"
            ): int(row["ID"])
            for _, row in current_expenses.iterrows()
        }

        selected_expense = st.selectbox(
            "Choose an expense",
            options=list(expense_options.keys()),
            key="delete_expense_choice"
        )

        confirm_delete = st.checkbox(
            "I confirm I want to delete this expense",
            key="confirm_expense_deletion"
        )

        if st.button("Delete Selected Expense", use_container_width=True):
            if not confirm_delete:
                st.warning("Please confirm before deleting.")
            else:
                selected_id = expense_options[selected_expense]
                delete_expense(selected_id, user_id)
                st.session_state.pop(
                    "confirm_expense_deletion", None
                )
                st.success("Expense deleted successfully.")
                st.rerun()

    st.divider()
    st.subheader("03 · View Settings")

    rows = st.selectbox(
        "History rows", [5, 10, 20, 50, "All"], index=1
    )

    st.divider()
    st.subheader("04 · Your Data")

    st.download_button(
        "Download CSV",
        data=load_data().to_csv(index=False).encode("utf-8"),
        file_name="my_expenses.csv",
        mime="text/csv",
        use_container_width=True
    )

# Dashboard data
df = load_data()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

current_month = datetime.now().month
current_year = datetime.now().year

monthly_expenses = df[
    (df["Date"].dt.month == current_month) &
    (df["Date"].dt.year == current_year)
]

monthly_total = monthly_expenses["Amount"].sum()

total = df["Amount"].sum()
count = len(df)
average = total / count if count else 0



# Premium Verdant Dashboard Header
with st.container(border=True):
    st.caption("🌿  VERDANT  /  PERSONAL FINANCE")

    st.title("Your money, made clearer.")

    st.write(
        "A smarter way to track spending, "
        "understand your habits, and stay in control."
    )

    st.caption("AI-POWERED EXPENSE TRACKING")


if "message" in st.session_state:
    st.success(st.session_state.message)

# Summary

# Premium Overview Cards
st.subheader("Your Overview")

a, b, c = st.columns(3, gap="large")

with a:
    with st.container(border=True):
        st.caption("TOTAL SPENDING")
        st.metric(
            label="",
            value=f"₹{total:,.2f}",
            border=False
        )

with b:
    with st.container(border=True):
        st.caption("EXPENSES RECORDED")
        st.metric(
            label="",
            value=f"{count}",
            border=False
        )

with c:
    with st.container(border=True):
        st.caption("AVERAGE EXPENSE")
        st.metric(
            label="",
            value=f"₹{average:,.2f}",
            border=False
        )


st.divider()

# # Budget and insight cards
left, right = st.columns([1, 1], gap="large")

with left:
    with st.container(border=True):
        st.subheader("🌿 Budget Progress")
        st.caption("Monitor your spending against your monthly budget.")

        if budget > 0:
            progress = min(monthly_total / budget, 1.0)
            st.progress(progress)

            st.markdown("**Amount spent**")
            st.markdown(f"### ₹{monthly_total:,.2f}")

            st.markdown("**Monthly budget**")
            st.write(f"₹{budget:,.2f}")

            remaining = budget - monthly_total

            if remaining >= 0:
                st.success(f"₹{remaining:,.2f} remaining")
            else:
                st.warning(f"₹{-remaining:,.2f} over budget")
        else:
            st.info("Set your budget in the sidebar.")

with right:
    with st.container(border=True):
        st.subheader("📊 Spending Insight")
        st.caption("Discover which category uses the most money.")

        if not df.empty:
            totals = df.groupby("Category")["Amount"].sum()
            category = totals.idxmax()
            value = totals.max()

            st.markdown("**Highest-spending category**")
            st.markdown(f"### {category}")
            st.markdown(f"₹{value:,.2f} spent")

            if total > 0:
                st.progress(min(value / total, 1.0))
                st.caption(
                    f"{value / total * 100:.1f}% of total spending"
                )
        else:
            st.info("Add an expense to see your spending insights.")

# Spending Charts - Side by Side
chart_left, chart_right = st.columns(2, gap="large")

with chart_left:
    with st.container(border=True):
        st.subheader("Spending by Category")

        if not df.empty:
            category_data = (
                df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )
            category_data = category_data[
                category_data["Amount"] > 0
            ]

            if not category_data.empty:
                fig = px.pie(
                    category_data,
                    names="Category",
                    values="Amount",
                    hole=0.65,
                    color_discrete_sequence=[
                        "#B7D8C0", "#D6E8D9", "#E8E3C9",
                        "#C5D5E8", "#D9CBE8", "#A8C9B5"
                    ]
                )

                fig.update_traces(
                    textinfo="label+percent",
                    textposition="inside",
                    textfont=dict(
                        color="#26352B",
                        size=12,
                        family="Arial Black"
                    ),
                    marker=dict(
                        line=dict(color="white", width=3)
                    )
                )

                
                fig.update_layout(
                    showlegend=True,
                    legend_title_text="Categories",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.20,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11, color="#425B4B")
                    ),
                    margin=dict(t=20, b=45, l=15, r=15),
                    height=380,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    font=dict(
                    color="#26352B",
                    size=12,
                    family="Arial"
                )
            )


                st.plotly_chart(
                    fig, use_container_width=True
                )
            else:
                st.info("Add an expense to see your category breakdown.")
        else:
            st.info("Your chart will appear after your first expense.")

with chart_right:
    with st.container(border=True):
        st.subheader("Monthly Spending Trend")

        if not df.empty:
            monthly_trend = df.dropna(
                subset=["Date"]
            ).copy()

            monthly_trend["Month"] = (
                monthly_trend["Date"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_trend = (
                monthly_trend.groupby("Month")["Amount"]
                .sum()
                .reset_index()
            )

            fig_trend = px.area(
                monthly_trend,
                x="Month",
                y="Amount",
                markers=True,
                color_discrete_sequence=["#7EAA8C"]
            )

            fig_trend.update_traces(
                line=dict(width=3),
                fill="tozeroy",
                fillcolor="rgba(126,170,140,0.18)"
            )

            
            fig_trend.update_layout(
                height=380,
                margin=dict(t=20, b=35, l=15, r=15),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(
                    color="#425B4B",
                    size=12,
                    family="Arial"
                ),
                xaxis_title=None,
                yaxis_title="Amount (₹)",
                showlegend=False,
                hovermode="x unified",
                xaxis=dict(
                    showgrid=False,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor="#EDF2EE",
                    zeroline=False
                )
            )


            st.plotly_chart(
                fig_trend, use_container_width=True
            )
        else:
            st.info("Your monthly trend will appear after your first expense.")

st.divider()



# Recent Transactions
with st.container(border=True):
    st.subheader("Recent Transactions")
    st.caption("A quick look at your latest spending activity.")

    if not df.empty:
        categories = sorted(df["Category"].dropna().unique())

        selected = st.multiselect(
            "Filter by category",
            options=categories,
            default=categories,
            placeholder="Choose categories",
            help="Select the categories you want to see."
        )
        history = (
            df[df["Category"].isin(selected)]
            .iloc[::-1]
            .copy()
        )

        st.caption(
            f"Showing {len(history)} of {count} expenses."
        )

        if not history.empty:
            display_history = history.copy()

            display_history["Amount"] = display_history["Amount"].apply(
                lambda x: f"₹{x:,.2f}"
            )

            display_history["Date"] = pd.to_datetime(
                display_history["Date"]
            ).dt.strftime("%d %b %Y")

            columns = ["ID", "Description", "Category", "Amount", "Date"]

            table_html = display_history[columns].to_html(
                index=False,
                border=0,
                classes="verdant-table",
                escape=True
            )

            st.markdown(
                """
                <style>
                .verdant-table-wrapper {
                    width: 100%;
                    overflow-x: auto;
                    border: 1px solid #DCE7DE;
                    border-radius: 14px;
                    background: #FFFFFF;
                }

                .verdant-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                    color: #30483A;
                    background: #FFFFFF;
                }

                .verdant-table thead th {
                    background: #EAF2EC;
                    color: #1F3D2E;
                    font-weight: 650;
                    text-align: left;
                    padding: 16px 18px;
                    border-bottom: 1px solid #DCE7DE;
                    white-space: nowrap;
                }

                .verdant-table tbody td {
                    padding: 15px 18px;
                    border-bottom: 1px solid #EDF2EE;
                    background: #FFFFFF;
                }

                .verdant-table tbody tr:last-child td {
                    border-bottom: none;
                }

                .verdant-table tbody tr:hover td {
                    background: #F4F8F5;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="verdant-table-wrapper">{table_html}</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("No transactions match the selected categories.")

    else:
        st.info("No expenses recorded yet.")

st.divider()

st.caption(
    "🌿 VERDANT · Built with Python, Streamlit & Machine Learning"
)
