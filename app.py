# ============================================================
# 🐺 THE DONZA WOLF EMPIRE: ULTIMATE COMMAND CENTER v5.5
# Combined APIs: Wallet + ERC20 + Price + History (Moralis)
# Network: BSC (0x38) | Built for: Zia Ahmed (Donza King) 👑
# ============================================================

import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Donza Wolf v5.5 | History", layout="wide", page_icon="🐺")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .wallet-box {
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        background: linear-gradient(145deg, #151515, #050505);
        margin-bottom: 20px;
        box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.2);
    }
    .net-worth { font-size: 28px; font-weight: bold; color: #00ff00; }
    .history-text { color: #888; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API CONFIG ---
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRiOGQ2MTA3LWVhMzgtNDYwNi05NjMzLWRiMzJjZGVjNTY3ZCIsIm9yZ0lkIjoiNjExOTAiLCJ1c2VySWQiOiI2MDgzOCIsInR5cGVJZCI6ImU3Nzc4Njg5LTk5OWQtNGExYS1iNDNmLTA3MjMxZjY0OWI0NCIsInR5cGUiOiJQUk9KRUNUIiwiaWF0IjoxNzIyMjIzMjAxLCJleHAiOjQ4Nzc5ODMyMDF9.W8zYot0-qm-bx5TCzjn55iFgdkAYPNdeeOamC-8UXt4"
CHAIN_ID = "0x38" 

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

# --- 3. THE MASTER DATA ENGINE ---
def scan_wallet_ultimate(name, address):
    headers = {"X-API-Key": MORALIS_API_KEY, "accept": "application/json"}
    data = {"name": name, "address": address, "assets": [], "total_usd": 0.0, "history": []}
    
    try:
        # A. GET BALANCES (Native + ERC20)
        bal_url = f"https://moralis.io{address}/tokens?chain={CHAIN_ID}&exclude_spam=true"
        bal_res = requests.get(bal_url, headers=headers, timeout=12).json()
        
        tokens = bal_res.get('result', [])
        for t in tokens:
            val = float(t.get('usd_value') or 0)
            data['total_usd'] += val
            if val > 0.1:
                data['assets'].append({
                    "Token": t.get('symbol'),
                    "Qty": round(float(t.get('balance_formatted', 0)), 2),
                    "Value": f"${val:,.2f}"
                })

        # B. GET TRANSACTION HISTORY (Last 5 TXs)
        hist_url = f"https://moralis.io{address}/history?chain={CHAIN_ID}&order=DESC&limit=5"
        hist_res = requests.get(hist_url, headers=headers, timeout=12).json()
        
        for tx in hist_res.get('result', []):
            tx_date = datetime.fromisoformat(tx['block_timestamp'].replace('Z', '')).strftime('%d-%m %H:%M')
            status = "✅ Confirmed" if tx['confirmed'] else "⏳ Pending"
            data['history'].append({
                "Date": tx_date,
                "Value (BNB)": f"{float(tx['value'])/10**18:.4f}",
                "Status": status
            })

        return data
    except:
        return data

# --- 4. UI DISPLAY ---
st.title("🐺 THE DONZA WOLF EMPIRE v5.5")
st.sidebar.info(f"🔄 Auto-Refresh Active | Network: BSC")
refresh_rate = st.sidebar.slider("Refresh Speed", 60, 600, 300)

if st.button("🚀 EXECUTE GLOBAL DEEP SCAN"):
    with st.spinner("Analyzing Blockchain History & Inventory..."):
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda x: scan_wallet_ultimate(x, WALLETS[x]), WALLETS.keys()))
        
        grand_total = sum(r['total_usd'] for r in results)
        st.metric("EMPIRE NET WORTH (USD)", f"${grand_total:,.2f}")
        
        cols = st.columns(3)
        for i, res in enumerate(results):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="wallet-box">
                    <h3 style="color:#FFD700; margin-bottom:0;">{res['name']}</h3>
                    <code style="font-size:9px; color:#555;">{res['address'][:18]}...</code>
                    <div class="net-worth">${res['total_usd']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Inventory & History"):
                    st.write("**Recent Assets:**")
                    st.table(res['assets']) if res['assets'] else st.write("No major tokens.")
                    
                    st.write("**Last 5 Transactions:**")
                    st.table(res['history']) if res['history'] else st.write("No recent TXs.")

# --- 5. REFRESH ---
time.sleep(refresh_rate)
st.rerun()
