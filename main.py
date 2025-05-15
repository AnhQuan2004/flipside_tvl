# from fastapi import FastAPI
# from flipside import Flipside

# app = FastAPI()

# flipside = Flipside(
#     "f0a727c1-d23e-449d-b353-5883a7fc39c2",
#     "https://api-v2.flipsidecrypto.xyz"
# )

# sql = """
# SELECT * FROM external.defillama.fact_chain_tvl
# """

# @app.get("/tvl-data")
# def get_tvl_data():
#     try:
#         result = flipside.query(sql)
#         return {"status": "success", "data": result.records}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

from fastapi import FastAPI
from flipside import Flipside
from typing import List, Dict
import time

app = FastAPI()

flipside = Flipside(
    "f0a727c1-d23e-449d-b353-5883a7fc39c2",
    "https://api-v2.flipsidecrypto.xyz"
)

LIMIT = 100000

@app.get("/tvl-data")
def get_tvl_data() -> Dict:
    sql_template = """
    SELECT *
    FROM external.defillama.fact_chain_tvl
    LIMIT {limit} OFFSET {offset}
    """

    offset = 0
    all_records = []

    try:
        while True:
            paginated_sql = sql_template.format(limit=LIMIT, offset=offset)
            result = flipside.query(paginated_sql)

            records = result.records
            if not records:
                break

            all_records.extend(records)

            if len(records) < LIMIT:
                break  # batch cuối cùng

            offset += LIMIT
            time.sleep(1)  # tránh gọi quá nhanh

        return {
            "status": "success",
            "total": len(all_records),
            "data": all_records
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
