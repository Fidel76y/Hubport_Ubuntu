import subprocess

def show_wifi():
    try:
        results = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "device", "wifi", "list"])
        results = results.decode("utf-8").strip()
        ssids = results.split("\n")
        for ssid in ssids:
            print(ssid)
        return ssids
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

show_wifi()
