import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Flow-Adjusted NAV Tracker")

uploaded_file = st.file_uploader(
    "Upload Daily NAV Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    required_cols = ["Date", "NAV", "Donation"]

    if not all(col in df.columns for col in required_cols):
        st.error("Excel must contain: Date, NAV, Donation")
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Ensure numeric
    df["NAV"] = pd.to_numeric(df["NAV"])
    df["Donation"] = pd.to_numeric(df["Donation"]).fillna(0)

    # Compute flow-adjusted returns
    adjusted_returns = [0]  # first day = baseline

    for i in range(1, len(df)):
        prev_nav = df.loc[i-1, "NAV"]
        current_nav = df.loc[i, "NAV"]
        donation = df.loc[i, "Donation"]

        adj_return = (current_nav - donation) / prev_nav - 1
        adjusted_returns.append(adj_return)

    df["Adjusted Return"] = adjusted_returns

    # Build synthetic NAV
    synthetic_nav = [df.loc[0, "NAV"]]

    for r in adjusted_returns[1:]:
        synthetic_nav.append(synthetic_nav[-1] * (1 + r))

    df["Flow Adjusted NAV"] = synthetic_nav

    st.subheader("NAV Table")
    st.dataframe(df)

    # Plot
    fig, ax = plt.subplots()

    ax.plot(df["Date"], df["NAV"], label="Reported NAV")
    ax.plot(df["Date"], df["Flow Adjusted NAV"], linestyle="--", label="Flow Adjusted NAV")

    ax.set_title("Continuous NAV (Donation Adjusted)")
    ax.legend()

    st.pyplot(fig)

    # Performance stats
    total_return = (synthetic_nav[-1] / synthetic_nav[0]) - 1

    st.metric(
        label="True Portfolio Return",
        value=f"{total_return:.2%}"
    )