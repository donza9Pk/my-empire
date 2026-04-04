# ============================================================
# 🐺 THE DONZA WOLF EMPIRE: TURBO COMMAND CENTER v4.5 (MASTER)
# Features: Auto-Refresh (5m) | 24h P/L | Live Price | BSC 0x38
# Built for: Zia Ahmed (Donza King) 👑
# ============================================================

import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- 1. CONFIG & EMPIRE THEME ---
st.set_page_config(page_title="Donza Wolf v4.5 | Turbo", layout="wide", page_icon="🐺")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .wallet-box {
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        background: linear-gradient(145deg, #111, #080808);
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
    }
    .net-worth { font-size: 28px; font-weight: bold; color: #00ff00; margin-top: 5px; }
    .refresh-text { color: #888; font-size: 12px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API & NETWORK CONFIG ---
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRiOGQ2MTA3LWVhMzgtNDYwNi05NjMzLWRiMzJjZGVjNTY3ZCIsIm9yZ0lkIjoiNjExOTAiLCJ1c2VySWQiOiI2MDgzOCIsInR5cGVJZCI6ImU3Nzc4Njg5LTk5OWQtNGExYS1iNDNmLTA3MjMxZjY0OWI0NCIsInR5cGUiOiJQUk9KRUNUIiwiaWF0IjoxNzIyMjIzMjAxLCJleHAiOjQ4Nzc5ODMyMDF9.W8zYot0-qm-bx5TCzjn55iFgdkAYPNdeeOamC-8UXt4"
CHAIN_ID = "0x38"  # BNB Smart Chain

WALLETS = {
    "Alpha Vault": "0x0eC7f1D93d2A39f695587cA1123482FC3e867e45",
    "Shadow Reserve": "0x70175abF9aCCa0FC10D3057eD876e87a464a1cC6",
    "OKX Fortress": "0x87cA7A6f57435b104BfA28B00596b4da6a64C2E7",
    "Wolf-04": "0xbB35180acA3eD3EA2028928Eb0BEa0EbD3D5c855",
    "Decent-05": "0x55e650Bded1C1b8Bd09Caea4251140A7922366Db",
    "Edge-06": "0xCC1EcF9aeB17b0d504DBD85Ea22436C25eebb6ed",
    "Crypto-Elite": "0x8F46Bc8aBE13739d56Ac1ff4BC2d7d0F057f6139",
    "Meta-Prime": "0xF60c9A7dAc0051664e82012f5F65ce9dbdc8Dc5E",
    "Binance-Admin": "0x43caebCa05728261D818EDE9a842ecec5Ab46047"
}

# --- 3. AUTO-REFRESH LOGIC (ST-STATEDE) ---
refresh_rate = st.sidebar.slider("Auto-Refresh Speed (Seconds)", 60, 600, 300)
# Yeh line automatically page ko refresh karti hai
st.empty() 

# --- 4. DATA ENGINES ---
def get_live_data(token_address):
    try:
        url = f"https://moralis.io{token_address}/price?chain={CHAIN_ID}"
        headers = {"accept": "application/json", "X-API-Key": MORALIS_API_KEY}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return float(data.get('usdPrice', 0)), float(data.get('24h_percent_change', 0))
    except: pass
    return 0.0, 0.0

def scan_wallet_turbo(name, address):
    try:
        bal_url = f"https://moralis.io{address}/erc20?chain={CHAIN_ID}"
        headers = {"accept": "application/json", "X-API-Key": MORALIS_API_KEY}
        res = requests.get(bal_url, headers=headers, timeout=15)
        tokens = res.json() if res.status_code == 200 else []
        
        wallet_assets = []
        total_usd = 0.0
        total_pnl = 0.0

        for t in tokens:
            qty = float(t.get('balance', 0)) / (10**int(t.get('decimals', 18)))
            if qty > 0.001:
                price, change = get_live_data(t['token_address'])
                value = qty * price
                total_usd += value
                pnl = (value * change / 100) if change else 0.0
                total_pnl += pnl
                
                wallet_assets.append({
                    "Symbol": t.get('symbol'),
                    "Qty": f"{qty:,.2f}",
                    "Price": f"${price:,.4f}",
                    "Value": f"${value:,.2f}",
                    "24h%": f"{change:+.2f}%"
                })
        return {"name": name, "address": address, "assets": wallet_assets, "total": total_usd, "pnl": total_pnl}
    except: return {"name": name, "address": address, "assets": [], "total": 0.0, "pnl": 0.0}

# --- 5. UI DISPLAY ---
st.title("🐺 THE DONZA WOLF EMPIRE v4.5")
st.markdown(f"<p class='refresh-text'>Auto-Sync Active: Refreshing every {refresh_rate}s | Last Sync: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# Main Scan Execution
with st.spinner("🔄 Syncing Empire Vaults via Moralis Turbo Engine..."):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda x: scan_wallet_turbo(x, x), WALLETS.items()))

# Summary Row
grand_total = sum(r['total'] for r in results)
grand_pnl = sum(r['pnl'] for r in results)

c1, c2 = st.columns(2)
c1.metric("TOTAL NET WORTH", f"${grand_total:,.2f}")
c2.metric("EMPIRE 24h P/L", f"${grand_pnl:,.2f}", delta=f"{grand_pnl:,.2f}")

st.divider()

# 9-GRID VAULTS
cols = st.columns(3)
for i, res in enumerate(results):
    with cols[i % 3]:
        pnl_color = "#00ff00" if res['pnl'] >= 0 else "#ff4b4b"
        st.markdown(f"""
        <div class="wallet-box">
            <h3 style="color:#FFD700; margin-bottom:0;">{res['name']}</h3>
            <code style="font-size:9px; color:#555;">{res['address']}</code>
            <div class="net-worth">${res['total']:,.2f}</div>
            <div style="color:{pnl_color}; font-size:13px; margin-top:5px;">
                24h: {'+' if res['pnl'] >= 0 else ''}{res['pnl']:,.2f} USD
            </div>
        </div>
        """, unsafe_allow_html=True)
        if res['assets']:
            with st.expander("Inventory Details"):
                st.table(res['assets'])

# --- 6. AUTO-REFRESH SCRIPT ---
# This part triggers the browser to reload
time.sleep(refresh_rate)
st.rerun()
