import streamlit as st
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# --- 1. CONFIG ---
st.set_page_config(page_title="Donza Wolf v5.6 | Zero Filter", layout="wide")

# Replace with your actual Moralis API Key
MORALIS_API_KEY = "YOUR_API_KEY_HERE" 
CHAIN_ID = "0x38" # BSC Mainnet

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

def scan_wallet_no_filter(name, address):
    headers = {"X-API-Key": MORALIS_API_KEY, "accept": "application/json"}
    data = {"name": name, "address": address, "assets": [], "total_usd": 0.0, "history": [], "error": None}
    
    try:
        # A. GET TOKENS - Using Correct API Gateway
        bal_url = f"https://moralis.io{address}/tokens?chain={CHAIN_ID}"
        response = requests.get(bal_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            data['error'] = f"API Error {response.status_code}: {response.text[:100]}"
            return data

        bal_res = response.json()
        tokens = bal_res.get('result', [])
        
        for t in tokens:
            qty = float(t.get('balance_formatted') or 0)
            usd_val = float(t.get('usd_value') or 0)
            
            if qty > 0:
                data['total_usd'] += usd_val
                data['assets'].append({
                    "Token": t.get('symbol', 'UNK'),
                    "Qty": f"{qty:,.4f}",
                    "Value": f"${usd_val:,.2f}"
                })

        # B. GET TRANSACTION HISTORY
        hist_url = f"https://moralis.io{address}?chain={CHAIN_ID}&limit=5"
        hist_res = requests.get(hist_url, headers=headers, timeout=15).json()
        
        for tx in hist_res.get('result', []):
            data['history'].append({
                "Date": tx['block_timestamp'][:16].replace('T', ' '),
                "Value": f"{float(tx['value'])/10**18:.4f} BNB",
                "To": f"{tx['to_address'][:10]}..."
            })
            
        return data
    except Exception as e:
        data['error'] = str(e)
        return data

# --- UI ---
st.title("🐺 THE DONZA WOLF v5.6")

if st.button("🚀 DEEP SCAN (NO FILTER)"):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda x: scan_wallet_no_filter(x, WALLETS[x]), WALLETS.keys()))
    
    grand_total = sum(r['total_usd'] for r in results)
    st.metric("TOTAL EMPIRE NET WORTH", f"${grand_total:,.2f}")
    
    # Track errors for the debug console
    errors_found = []

    for res in results:
        if res['error']:
            errors_found.append(f"**{res['name']}**: {res['error']}")
            
        with st.expander(f"📊 {res['name']} - Total: ${res['total_usd']:,.2f}"):
            if res['assets']: 
                st.table(res['assets'])
            else: 
                st.warning("No tokens found (or API limit reached).")
            
            st.write("**Last 5 Transactions:**")
            if res['history']: 
                st.table(res['history'])
            else: 
                st.info("No recent history found.")

    # --- DEBUG CONSOLE ---
    if errors_found:
        st.divider()
        st.error("### 🛠 DEBUG CONSOLE (Errors Detected)")
        for err in errors_found:
            st.write(err)
