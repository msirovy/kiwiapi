KIWIapi uloha
=============


Vyhledání letu
--------------
Jedním z úkolů téhle aplikace má být vyhledání nejrychlejšího nebo nejlevnějšího letu. A k tomu ti pomůže API od Kiwi.com. V Kiwi.com používáme jednoduchá API založená na HTTP, obvykle s payload v JSON formátu. A jestli jsi API ještě nikdy nepoužíval, klikni na tento odkaz:

  ```https://api.skypicker.com/flights?v=3&daysInDestinationFrom=6&daysInDestinationTo=7&flyFrom=49.2-16.61-250km&to=dublin_ie&dateFrom=03/04/2018&dateTo=09/04/2018&typeFlight=return&adults=1&limit=60```

Naše API pro hledání letů jsou veřejná, takže můžeš dokumentaci najít v Apiary.

Bookujeme
---------
Jakmile máš vybraný let, je na čase ho zabookovat. Pro rezervaci letu potřebuješ použít booking API (vytvořili jsme ho pro účely tohoto úkolu a nikdo po tobě nebude požadovat platbu za let):

  ```http://128.199.48.38:8080/booking```

Svět není perfektní a ne všechny projekty mají dokonalou dokumentaci. To se bohužel týká i tohoto API. Musíš zjistit, jak to funguje a zabookovat let. Hodně štěstí!

Spuštění aplikace
-----------------
Takhle spuštění tve aplikace musí fungovat:

```
  ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
  ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
  ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
  ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest
  

  --one-way (z tohoto udělej default option) indikuje potřebu zákazníka letět jenom jedním směrem, tedy pouze do nějakého místa
  --return 5 by měla zabookovat let s cestujícím, který v destinaci zůstává 5 nocí,
  --cheapest (default) zabookuje nejlevnější let a --fastest bude fungovat stejně
  --bags 2 by měla zabookovat let se 2 zavazadly
  --from a --to parametry potřebují podporu letiště IATA codes
```

Cele zadani
-----------
https://engeto.online/study/lesson/_wl9/unit/_36ZR
