import math

def get_float_input(prompt_text):
    while True:
        try:
            return float(input(prompt_text))
        except ValueError:
            print("Invalid input. Please enter a number.")

def normalize_weights(weights_dict):
    """Ensures that any dictionary of weights sums exactly to 1.0."""
    total_weight = sum(weights_dict.values())
    if total_weight == 0:
        return {k: 0 for k in weights_dict.keys()}
    return {k: v / total_weight for k, v in weights_dict.items()}

def run_dsbvf_engine():
    print("\n" + "="*50)
    print("="*50)
    
    # --- 1. Menu Switchboard ---
    print("\nSelect the Market Regime for the Asset:")
    print("1. India (Emerging Market)")
    print("2. USA (Developed Market - Reserve)")
    print("3. UK (Developed Market)")
    
    choice = input("\nEnter 1, 2, or 3: ")
    
    if choice == '1':
        country = "India"
        factors = ["India VIX", "US Dollar Index (DXY)", "EM Bond Spreads"]
    elif choice == '2':
        country = "USA"
        factors = ["US VIX (CBOE)", "10-Year Treasury Yield", "US High Yield Spreads"]
    elif choice == '3':
        country = "UK"
        factors = ["UK VIX (VFTSE)", "UK 10-Year Gilt Yield", "UK Corporate Spreads"]
    else:
        print("Invalid selection. Exiting.")
        return

    print(f"\n--- Initializing {country} Macro Framework ---")
    
    # --- 2. Interactive Data Collection ---
    base_ke = get_float_input(f"Enter the Base Cost of Equity (e.g., 10.0 for 10%): ")
    lambda_asset = get_float_input(f"Enter the Asset's Sensitivity Coefficient (\u03BB) (e.g., 0.02): ")
    alpha = get_float_input(f"Enter Conviction Alpha (0.0 to 1.0, where 1.0 is 100% historical): ")
    
    hist_weights = {}
    fund_weights = {}
    z_scores = {}
    
    print(f"\n--- Factor Inputs for {country} ---")
    for factor in factors:
        print(f"\n[{factor}]")
        hist_weights[factor] = get_float_input(f"  Historical Regression Weight (0-100): ")
        fund_weights[factor] = get_float_input(f"  Fundamental Target Weight (0-100)   : ")
        z_scores[factor] = get_float_input(f"  Current Z-Score (-3.0 to +3.0)      : ")

    # --- 3. The Mathematics ---
    hist_norm = normalize_weights(hist_weights)
    fund_norm = normalize_weights(fund_weights)
    
    blended_weights = {}
    for factor in factors:
        blended_weights[factor] = (alpha * hist_norm[factor]) + ((1 - alpha) * fund_norm[factor])
        
    m_t = sum(blended_weights[f] * z_scores[f] for f in factors)
    s_t = math.tanh(m_t)
    
    adjusted_ke = base_ke + (lambda_asset * s_t * 100)

    # --- 4. The Output ---
    print("\n" + "="*50)
    print(f"SBVM OUTPUT: {country.upper()} REGIME")
    print("="*50)
    
    print("\n[1] FINAL BLENDED MACRO WEIGHTS:")
    for factor in factors:
        print(f"    - {factor:<25}: {blended_weights[factor]*100:.1f}%")
        
    print(f"\n[2] COMPOSITE SENTIMENT SCORE (St):")
    print(f"    - St = {s_t:.4f}")
    
    print(f"\n[3] DISCOUNT RATE (COST OF EQUITY):")
    print(f"    - Base Ke     : {base_ke:.2f}%")
    print(f"    - Adjustment  : {(adjusted_ke - base_ke):+.2f}%")
    print(f"    - Adjusted Ke : {adjusted_ke:.2f}%")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_dsbvf_engine()
