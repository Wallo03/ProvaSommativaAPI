import streamlit as st
import requests
import json

def main():
    st.title("Startup BirdIT")
    url_API =st.text_input("inserisci url dell'api","http://localhost:8000/predict")
    rdspend = st.number_input("Inserisci R&D Spend", 0,1000000,73721)
    administration = st.number_input("Inserisci Administration", 0,1000000,121344)
    marketingspend = st.number_input("Inserisci Marketing Spend", 0,1000000,211025)

    ############## GET REQUEST #################
    if st.button("GET"):
        url = url_API
        url2 = f"?rdspend={rdspend}&administration={administration}&marketingspend={marketingspend}"
        link = url+url2
        st.write('"{}"'.format(link))
        response = requests.get(link)
        result =response.json()
        st.success(f"Il risulato è: {result['prediction']}")

    ############## POST REQUEST #################
    if st.button("POST"):
        url = url_API
        response =requests.post(url,
                                headers={"Content-Type": "application/json"},
                                data = json.dumps({
                                                   "rdspend":rdspend,
                                                   "administration":administration,
                                                   "marketingspend":marketingspend,
                                                   })
                                )
        result =response.json()
        st.success(f"Il risulato è: {result['prediction']}")

if __name__ == '__main__':
    main()