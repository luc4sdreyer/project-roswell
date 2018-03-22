import requests

from rootinsurance.policy import Application
from rootinsurance.policyholder import PolicyHolder
from rootinsurance.quote import GadgetQuote


class RootInsurance(object):
    def __init__(self, sandbox=False, key=None):
        self._url = "https://sandbox.root.co.za"
        self._base = self._url + "/v1/insurance/"
        self._key = key

    def post(self, path, json=None, **kwargs):
        if json:
            response = requests.post(self._base + path, json=json, auth=(self._key, ""))
        else:
            response = requests.post(self._base + path, data=kwargs, auth=(self._key, ""))
        return response

    def put(self, path, **params):
        response = requests.post(self._base + path, json=params, auth=(self._key, ""))
        return response

    def get(self, path, **params):
        response = requests.get(self._base + path, params=params, auth=(self._key, ""))
        return response

    def patch(self, path, **params):
        response = requests.patch(self._base + path, json=params, auth=(self._key, ""))
        return response


def main():
    # root = RootInsurance(sandbox=True, key="")
    # quotes = GadgetQuote(root, model_name='iPhone 6s 64GB LTE').get_quote()
    # policyHolder = PolicyHolder.get(root, "de7548d0-11db-45db-a05c-773c4fa19b18")
    # # policyHolder = PolicyHolder(SouthAfricanID(number="1234567"),
    # #                             date_of_birth="19840524",
    # #                             first_name="David",
    # #                             last_name="Ellefsen",
    # #                             email="david+juliettsandbox@ellefsen.za.net",
    # #                             cellphone=Cellphone(number="0833757169"))
    # # boundPolicyHolder = policyHolder.save(root)
    # # policyHolders = PolicyHolder.list(root)
    # # policyHolder.email = "david@ellefsen.za.net"
    # # policyHolder.save()
    # quotes[0].set_requirements(serial_number="1234567890")
    # application = Application.apply(quotes[0], policyHolder, quotes[0].suggested_premium)

    a = 5
    pass


if __name__ == '__main__':
    main()

