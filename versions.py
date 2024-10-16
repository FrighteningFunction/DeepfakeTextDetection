import requests

def get_python_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        requires_python = data.get("info", {}).get("requires_python", "Not specified")
        return requires_python
    return "Package not found"

with open("./BERT-Defense/BERT-Defense-or-GLTR-Defense_requirements.txt") as f:
    packages = [line.split("==")[0] for line in f if line.strip() and not line.startswith("#")]

for package in packages:
    version = get_python_version(package)
    print(f"{package}: {version}")