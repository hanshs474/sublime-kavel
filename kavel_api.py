"""Talks to https://www.kavel.ai. Standard library only, no Sublime imports,
so it can be run and tested on its own:  python3 kavel_api.py "a prompt"

Without an API key a call runs on Kavel's free anonymous allowance (text to image).
With a key it runs on your Kavel account: your credits and your plan's models.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = "https://www.kavel.ai"
KEYS_URL = BASE + "/settings/apikeys"
FREE_MODEL = "kavel-image-v1"
USER_AGENT = "kavel-sublime/1.0.0"


class KavelError(Exception):
    pass


def _http(method, url, body, headers):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = dict(headers, **{"User-Agent": USER_AGENT})
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode() or "{}")
        except ValueError:
            return {"code": -1, "message": "HTTP %d" % e.code}


def generate(prompt, api_key="", model="", aspect_ratio="1:1", timeout=360, poll_every=5,
             on_wait=None):
    """Generate one image and return its URL. Raises KavelError with a readable reason."""
    prompt = (prompt or "").strip()
    if not prompt:
        raise KavelError("write a prompt first")
    if api_key:
        headers = {"Authorization": "Bearer " + api_key}
    else:
        headers = {"x-anon-id": "st-" + uuid.uuid4().hex[:16]}
    env = _http("POST", BASE + "/api/ai/generate", {
        "provider": "kie",
        "mediaType": "image",
        "model": (model or FREE_MODEL) if api_key else FREE_MODEL,
        "scene": "text-to-image",
        "prompt": prompt,
        "options": {"aspect_ratio": aspect_ratio or "1:1"},
    }, headers)
    if env.get("code") != 0:
        raise KavelError(str(env.get("message") or "request refused"))
    data = env.get("data") or {}
    if data.get("wall"):
        raise KavelError("the free allowance is spent - add an API key from " + KEYS_URL)
    task = data.get("id")
    if not task:
        raise KavelError("Kavel returned no task id")

    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll_every)
        if on_wait:
            on_wait()
        try:
            if api_key:
                env = _http("POST", BASE + "/api/ai/query", {"taskId": task}, headers)
            else:
                env = _http("GET", BASE + "/api/ai/anon-query?" + urllib.parse.urlencode(
                    {"taskId": task, "provider": "kie", "mediaType": "image"}), None, headers)
        except (OSError, ValueError):
            continue  # a dropped poll is not a failed generation
        if env.get("code") != 0:
            continue
        data = env.get("data") or {}
        if data.get("status") == "failed":
            raise KavelError("generation failed - try another prompt")
        images = data.get("cleanImages") or data.get("images") or []
        if images:
            first = images[0]
            return first.get("url", "") if isinstance(first, dict) else first
    raise KavelError("still running after %d seconds (task %s)" % (timeout, task))


if __name__ == "__main__":
    import sys
    print(generate(" ".join(sys.argv[1:]) or "a paper-cut fox in a moonlit forest"))
