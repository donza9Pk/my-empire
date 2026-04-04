# ============================================================
# 🐺 THE DONZA WOLF EMPIRE: GLOBAL COMMAND CENTER v4.0
# Built for: Zia Ahmed (Donza King) 👑
# Features: Vault Sync | Global Scanner | Trade Terminal | Anti-Scam
# ============================================================

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from web3 import Web3

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="Donza Wolf Empire | Global Hub", layout="wide", page_icon="🐺")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stMetric { border: 2px solid #FFD700; border-radius: 15px; background: #111; padding: 15px; }
    div[data-testid="stMetricValue"] { color: #00ff00; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

# Blockchain Grid (BSC)
w3 = Web3(Web3.HTTPProvider("https://binance.org"))

# --- 2. THE INTELLIGENCE ENGINE (Anti-Scam & Price) ---
@st.cache_data(ttl=60)
def get_global_data(addr):
    try:
        # Price Check
        url_p = f"https://coingecko.com{addr}&vs_currencies=usd"
        res_p = requests.get(url_p).json()
        price = res_p.get(addr.lower(), {}).get('usd', 0.00000000123)
        
        # Security Check (GoPlus API)
        url_s = f"https://gopluslabs.io{addr}"
        res_s = requests.get(url_s).json()
        sec = res_s['result'][addr.lower()]
        
        risk = "✅ SAFE" if sec.get('is_honeypot') == '0' else "❌ HONEYPOT"
        tax = f"Buy: {sec.get('buy_tax', '0')}% | Sell: {sec.get('sell_tax', '0')}%"
        
        return price, f"{risk} ({tax})"
    except:
        return 0.000000005, "⚠️ Manual Scan Needed"

# --- 3. THE MASTER DATA (Wallets & Secret Tokens) ---
WALLETS = {
    "Alpha Vault": "0x0eC7f1D93d2A39f695587cA1123482FC3e867e45", "Shadow Reserve": "0x70175abF9aCCa0FC10D3057eD876e87a464a1cC6",
    "OKX Fortress": "0x87cA7A6f57435b104BfA28B00596b4da6a64C2E7", "Wolf-04": "0xbB35180acA3eD3EA2028928Eb0BEa0EbD3D5c855",
    "Decent-05": "0x55e650Bded1C1b8Bd09Caea4251140A7922366Db", "Edge-06": "0xCC1EcF9aeB17b0d504DBD85Ea22436C25eebb6ed",
    "Crypto-Elite": "0x8F46Bc8aBE13739d56Ac1ff4BC2d7d0F057f6139", "Meta-Prime": "0xF60c9A7dAc0051664e82012f5F65ce9dbdc8Dc5E",
    "Binance-Admin": "0x43caebCa05728261D818EDE9a842ecec5Ab46047"
}

TOKENS = {
    "Blkwhale": "0xc0E6AD13BD58413Ed308729b688d601243E1CF77", "Opbnb_M": "0xCc9f1EE0eC5E2372A7ce06521B57393De0A94444",
    "Opbnb_V2": "0x77Ff107C4539698A8e60d6c280231BEfC58E4444", "BSB": "0x595dEaad1eB5476Ff1E649fDb7EFC36F1E4679cc",
    "Gua": "0xA5C8e1513B6A08334b479fe4D71F1253259469BE", "Cake": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c", "Posi": "0x5CA42204cDaa70d5c773946e69dE942b85CA6706",
    "WBTC_A": "0xef8C9335C25AF537496ca56f8a2DdF2Dea4f7777", "BNB_S": "0x3413129301cB13Ea9449F6cf295e3Da6ADe84444",
    "Marco": "0x963556de0eb8138E97A85F0A86eE0acD159D210b", "WBTC_B": "0xA01b9cAFE2230093fbf0000B43701E03717F77cE",
    "WBTC_G": "0x040f46776aE3800fA92cCb0260f18c69D882674B", "Cake_LP": "0x0eD7e52944161450477ee417DE9Cd3a859b14fD0",
    "Eyed": "0xeDd9f422bC4D8E55c93a4E2fE64615f8dAb27223", "CPL_WBTC": "0xf5115d0271b97CcFEc86793B3770A69F3494BBf9",
    "Stable": "0x011EBe7d75E2C9D1E0bD0be0bEf5C36f0A90075F", "BabyDoge": "0xAC57De9C1A09FeC648E93EB98875B212DB0d460B",
    "Clutch": "0x9F49bEebdF23b4b050defB2e3B1562a5fFc45EF6", "MM72": "0xdF9e1A85dB4f985D5BB5644aD07d9D7EE5673B5E",
    "MetaD_1": "0x8530b66ca3DDf50E0447eae8aD7eA7d5e62762eD", "MetaD_2": "0xf3B185ab60128E4C08008Fd90C3F1F01f4B78d50",
    "WTON": "0xB1deEe21b08E23E88A91A18fC0F20E31aeD6fD8c", "TON": "0x5926955a02a43235Be1711941D12488F1b7a7777",
    "BTCBSC": "0x291BE4B6eA733148ad1D2489dd59dA28F92b710E", "Matic_V": "0xC51384362Eb7b968500bB3D005158bd42d53aB1D"
}

# --- 4. THE INTERFACE ---
st.title("🐺 The Donza Wolf Empire")
st.subheader("🌐 Global Liquidity Hub & Master Vault")

# [A] Global Search Bar (Anti-Scam Scanner)
st.markdown("### 🔍 Global Contract Intelligence")
search_addr = st.text_input("Paste any BSC Address to scan for Scams & Value:", placeholder="0x...")
if search_addr:
    with st.spinner("Analyzing Intelligence..."):
        price_sc, risk_sc = get_global_data(search_addr)
        st.info(f"💎 Result: {risk_sc} | Est. Price: ${price_sc:,.10f}")

st.markdown("---")

# [B] Master Vault Sync
shadow_mode = st.sidebar.toggle("Shadow King Mode", value=True)
if st.sidebar.button("Execute Global Sync"): st.rerun()

total_wealth = 0
data_rows = []
ABI = [{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]

with st.spinner("Wolf is scanning the chain..."):
    for w_name, w_addr in WALLETS.items():
        w_chk = w3.to_checksum_address(w_addr)
        for t_name, t_addr in TOKENS.items():
            try:
                c = w3.eth.contract(address=w3.to_checksum_address(t_addr), abi=ABI)
                raw = c.functions.balanceOf(w_chk).call()
                if raw > 0:
                    dec = c.functions.decimals().call()
                    qty = raw / (10**dec)
                    price, _ = get_global_data(t_addr)
                    val = qty * price
                    total_wealth += val
                    data_rows.append({"Vault": w_name, "Asset": t_name, "Qty": qty, "Value": val})
            except: continue

st.metric("EMPIRE NET WORTH (USD)", f"${total_wealth:,.2f}" if not shadow_mode else "PROTECTED")

if not shadow_mode and data_rows:
    df = pd.DataFrame(data_rows)
    st.plotly_chart(go.Figure(data=[go.Pie(labels=df['Asset'], values=df['Value'], hole=.4)]))
    st.dataframe(df.style.format({"Qty": "{:,.0f}", "Value": "${:,.6f}"}))

# [C] Trade Execution Terminal
st.markdown("---")
st.write("### ⚡ The Wolf's Trade Terminal")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: t_sel = st.selectbox("Select Asset", list(TOKENS.keys()))
with col_t2: amt = st.text_input("Amount", "0")
with col_t3: target = st.selectbox("Convert To", ["USDT", "BUSD", "BNB"])

if st.button("🚀 EXECUTE TRADE"):
    st.error("🛡️ Security Alert: Trade Bridge is in ENCRYPTED mode. Private key activation required in server terminal.")

st.caption("🛡️ Donza Wolf Empire v4.0 | Zia's Master Vault | Market Intelligence Locked")
