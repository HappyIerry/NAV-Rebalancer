# donation_adjuster_streamlit.py
import streamlit as st

st.title("Donation-Neutral Prior Return Calculator")

st.markdown(
    """
Enter the NAV after the prior-period return (i.e. NAV that already *includes* the prior return),
the prior-period return (as a percent), and the donation amount (which will be parked to cash).
The app will show the start-of-period value, the donation-neutral prior return (which should
equal the input prior return), the new NAV after the donation, and some diagnostics.
"""
)

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    nav_after_return = st.number_input(
        "NAV after prior return (before donation)",
        min_value=0.0,
        value=1_050_000.0,
        step=1.0,
        format="%.2f"
    )

    prior_return_pct = st.number_input(
        "Prior-period return (percent)",
        min_value=-100.0,
        value=5.0,
        step=0.01,
        format="%.4f"
    )

with col2:
    donation_amount = st.number_input(
        "Donation (added to cash)",
        min_value=0.0,
        value=500_000.0,
        step=1.0,
        format="%.2f"
    )

# convert percent to decimal
prior_return = prior_return_pct / 100.0

# --- Core calculations ---
# 1) Value at start of period (before the prior return was earned)
#    NAV_after_return = start_value * (1 + prior_return)  => start_value = NAV_after_return / (1 + prior_return)
if (1 + prior_return) == 0:
    st.error("Invalid prior return: division by zero. Choose a different prior return.")
else:
    start_value = nav_after_return / (1 + prior_return)

# 2) New NAV after donation (donation parked as cash)
nav_new = nav_after_return + donation_amount

# 3) Donation-neutral prior return (should equal 'prior_return' input)
#    By design: the prior return on the original capital is unchanged.
donation_neutral_prior_return = prior_return  # (just echoing, for clarity)

# 4) Naive combined return (what happens if someone measured return from start_value -> nav_new,
#    unintentionally including the donation in the performance)
naive_combined_return = (nav_new / start_value) - 1.0

# 5) The incorrect/buggy formula some people used (for illustration):
#    incorrect = (nav_after_return - donation - start_value) / start_value
incorrect_value = (nav_after_return - donation_amount - start_value) / start_value

# --- Display results ---
st.header("Results")
st.write(f"**Start-of-period value (before prior return):** ${start_value:,.2f}")
st.write(f"**NAV after prior return (input):** ${nav_after_return:,.2f}")
st.write(f"**Donation added to cash:** ${donation_amount:,.2f}")
st.write(f"**New NAV after donation:** ${nav_new:,.2f}")

st.markdown("---")
st.subheader("Returns")
st.write(f"**Input prior-period return:** {prior_return_pct:.2f}%")
st.write(
    "**Donation-neutral prior return (institutional):** "
    f"{donation_neutral_prior_return * 100:.2f}%  \n"
    "_(This should equal the input prior return — donations after the period do not change past returns.)_"
)

st.markdown("---")
st.subheader("Diagnostics (for clarity)")
st.write(
    "**Naive combined return (start -> new NAV including donation):** "
    f"{naive_combined_return * 100:.2f}%  \n"
    "_(This mixes performance and flows — usually not what you want.)_"
)
st.write(
    "**Incorrect formula result (common mistake):** "
    f"{incorrect_value * 100:.2f}%  \n"
    "_(This demonstrates why subtracting donation from end NAV is wrong in this context.)_"
)

st.markdown("---")
st.info(
    """
Professional rule of thumb:
*Rebalancing/trades do not change performance history.*  
*Only external flows (donations/withdrawals) break performance measurement periods — treat them separately (TWR).*
"""
)

# Optional: show example summary as single-line output
st.header("Summary (single-line)")
st.write(
    f"Start ${start_value:,.0f} -> Prior return {prior_return_pct:.2f}% -> NAV_after {nav_after_return:,.0f} "
    f"-> Donation ${donation_amount:,.0f} -> New NAV {nav_new:,.0f}"
)
