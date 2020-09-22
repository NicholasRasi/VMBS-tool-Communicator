import requests


class Metadata:
    PROVIDER_APIS = {"AWS": "http://169.254.169.254/latest/dynamic/instance-identity/document",
                     "AZURE": "http://169.254.169.254/metadata/instance?api-version=2019-06-01",
                     "GCP": "http://metadata.google.internal/computeMetadata/v1/instance/?recursive=true",
                     "EGI": "http://169.254.169.254/openstack/latest/meta_data.json"}

    def __init__(self):
        self.response_metadata = None
        self.metadata = {}

        self.get_provider()
        self.get_metadata()

    def get_provider(self):
        for provider in self.PROVIDER_APIS:
            try:
                req = requests.get(self.PROVIDER_APIS[provider],
                                   headers={'Metadata': 'true', 'Metadata-Flavor': 'Google'})
                if req.status_code == 200:
                    self.response_metadata = req.json()
                    print(self.response_metadata)
                    self.metadata["provider"] = provider
                    break
            except requests.exceptions.RequestException as e:
                pass


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
            self.metadata["group"] = self.response_metadata["compute"]["resourceGroupName"]
        elif self.metadata["provider"] == "GCP":
            self.metadata["id"] = self.response_metadata["name"]
            zone = self.response_metadata["zone"]
            type = self.response_metadata["machineType"]
            self.metadata["zone"] = zone[zone.rfind("/")+1:]
            self.metadata["type"] = type[type.rfind("/")+1:]
        elif self.metadata["provider"] == "EGI":
            self.metadata["id"] = self.response_metadata["name"]
