import os
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# UBUBIKO BW'AMATEGEKO Y'U RWANDA KANDI YAGABANYIJWE NEZA CYANE
LAW_DATABASE = {
    "1": {
        "id": "1",
        "title_rw": "Itegeko Nshinga rya Repubulika y'u Rwanda",
        "title_en": "Constitution of the Republic of Rwanda",
        "icon": "⚖️",
        "content_rw": "Ingingo ya 1: Umuryango nyarwanda uteye imbere ku bumwe n'ubwiyunge. Ingingo ya 10: Demokarasi n'uburenganzira bwa muntu ntibwogerwa. Ingingo ya 13: Agaciro k'umuntu kanyuranyije n'iyica rubazo.",
        "penalty_rw": "IBIHANO: Ikintu cyose, itegeko cyangwa gikorwa kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).",
        "content_en": "Article 1: The Rwandan State is a Republic. Article 10: Core values of rule of law and human rights. Article 13: Inviolability of human dignity.",
        "penalty_en": "SANCTION: Any law, act, or decree contrary to the Constitution is null and void under the law.",
        "tags": "itegeko nshinga, constitution, uburenganzira, nshinga, muntu, agaciro"
    },
    "2": {
        "id": "2",
        "title_rw": "Itegeko ry'Ibyaha n'Ibano (Penal Code)",
        "title_en": "Penal Code of Rwanda",
        "icon": "🚨",
        "content_rw": "Ingingo ya 120 (Ubujura): Gufata ikintu cy'undi utabyemerewe. Ingingo ya 166 (Gukubita/Gukomeretsa): Gukubita cyangwa gukomeretsa ku bushake bitera ubumuga buhoraho. Ingingo ya 211: Ruswa n'ibyaha bifitanye isano na yo.",
        "penalty_rw": "IBIHANO: Ubujura buhanishwa igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande kuva kuri 100,000 Frw kugeza kuri 500,000 Frw. Gukubita bihanishwa igifungo cy'imyaka 5 kugeza kuri 7.",
        "content_en": "Article 120 (Theft): Fraudulent appropriation of another's property. Article 166 (Assault): Intentional assault causing permanent disability. Article 211: Corruption and related offenses.",
        "penalty_en": "PENALTY: Petty theft is punishable by 6 months to 2 years prison and a fine of 100k to 500k RWF. Assault is punishable by 5 to 7 years imprisonment.",
        "tags": "ibyaha, penal, ubujura, theft, gukubita, ruswa, igifungo, amande, gukomeretsa"
    },
    "3": {
        "id": "3",
        "title_rw": "Itegeko ry'Umuryango n'Abantu (Family Law)",
        "title_en": "Law Governing Persons and Family",
        "icon": "🏠",
        "content_rw": "Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. Ingingo ya 52: Ubutane (Divorce) bushobora kwemezwa n'inkiko gusa. Ingingo ya 88: Abana bose bafite uburenganzira bungana ku izungura.",
        "penalty_rw": "IBIHANO: Gusezerana mu buryo bwa magendu cyangwa gushaka ubugira kabiri (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1 n'amande.",
        "content_en": "Article 35 (Marriage): Only civil marriage is legally recognized. Article 52: Divorce can only be granted by competent courts. Article 88: Equal succession and inheritance rights for all children.",
        "penalty_en": "PENALTY: Illegal marriage or bigamy is strictly prohibited and punishable by 6 months to 1 year imprisonment.",
        "tags": "umuryango, family, gushyingirwa, marriage, izungura, ubutane, divorce, abana"
    },
    "4": {
        "id": "4",
        "title_rw": "Itegeko ry'Umurimo mu Rwanda (Labor Law)",
        "title_en": "Law Governing Labor in Rwanda",
        "icon": "💼",
        "content_rw": "Ingingo ya 12: Amasezerano y'akazi agomba kwandikwa. Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. Ingingo ya 45: Akazi k'abana munsi y'imyaka 13 karabujijwe burundu.",
        "penalty_rw": "IBIHANO: Umukoresha wishe iri tegeko ryo kwirukana umukozi nta nteguza, ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (Notice indemnity).",
        "content_en": "Article 12: Employment contracts must be in writing. Article 28: Mandatory 1-month termination notice. Article 45: Child labor under 13 years is strictly prohibited.",
        "penalty_en": "PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.",
        "tags": "akazi, umurimo, contract, fire, kwirukanwa, umushahara, notice, amasezerano"
    },
    "5": {
        "id": "5",
        "title_rw": "Amategeko y'Umuhanda n'Ibyapa (Traffic Regulations)",
        "title_en": "Traffic and Road Safety Regulations",
        "icon": "🚗",
        "content_rw": "Ingingo ya 14: Gutwara ikinyabiziga nta permis cyangwa uruhushya rwo gutwara rwemewe. Ingingo ya 22: Kurenza umuvuduko itandukanyijwe n'ibyapa (Speeding) mu mihanda.",
        "penalty_rw": "IBIHANO: Gutwara nta permis bihanishwa amande ya 50,000 Frw no gufatira ikinyabiziga n'igipolisi. Kurenza umuvuduko (Speeding) bihanishwa amande ya 25,000 Frw.",
        "content_en": "Article 14: Driving without a valid driver's license. Article 22: Exceeding speed limits specified by road signs.",
        "penalty_en": "PENALTY: Driving without a license attracts a 50,000 RWF fine and vehicle impoundment. Exceeding speed limits (Speeding) attracts a 25,000 RWF fine.",
        "tags": "umuhanda, imodoka, permis, license, amande, police, vitesse, ibyapa"
    }
}

LITIGATION_CASES = []
COMMENTS_STORE = {"1": [], "2": [], "3": [], "4": [], "5": []}

@app.route("/file-case", methods=["POST"])
def file_case():
    phone = request.form.get("phone")
    category = request.form.get("category")
    details = request.form.get("details")
    if phone and details:
        case = {"phone": phone, "category": category, "details": details, "status": "Pending Analysis"}
        LITIGATION_CASES.append(case)
        return jsonify({"status": "Success", "cases_count": len(LITIGATION_CASES)})
    return jsonify({"status": "Error"}), 400

@app.route("/add-comment", methods=["POST"])
def add_comment():
    law_id = request.form.get("law_id")
    name = request.form.get("name", "Umusomyi Mwiza")
    text = request.form.get("text")
    if law_id in COMMENTS_STORE and text:
        COMMENTS_STORE[law_id].append({"name": name, "text": text})
        return jsonify({"status": "Success", "comments": COMMENTS_STORE[law_id]})
    return jsonify({"status": "Error"}), 400

@app.route("/", methods=["GET"])
def dashboard():
    html_template = """
    <!DOCTYPE html>
    <html lang="rw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rwanda Law - GAD MASOZERA</title>
        <script src="https://jsdelivr.net"></script>
    </head>
    <body class="bg-slate-100 font-sans text-slate-800 antialiased min-h-screen">
        <header class="bg-gradient-to-r from-emerald-800 to-teal-700 text-white shadow-xl sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-6 py-5 flex flex-col md:flex-row justify-between items-center gap-4">
                <div>
                    <h1 class="text-3xl font-black tracking-tight">🇷🇼 Rwanda Law Access Hub</h1>
                    <p class="text-emerald-100 text-sm mt-1 font-medium">Developed by <span class="underline font-bold decoration-teal-300 decoration-2">GAD MASOZERA</span></p>
                </div>
                <div class="bg-emerald-900/60 border border-emerald-500/30 px-5 py-2 rounded-full text-xs font-bold uppercase text-emerald-200">Innovative AI Portal</div>
            </div>
        </header>

        <main class="max-w-7xl mx-auto px-6 py-10">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
                <div class="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-emerald-600">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">USSD Code Gateway</p>
                    <p class="text-2xl font-black text-emerald-600 mt-1 font-mono">*384*61254#</p>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-orange-500">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">AI Legal Counselor</p>
                    <p class="text-xl font-bold text-orange-600 mt-1">Online / Smart</p>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-blue-500">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Live Cases Filed</p>
                    <p id="casesCount" class="text-2xl font-black text-slate-700 mt-1">0 Active</p>
                </div>
            </div>

            <!-- Search Area Header -->
            <div class="mb-6 flex flex-col sm:flex-row gap-4 justify-between items-center">
                <h2 class="text-2xl font-extrabold text-slate-800 tracking-tight">Amategeko y'u Rwanda n'Ibihano birimo</h2>
                <div class="w-full sm:w-72 relative">
                    <input type="text" id="searchInput" onkeyup="filterSystem()" placeholder="Shakisha amategeko hano..." class="w-full bg-white border border-slate-200 rounded-xl py-2.5 px-4 focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm shadow-inner">
                </div>
            </div>

            <!-- Vertical Tabs Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Tabs Sidebar Menu -->
                <div class="space-y-2">
                    {% for key, law in laws.items() %}
                    <button onclick="showLaw('{{ key }}')" id="btn-{{ key }}" class="law-tab-btn w-full text-left px-5 py-4 rounded-xl font-bold flex items-center gap-3 border border-transparent transition shadow-xs {% if key == '1' %}bg-emerald-600 text-white shadow-md{% else %}bg-white text-slate-700 hover:bg-slate-50 hover:border-slate-200{% endif %}">
                        <span class="text-2xl">{{ law.icon }}</span>
                        <div class="truncate">
