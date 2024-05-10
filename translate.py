
class Translate:

    def __init__(self):

        self.arg_names = ['O', 'B-Subsumtion', 'I-Subsumtion', 'B-Entscheidung des EGMR', 'I-Entscheidung des EGMR',
                    'B-Vorherige Rechtsprechung des EGMR', 'I-Vorherige Rechtsprechung des EGMR',
                   'B-Intitutionelle Argumente - Einschätzungsspielraum/Margin of Appreciation',
                   'I-Intitutionelle Argumente - Einschätzungsspielraum/Margin of Appreciation',
                   'B-Intitutionelle Argumente - Distinguishing', 'I-Intitutionelle Argumente - Distinguishing',
                   'B-Intitutionelle Argumente - Overruling', 'I-Intitutionelle Argumente - Overruling',
                   'B-Verhältnismäßigkeitsprüfung - Angemessenheit/Erforderlichkeit',
                   'I-Verhältnismäßigkeitsprüfung - Angemessenheit/Erforderlichkeit',
                   'B-Verhältnismäßigkeitsprüfung - Geeignetheit', 'I-Verhältnismäßigkeitsprüfung - Geeignetheit',
                   'B-Verhältnismäßigkeitsprüfung - Legitimer Zweck', 'I-Verhältnismäßigkeitsprüfung - Legitimer Zweck' ,
                   'B-Verhältnismäßigkeitsprüfung - Rechtsgrundlage', 'I-Verhältnismäßigkeitsprüfung - Rechtsgrundlage',
                   'B-Auslegungsmethoden - Rechtsvergleichung', 'I-Auslegungsmethoden - Rechtsvergleichung',
                   'B-Auslegungsmethoden - Sinn & Zweck', 'I-Auslegungsmethoden - Sinn & Zweck',
                   'B-Auslegungsmethoden - Systematische Auslegung', 'I-Auslegungsmethoden - Systematische Auslegung',
                   'B-Auslegungsmethoden - Historische Auslegung', 'I-Auslegungsmethoden - Historische Auslegung',
                   'B-Auslegungsmethoden - Wortlaut', 'I-Auslegungsmethoden - Wortlaut',
                   'B-Konsens der prozessualen Parteien', 'I-Konsens der prozessualen Parteien']

        self.cln_names = self.clean_names()

        self.dictionary = {"Verhältnismäßigkeitsprüfung": "Test of the principle of proportionality",
                      "Auslegungsmethoden": "Method of interpretation",
                      "Intitutionelle Argumente": "Institutional arguments",
                      "Historische Auslegung": "Historical interpretation",
                      "Rechtsvergleichung": "Comparative law",
                      "Systematische Auslegung": "Systematic interpretation",
                      "Wortlaut": "Textual interpretation",
                      "Wortlaut Auslegung": "Textual interpretation",
                      "Sinn & Zweck": "Teleological interpretation",
                      "Sinn & Zweck Auslegung": "Teleological interpretation",
                      "Angemessenheit/Erforderlichkeit": "Necessity/Proportionality",
                      "Angemessenheit": "Necessity",
                      "Erforderlichkeit": "Proportionality",
                      "Geeignetheit": "Suitability",
                      "Legitimer Zweck": "Legitimate purpose",
                      "Rechtsgrundlage": "Legal basis",
                      "Einschätzungsspielraum/Margin of Appreciation": "Margin of Appreciation",
                      "Einschätzungsspielraum": "Margin of Appreciation",
                      "Entscheidung des EGMR": "Decision of the ECHR",
                      "Vorherige Rechtsprechung des EGMR": "Precedents of the ECHR",
                      "Subsumtion": "Application to the concrete case",
                      "Konsens der prozessualen Parteien": "Non contestation by the parties"}

    def clean_names(self):
        clean_names = list(set(["-".join(name.split("-")[1:]) for name in self.arg_names if name]))
        clean_names = [name for name in clean_names if name]
        return clean_names

    def translate(self, names):
        new_name = []
        if " – " in names:
            splitted = names.split(" – ")
        else:
            splitted = names.split(" - ")
        for part in splitted:
            try:
                new_name.append(self.dictionary[part])
            except:
                new_name.append(part)
        return " - ".join(new_name)


if __name__ == '__main__':
    T = Translate()
    for name in sorted(T.cln_names):
        print(T.translate(name))