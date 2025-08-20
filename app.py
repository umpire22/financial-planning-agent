import streamlit as st
import pandas as pd

st.title("💰 Financial Planning Agent")

st.write("Plan your budget, savings, and financial health with this AI-inspired tool.")

# --- Option 1: Manual Entry ---
st.subheader("Manual Financial Planning")

income = st.number_input("Monthly Income ($)", min_value=0, step=100)
expenses = st.number_input("Monthly Expenses ($)", min_value=0, step=50)
savings_goal = st.number_input("Target Monthly Savings ($)", min_value=0, step=50)

if st.button("Analyze My Finances"):
    st.subheader("📊 Financial Health Report")

    if income == 0:
        st.error("Please enter your income to continue.")
    else:
        savings = income - expenses
        savings_percent = (savings / income) * 100 if income > 0 else 0

        st.write(f"**Total Income:** ${income}")
        st.write(f"**Total Expenses:** ${expenses}")
        st.write(f"**Current Savings:** ${savings} ({savings_percent:.1f}%)")

        # Analysis
        if savings < 0:
            st.write("⚠️ You are overspending. Try reducing expenses.")
        elif savings_percent < 10:
            st.write("⚠️ Savings rate is very low. Aim for at least 20%.")
        else:
            st.write("✅ Good savings rate! Keep it up.")

        # 50/30/20 Rule Recommendation
        needs = income * 0.5
        wants = income * 0.3
        ideal_savings = income * 0.2

        st.subheader("📌 Recommended Budget (50/30/20 Rule)")
        st.write(f"Needs (50%): ${needs}")
        st.write(f"Wants (30%): ${wants}")
        st.write(f"Savings (20%): ${ideal_savings}")

        if savings_goal > 0:
            if savings >= savings_goal:
                st.success(f"🎯 You are on track to meet your savings goal of ${savings_goal} per month!")
            else:
                st.warning(f"⚠️ You need to save an extra ${savings_goal - savings} to reach your goal.")

# --- Option 2: Upload CSV ---
st.subheader("Batch Financial Analysis (Upload CSV)")
uploaded_file = st.file_uploader("Upload financial data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("📄 Uploaded Data")
    st.dataframe(df.head())

    def analyze_row(row):
        savings = row["Income"] - row["Expenses"]
        if savings < 0:
            return "Overspending"
        elif (savings / row["Income"]) * 100 < 10:
            return "Low Savings"
        elif (savings / row["Income"]) * 100 >= 20:
            return "Healthy Savings"
        else:
            return "Moderate Savings"

    df["Financial_Status"] = df.apply(analyze_row, axis=1)

    st.subheader("📊 Analysis Results")
    st.dataframe(df)

    # Download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Results", data=csv, file_name="financial_analysis.csv")
