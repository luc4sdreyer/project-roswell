from roswell.rootinsurance.utils import Cellphone, ID


class Application(object):
    def __init__(self, root, **kwargs):
        self._root = root
        self._v = kwargs

    def __getattr__(self, item):
        return self._v.get(item, None)

    @staticmethod
    def apply(quotepackage, policyholder, monthly_premium):
        _root = quotepackage._root
        _v = {
            'quote_package_id': quotepackage.quote_package_id,
            'policyholder_id': policyholder.policyholder_id,
            'monthly_premium': monthly_premium
        }
        _v.update(quotepackage.get_requirements())

        response = _root.post("applications", **_v)
        return Application(_root, **response.json())


class Beneficiary(object):
    def __init__(self, first_name, last_name, id, percentage, cellphone=None):
        self._v = {
            'first_name': first_name,
            'last_name': last_name,
            'id': id,
            'percentage': percentage,
            'cellphone': cellphone,
        }

    def __getattr__(self, item):
        return self._v.get(item, None)

    @staticmethod
    def from_primitive(primitive):
        return Beneficiary(first_name=primitive['first_name'],
                           last_name=primitive['last_name'],
                           percentage=primitive['percentage'],
                           id=ID.from_primitive(primitive['id']),
                           cellphone=Cellphone.from_primitive(primitive['cellphone']))

    def to_primitive(self):
        _v = {}
        _v.update(self._v)
        _v['id'] = _v['id'].to_primitive() if isinstance(_v['id'], ID) else _v['id']
        _v['cellphone'] = _v['cellphone'].to_primitive() if isinstance(_v['cellphone'], Cellphone) else _v['cellphone']
        return _v


class Policy(object):
    def __init__(self, root, bound=False, **kwargs):
        self._root = root
        self._bound = bound
        self._v = kwargs

    def __getattr__(self, item):
        if item == 'beneficiaries':
            return [Beneficiary(**x) for x in self._v.get(item, [])]
        return self._v.get(item, None)

    def save(self):
        if not self._bound:
            # error we need a root object in this case
            return

        params = {}
        if self.app_data:
            params['app_data'] = self.app_data
        response = self._root.patch("policy/" + self.policy_id, **params)
        return Policy(bound=True, root=self._root, **(response.json()))

    def cancel(self, reason=""):
        if not self._bound:
            # error we need a root object in this case
            return

        params = {}
        if self.app_data:
            params['reason'] = reason
        response = self._root.post("policy/" + self.policy_id + "/cancel", **params)
        return Policy(bound=True, root=self._root, **(response.json()))

    def billing(self, billing_amount):
        if not self._bound:
            # error we need a root object in this case
            return

        params = {}
        if self.app_data:
            params['billing_amount'] = billing_amount
        response = self._root.post("policy/" + self.policy_id + "/billing", **params)
        return Policy(bound=True, root=self._root, **(response.json()))

    def events(self):
        if not self._bound:
            return []
        response = self._root.get("policy/" + self.policy_id + "/events")
        return response.json()

    def beneficiaries(self):
        if not self._bound:
            return []
        response = self._root.get("policy/" + self.policy_id + "/beneficiaries")
        return [Beneficiary(**x) for x in response.json()]

    def update_beneficiaries(self, beneficiaries):
        if not self._bound:
            # error we need a root object in this case
            return

        primitive_beneficiaries = [x.to_primitive() for x in beneficiaries]
        response = self._root.put("policy/" + self.policy_id + "/beneficiaries", json=primitive_beneficiaries)



    @staticmethod
    def issue(application, app_data={}):
        _root = application._root
        _v = {
            'application_id': application.application_id,
            'app_data': app_data
        }
        response = _root.post("policies", **_v)
        return Policy(_root, **response.json())

    @staticmethod
    def list(root, id_number=""):
        response = root.get("policies/" + id_number)
        return [Policy(root, bound=True, **x) for x in response.json()]

    @staticmethod
    def get(root, policy_id):
        response = root.get("policyholders/" + policy_id)
        params = {
            'root': root,
            'bound': True
        }
        params.update(response.json())
        return Policy(**params)
