import streamlit as st
import requests

# 9 Master Wallets
wallets = {
    "Trust Wallet": "0x0eC7f1D93d2A39f695587cA1123482FC3e867e45",
    "Wallet 2": "0x70175abF9aCCa0FC10D3057eD876e87a464a1cC6",
    "OKX Wallet": "0x87cA7A6f57435b104BfA28B00596b4da6a64C2E7",
    "Wallet 4": "0xbB35180acA3eD3EA2028928Eb0BEa0EbD3D5c855",
    "Decent Wallet": "0x55e650Bded1C1b8Bd09Caea4251140A7922366Db",
    "Edge Wallet": "0xCC1EcF9aeB17b0d504DBD85Ea22436C25eebb6ed",
    "Crypto.com": "0x8F46Bc8aBE13739d56Ac1ff4BC2d7d0F057f6139",
    "MetaMask": "0xF60c9A7dAc0051664e82012f5F65ce9dbdc8Dc5E",
    "Binance Wallet": "0x43caebCa05728261D818EDE9a842ecec5Ab46047"
}

st.set_page_config(page_title="9-Wallet Empire", layout="wide")
st.title("📊 Almi Satah Live Portfolio")

# Price Feed
def get_bnb_price():
    try:
        r = requests.get("https://binance.com")
        return float(r.json()['price'])
    except: return 600.0

price = get_bnb_price()
st.metric("Current BNB Price", f"${price:,.2f}")
st.info("System Online: Dashboard is Live! 🚀")
