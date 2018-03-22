from collections import defaultdict
from flask import Flask, request, jsonify

from rootinsurance.policy import Application, Policy
from rootinsurance.policyholder import PolicyHolder
from rootinsurance.quote import TermQuote
from rootinsurance.root import RootInsurance
from rootinsurance.utils import SouthAfricanID, Cellphone

from datetime import datetime

app = Flask(__name__)
root = RootInsurance(
    key="sandbox_NzNmN2UzZDEtYzA2Ny00Y2I2LTgxMTItODdiMjU1ZjYzZTQ5LnNrZDMtc05yaVJsMHR4eEZ1aEZZWXVsMzZwTGNLeFBO")

state = defaultdict(dict)


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
    return int(difference.days/365.25)


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

            policy_holder = _create_policyholder(firstname=parameters['last_name'],
                                                 lastname=parameters['first_name'],
                                                 id=id, email=None, cellphone=None)
            application = Application.apply(quote[0], policy_holder, quote[0].suggested_premium)
            policy = Policy.issue(application=application, )





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


def cli(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    cli("0.0.0.0", 8080, True)
