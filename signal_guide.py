SIGNAL_GUIDE_TEXT = """
# 🧭 Market Risk Signal Guide
Below is a unified reference for every indicator used in this dashboard.  
Formatting, clarity, and navigation have been improved **without changing your original sequence**.

---

# 🔗 Quick Navigation
- [Market Risk Signals](#🧭-market-risk-signal-guide)
- [FRED Macro Indicators](#🧭--fred-macro-indicator-guide)
- [Recession Risk Model](#🧭-recession-risk-model--explanation-guide)
- [Volatility Indicators](#🧭-volatility-indicators)
- [Credit Market Indicators](#🧭-credit-market-indicators)
- [Treasury Yield Indicators](#🧭-treasury-yield-indicators)
- [Liquidity Indicators](#🧭-liquidity-indicators)
- [Global Risk Indicators](#🧭-global-risk-indicators)
- [Composite Stress Score](#🧭-composite-stress-score-mss)
- [Interpretation Framework](#🧭-interpretation-framework)

---

# 🧭  FRED Macro Indicator Guide
Macro indicators retrieved from FRED. These form the deeper economic backdrop behind all market signals.

---

## 🟦 High Yield Spread — HY_OAS (BAMLH0A0HYM2)
Measures the extra yield junk bonds pay over Treasuries.

**Why it matters**
- Early warning indicator of credit stress  
- Spikes ahead of recessions and equity drawdowns  

**Interpretation**
- **> 5%** → rising stress  
- **3–5%** → normal  
- **< 3%** → easy credit conditions  

---

## 🟩 NFCI — National Financial Conditions Index
A broad liquidity and financial conditions index covering:
- credit spreads  
- volatility  
- funding stress  
- leverage  
- money markets  

**Interpretation**
- **> 0** → tighter-than-average → stress  
- **< 0** → easier-than-average → supportive liquidity  

---

## 🟨 TOTALSL — Total Consumer Credit Outstanding
Total borrowing by consumers (credit cards, auto loans, personal loans).

**Interpretation**
- **Rising** → demand supported  
- **Flat** → early weakness  
- **Declining** → recessionary behavior  

---

## 🟥 Treasury Yields — DGS2, DGS10, DGS30
Key interest rates across maturities.

### **DGS2 (2-year)**
Tracks Federal Reserve expectations.

### **DGS10 (10-year)**
Reflects long-run growth & inflation expectations.

### **DGS30 (30-year)**
Shows structural inflation expectations and long-term funding costs.

**Interpretation**
- Falling → recession fear  
- Rising → tighter liquidity / inflation  
- Flattening → late-cycle  
- Inversion → recession signal  

---

## 🧩 How These Indicators Fit Together
- **HY_OAS** → fast credit stress  
- **NFCI** → systemic liquidity conditions  
- **TOTALSL** → consumer demand strength  
- **Treasury yields** → macro regime & cycle turning points  

Together, they describe the true macroeconomic environment behind markets.

---

# 🧭 Using the Z-Score Panel
Z-scores standardize indicators with different units onto a comparable scale.

- **Z > +1** → stressed  
- **Z < −1** → very easy conditions  
- **Z ≈ 0** → normal  

This shows which macro components are creating risk.

---

# 🧭 Recession Risk Model — Explanation Guide
Model estimating recession probability for 2026–27.

---

## 1️⃣ Yield Curve (10Y – 3M Spread)
The strongest recession predictor.

- **Deep inversion** → recession likely in 6–18 months  

---

## 2️⃣ High-Yield Spread (HY OAS)
Credit deterioration usually precedes recessions.

---

## 3️⃣ Unemployment 12-Month Change (Δ UNRATE)
Recessions begin when unemployment **starts rising**, not when it is high.

---

## 4️⃣ CAPE (Shiller Cyclically Adjusted P/E)
Valuation risk: high CAPE = fragile markets.

---

## 5️⃣ Structural Fragility (constant = 1)
Represents persistent systemic risks:
- mega-cap concentration  
- leverage  
- liquidity plumbing weaknesses  

---

## 6️⃣ Retiree Wealth Vulnerability (constant = 1)
Based on BCA Research:
> Excess retirees depend heavily on portfolio wealth to sustain spending.

This increases recession sensitivity when markets fall.

---

## 7️⃣ Model Logic (Simplified)
All components → z-scores → weighted sum → logistic function:

Probability = 1 / (1 + exp(-X))

The logistic function converts the weighted macro signals into a clean probability between 0 and 1.

---

# 🧭 Volatility Indicators

### **VIX**
Near-term equity volatility.  
- High: risk-off  
- Low: complacency  

### **VIX3M / VIX6M**
Forward volatility expectations.

### **VXN**
Tech-sector volatility (important for crypto correlations).

### **SKEW**
Tail-risk hedging index.  
- High: crash probability priced in  

---

# 🧭 Credit Market Indicators

### **HYG**
Junk bond ETF → credit stress signal.

### **JNK**
Confirmation signal for HYG.

### **LQD**
Investment-grade credit (safe corporate debt).

### **HYG/LQD Ratio**
One of the strongest real-time risk indicators:
- Falling → strong risk-off signal  

---

# 🧭 Treasury Yield Indicators

### **TNX (10-year)**  
Macro benchmark.  
- Rising → tightening  
- Falling → recession concern  

### **FVX (5-year)**  
Medium-term expectations.

### **TYX (30-year)**  
Long-term inflation regime & fiscal confidence.

---

# 🧭 Liquidity Indicators

### **UUP**
Rising USD → tighter global liquidity → risk-off.

### **SHY / IEI**
Short-term Treasury demand → safe-haven flow.

---

# 🧭 Global Risk Indicators

### **EEM**
Emerging markets ETF → sensitive to global funding stress.  

---

# 🧭 Composite Stress Score (MSS)

- **< 40** → Calm  
- **40–55** → Normal  
- **55–70** → Risk-off  
- **> 70** → Severe stress / crash risk  

Weighted mix of:
- volatility  
- credit  
- liquidity  
- yields  
- global risk  

---

# 🧭 Interpretation Framework
A full-cycle view of how risk propagates:

1. **Volatility rises first**  
2. **Credit spreads widen**  
3. **Yields & USD confirm tightening**  
4. **Liquidity & EM turn risk-off**  
5. **Macro indicators weaken**  
6. **Recession probability rises**  
7. **Composite Stress Score spikes**  

This flow helps detect regime shifts before they appear in prices.

---
"""
