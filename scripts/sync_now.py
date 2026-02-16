#!/usr/bin/env python3
"""
Run the NBA data sync: fetch from external API, upsert into Postgres, invalidate caches.

Usage (from project root):
  python scripts/sync_now.py
  # or
  python -m scripts.sync_now

If the NBA API is down, exits with an error and does not modify the database.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from app.cache import delete_keys_by_prefix
from app.ingest.sync import run_sync


def main() -> None:
    print("Syncing NBA data from external API...")
    try:
        summary = run_sync()
    except Exception as e:
        print(f"Sync failed (API may be down): {e}")
        sys.exit(1)

    print("Sync complete:")
    print(f"  {summary}")

    deleted = delete_keys_by_prefix("teams:")
    print(f"  Cache invalidated: {deleted} keys (prefix 'teams:')")
    print("Done.")


if __name__ == "__main__":
    main()
