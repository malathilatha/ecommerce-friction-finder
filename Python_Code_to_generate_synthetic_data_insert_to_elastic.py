# ============================================
# E-COMMERCE FRICTION FINDER - COMPLETE SETUP
# ============================================

# STEP 1: Install dependencies
!pip install elasticsearch faker -q

# STEP 2: Configure your Elasticsearch credentials
# 👇 REPLACE THESE WITH YOUR ACTUAL VALUES 👇
ES_CLOUD_ID = "your_elastic_cloud_id"  # Copy from Elastic Cloud
ES_API_KEY = "your_api_key"    # Copy from Elastic Cloud

# ============================================
# DATA GENERATION
# ============================================
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import uuid

fake = Faker()

print("="*60)
print("🔄 GENERATING SYNTHETIC E-COMMERCE DATA")
print("="*60)

# Sample product catalog
PRODUCTS = [
    {"id": "prod_001", "name": "Wireless Mouse", "price": 29.99},
    {"id": "prod_002", "name": "USB-C Cable", "price": 15.99},
    {"id": "prod_003", "name": "Laptop Stand", "price": 49.99},
    {"id": "prod_004", "name": "Mechanical Keyboard", "price": 89.99},
    {"id": "prod_005", "name": "Wireless Headphones", "price": 129.99},
    {"id": "prod_006", "name": "Phone Case", "price": 19.99},
    {"id": "prod_007", "name": "Screen Protector", "price": 9.99},
    {"id": "prod_008", "name": "Power Bank", "price": 39.99},
    {"id": "prod_009", "name": "Webcam", "price": 79.99},
    {"id": "prod_010", "name": "External SSD", "price": 119.99},
]

SEARCH_TERMS = [
    "wireless mouse", "laptop charger", "usb-c cable", "wireless headphone",
    # Problematic searches (0 results)
    "usbc cable", "wireles headphones", "laptop chargr", "mous",
    "keybord", "headfone", "screen protecter", "blutooth speaker",
]

SITE_URLS = [
    "/", "/products", "/cart", "/checkout", "/checkout/payment",
    "/product/prod_001", "/product/prod_002", "/product/prod_003",
]

ERROR_URLS = [
    "/product/old-laptop-123", "/product/discontinued-item",
]

def generate_timestamp():
    now = datetime.utcnow()
    random_date = now - timedelta(
        days=random.randint(0, 7),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    return random_date.isoformat() + "Z"

# Generate user sessions
print("\n→ Generating 2000 user sessions...")
user_sessions = []
for i in range(2000):
    url = random.choice(SITE_URLS)
    page_load_time = round(random.uniform(3.5, 8.0), 2) if "payment" in url else round(random.uniform(0.5, 3.0), 2)
    user_sessions.append({
        "session_id": f"sess_{uuid.uuid4().hex[:12]}",
        "user_id": f"user_{random.randint(1,200):04d}",
        "timestamp": generate_timestamp(),
        "page_url": url,
        "page_load_time": page_load_time,
        "action": random.choice(["view_page", "view_product"]),
        "bounce": page_load_time > 4.0 and random.random() > 0.3,
    })

# Generate search queries
print("→ Generating 1000 search queries...")
search_queries = []
for i in range(1000):
    search_term = random.choice(SEARCH_TERMS)
    problematic = search_term in ["usbc cable", "wireles headphones", "laptop chargr", "mous", "keybord"]
    search_queries.append({
        "query_id": f"q_{uuid.uuid4().hex[:8]}",
        "user_id": f"user_{random.randint(1,200):04d}",
        "search_term": search_term,
        "results_count": 0 if problematic else random.randint(1, 15),
        "timestamp": generate_timestamp(),
    })

# Generate cart events
print("→ Generating 800 cart events...")
cart_events = []
for i in range(800):
    product = random.choice(PRODUCTS)
    cart_events.append({
        "cart_id": f"cart_{uuid.uuid4().hex[:12]}",
        "user_id": f"user_{random.randint(1,200):04d}",
        "action": "add_to_cart",
        "product_id": product["id"],
        "product_name": product["name"],
        "timestamp": generate_timestamp(),
        "cart_value": round(product["price"] * random.randint(1, 3), 2)
    })

# Generate checkout flows
print("→ Generating 600 checkout flows...")
checkout_flows = []
checkout_steps = ["cart", "shipping", "payment", "review", "complete"]
for i in range(600):
    checkout_id = f"co_{uuid.uuid4().hex[:12]}"
    user_id = f"user_{random.randint(1,200):04d}"
    max_step = random.randint(0, 4)

    for step_idx in range(max_step + 1):
        step = checkout_steps[step_idx]
        time_spent = random.randint(60, 180) if step == "payment" else random.randint(10, 45)
        checkout_flows.append({
            "checkout_id": checkout_id,
            "user_id": user_id,
            "step": step,
            "time_spent": time_spent,
            "completed": (step == "complete"),
            "abandoned": (step_idx == max_step and step != "complete"),
            "timestamp": generate_timestamp(),
            "cart_value": round(random.uniform(50, 500), 2)
        })

# Generate error logs
print("→ Generating 300 error logs...")
error_logs = []
for i in range(300):
    url = random.choice(ERROR_URLS + SITE_URLS)
    error_logs.append({
        "error_id": f"err_{uuid.uuid4().hex[:8]}",
        "url": url,
        "error_code": 404 if url in ERROR_URLS else random.choice([500, 502, 404]),
        "timestamp": generate_timestamp(),
        "user_id": f"user_{random.randint(1,200):04d}",
    })

print(f"\n✅ Generated {len(user_sessions) + len(search_queries) + len(cart_events) + len(checkout_flows) + len(error_logs)} total records")

# ============================================
# ELASTICSEARCH INGESTION
# ============================================
from elasticsearch import Elasticsearch, helpers

print("\n" + "="*60)
print("📤 INGESTING DATA TO ELASTICSEARCH")
print("="*60)

# Check credentials
if ES_CLOUD_ID == "YOUR_CLOUD_ID_HERE" or ES_API_KEY == "YOUR_API_KEY_HERE":
    print("\n❌ ERROR: Please update ES_CLOUD_ID and ES_API_KEY at the top of this cell!")
    print("\n📝 How to get them:")
    print("   1. Go to Elastic Cloud console")
    print("   2. Click your project")
    print("   3. Copy Cloud ID")
    print("   4. Go to Management → API Keys → Create API Key")
    raise ValueError("Credentials not configured")

# Connect to Elasticsearch
print("\n🔌 Connecting to Elasticsearch...")
es = Elasticsearch(
    cloud_id=ES_CLOUD_ID,
    api_key=ES_API_KEY
)

if es.ping():
    print("✅ Connected successfully!")
else:
    raise ConnectionError("❌ Failed to connect")

# Index mappings
INDICES = {
    "user-sessions": {
        "properties": {
            "session_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "timestamp": {"type": "date"},
            "page_url": {"type": "keyword"},
            "page_load_time": {"type": "float"},
            "action": {"type": "keyword"},
            "bounce": {"type": "boolean"},
        }
    },
    "search-queries": {
        "properties": {
            "query_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "search_term": {"type": "text"},
            "results_count": {"type": "integer"},
            "timestamp": {"type": "date"},
        }
    },
    "cart-events": {
        "properties": {
            "cart_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "action": {"type": "keyword"},
            "product_id": {"type": "keyword"},
            "product_name": {"type": "text"},
            "timestamp": {"type": "date"},
            "cart_value": {"type": "float"}
        }
    },
    "checkout-flows": {
        "properties": {
            "checkout_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "step": {"type": "keyword"},
            "time_spent": {"type": "integer"},
            "completed": {"type": "boolean"},
            "abandoned": {"type": "boolean"},
            "timestamp": {"type": "date"},
            "cart_value": {"type": "float"}
        }
    },
    "error-logs": {
        "properties": {
            "error_id": {"type": "keyword"},
            "url": {"type": "keyword"},
            "error_code": {"type": "integer"},
            "timestamp": {"type": "date"},
            "user_id": {"type": "keyword"},
        }
    }
}

# Create indices
print("\n📋 Creating indices...")
for index_name, mapping in INDICES.items():
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"  ⚠️  Deleted existing index: {index_name}")

    es.indices.create(index=index_name, body={"mappings": mapping})
    print(f"  ✅ Created: {index_name}")

# Ingest data
datasets = {
    "user-sessions": user_sessions,
    "search-queries": search_queries,
    "cart-events": cart_events,
    "checkout-flows": checkout_flows,
    "error-logs": error_logs
}

print("\n📤 Ingesting documents...")
total_docs = 0
for index_name, documents in datasets.items():
    actions = [{"_index": index_name, "_source": doc} for doc in documents]
    success, failed = helpers.bulk(es, actions, stats_only=True)
    print(f"  ✅ {index_name}: {success} documents")
    total_docs += success

print(f"\n✅ TOTAL DOCUMENTS INGESTED: {total_docs}")

# Verify
print("\n🔍 Verifying data...")
for index_name in INDICES.keys():
    count = es.count(index=index_name)['count']
    print(f"  ✅ {index_name}: {count} docs")

print("\n" + "="*60)
print("🎉 DATA SETUP COMPLETE!")
print("="*60)
print("\n📊 Next: Test these ES|QL queries in Kibana Dev Tools:\n")
print("1. Failed searches:")
print('   FROM "search-queries" | WHERE results_count == 0 | STATS count = COUNT(*) BY search_term | SORT count DESC\n')
print("2. Slow pages:")
print('   FROM "user-sessions" | WHERE page_load_time > 3.0 | STATS avg_load = AVG(page_load_time) BY page_url | SORT avg_load DESC\n')
print("3. Cart abandonment:")
print('   FROM "checkout-flows" | WHERE abandoned == true | STATS count = COUNT(*) BY step\n')
print("\n🚀 Ready to build your agent!")