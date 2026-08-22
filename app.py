import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# UBUBIKO BW'AMATEGEKO Y'U RWANDA - YASOBANUTSE NEZA MU KINYARWANDA N'ICYONGEREZA
LAW_DATABASE = {
    "1": {
        "title_rw": "Itegeko Nshinga rya Repubulika y'u Rwanda",
        "title_en": "Constitution of the Republic of Rwanda",
        "icon": "⚖️",
        "color": "emerald",
        "content_rw": "Ingingo ya 1: Umuryango nyarwanda uteye imbere ku bumwe n'ubwiyunge. Ingingo ya 10: Demokarasi n'uburenganzira bwa muntu ntibwogerwa. Ingingo ya 13: Agaciro k'umuntu kanyuranyije n'iyica rubzo.",
        "content_en": "Article 1: The Rwandan State is a Republic. Article 10: Core values of rule of law and human rights. Article 13: Inviolability of human dignity.",
        "penalty_rw": "IBIHANO: Ikintu cyose, itegeko cyangwa gikorwa kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).",
        "penalty_en": "SANCTION: Any law, act, or decree contrary to the Constitution is null and void under the law.",
        "tags": "itegeko nshinga, constitution, uburenganzira, nshinga, muntu, agaciro"
    },
    "2": {
        "title_rw": "Itegeko ry'Ibyaha n'Ibano (Penal Code)",
        "title_en": "Penal Code of Rwanda",
        "icon": "🚨",
        "color": "rose",
        "content_rw": "Ingingo ya 120 (Ubujura): Gufata ikintu cy'undi utabyemerewe. Ingingo ya 166 (Gukubita/Gukomeretsa): Gukubita cyangwa gukomeretsa ku bushake bitera ubumuga buhoraho. Ingingo ya 211: Ruswa n'ibyaha bifitanye isano na yo.",
        "content_en": "Article 120 (Theft): Fraudulent appropriation of another's property. Article 166 (Assault): Intentional assault causing permanent disability. Article 211: Corruption and related offenses.",
        "penalty_rw": "IBIHANO: Ubujura buhanishwa igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande kuva kuri 100,000 Frw kugeza kuri 500,000 Frw. Gukubita bihanishwa igifungo cy'imyaka 5 kugeza kuri 7.",
        "penalty_en": "PENALTY: Petty theft is punishable by 6 months to 2 years prison and a fine of 100k to 500k RWF. Assault is punishable by 5 to 7 years imprisonment.",
        "tags": "ibyaha, penal, ubujura, theft, gukubita, ruswa, igifungo, amande, gukomeretsa"
    },
    "3": {
        "title_rw": "Itegeko ry'Umuryango n'Abantu (Family Law)",
        "title_en": "Law Governing Persons and Family",
        "icon": "🏠",
        "color": "violet",
        "content_rw": "Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. Ingingo ya 52: Ubutane (Divorce) bushobora kwemezwa n'inkiko gusa. Ingingo ya 88: Abana bose bafite uburenganzira bungana ku izungura.",
        "content_en": "Article 35 (Marriage): Only civil marriage is legally recognized. Article 52: Divorce can only be granted by competent courts. Article 88: Equal succession and inheritance rights for all children.",
        "penalty_rw": "IBIHANO: Gusezerana mu buryo bwa magendu cyangwa gushaka ubugira kabiri (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1 n'amande.",
        "penalty_en": "PENALTY: Illegal marriage or bigamy is strictly prohibited and punishable by 6 months to 1 year imprisonment.",
        "tags": "umuryango, family, gushyingirwa, marriage, izungura, ubutane, divorce, abana"
    },
    "4": {
        "title_rw": "Itegeko ry'Umurimo mu Rwanda (Labor Law)",
        "title_en": "Law Governing Labor in Rwanda",
        "icon": "💼",
        "color": "amber",
        "content_rw": "Ingingo ya 12: Amasezerano y'akazi agomba kwandikwa. Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. Ingingo ya 45: Akazi k'abana munsi y'imyaka 13 karabujijwe burundu.",
        "content_en": "Article 12: Employment contracts must be in writing. Article 28: Mandatory 1-month termination notice. Article 45: Child labor under 13 years is strictly prohibited.",
        "penalty_rw": "IBIHANO: Umukoresha wishe iri tegeko ryo kwirukana umukozi nta nteguza, ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (Notice indemnity).",
        "penalty_en": "PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.",
        "tags": "akazi, umurimo, contract, fire, kwirukanwa, umushahara, notice, amasezerano"
    },
    "5": {
        "title_rw": "Amategeko y'Umuhanda n'Ibyapa (Traffic Regulations)",
        "title_en": "Traffic and Road Safety Regulations",
        "icon": "🚗",
        "color": "blue",
        "content_rw": "Ingingo ya 14: Gutwara ikinyabiziga nta permis cyangwa uruhushya rwo gutwara rwemewe. Ingingo ya 22: Kurenza umuvuduko itandukanyijwe n'ibyapa (Speeding) mu mihanda.",
        "content_en": "Article 14: Driving without a valid driver's license. Article 22: Exceeding speed limits specified by road signs.",
        "penalty_rw": "IBIHANO: Gutwara nta permis bihanishwa amande ya 50,000 Frw no gufatira ikinyabiziga n'igipolisi. Kurenza umuvuduko (Speeding) bihanishwa amande ya 25,000 Frw.",
        "penalty_en": "PENALTY: Driving without a license attracts a 50,000 RWF fine and vehicle impoundment. Exceeding speed limits (Speeding) attracts a 25,000 RWF fine.",
        "tags": "umuhanda, imodoka, permis, license, amande, police, vitesse, ibyapa"
    },
    "6": {
        "title_rw": "Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)",
        "title_en": "Cybercrimes and Cybersecurity Law",
        "icon": "💻",
        "color": "cyan",
        "content_rw": "Ingingo ya 32: Kwinjira mu buryo butemewe mu miterere ya mudasobwa cyangwa uburyo bw'itumanaho bw'undi muntu. Ingingo ya 38: Guhimba cyangwa guhindura amakuru mu buryo bw'uburyarya.",
        "content_en": "Article 32: Unauthorized hacking or access to a computer system. Article 38: Data forgery and cyber fraud.",
        "penalty_rw": "IBIHANO: Igifungo kuva ku mwaka 1 kugeza ku myaka 3 n'amande kuva kuri miliyoni 1 kugeza kuri miliyoni 3 Frw.",
        "penalty_en": "PENALTY: Imprisonment from 1 to 3 years and a fine of 1,000,000 RWF to 3,000,000 RWF.",
        "tags": "internet, cybersecurity, cybercrime, mudasobwa, hacking, guhimba"
    },
    "7": {
        "title_rw": "Itegeko ry'Uburenganzira bw'Umwana (Child Protection)",
        "title_en": "Law on Child Protection and Rights",
        "icon": "👶",
        "color": "indigo",
        "content_rw": "Ingingo ya 5: Umwana wese afite uburenganzira bwo kwandikwa mu bitabo by'amajwi y'abavutse. Ingingo ya 18: Gukubita n'ibihano bibabaza umubiri ku mwana birabujijwe haba mu rugo cyangwa ku ishuri.",
        "content_en": "Article 5: Every child has a right to be registered at birth. Article 18: Corporal punishment and abuse of children are strictly prohibited at home and school.",
        "penalty_rw": "IBIHANO: Umuntu wese gukubita cyangwa guhohotera umwana bihannywe n'amategeko y'ibyaha, bishobora kuvamo igifungo kuva ku mezi 2 kugeza ku myaka 2.",
        "penalty_en": "PENALTY: Anyone who subjects a child to corporal punishment faces imprisonment of 2 months to 2 years.",
        "tags": "umwana, child, uburenganzira, protection, ishuri, gukubita"
    }
}

# --- LUXURY MULTI-PAGE TEMPLATE WITH LIVE JAVASCRIPT NAVIGATION ---
@app.route("/", methods=["GET"])
def dashboard():
    laws_list = []
    for k, v in LAW_DATABASE.items():
        laws_list.append({
            "id": k,
            "title_rw": v["title_rw"],
            "title_en": v["title_en"],
            "icon": v["icon"],
            "color": v["color"],
            "content_rw": v["content_rw"],
            "content_en": v["content_en"],
            "penalty_rw": v["penalty_rw"],
            "penalty_en": v["penalty_en"],
            "tags": v["tags"]
        })

