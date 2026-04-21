import json
import requests
import time
import random
import os
import threading

# =============================================
# 🔧 CONFIGURATION
# =============================================

# Add as many cookies as you want!
# More cookies = faster checking
COOKIES = [
    "YOUR_COOKIE_1_HERE",
    "YOUR_COOKIE_2_HERE",
    "YOUR_COOKIE_3_HERE",
]

VOUCHER_VALUES = {
    "SO6": 1000
}

# =============================================
# RESULTS
# =============================================
valid_vouchers = []
results_lock = threading.Lock()

# =============================================
# HELPERS
# =============================================
def get_voucher_value(code):
    prefix = code[:3].upper()
    return VOUCHER_VALUES.get(prefix, 0)

def get_headers(cookie):
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://www.sheinindia.in",
        "referer": "https://www.sheinindia.in/cart",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "x-tenant-id": "SHEIN",
        "cookie": cookie
    }

def apply_voucher(session, code, headers):
    url = "https://www.sheinindia.in/api/cart/apply-voucher"
    payload = {"voucherId": code, "device": {"client_type": "web"}}
    try:
        response = session.post(url, json=payload, headers=headers, timeout=45)
        try:
            return response.status_code, response.json()
        except:
            return response.status_code, {"errorMessage": "Non-JSON"}
    except:
        return None, None

def reset_voucher(session, code, headers):
    url = "https://www.sheinindia.in/api/cart/reset-voucher"
    payload = {"voucherId": code, "device": {"client_type": "web"}}
    try:
        session.post(url, json=payload, headers=headers, timeout=20)
    except:
        pass

def is_valid(response_data):
    if not response_data:
        return False
    if isinstance(response_data, str):
        return False
    if "errorMessage" in response_data and isinstance(response_data["errorMessage"], str):
        if "Block" in response_data["errorMessage"]:
            return False
    if "errorMessage" in response_data:
        err = response_data.get("errorMessage", {})
        if isinstance(err, dict):
            errors = err.get("errors", [])
            for error in errors:
                if isinstance(error, dict):
                    if error.get("type") == "VoucherOperationError":
                        if "not applicable" in error.get("message", "").lower():
                            return False
    return "errorMessage" not in response_data

# =============================================
# CHECKER THREAD - Each cookie checks its batch
# =============================================
def check_batch(cookie_index, cookie, codes):
    session = requests.Session()
    headers = get_headers(cookie)

    print(f"🍪 Cookie {cookie_index + 1} → Checking {len(codes)} codes...")

    for i, code in enumerate(codes, 1):
        value = get_voucher_value(code)
        print(f"  [{cookie_index + 1}] {i}/{len(codes)} → {code}")

        status, response = apply_voucher(session, code, headers)

        if status is None:
            time.sleep(2)
            continue

        if is_valid(response):
            print(f"  ✅ VALID: {code} (₹{value})")
            with results_lock:
                valid_vouchers.append((code, value))
        else:
            reset_voucher(session, code, headers)
            print(f"  ❌ Invalid: {code}")

        time.sleep(random.uniform(2, 4))

    session.close()
    print(f"✅ Cookie {cookie_index + 1} done!")

# =============================================
# LOAD VOUCHERS
# =============================================
def load_vouchers():
    if not os.path.exists("vouchers.txt"):
        print("❌ vouchers.txt not found!")
        return []
    codes = []
    with open("vouchers.txt", "r") as f:
        for line in f:
            line = line.strip().upper()
            if line and not line.startswith("==="):
                codes.append(line)
    return codes

# =============================================
# SAVE RESULTS
# =============================================
def save_results():
    if not valid_vouchers:
        print("\n😔 No valid vouchers found!")
        return

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("valid_vouchers.txt", "a", encoding="utf-8") as f:
        f.write(f"\n✅ Valid Vouchers - {timestamp}\n")
        f.write("=" * 40 + "\n")
        grouped = {}
        for code, val in valid_vouchers:
            grouped.setdefault(val, []).append(code)
        for val in sorted(grouped.keys(), reverse=True):
            f.write(f"\n💰 Worth ₹{val}:\n")
            for code in grouped[val]:
                f.write(f"  {code}\n")

    total = sum(val for _, val in valid_vouchers)
    print(f"\n🎉 Found {len(valid_vouchers)} valid vouchers!")
    print(f"💰 Total Value: ₹{total}")
    print("\n✅ Valid codes:")
    for code, val in valid_vouchers:
        print(f"  ✅ {code} — ₹{val}")

# =============================================
# MAIN
# =============================================
def main():
    print("=" * 50)
    print("     SHEIN VOUCHER CHECKER")
    print("     🔥 Multi-Cookie Edition 🔥")
    print("=" * 50)

    # Load vouchers
    codes = load_vouchers()
    if not codes:
        return

    print(f"\n📋 Total codes: {len(codes)}")
    print(f"🍪 Total cookies: {len(COOKIES)}")

    # Filter empty cookies
    active_cookies = [c for c in COOKIES if c and c != "YOUR_COOKIE_1_HERE" and c != "YOUR_COOKIE_2_HERE" and c != "YOUR_COOKIE_3_HERE"]

    if not active_cookies:
        print("❌ No valid cookies found! Please add your cookies!")
        return

    print(f"✅ Active cookies: {len(active_cookies)}")

    # Split codes among cookies
    chunk_size = max(1, len(codes) // len(active_cookies))
    chunks = []
    for i in range(0, len(codes), chunk_size):
        chunks.append(codes[i:i + chunk_size])

    # Make sure all codes are covered
    while len(chunks) > len(active_cookies):
        chunks[-2].extend(chunks[-1])
        chunks.pop()

    print(f"\n🚀 Starting check with {len(active_cookies)} cookies simultaneously...\n")

    # Start threads for each cookie
    threads = []
    for i, (cookie, chunk) in enumerate(zip(active_cookies, chunks)):
        t = threading.Thread(target=check_batch, args=(i, cookie, chunk))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\n" + "=" * 50)
    print("✅ All checks complete!")
    save_results()
    print("=" * 50)

if __name__ == "__main__":
    main()
