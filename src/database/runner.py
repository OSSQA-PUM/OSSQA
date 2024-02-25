import requests


def add_SBOM(id, name):
    r = requests.post("http://127.0.0.1:5080/add_SBOM", json={"id": id, "name": name})
    print(r)

def add_dependency(id, score):
    r = requests.post("http://127.0.0.1:5080/add_dependency", json={"id": id, "score": score})
    print(r)
