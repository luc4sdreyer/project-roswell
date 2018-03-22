from rootinsurance.utils import ID, Cellphone


class PolicyHolder(object):
    def __init__(self, id=None, date_of_birth=None, first_name=None, last_name=None, email=None, cellphone=None,
                 gender=None, app_data=None, policyholder_id=None, root=None, bound=False, **kwargs):
        self._bound = bound
        self._root = root
        if isinstance(id, dict):
            self._id = ID.from_primitive(id)
        else:
            self._id = id
        if isinstance(cellphone, dict):
            self._cellphone = Cellphone.from_primitive(cellphone)
        else:
            self._cellphone = cellphone
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._app_data = app_data
        self._policyholder_id = policyholder_id
        self._other = kwargs

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def cellphone(self):
        return self._cellphone

    @cellphone.setter
    def cellphone(self, value):
        self._cellphone = value

    @property
    def app_data(self):
        return self._app_data

    @app_data.setter
    def app_data(self, value):
        self._app_data = value

    @property
    def id(self):
        return self._id

    @property
    def policyholder_id(self):
        return self._policyholder_id

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def gender(self):
        return self._gender

    def save(self, root=None):
        if not root:
            root = self._root

        if not (self._bound or root):
            # error we need a root object in this case
            pass

        if self._bound:
            params = {}
            if self.email:
                params['email'] = self.email
            if self.cellphone and isinstance(self.cellphone, Cellphone):
                params['cellphone'] = self.cellphone.to_primitive()
            if self.app_data:
                params['app_data'] = self.app_data
            response = root.patch("policyholders/" + self.policyholder_id, **params)
        else:
            params = {
                'id': self.id.to_primitive(),
                'date_of_birth': self.date_of_birth,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'gender': self.gender
            }
            if self.email:
                params['email'] = self.email
            if self.cellphone:
                params['cellphone'] = self.cellphone.to_primitive()
            if self.app_data:
                params['app_data'] = self.app_data
            response = root.post("policyholders", json=params)
        return PolicyHolder(bound=True, root=root, **(response.json()))

    @staticmethod
    def get(root, policyholder_id):
        response = root.get("policyholders/" + policyholder_id)
        params = {
            'root': root,
            'bound': True
        }
        params.update(response.json())
        return PolicyHolder(**params)

    @staticmethod
    def list(root, id_number=""):
        response = root.get("policyholders/" + id_number)
        return [PolicyHolder(bound=True, **x) for x in response.json()]

