import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# UBUBIKO BW'AMATEGEKO Y'U RWANDA N'IBIHANO (PYTHON DICTIONARY)
LAW_DATABASE = {
    "1": {
        "title_rw": "Itegeko Nshinga rya Repubulika y'u Rwanda",
        "title_en": "Constitution of Rwanda",
        "content_rw": "Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 13: Agaciro k'umuntu ntibwogerwa. IBIHANO: Ikintu cyose kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).",
        "content_en": "Article 1: The Rwandan State is a Republic. Article 13: Inviolability of human dignity. SANCTION: Any law or act contrary to the Constitution is null and void.",
        "tags": "itegeko nshinga, constitution, uburenganzira"
    },
    "2": {
        "title_rw": "Itegeko ry'Ibyaha n'Ibano (Penal Code)",
        "title_en": "Penal Code of Rwanda",
        "content_rw": "Ingingo ya 120 (Ubujura): IBIHANO: Igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande ari hagati ya 100,000 Frw na 500,000 Frw. Ingingo ya 166 (Gukubita/Gukomeretsa): IBIHANO: Igifungo cy'imyaka 5 kugeza kuri 7 n'amande.",
        "content_en": "Article 120 (Theft): PENALTY: Imprisonment of 6 months to 2 years and a fine of 100k to 500k RWF. Article 166 (Assault): PENALTY: Imprisonment of 5 to 7 years.",
        "tags": "ibyaha, penal, ubujura, theft, gukubita"
    },
    "3": {
        "title_rw": "Itegeko ry'Umuryango n'Abantu (Family Law)",
        "title_en": "Law Governing Persons and Family",
        "content_rw": "Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. IBIHANO: Gusezerana mu buryo bwa magendu (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1.",
        "content_en": "Article 35 (Marriage): Only civil marriage is recognized. PENALTY: Illegal marriage or bigamy is punishable by 6 months to 1 year imprisonment.",
        "tags": "umuryango, family, gushyingirwa, marriage, izungura"
    },
    "4": {
        "title_rw": "Itegeko ry'Umurimo mu Rwanda (Labor Law)",
        "title_en": "Law Governing Labor in Rwanda",
        "content_rw": "Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. IBIHANO: Umukoresha wishe iri tegeko ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (1 month notice salary damage).",
        "content_en": "Article 28: 1-month termination notice. PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.",
        "tags": "akazi, umurimo, contract, fire, kwirukanwa"
    },
    "5": {
        "title_rw": "Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)",
        "title_en": "Traffic Regulations",
        "content_rw": "Ingingo ya 14 (Gutwara nta permis): IBIHANO: Amande ya 50,000 Frw no gufatira ikinyabiziga. Ingingo ya 22 (Kurenza umuvuduko/Speeding): IBIHANO: Amande y'amafaranga 25,000 Frw ako kanya.",
        "content_en": "Article 14 (No license): PENALTY: Fine of 50,000 RWF and vehicle impoundment. Article 22 (Speeding): PENALTY: Fixed traffic fine of 25,000 RWF.",
        "tags": "umuhanda, imodoka, permis, license, amande"
    },
    "6": {
        "title_rw": "Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)",
        "title_en": "Cybercrimes Law",
        "content_rw": "Ingingo ya 32 (Kwinjira mu miterere ya mudasobwa y'undi): IBIHANO: Igifungo kuva ku mwaka 1 kugeza ku myaka 3 n'amande kuva kuri miliyoni 1 kugeza kuri miliyoni 3 Frw.",
        "content_en": "Article 32 (Unauthorized hacking/access): PENALTY: Imprisonment of 1 to 3 years and a fine of 1M to 3M RWF.",
        "tags": "internet, cybersecurity, cybercrime, mudasobwa"
    },
    "7": {
        "title_rw": "Itegeko ry'Uburenganzira bw'Umwana (Child Protection)",
        "title_en": "Law on Child Protection",
        "content_rw": "Ingingo ya 18 (Gukubita umwana): Karabujijwe burundu. IBIHANO: Umuntu wese gukubita umwana bihannywe n'amategeko y'ibyaha, bishobora kuvamo igifungo kuva ku mezi 2 kugeza ku myaka 2.",
        "content_en": "Article 18 (Corporal punishment): Prohibited. PENALTY: Anyone who subjects a child to corporal punishment faces imprisonment of 2 months to 2 years.",
        "tags": "umwana, child, uburenganzira, protection"
    }
}

# --- WEBSITE DASHBOARD INJSON --
@app.route("/", methods=["GET"])
def dashboard():
    laws_list = [{"id": k, "title": v["title_rw"], "content_rw": v["content_rw"], "content_en": v["content_en"]} for k, v in LAW_DATABASE.items()]
    return jsonify({
        "status": "Live",
        "developer": "GAD MASOZERA",
        "message": "Rwanda Law App Server Running 100% Perfect",
        "laws_count": len(laws_list),
        "laws": laws_list
    })

# --- USSD CORE SERVICE ---
@app.route("/ussd", methods=["POST"])
def ussd_handler():
    text_input = request.form.get("text", "")
    steps = text_input.split('*') if text_input else []
    
    if text_input == "":
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English\n3. Quick Search"

    elif len(steps) == 1:
        lang = steps[0]
        if lang in ["1", "2"]:
            menu = "CON Hitamo Icyiciro:\n" if lang == "1" else "CON Choose Category:\n"
            for k, v in LAW_DATABASE.items():
                title = v["title_rw"] if lang == "1" else v["title_en"]
                menu += f"{k}. {title}\n"
            return menu
        elif lang == "3":
            return "CON Andika ijambo ushaka (e.g., akazi, ibyaha, amande):"
        return "END Invalid input."

    elif len(steps) == 2 and steps[0] == "3":
        keyword = steps[1].lower().strip()
        for k, v in LAW_DATABASE.items():
            if keyword in v["tags"]:
                return f"CON {v['content_rw']}\n\n9. Siga Ubufasha (Legal Aid)"
        return "END Ntacyo twabonye. / No results found."

    elif len(steps) == 2:
        lang, category = steps[0], steps[1]
        if category in LAW_DATABASE:
            v = LAW_DATABASE[category]
            content = v["content_rw"] if lang == "1" else v["content_en"]
            aid_opt = "\n\n9. Gusa Ubufasha" if lang == "1" else "\n\n9. Request Legal Aid"
            return f"CON {content}{aid_opt}"
        return "END Invalid Category."

    elif len(steps) == 3 and steps[2] == "9":
        return "END Murakoze. Umunyamategeko agiye kuguhamagara mukanya. / A lawyer will call you."

    return "END System error."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
