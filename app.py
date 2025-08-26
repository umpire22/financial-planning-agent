import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="💰 Financial Planning Agent",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #FFFFFF; }
        .stButton>button, .stDownloadButton>button { background-color: #FF6F61; color: white; font-size: 16px; border-radius: 12px; padding: 10px 20px; margin-top: 10px; }
        h1, h2, h3, h4 { color: #FFD700; }
        .stMetric-label, .stMetric-value, .stMetric-delta { color: #FFFFFF; }
        .stDataFrame td, .stDataFrame th { color: #FFFFFF; background-color: #1E1E1E; }
    </style>
""", unsafe_allow_html=True)

# --- APP TITLE ---
st.title("💰 Financial Planning Agent")
st.markdown("Plan your budget, savings, and financial health with this AI-powered tool 🌙")

# --- SIDEBAR ---
st.sidebar.header("Options")
mode = st.sidebar.radio("Choose Input Mode:", ["Manual Entry", "Upload CSV"])
currency = st.sidebar.radio("Select Currency:", ["Dollar ($)", "Naira (₦)"])
curr_symbol = "$" if currency == "Dollar ($)" else "₦"

# --- MANUAL ENTRY MODE ---
if mode == "Manual Entry":
    st.subheader("📝 Manual Financial Planning")

    income = st.number_input(f"Monthly Income ({curr_symbol})", min_value=0, step=100)
    expenses = st.number_input(f"Monthly Expenses ({curr_symbol})", min_value=0, step=50)
    savings_goal = st.number_input(f"Target Monthly Savings ({curr_symbol})", min_value=0, step=50)

    if st.button("Analyze My Finances"):
        if income == 0:
            st.error("Please enter your income to continue.")
        else:
            savings = income - expenses
            savings_percent = (savings / income) * 100 if income > 0 else 0

            # Show metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("💵 Total Income", f"{curr_symbol}{income}")
            col2.metric("📉 Total Expenses", f"{curr_symbol}{expenses}")
            col3.metric("💰 Current Savings", f"{curr_symbol}{savings}", delta=f"{savings_percent:.1f}%")

            # Progress bar for savings goal
            if savings_goal > 0:
                progress = min(savings / savings_goal, 1.0)
                st.progress(progress)
                st.write(f"Savings Goal Progress: {curr_symbol}{savings} / {curr_symbol}{savings_goal}")

            # Financial advice
            if savings < 0:
                st.warning("⚠️ You are overspending. Try reducing expenses.")
            elif savings_percent < 10:
                st.warning("⚠️ Savings rate is very low. Aim for at least 20%.")
            else:
                st.success("✅ Good savings rate! Keep it up.")

            # 50/30/20 Rule
            needs = income * 0.5
            wants = income * 0.3
            ideal_savings = income * 0.2

            st.subheader("📌 Recommended Budget (50/30/20 Rule)")
            budget_df = pd.DataFrame({
                "Category": ["Needs (50%)", "Wants (30%)", "Savings (20%)"],
                "Amount": [f"{curr_symbol}{needs}", f"{curr_symbol}{wants}", f"{curr_symbol}{ideal_savings}"]
            })
            st.dataframe(budget_df, use_container_width=True)

            # Pie chart
            fig, ax = plt.subplots()
            ax.pie([needs, wants, ideal_savings],
                   labels=["Needs", "Wants", "Savings"],
                   autopct='%1.1f%%',
                   colors=["#3498DB", "#F1C40F", "#2ECC71"])
            st.pyplot(fig)

# --- CSV UPLOAD MODE ---
else:
    st.subheader("📂 Batch Financial Analysis (Upload CSV)")
    uploaded_file = st.file_uploader("Upload financial data (CSV)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Validate CSV
        required_cols = ["Income", "Expenses"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain columns: {required_cols}")
        else:
            st.write("📄 Uploaded Data")
            st.dataframe(df.head(), use_container_width=True)

            # Analysis function
            def analyze_row(row):
                if row["Income"] == 0:
                    return "No Income Provided"
                savings = row["Income"] - row["Expenses"]
                percent = (savings / row["Income"]) * 100
                if savings < 0:
                    return "Overspending"
                elif percent < 10:
                    return "Low Savings"
                elif percent >= 20:
                    return "Healthy Savings"
                else:
                    return "Moderate Savings"

            df["Savings"] = df["Income"] - df["Expenses"]
            df["Financial_Status"] = df.apply(analyze_row, axis=1)

            # Format currency for display
            df_display = df.copy()
            df_display["Income"] = df_display["Income"].apply(lambda x: f"{curr_symbol}{x}")
            df_display["Expenses"] = df_display["Expenses"].apply(lambda x: f"{curr_symbol}{x}")
            df_display["Savings"] = df_display["Savings"].apply(lambda x: f"{curr_symbol}{x}")

            st.subheader("📊 Analysis Results")
            st.dataframe(df_display, use_container_width=True)

            # Download results
            df_download = df.copy()
            csv = df_download.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Download Results", data=csv, file_name="financial_analysis.csv")
