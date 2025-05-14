from fastapi import FastAPI
from flipside import Flipside

app = FastAPI()

flipside = Flipside(
    "f0a727c1-d23e-449d-b353-5883a7fc39c2",
    "https://api-v2.flipsidecrypto.xyz"
)

sql = """
SELECT * FROM external.defillama.fact_chain_tvl
"""

@app.get("/tvl-data")
def get_tvl_data():
    try:
        result = flipside.query(sql)
        return {"status": "success", "data": result.records}
    except Exception as e:
        return {"status": "error", "message": str(e)}
