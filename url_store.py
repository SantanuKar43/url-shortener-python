import redis
import util

prefix = "uss-py:"
ctr_key = "ctr"

# Connect to the local Redis server with default settings
# decode_responses=True returns strings instead of bytes
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # Check if the connection is active
    print(r.ping()) # Output: True
    if r.exists(prefix + ctr_key) == 0:
        r.set(prefix + ctr_key, 10000)
except redis.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

def create(url: str) -> str:
    count = r.incr(prefix + ctr_key)
    short_id = util.gen_short_id(count)
    r.set(prefix + short_id, url)
    return short_id

def get(short_id: str) -> str:
    return r.get(prefix + short_id)

def delete(short_id: str):
    r.delete(prefix + short_id)
