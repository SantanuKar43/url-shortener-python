import redis
import os
import base58
from urllib.parse import urlparse

prefix = "uss-py:"
ctr_key = "ctr"

# Connect to the local Redis server with default settings
# decode_responses=True returns strings instead of bytes
def initialise_redis():
    try:
        r = redis.Redis(host = os.getenv("REDIS_HOST", "localhost"), 
                        port = os.getenv("REDIS_PORT", "6379"), 
                        decode_responses=True)
        # Check if the connection is active
        print(r.ping()) # Output: True
        if r.exists(prefix + ctr_key) == 0:
            r.set(prefix + ctr_key, 10000)
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def create(url: str, r) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme == '':
        parsed_url = parsed_url._replace(scheme="https")
    count = r.incr(prefix + ctr_key)
    short_id = create_short_id(count)
    r.set(prefix + short_id, parsed_url.geturl())
    return short_id

def resolve_url(short_id: str, r) -> str:
    return r.get(prefix + short_id)

def delete(short_id: str, r):
    r.delete(prefix + short_id)

def create_short_id(n: int):
    return base58.b58encode_int(n).decode("utf-8")