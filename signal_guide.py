# signal_guide.py
SIGNAL_GUIDE_TEXT = """
# 📘 Market Risk Signal Guide

Below is a summary of each indicator used in this dashboard and what it implies about market risk.

---

## 🟦 Volatility Indicators
### **VIX (S&P 500 Volatility Index)**
- Measures expected near-term volatility in large-cap U.S. equities.
- **High VIX (>20)** → Fear, uncertainty, possible correction.
- **Low VIX (<13)** → Complacency; often precedes volatility spikes.

### **VIX3M (3-month volatility) & VIX6M (6-month volatility)**
- Longer-term volatility expectations.
- When **VIX3M > VIX** = elevated forward-looking risk.

### **VXN (Nasdaq Volatility Index)**
- Tech-sector volatility.
- Large spike → Tech-led risk-off (important since crypto often correlates with tech).

### **SKEW Index**
- Measures tail-risk: probability of extreme downside.
- **High SKEW (>140)** → Institutions hedging against crash risk.

---

## 🟩 Credit Market Indicators
### **HYG (High-Yield Corporate Bond ETF)**
- Tracks junk bonds.
- Sharp declines indicate rising credit stress.

### **JNK (Alternate High-Yield ETF)**
- Confirms HYG signals.

### **LQD (Investment-Grade Corporate Bond ETF)**
- Safer bonds; when LQD rises while HYG falls → risk-off.

### **HYG/LQD Ratio**
- **Falling ratio** → big warning of credit tightening and risk aversion.

---

## 🟧 Treasury Yield Indicators
### **TNX (10-year Treasury Yield)**
- Global macro benchmark.
- Rising yield → liquidity tightening / inflation risk.
- Sharp drops → flight-to-safety (recession concern).

### **FVX (5-year yield)**  
### **TYX (30-year yield)**  
- Yield curve shape = economic cycle signal.

---

## 🟨 Liquidity Indicators
### **UUP (U.S. Dollar Index ETF)**
- Rising dollar = global liquidity tightening → bearish risk assets.

### **SHY / IEI**
- Treasury ETF demand proxies safe-haven flows.

---

## 🟥 Global Risk Indicators
### **EEM (Emerging Markets ETF)**
- Sensitive to global funding conditions.
- Falling EM = risk-off in global markets.

---

## 🟪 Composite Stress Score (MSS)
- Weighted combination of volatility, credit, liquidity, yields, and EM signals.
- **< 40** → Calm  
- **40–55** → Normal  
- **55–70** → Risk-off  
- **> 70** → **Severe Stress (crash risk)**  

---

## 🧭 Interpretation Framework
- **Volatility rises first** → market nervousness  
- **Credit stress rises second** → structural market weakness  
- **Yields and USD add macro context**  
- **EM and liquidity confirm global contagion**  
- **MSS summarizes all into one score**

This panel helps you understand **why the risk score moves** and which category contributes most.
"""
