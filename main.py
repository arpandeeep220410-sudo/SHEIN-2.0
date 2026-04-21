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
    "bm_ss=ab8e18ef4e; bm_mi=DB80D67283F47583FF1658D3B78CA492~YAAQHSIPeuyiC62dAQAA32gjsh9lk8qbyLJArJmfDroLtMthu65oznPCdKBU02ujfWrwsd3CDYU/aFoQauTD6GqeoZav1BcGAfiQIL8mDFfqWYuZFFtjU53RMGihMePJOvqEQpl9OIH2rO0W0IDwBZOy7LvtMFTP8sVxiqlPMjP6VjEkYdc4bzF1F8qMpQsAshD6ezpZwapYgTOr2xdC5q7tNe61KmYsHT+/1o3NNkld7olJfrVfP4fYUC2r5hjmfGtXG90JlR8m0Zni8rdIn+kjHVKgO3of3IT2dqZk3viKoK6884erN+0v7DVdElk3~1; bm_sc=4~1~745222542~YAAQHSIPeu6iC62dAQAA32gjsgfl+dgZfSS3c4hLo05MCkm3x2NViv/+zD9S2scdssxjYGF4ECB/uWpqpzEWZq29NmA9+gqocVhUBtAaxZn08ChLfpHLhymucf4BrUUJqUGtB8R+cp/t1OtRFEJ2cxiIdLBhtKH9KdvoELhV5TZGxyQGYxdjb9L/0I8jcqoISRm6GHv7Py1FaBqs24tnNxfb+94/OhbitFzedCWHVzrYtXRTHc4VAchYZDxO1fEFmEu9ZFZU33Pjc4twB3W64lrnWCqZwQD/7N4M7myVPvaG2lDnN1c93kSGXaPcBrQd6xFvgEMIU5vh5saETGmVFyYX/7tocHVqUeAWWWs/3GaTzZ0KmDHsQzV+SwoSgVCSKn0CTzQ+yXLJ2BOh/loZStisPJ4IvxPklSFd3XO+7YeMKtQdJuIwWYlfWFcfQSS7z1yiXxoA8JGY7iKVI+F6KezoO9ArYAsdpz0E8ZCC7PUNIos4i/zIOvyJjfKy0zgiwS9CFz1H25QkaguwnvC5I2YcWRarPQ0=~0~0~0; ak_bmsc=0163D47C4480743EF8D3FA7CA93079AC~000000000000000000000000000000~YAAQHSIPegSjC62dAQAA2Wwjsh8czOGfeBlQe7+s3Oe8BhAfuOitF18dzIVKS8wgMqiSLio78YTRRJH5prgkZn9RmhztTrum3hT72/VGiOArUCJB5ukeu0C8+0CE4H7dwfv0WlvVTQ7J2aQGE1apsHjWJoFksWpbLA2CT2Eh24MiRguBg96QFMJknH6vR8nTsvJNmpCAo4N4ADzLc0YAi8UYPiegrT4iovf7V7+lQXLHWLFQcPN9DiJhY582TvS/odxB8+uhA6PdQwi1Jks0ocno1sztZ32kOzJHETZQ3qc73tLEtxKpwszUCc0ozCODyCooVaMO1fDjvpBlcCibVAmyp+1KiFoPKBATt+V7BEYTUheJCCNPeYPixSXQckbEaqZnBAzDNcUbVsiXHu/0wh7ddKX1WUHk7pp2IrLS3bhRZd92MXlE+KlINVZxyXhfyjBWmvlOVd99i/xFSCXEEic37zBvnU9o81GogEiixg4YDkjj5D+7g4aosaeDMyuBdAY=; perf=true; V=1; _fpuuid=8WuKQWrQcH9T2LsjeD0dV; deviceId=8WuKQWrQcH9T2LsjeD0dV; sessionId=sess_1776810159938_qf31rv046; navigation_cookie=false; os=4; vr=WEB-2.0.11; ifa=4937caee-6b40-45b7-b91b-7438cf7b50f5; jioAdsFeatureVariant=true; EI=sJXtr44BcA8qnJyd7OUvnKDc5GxZSVwIopWx6XSzNtVB7MwZTawoEt5a4XqmXIul; mE=she*******************%40gmail.com; mN=90XXXXX984; uI=9031280984; un=priyanshu%20k; MN=9031280984; CI=d99d6651-59b8-47c2-b25d-9c84507eaa0a; PK=9btfMWfs98RVhuRqYwPgKm20Tt1j4b8cEYaYYMZylTRD6kw6XUUr5FqJZmzsD1Dk; SN=arpandeep; G=M; U=pushpadevi1990pd%40gmail.com; A=eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzaGVpbl9wdXNocGFkZXZpMTk5MHBkQGdtYWlsLmNvbSIsInBrSWQiOiJkOTlkNjY1MS01OWI4LTQ3YzItYjI1ZC05Yzg0NTA3ZWFhMGEiLCJjbGllbnROYW1lIjoid2ViX2NsaWVudCIsInJvbGVzIjpbeyJuYW1lIjoiUk9MRV9DVVNUT01FUkdST1VQIn1dLCJtb2JpbGUiOiI5MDMxMjgwOTg0IiwidGVuYW50SWQiOiJTSEVJTiIsImV4cCI6MTc3OTQwMTcxOSwidXVpZCI6ImQ5OWQ2NjUxLTU5YjgtNDdjMi1iMjVkLTljODQ1MDdlYWEwYSIsImlhdCI6MTc3NjgwOTcxOSwiZW1haWwiOiJwdXNocGFkZXZpMTk5MHBkQGdtYWlsLmNvbSJ9.s14zx79UTTgKKJHV39z3pzVwGF-RqK8ocLJ9Z0fjiFH1zb8UttDaYdK_wEUfroCT_6Azij9mM5fjEeSxPYParZ_RRTP1O0oIGAQ2a2xSiSE9q4OWP9bJT1Y_qk-3Tit7GYpAQ0v9DFmHCcK1rjvhJbYtDh9g9BiXkHLQhiL01UlSzS3EoLlTmz_PH4woylSUJhBYtOvuOQAj1tr5aov5FEdLajJMLa-BrVxk_clFMF8TeRwp0kiov4ExWGC4CefVo2sp5w9Py8tEJ5eA40mdOF2v50xCKdhsBpfVLcIFnYpa6KUpe6-iBURuQ91jcbxPXZb8ReH59Zedpr_Vn5cAYQ; LS=LOGGED_IN; R=eyJhbGciOiJSUzI1NiJ9.eyJzZXNzaW9uIjp7InNlc3Npb25JZCI6ImNkYmZmMDM1LTdhZGItNGQzMi1iMDhjLTEzNTY1NTE5ZGIyMSIsImNsaWVudE5hbWUiOiJ3ZWJfY2xpZW50Iiwicm9sZXMiOlt7Im5hbWUiOiJST0xFX0NVU1RPTUVSR1JPVVAifV19LCJ0eXBlIjoicmVmcmVzaCIsInRlbmFudElkIjoiU0hFSU4iLCJzdWIiOiJzaGVpbl9wdXNocGFkZXZpMTk5MHBkQGdtYWlsLmNvbSIsImV4cCI6MTc5MjM2MTE5MywiaWF0IjoxNzc2ODA5MTkzfQ.HzlikgHf2eAXNYIgsN5HRBxmyk-9ro8erMrf8oWibtJCdO_oMNtwI2W82sYPLYxbHvDkYLF-ZvxV8MUxyUgvEF3l6hierN3f2UNwalihq7Y56F9kfjzBUUMHt2kdVfLzxkrAdwwN_W0HuwrtZkeX5T8wL3OZLEL4BCITUM7fSsUrvIhSU10tfjzMlVOAYOQ6rUMiFzOxItEiBzDgEJ4g6ktxmsa4x-7rn-Mi4h-FmESUDhRlWzMHXiMDhF2e6Qo7pk_pdkVmTiUpA8YwMwsYQ8BBXOPywemR9IZEHvRZNcXYkT3wSbTQrA6fa7WluKk7A6x9FijOjmdEzNuOBJxe4Q; M=SH0038709830; GUID=aae35a65-6e5d-49c5-ac47-9b52dce60ada; C=SH0038709830; TS0119eff6=015d0fa226e47ddb3aaacd1b80c9eb79853e57e3485caeea3081daedb1c595aca69d77e6d8c02949ea76f73a673bd2e330f3f0b180e0c9f182f37dde9bea4c8a65ea3372a34fc9b079f14165f9093f527d9baff5983e2279280f5ab7dec8bf10c55f5ca281; customerType=Existing; userCohortValues=[{"key":"shein_v1","value":"economy|na,mjeans,men,cl30d"}]; customerType=Existing; deviceCohortValue=%5B%5D; bm_lso=B6497DBB06745DEF4648E7CD89646E3FEEE09EE2C9F9DD1D28544F93A52D88A1~YAAQHSIPekGkC62dAQAAe0MksgeZb8RpFoX4ALU75jHI5Be4bHhiicJZyANa/9n30e0L0vEIRh69JsATrT2lrA5palZQ3/optb7iOfslQspp8fQ6145S9EgGlZpkFQUae1/A2AD6d/zysg98+0X+JfTwRaS8Z4IjflnZKCrvof0xLIYoCnn+t6BjYdTTmgfFQHwv5vm4f0MNz8r2h3syJDJsq+rDsDlhUKACDJT7Y7suYSY2jEIWYZRstmSLOx5SCiLm06ZQsYVx/zBksSr44OPH4r1d9iOH7a/vucsaLmQPrK1TQJLDxGIp+ccnzLuby9KfdZOVM4i1gk6Jt09XrmvDxhJFVJGHO+foJ2JKRRknmFDWkLRzOBcwA2NGJM5u1/7nMEaE2ILIhp1Rh48+yv1tP2iD9GOe/gBYU60+C7E9ew3hS6HCLUmNeEg7tYS904H/YcceLE4iMqneCvrx6n+X0l0lneHXF8Dqxa4vaLK73K2VpOv+npRTpyHiWQ==~1776810216820; TS01b6f9b7=015d0fa2266fd90ee8a4b14afee16d8e9ff14700265caeea3081daedb1c595aca69d77e6d832c41f951a77be7a29bbf5f0c9ed093414fe057e8811cf52ea1ea69f23711864a51208598fae10274bf5de70cad0d1d551ef50cf00e4fae509d84b1d7efcc1e824bd90927020ff84655472115b150a64; _abck=502C24E0149C94F4F38E3F77B7610C93~0~YAAQHSIPepmkC62dAQAAyoAksg8OCz2AugGwcSUdrJb2rqBhWdzWRrmowdvhey53gda7edY3/pYGbeJEDy3r1dLKrNYARTiDrAu8Ohj0v8kB6TpYGCUzrJ+EHzWj0s9YtD4+BrNJpekfPLc2BiYSife5RHUiyG2IbOvi7ZsogFi8P5jKhSloAmrzeLizZBNI/RLCbLnZUDo5fPgws8KLdm1DlyEOAMRYHIS8yAjSY3y1Q8cDKoLmixglRT/9DUhRsKEEv1+Xo40q9Mp1oXt7+h4JOVrDuiehB+4Vsn1EXQcdnxejZlgHvJ7AndH/fGywrhYRTvA2n8LkDeWFEtfvRyMxhEFDdpsa02mwZHiHxF+SJTd78rsttHdbqk30cpX1ekVszgrlyImkgj82mBjUoSLeg432aZMvNYQR8f5jo58JhUoNzVSzn7jXdJO+sOqnNRF/l3Td2Brwq5Xooq2ZYCZ0F+wJMj1vP6WTmNW+gs4S5xHRwkRst1pmvWrvBPcx6pImb3RFrxqsQkRmuBqs8iNwukrOpCbFCBFW0EXlUGoXr2teMDY42GRlhsuvP8+r7NovOZ6ws6PhHCahueIAXdJc88NTjZcaEjNAJye7viohBVzwxMbOgepjBWZDpaI3EPsfJvO07h54eXGPOs5uP9f5d1GZ9uENMRpTpkC9+5h/FrFo9JM6G5ggtXObUwToYhU7fS/Xb0SiBrA1FEYwhLhH1GNp7hmhG+tV1gFT4DI7faE6alaJUCewlTIRj/7Hkc0EHV8BOBeJ4GJAYwm1UUWV3nvUiM4HNAzdUQoDRfBACIo11D5bCwNyvrbzKfhLQ432nQsYXKI=~-1~-1~1776813756~AAQAAAAF%2f%2f%2f%2f%2f2JJ7MDNVICj93VzTgHKQWEuptoXiI9wjqltgRs4ZEaKxSPE%2frRJQcYfS7ppV+D4yIFgUB3lXXUgmdc82gw+BeKKf2KeOzBGAqCX~-1; bookingType=SHEIN; bm_s=YAAQHSIPeuykC62dAQAAVqsksgXfVKWjWAUe1QRNKdKYTIM8eQ3K5GkNTNEADAvk/oU4JZwigDFAUGKCPURCblrspG05rQzi8usR9gL7Yc5jNZWN+cPNNQt8Wb6zJrp89RKQD2Zm/SgUS5DsyKXCUY1dsSXAepbq5DTfUvZ6z8Cl+oBv9ddPgwCzciGK31s6CCzn3rDNztdWyV4FgH83+7oTz3cmLvR7yvnQ1LFrU9KILCSxwKyUiaKNjVgau/RuMteqNhCo6mw8UhtjHr2FsFqwgyHtWR37zQl2tT5CGeqFNLb7OR9AQuff4l1LzeN6KZfJ3DRUHersc4dpqZ8EQVh/na1/0LAWKPKrLQWbOnzotb/7oupmgGbyfivrUVjao/c0hdvcbkx8rEFK7xPmHEFtTad5bxvUNmgUSFapY9ldEHlEroeuwm4YoHCnz8q2HbaRE5ec4abzWokt9Z7bVyf6nuofcsxxhYh5FyA+Ghk9sw2nhmwIzmaNPzrYfFwpdH1m0mr5Q9K8Ezl3MK6/K5LSqekOM4G7rbFOEddqIotEt8ubs6xypL0f0PoD+GOT3oHiBNT49sqg0GlXV62REnimrY/+aLDP3aOWseVWuV2x4+D7W4r3PGWeZUWEPM3IZvh2aC+/UinrZ7rL510LtmENl2aFIDidpcuqjJwJyMZS7aCeqCpV6xSbJ0ujPdc1YUltkRDpzEE7YzzSlFqX3iUWtqL4R5DkEWsbFakOrI3+rAbPONQu4KK4gdsNNo8YvtF40lbfO4D1cQxlslEQPeoCu9yipETNwRVqSnMVCqPinVKP1RTokdoiIi8ns4rkc9g7RPYm72erzwndc/ct6Ur4NCrOOmYcU4aRgBHr0fFk14MQxjPAHRExSgB0/MCqB/H/tqPTMri0S6mW//mvdM+vjxWjeR7CQtesX1je9lD4sQpEktG7CdLHNWgxKs4=; bm_so=28E0B90DD49F92FBB99DBDBBE5F17F77A33F30829A0437F407BEBBFFB4D69C1F~YAAQHSIPeu2kC62dAQAAVqsksgecYi48EpZoa6rnXicBSK5wVy8lTnflIq1OSfJHy43dhn2M/R5DFxHk4r5XbStBI1ISkm4m572S2HQus6HbMjQupxib4bJ6ZU/ceUHGv/hi8d1hRTf5LxXv23iVgLBodrj9tjjwPJo69cGKoSjPH0q1gz7/Dt5eC0pKjknN6RldMOVZy15fUi79QvuH6n45ad93nLAZX7AlSF+ZwizpW9OcxZaVD36Z8KqxImeVZGaKTX41obAOh8G3rBk1euhaVDaUs5rn9jvlQatb17Xo1jYwjM1SXarpNQ58vKbIlUdjmwJMJjckCEHzFCYkDDJTPM7Y0y+PUc9j9AWXsBWeDcLZjc+9UZ4dmyLR7KwtqT2u745lCtK+ZuOoW8uFqWN2cjL190sz6yL8in72UbjSaxP6HOaBS5Iy38UdTexjHNsoszWpxuOdBuntIYYPmup3orJW3b/zlfp/VPxUZqN4npwnQAMRlsBj8Y09dg==; bm_sv=085CC54C2051A536863CA2A6657C33BD~YAAQHSIPeu6kC62dAQAAVqsksh+VTTzVia52We0bHO/oBIKvSv5D0+mEKo3YUlj64M8fjionrY15bCXRS+7FCtKN18971gDpaS2ENQg2Zc4FozVXSZy+BWWpjRMUpwRO9XlZ30YIc5thgq10149fuFsdb23tpUZhLAP37tmub60Uo6bLzv6NbvwfAoHkAnfBc5LBQFgMeDvCOM5gaE6zFBapla71EkGAGx/My7NU8SYSwp9oZIDz6vsaNLQ8K7/0nH9oxw==~1; bm_sz=C5D45F0F4395C2668F1DCDBDD4AA60F3~YAAQHSIPeu+kC62dAQAAVqsksh+LV7yieCm5PWOIPCJWM30eZV9fZVY7G7Mi2hx5I+dBL4m4UDt9OqauO51WryMZXH2+h06c+uupYNFPsj4xiH0CiezaO2BfiFkZoEJ0RkFCBmqsGmrREcpmez6rSthjbLEzh2IMMSZDQJBZ4czEV+dmmo3U2+cYUbm7bvzhazXsWlm5EXCWs9ZJeE/I/ZvOaqIlfIdbwBQHozlgnTDMqrbHENJZqnqSwoaZUMRhUdr6ltHZk+Dtkee6bPpj1zckcGgUWDVvSNkkif8sy1mgXGbtTAOAlaQRe90NH1MTS92SKMWvt1MyhA1ycY1CrfMjIMKu//Kxs4zidpOUggJaCTc4sxVeka/a1EUuZ+v6PU7ms2MbDhy6ZOiUbvtXfJt0g906a/ZqybBCdRTOtO589GzZY8tBUWgnBX+0a5J9N1FyHdsNGsw3d2fFTADq93++ucRZY7UclddDKJ/GqTDnu5UQusbH/ODUxm4IgDnP2uYq5wZHUU1D3Ssl2vo9IKUnON82Wml8/oVaFdXI0Xte6AeSk7jAfno=~3621944~4601413",
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
