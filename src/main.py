from zipfile import BadZipfile

import requests, sys, os, getpass, zipfile

args = sys.argv[1:]
if len(args) < 1:
    print("Help: pam test (installing package test)")
    raise SystemExit
if len(args) > 1:
    branch = args[1]
else:
    branch = "main"

path = f"/Users/{getpass.getuser()}/"

if path.removesuffix("/") in os.listdir(path.removesuffix("/")):
    os.mkdir(path.removesuffix("/") + "/PAM_Packages")

repo = f"PAM-Manager/{args[0]}"

output_zip = "PAMTemp.zip"
url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
response = requests.get(url, stream=True)

with open(output_zip, "wb") as f:
    for chunk in response.iter_content(chunk_size=128):
        f.write(chunk)
try:
    with zipfile.ZipFile(output_zip, "r") as zip_ref:
        found_files = [f for f in zip_ref.namelist()]

        for file in found_files:
            zip_ref.extract(file, path.removesuffix("/") + "/PAM_Packages")

except BadZipfile:
    print("Not a package")
    os.remove("PAMTemp.zip")
    raise SystemExit


os.remove(output_zip)
print(f"Found downloaded package in {path.removesuffix("/")}/PAM_Packages/{repo.split("/")[1]}-{branch}")
