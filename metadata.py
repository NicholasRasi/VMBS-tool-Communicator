import requests


class Metadata:
    PROVIDER_APIS = {"AWS": "http://169.254.169.254/latest/dynamic/instance-identity/document",
                     "AZURE": "http://169.254.169.254/metadata/instance?api-version=2019-06-01"}

    def __init__(self):
        self.response_metadata = None
        self.metadata = {}

        self.get_provider()
        self.get_metadata()

    def get_provider(self):
        for provider in self.PROVIDER_APIS:
            req = requests.get(self.PROVIDER_APIS[provider], headers={'Metadata': 'true'})
            if req.status_code == 200:
                self.response_metadata = req.json()
                print(self.response_metadata)
                self.metadata["provider"] = provider
                break

    def get_metadata(self):
        # parse metadata
        if self.metadata["provider"] == "AWS":
            self.metadata["id"] = self.response_metadata["instanceId"]
            self.metadata["region"] = self.response_metadata["region"]
            self.metadata["zone"] = self.response_metadata["availabilityZone"]
            self.metadata["type"] = self.response_metadata["instanceType"]
        elif self.metadata["provider"] == "AZURE":
            self.metadata["id"] = self.response_metadata["compute"]["name"]
            self.metadata["region"] = self.response_metadata["compute"]["location"]
