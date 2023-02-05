from fastapi import FastAPI
from .utils.dns import DNS


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/dns/{record_type}/{domain}")
async def get_dns(record_type: str, domain: str):
    # Get the DNS record for the given record type and domain
    return {"record_type": record_type, "domain": domain, "dns": DNS().query(domain, record_type), "is_valid": DNS().is_valid(domain, record_type)}
