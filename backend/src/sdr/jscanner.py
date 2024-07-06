import requests

from src.sdr.sdr import SDR


class JScanner(SDR):
    """
    openjdk-17
    ./v1_test
    java -jar hub_test.jar --uber.url=localhost:8000
    hypercorn main:app --worker-class trio
    pip install anyio[trio]
    """
    def __init__(self):
        self.url = "http://localhost:8080/api/global/graph"

    def subscribe(self, recv):
        requests.post(f"{self.url}/sub", json={"graph": [recv.dict()]})

    def unsubscribe(self, recv):
        requests.post(f"{self.url}/unsub", json=recv.dict())
