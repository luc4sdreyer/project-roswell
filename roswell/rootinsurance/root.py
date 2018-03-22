import requests

from rootinsurance.quote import GadgetQuote, TermQuote


class RootInsurance(object):
    def __init__(self, sandbox=False, key=None):
        self._url = "https://sandbox.root.co.za"
        self._base = self._url + "/v1/insurance/"
        self._key = key

    def post(self, path, json=None, **kwargs):
        if json:
            response = requests.post(self._base + path, json=json, auth=(self._key, ""))
        else:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(self._base + path, data=kwargs, headers=headers, auth=(self._key, ""))
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
    root = RootInsurance(sandbox=True,
                         key="sandbox_NzNmN2UzZDEtYzA2Ny00Y2I2LTgxMTItODdiMjU1ZjYzZTQ5LnNrZDMtc05yaVJsMHR4eEZ1aEZZWXVsMzZwTGNLeFBO")
    quotes = TermQuote(root,
                       cover_amount=50000000,
                       cover_period='1_year',
                       basic_income_per_month=1500000,
                       education_status='undergraduate_degree',
                       smoker=False,
                       gender='male',
                       age=33).get_quote()
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
