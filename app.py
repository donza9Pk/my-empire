import streamlit as st
import requests
import pandas as pd
import io
from concurrent.futures import ThreadPoolExecutor

# --- 1. CONFIG ---
st.set_page_config(page_title="Donza Wolf v6.5 | Excel Pro", layout="wide")

# Aapki BscScan API Key
BSCSCAN_API_KEY = "M8E2GB3MSH62QHKWTENVZWRXN67ZKJFBYK" 

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

def get_wallet_data(name, address):
    data = {"Wallet Name": name, "Address": address, "BNB Balance": 0.0, "tokens": [], "history": []}
    try:
        # 1. BNB Balance
        bnb_url = f"https://bscscan.com{address}&tag=latest&apikey={BSCSCAN_API_KEY}"
        bnb_res = requests.get(bnb_url, timeout=10).json()
        if bnb_res['status'] == '1':
            data['BNB Balance'] = float(bnb_res['result']) / 10**18

        # 2. BEP-20 Transfers (Zero Filter)
        token_url = f"https://bscscan.com{address}&startblock=0&endblock=99999999&sort=desc&apikey={BSCSCAN_API_KEY}"
        token_res = requests.get(token_url, timeout=10).json()
        seen_tokens = {}
        if token_res['status'] == '1':
            for tx in token_res['result']:
                symbol = tx['tokenSymbol']
                if symbol not in seen_tokens and len(seen_tokens) < 15:
                    seen_tokens[symbol] = {"Token": symbol, "Name": tx['tokenName']}
            data['tokens'] = list(seen_tokens.values())

        # 3. History
        hist_url = f"https://bscscan.com{address}&offset=5&sort=desc&apikey={BSCSCAN_API_KEY}"
        hist_res = requests.get(hist_url, timeout=10).json()
        if hist_res['status'] == '1':
            for tx in hist_res['result']:
                data['history'].append({
                    "Date": pd.to_datetime(int(tx['timeStamp']), unit='s').strftime('%Y-%m-%d %H:%M'),
                    "Value": f"{float(tx['value'])/10**18:.4f} BNB",
                    "Type": "OUT" if tx['from'].lower() == address.lower() else "IN"
                })
        return data
    except: return data

# --- UI ---
st.title("🐺 THE DONZA WOLF v6.5")
st.markdown("---")

if st.button("🚀 EXECUTE DEEP SCAN"):
    with st.spinner("Compiling Blockchain Intelligence..."):
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(lambda x: get_wallet_data(x, WALLETS[x]), WALLETS.keys()))

    # Calculate Total
    total_bnb = sum(r['BNB Balance'] for r in results)
    st.metric("TOTAL EMPIRE BNB", f"{total_bnb:,.4f} BNB")

    # --- EXCEL EXPORT LOGIC ---
    df_summary = pd.DataFrame([{"Wallet": r['Wallet Name'], "Address": r['Address'], "BNB": r['BNB Balance']} for r in results])
    
    # Create Excel Buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary.to_excel(writer, index=False, sheet_name='Empire_Summary')
        # Add detailed sheets for each wallet
        for r in results:
            if r['tokens']:
                pd.DataFrame(r['tokens']).to_excel(writer, index=False, sheet_name=f"{r['Wallet Name'][:15]}_Tokens")

    st.download_button(
        label="📥 DOWNLOAD EMPIRE REPORT (EXCEL)",
        data=output.getvalue(),
        file_name=f"Donza_Wolf_Report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Display Results in UI
    for res in results:
        with st.expander(f"📊 {res['Wallet Name']} - {res['BNB Balance']:.4f} BNB"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Tokens Found:**")
                st.table(res['tokens']) if res['tokens'] else st.info("No tokens.")
            with col2:
                st.write("**Recent History:**")
                st.table(res['history']) if res['history'] else st.info("No history.")

st.sidebar.success("V6.5: Excel Engine Integrated.")
