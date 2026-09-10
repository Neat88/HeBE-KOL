"""Shared paths so every script in the chain runs from the repo, not a session scratchpad."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT  = os.path.join(ROOT, "analysis", "out")
XLSX = os.path.join(DATA, "HeBE_KH_KOL_Data.xlsx")
os.makedirs(OUT, exist_ok=True)
def o(name): return os.path.join(OUT, name)
