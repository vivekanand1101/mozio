import pycountry

LANGUAGES = [(lang.iso639_3_code, lang.name)
             for lang in sorted(pycountry.languages, key=lambda x: x.name)]

CURRENCIES = [(cur.letter, cur.name)
              for cur in sorted(pycountry.currencies, key=lambda x: x.name)]
