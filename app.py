# ============================================================
# 🐺 THE DONZA WOLF EMPIRE: TURBO COMMAND CENTER v4.5
# Built for: Zia Ahmed (Donza King) 👑
# Features: Real-time Price Tracking | BSC 0x38 | Multi-Wallet
# ============================================================

import streamlit as st
import requests
import pandas as pd
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
        background: linear-gradient(145deg, #111, #050505);
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
    }
    .net-worth { font-size: 26px; font-weight: bold; color: #00ff00; }
    .token-price { color: #FFD700; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API CONFIG ---
MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRiOGQ2MTA3LWVhMzgtNDYwNi05NjMzLWRiMzJjZGVjNTY3ZCIsIm9yZ0lkIjoiNjExOTAiLCJ1c2VySWQiOiI2MDgzOCIsInR5cGVJZCI6ImU3Nzc4Njg5LTk5OWQtNGExYS1iNDNmLTA3MjMxZjY0OWI0NCIsInR5cGUiOiJQUk9KRUNUIiwiaWF0IjoxNzIyMjIzMjAxLCJleHAiOjQ4Nzc5ODMyMDF9.W8zYot0-qm-bx5TCzjn55iFgdkAYPNdeeOamC-8UXt4"
CHAIN_ID = "0x38"  # BSC

# --- 3. WALLETS ---
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

# --- 4. REAL-TIME PRICE ENGINE ---
def get_token_price(token_address):
    """Token ki live USD price Moralis se leti hai"""
    try:
        url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address}/price?chain={CHAIN_ID}"
        headers = {"accept": "application/json", "X-API-Key": MORALIS_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return float(response.json().get('usdPrice', 0))
    except:
        pass
    return 0.0

def scan_wallet_turbo(name, address):
    try:
        # Get Balances
        bal_url = f"https://moralis.io{address}/erc20?chain={CHAIN_ID}"
        headers = {"accept": "application/json", "X-API-Key": MORALIS_API_KEY}
        res = requests.get(bal_url, headers=headers, timeout=15)
        
        tokens = res.json() if res.status_code == 200 else []
        wallet_assets = []
        wallet_total = 0.0

        for t in tokens:
            qty = float(t.get('balance', 0)) / (10**int(t.get('decimals', 18)))
            if qty > 0.00001:  # Filter out very small dust
                # Live Price Fetching
                price = get_token_price(t['token_address'])
                value = qty * price
                wallet_total += value
                
                wallet_assets.append({
                    "Symbol": t.get('symbol'),
                    "Balance": round(qty, 4),
                    "Price": f"${price:,.4f}",
                    "Value (USD)": f"${value:,.2f}"
                })
        
        return {"name": name, "address": address, "assets": wallet_assets, "total": wallet_total}
    except Exception as e:
        return {"name": name, "address": address, "assets": [], "total": 0.0, "error": str(e)}

# --- 5. UI ---
st.title("🐺 THE DONZA WOLF EMPIRE v4.5")
st.subheader("🌐 Turbo Price-Sync Engine Active")

if st.button("🚀 START GLOBAL EMPIRE SCAN"):
    with st.spinner("Syncing with BNB Smart Chain & Fetching Live Prices..."):
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda x: scan_wallet_turbo(x[0], x[1]), WALLETS.items()))
        
        grand_total = sum(r['total'] for r in results)
        st.metric("TOTAL EMPIRE NET WORTH", f"${grand_total:,.2f}")
        
        cols = st.columns(3)
        for i, res in enumerate(results):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="wallet-box">
                    <h3 style="color:#FFD700;">{res['name']}</h3>
                    <p style="font-size:10px; color:#666;">{res['address']}</p>
                    <div class="net-worth">${res['total']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                if res['assets']:
                    with st.expander("Show Live Assets"):
                        st.table(res['assets'])

st.sidebar.success("Prices Updated Real-time via Moralis")
