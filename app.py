import streamlit as st
import pandas as pd
import numpy as np

# Page config for mobile
st.set_page_config(
    page_title="Mortgage Comparison Tool",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better mobile experience
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_monthly_payment(total_borrowed, interest_rate_annual, number_of_years):
    """Calculate monthly payment for French-style mortgage."""
    monthly_interest_rate = (interest_rate_annual / 100) / 12
    number_of_months = number_of_years * 12
    
    if monthly_interest_rate > 0:
        monthly_payment = total_borrowed * (monthly_interest_rate * (1 + monthly_interest_rate)**number_of_months) / \
                          ((1 + monthly_interest_rate)**number_of_months - 1)
    else:
        monthly_payment = total_borrowed / number_of_months
    
    return monthly_payment, number_of_months

def calculate_annual_interest(total_borrowed, monthly_payment, monthly_interest_rate):
    """Calculate annual interest paid in the first year (for ROCE calculation)."""
    remaining_balance = total_borrowed
    annual_interest = 0
    
    # Calculate interest for first 12 months
    for _ in range(12):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance = remaining_balance - principal_payment
        annual_interest += interest_payment
    
    return annual_interest

def calculate_total_interest(total_borrowed, monthly_payment, number_of_months, monthly_interest_rate):
    """Calculate total interest paid over the loan term."""
    remaining_balance = total_borrowed
    total_interest_paid = 0
    
    for _ in range(1, number_of_months + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance = remaining_balance - principal_payment
        total_interest_paid += interest_payment
    
    return total_interest_paid

def calculate_roce(annual_rental_income, annual_interest_cost, annual_fees, down_payment):
    """Calculate Return on Capital Employed (ROCE).
    
    Note: Only interest and fees are costs. Principal payments build equity (capital creation).
    ROCE = (Annual Rental Income - Annual Interest - Annual Fees) / Down Payment × 100
    """
    annual_net_income = annual_rental_income - annual_interest_cost - annual_fees
    if down_payment > 0:
        roce = (annual_net_income / down_payment) * 100
    else:
        roce = float('inf') if annual_net_income > 0 else float('-inf')
    return roce, annual_net_income

# Title
st.title("🏦 Bank Mortgage Comparison Tool")
st.markdown("Compare multiple bank mortgage offers and find the best option based on **ROCE (Return on Capital Employed)**")
st.markdown("**ROCE = (Annual Rental Income - Annual Interest - Annual Fees) / Down Payment × 100**")
st.info("💡 **Note:** Principal payments build equity (capital creation), so only interest and fees are considered costs.")

# Sidebar for property details
with st.sidebar:
    st.header("Property Details")
    property_price = st.number_input(
        "Property Price ($)",
        min_value=0.0,
        value=106650.0,
        step=1000.0,
        format="%.2f"
    )
    monthly_rental_income = st.number_input(
        "Monthly Rental Income ($)",
        min_value=0.0,
        value=675.0,
        step=50.0,
        format="%.2f"
    )
    annual_rental_income = monthly_rental_income * 12
    
    st.markdown("---")
    st.markdown(f"**Annual Rental Income:** ${annual_rental_income:,.2f}")

# Main content
st.header("Bank Offers")

# Initialize session state for bank offers
if 'bank_offers' not in st.session_state:
    st.session_state.bank_offers = []

# Form to add new bank offer
with st.expander("➕ Add New Bank Offer", expanded=len(st.session_state.bank_offers) == 0):
    with st.form("add_bank_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            bank_name = st.text_input("Bank Name", placeholder="e.g., Bank A")
            interest_rate = st.number_input(
                "Interest Rate (%)",
                min_value=0.0,
                max_value=20.0,
                value=3.5,
                step=0.1,
                format="%.2f"
            )
            loan_amount = st.number_input(
                "Loan Amount ($)",
                min_value=0.0,
                value=74200.0,
                step=1000.0,
                format="%.2f"
            )
        
        with col2:
            loan_term = st.number_input(
                "Loan Term (years)",
                min_value=1,
                max_value=50,
                value=25,
                step=1
            )
            monthly_fees = st.number_input(
                "Monthly Fees ($)",
                min_value=0.0,
                value=150.0,
                step=10.0,
                format="%.2f",
                help="Combined: insurance + cleaning + taxes"
            )
            down_payment = st.number_input(
                "Down Payment ($)",
                min_value=0.0,
                value=32450.0,
                step=1000.0,
                format="%.2f"
            )
        
        submitted = st.form_submit_button("Add Bank Offer", use_container_width=True)
        
        if submitted and bank_name:
            new_offer = {
                'bank_name': bank_name,
                'interest_rate_annual': interest_rate,
                'number_of_years': loan_term,
                'loan_amount': loan_amount,
                'monthly_fees': monthly_fees,
                'down_payment': down_payment
            }
            st.session_state.bank_offers.append(new_offer)
            st.success(f"Added {bank_name}!")
            st.rerun()

# Display current bank offers
if st.session_state.bank_offers:
    st.subheader(f"Current Offers ({len(st.session_state.bank_offers)})")
    
    # Show list of added banks with delete option
    for idx, offer in enumerate(st.session_state.bank_offers):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{offer['bank_name']}** - {offer['interest_rate_annual']:.2f}% | {offer['number_of_years']} years | ${offer['loan_amount']:,.0f}")
        with col2:
            if st.button("🗑️", key=f"delete_{idx}", help="Delete this offer"):
                st.session_state.bank_offers.pop(idx)
                st.rerun()
    
    st.markdown("---")
    
    # Calculate and display comparison
    if st.button("🔄 Calculate Comparison", use_container_width=True, type="primary"):
        comparison_data = []
        
        for offer in st.session_state.bank_offers:
            # Calculate monthly mortgage payment
            monthly_payment, number_of_months = calculate_monthly_payment(
                offer['loan_amount'],
                offer['interest_rate_annual'],
                offer['number_of_years']
            )
            
            # Calculate annual interest (first year) - this is the actual cost
            monthly_interest_rate = (offer['interest_rate_annual'] / 100) / 12
            annual_interest = calculate_annual_interest(
                offer['loan_amount'],
                monthly_payment,
                monthly_interest_rate
            )
            
            # Calculate annual fees
            annual_fees = offer['monthly_fees'] * 12
            
            # Calculate annual principal payment (equity building)
            annual_principal = (monthly_payment * 12) - annual_interest
            
            # Calculate ROCE (only interest and fees are costs)
            roce, annual_net_income = calculate_roce(
                annual_rental_income,
                annual_interest,
                annual_fees,
                offer['down_payment']
            )
            
            # Calculate total interest over loan term
            total_interest = calculate_total_interest(
                offer['loan_amount'],
                monthly_payment,
                number_of_months,
                monthly_interest_rate
            )
            
            comparison_data.append({
                'Bank': offer['bank_name'],
                'Interest Rate (%)': offer['interest_rate_annual'],
                'Loan Term (years)': offer['number_of_years'],
                'Loan Amount': offer['loan_amount'],
                'Down Payment': offer['down_payment'],
                'Monthly Payment': round(monthly_payment, 2),
                'Monthly Fees': offer['monthly_fees'],
                'Annual Interest': round(annual_interest, 2),
                'Annual Principal': round(annual_principal, 2),
                'Annual Fees': round(annual_fees, 2),
                'Annual Net Income': round(annual_net_income, 2),
                'ROCE (%)': round(roce, 2),
                'Total Interest (lifetime)': round(total_interest, 2)
            })
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame(comparison_data)
        
        # Sort by ROCE (descending)
        comparison_df = comparison_df.sort_values('ROCE (%)', ascending=False).reset_index(drop=True)
        
        # Store in session state
        st.session_state.comparison_df = comparison_df
        
        # Display summary metrics
        st.subheader("📊 Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Property Price", f"${property_price:,.0f}")
        with col2:
            st.metric("Monthly Rental", f"${monthly_rental_income:,.0f}")
        with col3:
            st.metric("Annual Rental", f"${annual_rental_income:,.0f}")
        
        # Display comparison table
        st.subheader("📋 Comparison Table")
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Show best option
        if len(comparison_df) > 0:
            best_bank = comparison_df.iloc[0]
            
            st.markdown("---")
            st.subheader("🏆 Best Option (Highest ROCE)")
            
            # Create metrics for best option
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Bank", best_bank['Bank'])
            with col2:
                st.metric("ROCE", f"{best_bank['ROCE (%)']:.2f}%", delta=f"{best_bank['ROCE (%)']:.2f}%")
            with col3:
                st.metric("Annual Net Income", f"${best_bank['Annual Net Income']:,.2f}")
            with col4:
                st.metric("Annual Interest", f"${best_bank['Annual Interest']:,.2f}")
            
            # Detailed info
            with st.expander("📝 Detailed Information", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Interest Rate:** {best_bank['Interest Rate (%)']:.2f}%")
                    st.write(f"**Loan Term:** {best_bank['Loan Term (years)']} years")
                    st.write(f"**Loan Amount:** ${best_bank['Loan Amount']:,.2f}")
                    st.write(f"**Down Payment:** ${best_bank['Down Payment']:,.2f}")
                with col2:
                    st.write(f"**Monthly Payment:** ${best_bank['Monthly Payment']:,.2f}")
                    st.write(f"**Monthly Fees:** ${best_bank['Monthly Fees']:,.2f}")
                    st.write(f"**Annual Interest:** ${best_bank['Annual Interest']:,.2f}")
                    st.write(f"**Annual Principal (equity):** ${best_bank['Annual Principal']:,.2f}")
                    st.write(f"**Total Interest (lifetime):** ${best_bank['Total Interest (lifetime)']:,.2f}")
    
    # Show previous comparison if exists
    elif 'comparison_df' in st.session_state:
        st.subheader("📋 Previous Comparison")
        st.dataframe(
            st.session_state.comparison_df,
            use_container_width=True,
            hide_index=True
        )
        
        if len(st.session_state.comparison_df) > 0:
            best_bank = st.session_state.comparison_df.iloc[0]
            st.info(f"🏆 Best Option: **{best_bank['Bank']}** with ROCE of **{best_bank['ROCE (%)']:.2f}%**")
else:
    st.info("👆 Add at least one bank offer to start comparing!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Add this page to your phone's home screen for quick access!")

