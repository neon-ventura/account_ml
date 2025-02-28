from fastapi import FastAPI
import requests
import webbrowser

app = FastAPI()

LINK_AUTH = "https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=5864919107606556&redirect_uri=https://boostfy.vercel.app/"

ACCESS_TOKEN = "APP_USR-5864919107606556-022811-fef51fff1149b468f087e925e729d9be-1978970820"
API_URL = "https://api.mercadolibre.com/users/me"

@app.get("/")
def get_user_info():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    res = requests.get(API_URL, headers=headers)
    user_data = res.json()
    
    # Extraindo os dados desejados
    user_name = user_data.get("nickname")
    
    registration_identifiers = user_data.get("registration_identifiers", [])
    user_phone = (registration_identifiers[0].get("metadata", {}).get("number")
                  if registration_identifiers else None)
    
    user_cnpj = user_data.get("identification", {}).get("number")
    user_address = user_data.get("address")
    user_perfil_link = user_data.get("permalink")
    user_reputation = user_data.get("seller_reputation")
    user_metrics = user_data.get("metrics")
    user_buyer_reputation = user_data.get("buyer_reputation")
    user_mercadoenvios = user_data.get("mercadoenvios")
    user_picture_url = user_data.get("thumbnail", {}).get("picture_url")

    if user_name == None:
        print("Token expirado! Pegar novamente")
        webbrowser.open(LINK_AUTH)
        return
    
    return {
        "user_name": user_name,
        "user_phone": user_phone,
        "user_cnpj": user_cnpj,
        "user_address": user_address,
        "user_perfil_link": user_perfil_link,
        "user_reputation": user_reputation,
        "user_metrics": user_metrics,
        "user_buyer_reputation": user_buyer_reputation,
        "user_mercadoenvios": user_mercadoenvios,
        "user_picture_url": user_picture_url
    }
