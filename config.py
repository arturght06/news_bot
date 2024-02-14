import os
from dotenv import load_dotenv

load_dotenv(".env")

token: str = os.getenv("TOKEN")
admin_id = [int(i) for i in os.getenv("ADMIN_ID")[1:-1].split(",")]
adminPanelPasswords = [i.replace("\"", "").replace(" ", "") for i in os.getenv("ADMIN_PASSWORDS")[1:-1].split(",")]
mongodb_cluster_link: str = os.getenv("MONGODB_CLUSTER_LINK")

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

alert_channel_id = os.getenv("ALERT_CHANNEL_ID")
