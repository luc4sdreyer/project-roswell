from collections import defaultdict

import apiai
from flask import Flask, request, jsonify

from rootinsurance.policy import Application, Policy
from rootinsurance.policyholder import PolicyHolder
from rootinsurance.quote import TermQuote
from rootinsurance.root import RootInsurance
from rootinsurance.utils import SouthAfricanID, Cellphone

from datetime import datetime
import random

app = Flask(__name__)
root = RootInsurance(
    key="sandbox_NzNmN2UzZDEtYzA2Ny00Y2I2LTgxMTItODdiMjU1ZjYzZTQ5LnNrZDMtc05yaVJsMHR4eEZ1aEZZWXVsMzZwTGNLeFBO")
ai = apiai.ApiAI("3cb50c0369bf48a4882be6edf1eb526a")
state = defaultdict(dict)


def _random_id_number():
    return _get_id_number(sequence=str(random.randint(999)))


def _get_id_number(year='86', month='05', day='06', gender='male', sequence='000'):
    id_num = '%s%s%s%s%s08' % (year, month, day, 4 if gender == 'female' else 5, sequence)
    odd = 0
    for i in xrange(len(id_num)):
        if (i % 2) == 0:
            odd += int(id_num[i])

    even = ''
    for i in xrange(len(id_num)):
        if (i % 2) == 1:
            even += id_num[i]

    even = int(even) * 2
    even = sum(map(lambda x: int(x), str(even)))
    total = even + odd

    control = str(10 - int(str(total)[-1]))
    id_num += control
    return id_num


def _create_policyholder(firstname, lastname, id, email=None, cellphone=None):
    policyHolder = PolicyHolder(id=SouthAfricanID(number=id),
                                first_name=firstname,
                                last_name=lastname,
                                email=email,
                                cellphone=(Cellphone(number=cellphone) if cellphone else None))
    return policyHolder.save(root)


def _create_quote(cover_amount, cover_period, gender, age):
    quote = TermQuote(root,
                      cover_amount=cover_amount,
                      cover_period=cover_period,
                      basic_income_per_month=1500000,
                      education_status=TermQuote.EDUCATION_UNDERGRADUATE,
                      smoker=False,
                      gender=gender,
                      age=age)
    return quote.get_quote()


def _get_period(param):
    period = param['amount']
    if 1 <= period < 2:
        return TermQuote.DURATION_1_YEAR
    if 2 <= period < 5:
        return TermQuote.DURATION_2_YEAR
    if 5 <= period < 10:
        return TermQuote.DURATION_5_YEAR
    if 10 <= period < 15:
        return TermQuote.DUATION_10_YEAR
    if 15 <= period < 20:
        return TermQuote.DURATION_15_YEAR
    if period == 20:
        return TermQuote.DURATION_20_YEAR
    if period > 20:
        return TermQuote.DURATION_LIFE


def _gender_from_id(param):
    if param[6] == '5':
        return 'male'
    return 'female'


def _age_from_id(param):
    dateStr = param[0:6]
    now = datetime.now()
    birthday = datetime.strptime(dateStr, '%y%m%d')
    difference = now - birthday
    return int(difference.days / 365.25)


def cents_to_rands(suggested_premium):
    return "R" + str((suggested_premium / 100))


@app.route("/api/", methods=["POST"])
def api():
    try:
        req = request.json
        print(request.json)
        parameters = req['result']['parameters']
        sessionid = req['sessionId']
        if parameters['request_type'] == 'quote':
            id_number = _get_id_number()
            parameters['id_number'] = id_number

            quote = _create_quote(cover_amount=parameters['cover_amount'],
                                  cover_period=_get_period(parameters['period']),
                                  gender=_gender_from_id(parameters['id_number']),
                                  age=_age_from_id(parameters['id_number']))

            state[sessionid].update({'quote': quote, 'id_number': parameters['id_number']})
            response = "Your monthly premium will be " + cents_to_rands(
                quote[0].suggested_premium) + ". Is this OK?"
            return jsonify({"speech": response, "displayText": response})

        if parameters['request_type'] == 'buy_policy':
            quote = state[sessionid]['quote']
            id = state[sessionid]['id_number']

            policy_holder = _create_policyholder(firstname=parameters['first_name'],
                                                 lastname=parameters['last_name'],
                                                 id=id, email=None, cellphone=None)
            application = Application.apply(quote[0], policy_holder, quote[0].suggested_premium)
            state[sessionid].update({'application': application, 'policy_holder': policy_holder})

            r = ai.text_request()
            r.session_id = sessionid
            r.query = "Hello"
            r.getresponse()

            response = "One more step to go :) Happy to go ahead?"
            return jsonify({"speech": response, "displayText": response})

        if parameters['request_type'] == 'confirm':
            application = state[sessionid]['application']
            policy = Policy.issue(application=application)

            state[sessionid].update({'policy': policy})
            response = "Congratulations! you are now have your very own tin-foil hat! Your policy number is: " + policy.policy_number
            return jsonify({"speech": response, "displayText": response})

        #     response = "I am afraid I don't know about %s" % raw_coin
        #     return jsonify({"speech": response, "displayText": response})
        #
        # price = coin_price_per_coin(coin)
        # if not price:
        #     response = "I am afraid I don't know the price of %s" % raw_coin
        # else:
        #     response = "The price of %s is $%s" % (currency[coin], price['USD'])
        return jsonify({})
    except AttributeError as e:
        return jsonify({"speech": e, "displayText": e})


@app.route("/")
def main():
    return "Welcome!"


def cli(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    cli("0.0.0.0", 8080, True)
