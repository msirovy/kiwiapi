#!/usr/bin/env python3
#    --one-way (z tohoto udělej default option) indikuje potřebu zákazníka letět jenom jedním směrem, tedy pouze do nějakého místa
#    --return 5 by měla zabookovat let s cestujícím, který v destinaci zůstává 5 nocí,
#    --cheapest (default) zabookuje nejlevnější let a --fastest bude fungovat stejně
#    --bags 2 by měla zabookovat let se 2 zavazadly
#    --from a --to parametry potřebují podporu letiště IATA codes
#
# TESTS
# ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
# ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
# ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
# ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest


# cliUI part
try:
    import click
except ModuleNotFoundError:
    print("please install click module for python3 by command: pip3 install click")
    exit(1)

# API part
from requests import post, get
from json import loads, dumps

from datetime import datetime as dTime
from datetime import timedelta as tDelta
from dateutil import parser
from pprint import pprint


INFO = """
Token:      {booking_token}


From:       {cityFrom}
To:         {cityTo}

Fly detail
----------------------------------
departure:  {dTime}
arrive:     {aTime}
duration:   {fly_duration}
----------------------------------

Price:      {conversion}

"""

def fly_search(flyFrom, to, dateFrom, dateTo, returnFrom, returnTo, typeFlight, sort):
    """ Kiwi search api implementation
    """
    req='https://api.skypicker.com/flights?v=3&adults=1&limit=1'
    for k in ['flyFrom', 'to', 'dateFrom', 'dateTo', 'returnFrom', 'returnTo', 'typeFlight', 'sort']:
        if locals().get(k) not in ('None', -1):
            print(k)
            req += "&{}={}".format(k, locals().get(k))
    print(req)
    ret = loads(get(req).text)
    print(INFO.format_map(ret['data'][0]))
    return ret['data'][0]['booking_token']

def book_fly(booking_token, bags):
    data = {
        "currency": "EUR",
        "passengers": {
            0: {
                "email": "msirovy@gmail.com",
                "firstName": "Marek",
                "lastName": "Sirovy", 
                "documentID": "CZ6729H11HDJC762U3",
                "birthday": "10/05/1990", 
                "title": "Mr"
            },
        },
        "bags": bags,
        "booking_token": booking_token
    }
    ret = post('http://128.199.48.38:8080/booking', json=data).text
    print("Thanks for the booking... :-)")
    print(ret)


@click.command()
@click.option('--date', default=None, required=True,
                            help="Date when trip should begin")
@click.option('--from', 'depart', default=None, required=True,
                            help="Depart airport IATA code (where your trip should begins)")
@click.option('--to', 'arrive', default=None, required=True,
                            help="Arrive airport IATA code (where your trip should ends)")
@click.option('--fastest', 'sort', flag_value='duration', default=True,
                            help="Find fastest way to destination (DEFAULT)")
@click.option('--cheapest', 'sort', flag_value='price',
                            help="Find cheapest way to destination (You can use cheapest/fastest, do not both)")
@click.option('--bags', 'bags', default=0, type=int,
                            help="How many bags do you use")
@click.option('--one-way', 'typeFlight', flag_value="oneway", default=True,
                            help="Search one way fly (DEFAULT)")
@click.option('--return', 'typeFlight', default="oneway",
                            help="How many days you stay before return (do not use with --one-way option)")
def cli(date, depart, arrive, sort, bags, typeFlight=-1):
    date = parser.parse(date).strftime('%d/%m/%Y')
    click.echo("Please wait, searcing for flights with this parameters:")
    click.echo("- Depart date: %s" % date)
    click.echo("- Depart airport: %s" % depart)
    click.echo("- Arrive airport: %s" % arrive)
    click.echo("- Sort trips by: %s" % sort)
    click.echo("- Number of bags: %s" % bags)
    try:
        return_after = int(typeFlight)
        return_date = dTime.strptime(date, '%Y-%m-%d') + tDelta(return_after)
        return_date = return_date.strftime('%d/%m/%Y')
        click.echo("- Return date: %s" % return_date)
        typeFlight="return"
        
    except ValueError:
        click.echo("- Return date: One way trip")
        return_date="None"
        typeFlight="oneway"

    token = fly_search(flyFrom=depart, to=arrive, dateFrom=date, dateTo=date, returnFrom=return_date, returnTo=return_date, typeFlight=typeFlight, sort=sort)
    if click.confirm("Would you like to book flight (the price is without luggage)"): 
        book_fly(token, bags)

if __name__ == '__main__':
    cli()

