# OverTheWire: Bandit Automation
This script will automatically connect to the Bandit servers and solve the challenges, saving the passwords along the way.
Passwords are saved to `cache/bandit_flags_cache.json`, which can be manipulated to force levels to be replayed.

## Running with Docker
- Clone the repo
- Install Docker
  - On Windows, make sure your Docker engine is running
- run `docker compose up`
If any code is changed, run `docker compose up --build` to include your changes in the new run

## Running locally
- Create and activate a virtual environment
- run `pip install -r requirements.txt`
- run `main.py` using Python
  - run `main.py --fresh` to automatically clear the flags cache before running