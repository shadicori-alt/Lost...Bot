# services/shopify_sync.py
import requests, os, json
from models.models import Product, SessionLocal
from datetime import datetime

SHOP_DOMAIN = "free-move-eg.myshopify.com"

def fetch_products():
    url = f"https://{SHOP_DOMAIN}/products.json?limit=250"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        raise Exception("Shopify fetch failed")
    data = r.json()
    return data.get('products', [])

def sync_products():
    products = fetch_products()
    db = SessionLocal()
    for p in products:
        shop_id = str(p.get('id'))
        prod = db.query(Product).filter(Product.shopify_id==shop_id).first()
        title = p.get('title')
        desc = p.get('body_html')
        variants = p.get('variants', [])
        price = float(variants[0].get('price')) if variants else 0.0
        meta = json.dumps(p)
        if not prod:
            prod = Product(shopify_id=shop_id, title=title, description=desc, price=price, metadata=meta, last_synced=datetime.utcnow())
            db.add(prod)
        else:
            prod.title = title
            prod.description = desc
            prod.price = price
            prod.metadata = meta
            prod.last_synced = datetime.utcnow()
    db.commit()
    db.close()
