"""
Analytics API
"""
import argparse
import json

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from spai.storage import Storage

app = FastAPI(title="analytics")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def analytics():
    """
    Return vegetation analytics

    Returns
    -------
    analytics : dict
        Dictionary with vegetation analytics

    Raises
    ------
    HTTPException
        If analytics file doesn't exist
    """
    try:
        storage = Storage("data")
        analytics = storage.read("AOI_Vegetation_Quality.json")
        if isinstance(analytics.index, pd.DatetimeIndex):
            analytics.index = analytics.index.strftime("%Y-%m-%d")
        analytics = analytics.to_dict()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# need this to run in background
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
