"""
Analytics API
"""

import argparse

import uvicorn
import pandas as pd
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

storage = Storage()["data"]


@app.get("/{analytics_file}")
async def analytics(analytics_file: str):
    """
    Return water quality analytics

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Returns
    -------
    analytics : dict
        Dictionary with water quality analytics

    Raises
    ------
    HTTPException
        If analytics file doesn't exist
    """
    try:
        analytics = storage.read(f"{analytics_file}.json")
        # Format date to ensure it is in the correct format
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
