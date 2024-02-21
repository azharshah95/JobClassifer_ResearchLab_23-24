def init():
    global regions, systematik, dauer, unterrichtszeit, unterrichtsform, beginntermin
    regions_list = [
        "BAW",
        "BAY",
        "BER",
        "BRA",
        "BRE",
        "HAM",
        "HES",
        "MBV",
        "NDS",
        "NRW",
        "RPF",
        "SAA",
        "SAC",
        "SAN",
        "SLH",
        "TH%C3%9C",
        "iGB",
        "iP",
        "iCH",
        "iA",
        "iE"
    ]
    regions = regions_list

    # Unterrichtszeit: 1=Vollzeit, 2=Teilzeit.
    unterrichtszeit = [1, 2]

    # Systematik: C=Berufliche Qualifikation, D=Aufstiegsweiterbildung, CD=Systematiksuche.
    systematik = ["C", "D", "CD"]

    # Dauer: 0=Auf Anfrage, 1,2=bis eine Woche, 1,2,3=bis ein Monat, 1,2,3,4=bis drei Monate, 1,2,3,4,5=bis sechs Monate, 1,2,3,4,5,6=bis ein Jahr, 7,8,9=mehr als ein Jahr
    dauer = [
        "1",
        "2",
        "3",
        "4",
        "6",
        "7",
        "8",
        "9",
        "0"]

    # Unterrichtsform: 101=Präsenzveranstaltung, 102=Seminar, 103=Workshop, 104=Praxistraining, 105=Sonstige Präsenzveranstaltung, 201=Virtuelles Klassenzimmer, 202=Online-Seminar, 203=Online-Coaching, 204=Selbstlernmodul, 206=Sonstige digitale Lernformen, 301=Blended Learning, 302=Combined Learning, 303=Hybrid Learning, 304=Sonstige kombinierte Lernformen,401=Fernunterricht, 402=Fernlehrgang, 403=Sonstiger Fernunterricht. Mehrere Komma-getrennte Angaben möglich (z.B. uf=101,202).
    unterrichtsform = [
        101,
        102,
        103,
        104,
        105,
        201,
        202,
        203,
        204,
        206,
        301,
        302,
        303,
        304,
        401,
        402,
        403
    ]

    # Beginntermin (0=regelmäßiger Start, 1=diesen Monat, 2=Folgemonat, 3=in zwei Monaten, 4=in drei Monaten, 5=in mehr als drei Monaten)
    beginntermin = [0, 1, 2, 3, 4, 5, 6]
