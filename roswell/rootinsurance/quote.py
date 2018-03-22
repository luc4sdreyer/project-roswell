class Quote(object):
    def __init__(self, root, **kwargs):
        self._data = kwargs
        self._root = root

    def __getattr__(self, item):
        return self._data.get(item, None)

    def to_primitive(self):
        return self._data

    @staticmethod
    def from_primitive(root, primitive):
        if primitive['type'] == 'root_gadgets':
            return GadgetQuote(root, **primitive)
        if primitive['type'] == 'root_funeral':
            return GadgetQuote(root, **primitive)
        if primitive['type'] == 'root_term':
            return GadgetQuote(root, **primitive)

    def get_quote(self):
        response = self._root.post('quote', **self.to_primitive())
        # TODO: add some error checking
        print("Response [%s] - %s" % (response.status_code, response.text))
        if response.status_code != 200:
            raise AttributeError("Invalid Quote")
        return [QuotePackage(self._root, **x) for x in response.json()]


class GadgetQuote(Quote):
    def __init__(self, root, model_name=None, make=None, model=None, type='root_gadgets'):
        opts = {
            'type': type,
            'model_name': model_name,
            'make': make,
            'model': model,
        }
        super(GadgetQuote, self).__init__(root, **opts)

    def set_requirements(self, serial_number):
        return {'serial_number': serial_number}


class FuneralQuote(Quote):
    def __init__(self, root, cover_amount, has_spouse, number_of_children, extended_family_ages, type='root_funeral'):
        opts = {
            'type': type,
            'cover_amount': cover_amount,
            'has_spouse': has_spouse,
            'number_of_children': number_of_children,
            'extended_family_ages': extended_family_ages
        }
        super(FuneralQuote, self).__init__(root, **opts)

    def set_requirements(self, spouse_id=None, children_ids=None, extended_family_ids=None):
        return {'spouse_id': spouse_id,
                'children_ids': children_ids,
                'extended_family_ids': extended_family_ids}


class TermQuote(Quote):
    DURATION_1_YEAR = '1_year'
    DURATION_2_YEAR = '2_years'
    DURATION_5_YEAR = '5_years'
    DURATION_10_YEAR = '10_years'
    DURATION_15_YEAR = '15_years'
    DURATION_20_YEAR = '20_years'
    DURATION_LIFE = 'whole_life'

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    EDUCATION_NO_MATRIC = 'grade_12_no_matric'
    EDUCATION_MATRIC = 'grade_12_matric'
    EDUCATION_DIPLOMA = 'diploma_or_btech'
    EDUCATION_UNDERGRADUATE = 'undergraduate_degree'
    EDUCATION_PROFESSIONAL = 'professional_degree'

    def __init__(self, root, cover_amount, cover_period, basic_income_per_month, education_status, smoker, gender, age,
                 type='root_term'):
        opts = {
            'type': type,
            'cover_amount': cover_amount,
            'cover_period': cover_period,
            'basic_income_per_month': basic_income_per_month,
            'education_status': education_status,
            'smoker': smoker,
            'gender': gender,
            'age': 18
        }
        super(TermQuote, self).__init__(root, **opts)

    def set_requirements(self):
        return {}


class QuotePackage(object):
    def __init__(self, root, **primitive):
        self._root = root
        self._v = primitive
        self._application = {}

    def __getitem__(self, item):
        return self._v.get(item, None)

    def __getattr__(self, item):
        if item == "module":
            return Quote.from_primitive(self._root, self._v[item])
        return self._v.get(item, None)

    def set_requirements(self, **kwargs):
        self._application = self.module.set_requirements(**kwargs)

    def get_requirements(self):
        return self._application
