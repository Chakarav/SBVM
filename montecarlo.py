import numpy as np

ebitda_y1 = 223737.71
tax_rate = 0.1316
wc_rate = 0.1421
g2 = 0.04
net_debt = 117102.00
shares = 1353.2

g1_sim = np.random.normal(0.10, 0.02, 10000)
capex_sim = np.random.normal(0.6509, 0.05, 10000)
wacc_sim = np.random.normal(0.0959, 0.005, 10000)

# --- 3. Cash Flow Calculations  ---
fcf1 = ebitda_y1 * (1 - tax_rate - capex_sim + wc_rate)
fcf2 = fcf1 * (1 + g1_sim)
fcf3 = fcf2 * (1 + g1_sim)
fcf4 = fcf3 * (1 + g1_sim)

# --- 4. Terminal Value ---
tv = (fcf4 * (1 + g2)) / (wacc_sim - g2)

# --- 5. Present Value Discounting ---
pv_fcf1 = fcf1 / (1 + wacc_sim)**1
pv_fcf2 = fcf2 / (1 + wacc_sim)**2
pv_fcf3 = fcf3 / (1 + wacc_sim)**3
pv_fcf4 = fcf4 / (1 + wacc_sim)**4
pv_tv = tv / (1 + wacc_sim)**4

# --- 6. Enterprise Value to Equity Value ---
ev = pv_fcf1 + pv_fcf2 + pv_fcf3 + pv_fcf4 + pv_tv
equity_value = ev - net_debt
intrinsic_value = equity_value / shares

print(f"5th Percentile (Worst Case): {np.percentile(intrinsic_value, 5):.2f}")
print(f"Median Intrinsic Value: {np.median(intrinsic_value):.2f}")
print(f"95th Percentile (Best Case): {np.percentile(intrinsic_value, 95):.2f}")
print(f"Probability overvalued: {np.mean(intrinsic_value < 1441.30) * 100:.2f}%")
