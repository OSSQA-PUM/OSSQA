import requests
import json


def convert(json_file):
    f = open(json_file, "r", encoding="utf8")
    data = json.load(f)
    add_sbom(data)
    f.close()


def add_sbom(json_file):
    r = requests.post("http://127.0.0.1:5080/add_SBOM", json=json_file)
    print(r)


def test_add_sbom():
    for i in range(1, 10):
        print(f"sbom{i}.json")
        convert(f"sbom{i}.json")

def test_add_sbomscore():
    convert("SBOM2_results.json")


