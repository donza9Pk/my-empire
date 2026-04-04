import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from web3 import Web3
from concurrent.futures import ThreadPoolExecutor
import time

# --- 1. SETUP ---
st.set_page_config(page_title="Donza Wolf Empire | Master Vault", layout="wide", page_icon="🐺")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-box { border: 2px solid #FFD700; border-radius: 15px; background: #111; padding: 25px; text-align: center; margin-bottom: 20px; }
    .status-text { color: #888; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; }
    .value-text { font-size: 48px; font-weight: bold; margin-top: 10px; color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# Connection: High-speed Ankr RPC with timeout fix
w3 = Web3(Web3.HTTPProvider("https://ankr.com", request_kwargs={'timeout': 60}))

# --- 2. PRICE ENGINE ---
@st.cache_data(ttl=300)
def get_live_price(token_addr):
    try:
        url = f"https://coingecko.com{token_addr.lower()}&vs_currencies=usd"
        response = requests.get(url).json()
        price = response[token_addr.lower()]['usd']
        return float(price)
    except:
        return 0.000000001

# --- 3. MASTER DATA ---
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

TOKENS = {
    "Blkwhale": "0xc0E6AD13BD58413Ed308729b688d601243E1CF77",
    "Opbnb_M": "0xCc9f1EE0eC5E2372A7ce06521B57393De0A94444",
    "Opbnb_V2": "0x77Ff107C4539698A8e60d6c280231BEfC58E4444",
    "BSB": "0x595dEaad1eB5476Ff1E649fDb7EFC36F1E4679cc",
    "Gua": "0xA5C8e1513B6A08334b479fe4D71F1253259469BE",
    "Cake": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    "Posi": "0x5CA42204cDaa70d5c773946e69dE942b85CA6706",
    "WBTC_V1": "0xef8C9335C25AF537496ca56f8a2DdF2Dea4f7777",
    "BNB_Peg": "0x3413129301cB13Ea9449F6cf295e3Da6ADe84444",
    "Marco": "0x963556de0eb8138E97A85F0A86eE0acD159D210b",
    "WBTC_V2": "0xA01b9cAFE2230093fbf0000B43701E03717F77cE",
    "WBTC_V3": "0x040f46776aE3800fA92cCb0260f18c69D882674B",
    "Cake_LP": "0x0eD7e52944161450477ee417DE9Cd3a859b14fD0",
    "Eyed": "0xeDd9f422bC4D8E55c93a4E2fE64615f8dAb27223",
    "CPL-WBTC": "0xf5115d0271b97CcFEc86793B3770A69F3494BBf9",
    "Stable": "0x011EBe7d75E2C9D1E0bD0be0bEf5C36f0A90075F",
    "BabyDoge_Eth": "0xAC57De9C1A09FeC648E93EB98875B212DB0d460B",
    "Clutch": "0x9F49bEebdF23b4b050defB2e3B1562a5fFc45EF6",
    "MM72": "0xdF9e1A85dB4f985D5BB5644aD07d9D7EE5673B5E",
    "MetaDoge_BNB": "0x8530b66ca3DDf50E0447eae8aD7eA7d5e62762eD",
    "MetaDoge_V2": "0xf3B185ab60128E4C08008Fd90C3F1F01f4B78d50",
    "WTon": "0xB1deEe21b08E23E88A91A18fC0F20E31aeD6fD8c",
    "Ton_Coin": "0x5926955a02a43235Be1711941D12488F1b7a7777",
    "BTC_BSC": "0x291BE4B6eA733148ad1D2489dd59dA28F92b710E",
    "Matics_9800": "0xC51384362Eb7b968500bB3D005158bd42d53aB1D"
}

ABI = [{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]

# --- 4. DEEP SCANNER ENGINE (WITH RETRY LOGIC) ---
def scan_wallet_token(args):
    w_name, w_addr, t_name, t_addr = args
    for attempt in range(3): # TRY 3 TIMES
        try:
            w_chk = w3.to_checksum_address(w_addr)
            c = w3.eth.contract(address=w3.to_checksum_address(t_addr), abi=ABI)
            raw = c.functions.balanceOf(w_chk).call()
            if raw > 0:
                dec = c.functions.decimals().call()
                qty = raw / (10**dec)
                price = get_live_price(t_addr)
                return {"Vault": w_name, "Asset": t_name, "Qty": qty, "Value": qty * price}
            return None
        except Exception as e:
            if attempt == 2: return None # Give up after 3 attempts
            time.sleep(1) # Wait 1 second before retry

# --- 5. INTERFACE ---
st.title("🐺 The Donza Wolf Empire v5.2")
st.sidebar.header("Empire Force Scanner")
shadow_mode = st.sidebar.toggle("Shadow King Mode", value=False)

if st.sidebar.button("⚡ FORCE RE-SCAN ALL VAULTS"):
    st.cache_data.clear()
    st.rerun()

scan_tasks = [(w_n, w_a, t_n, t_a) for w_n, w_a in WALLETS.items() for t_n, t_a in TOKENS.items()]

with st.status("🐺 Wolf is Deep Scanning 270 combinations...", expanded=False) as status:
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(scan_wallet_token, scan_tasks))
    data_rows = [r for r in results if r is not None]
    status.update(label="Deep Sync Complete!", state="complete")

total_wealth = sum(row['Value'] for row in data_rows)
display_val = "PROTECTED 🛡️" if shadow_mode else f"${total_wealth:,.2f}"

st.markdown(f"""
    <div class="main-box">
        <p class="status-text">TOTAL EMPIRE NET WORTH (9 VAULTS)</p>
        <div class="value-text">{display_val}</div>
    </div>
""", unsafe_allow_html=True)

if not shadow_mode and data_rows:
    df = pd.DataFrame(data_rows)
    st.plotly_chart(go.Figure(data=[go.Pie(labels=df['Asset'], values=df['Value'], hole=.4)]))
    st.dataframe(df.style.format({"Qty": "{:,.4f}", "Value": "${:,.2f}"}))
