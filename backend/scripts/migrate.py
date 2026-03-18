#!/usr/bin/env python3
"""Script to run migrations."""

import subprocess
import sys

def main():
    """Run Alembic migrations."""
    print("Running database migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Migrations completed successfully")
        return 0
    else:
        print(f"✗ Migration failed:\n{result.stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
