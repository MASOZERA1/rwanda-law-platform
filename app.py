import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# UBUBIKO BW'AMATEGEKO Y'U RWANDA N'IBIHANO (PYTHON DICTIONARY)
LAW_DATABASE = {
    "1": {
        "title_rw": "Itegeko Nshinga rya Repubulika y'u Rwanda",
        "title_en": "Constitution of Rwanda",
        "content_rw": "Ingingo ya 1: Umuryango nyarwanda uteye imbere. Ingingo ya 13: Agaciro k'umuntu ntibwogerwa. IBIHANO: Ikintu cyose kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko (Null and void).",
        "content_en": "Article 1: The Rwandan State is a Republic. Article 13: Inviolability of human dignity. SANCTION: Any law or act contrary to the Constitution is null and void.",
        "tags": "itegeko nshinga, constitution, uburenganzira, nshinga, muntu, agaciro"
    },
    "2": {
        "title_rw": "Itegeko ry'Ibyaha n'Ibano (Penal Code)",
        "title_en": "Penal Code of Rwanda",
        "content_rw": "Ingingo ya 120 (Ubujura): IBIHANO: Igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande ari hagati ya 100,000 Frw na 500,000 Frw. Ingingo ya 166 (Gukubita/Gukomeretsa): IBIHANO: Igifungo cy'imyaka 5 kugeza kuri 7 n'amande.",
        "content_en": "Article 120 (Theft): PENALTY: Imprisonment of 6 months to 2 years and a fine of 100k to 500k RWF. Article 166 (Assault): PENALTY: Imprisonment of 5 to 7 years.",
        "tags": "ibyaha, penal, ubujura, theft, gukubita, ruswa, igifungo, amande, gukomeretsa"
    },
    "3": {
        "title_rw": "Itegeko ry'Umuryango n'Abantu (Family Law)",
        "title_en": "Law Governing Persons and Family",
        "content_rw": "Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta. IBIHANO: Gusezerana mu buryo bwa magendu (Bigamy/Polygamy) bihanishwa igifungo cy'mezi 6 kugeza ku mwaka 1.",
        "content_en": "Article 35 (Marriage): Only civil marriage is recognized. PENALTY: Illegal marriage or bigamy is punishable by 6 months to 1 year imprisonment.",
        "tags": "umuryango, family, gushyingirwa, marriage, izungura, ubutane, divorce, abana"
    },
    "4": {
        "title_rw": "Itegeko ry'Umurimo mu Rwanda (Labor Law)",
        "title_en": "Law Governing Labor in Rwanda",
        "content_rw": "Ingingo ya 28: Integuza y'ukwezi imbere yo kwirukana umukozi. IBIHANO: Umukoresha wishe iri tegeko ategekwa kwandukura no kwishyura umushahara w'ukwezi kwose nshumbushanyo (1 month notice salary damage).",
        "content_en": "Article 28: 1-month termination notice. PENALTY: Violators must pay the worker 1 month full salary as indemnity for lack of notice.",
        "tags": "akazi, umurimo, contract, fire, kwirukanwa, umushahara, notice, amasezerano"
    },
    "5": {
        "title_rw": "Amategeko y'Umuhanda n'Ibyapa (Traffic Decree)",
        "title_en": "Traffic Regulations",
        "content_rw": "Ingingo ya 14 (Gutwara nta permis): IBIHANO: Amande ya 50,000 Frw no gufatira ikinyabiziga. Ingingo ya 22 (Kurenza umuvuduko/Speeding): IBIHANO: Amande y'amafaranga 25,000 Frw ako kanya.",
        "content_en": "Article 14 (No license): PENALTY: Fine of 50,000 RWF and vehicle impoundment. Article 22 (Speeding): PENALTY: Fixed traffic fine of 25,000 RWF.",
        "tags": "umuhanda, imodoka, permis, license, amande, police, vitesse, ibyapa"
    },
    "6": {
        "title_rw": "Itegeko ry'Ibyaha bikorerwa kuri Internet (Cybercrime Law)",
        "title_en": "Cybercrimes Law",
        "content_rw": "Ingingo ya 32 (Kwinjira mu miterere ya mudasobwa y'undi): IBIHANO: Igifungo kuva ku mwaka 1 kugeza ku myaka 3 n'amande kuva kuri miliyoni 1 kugeza kuri miliyoni 3 Frw.",
        "content_en": "Article 32 (Unauthorized hacking/access): PENALTY: Imprisonment of 1 to 3 years and a fine of 1M to 3M RWF.",
        "tags": "internet, cybersecurity, cybercrime, mudasobwa, hacking, guhimba"
    },
    "7": {
        "title_rw": "Itegeko ry'Uburenganzira bw'Umwana (Child Protection)",
        "title_en": "Law on Child Protection",
        "content_rw": "Ingingo ya 18 (Gukubita umwana): Karabujijwe burundu. IBIHANO: Umuntu wese gukubita umwana bihannywe n'amategeko y'ibyaha, bishobora kuvamo igifungo kuva ku mezi 2 kugeza ku myaka 2.",
        "content_en": "Article 18 (Corporal punishment): Prohibited. PENALTY: Anyone who subjects a child to corporal punishment faces imprisonment of 2 months to 2 years.",
        "tags": "umwana, child, uburenganzira, protection, ishuri, gukubita"
    }
}

# --- PREMIUM WEB PORTAL WITH JAVASCRIPT LIVE SEARCH ---
@app.route("/", methods=["GET"])
def dashboard():
    laws_json_js = []
    for k, v in LAW_DATABASE.items():
        laws_json_js.append({
            "id": k,
            "title_rw": v["title_rw"],
            "title_en": v["title_en"],
            "content_rw": v["content_rw"],
            "content_en": v["content_en"],
            "tags": v["tags"]
        })

    html_template = """
    <!DOCTYPE html>
    <html lang="rw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rwanda Law - GAD MASOZERA Portal</title>
        <!-- Tailwind CSS Framework for modern design -->
        <script src="https://jsdelivr.net"></script>
    </head>
    <body class="bg-slate-50 font-sans text-slate-800 antialiased min-h-screen">
        
        <!-- Header Section -->
        <header class="bg-gradient-to-r from-emerald-700 via-emerald-600 to-teal-600 text-white shadow-lg sticky top-0 z-50 backdrop-blur-md">
            <div class="max-w-6xl mx-auto px-6 py-5 flex flex-col md:flex-row justify-between items-center gap-4">
                <div class="text-center md:text-left">
                    <h1 class="text-3xl font-extrabold tracking-tight flex items-center justify-center md:justify-start gap-2">
                        🇷🇼 Rwanda Law Access Hub
                    </h1>
                    <p class="text-emerald-100 text-sm mt-1 font-medium">
                        Developed by <span class="underline decoration-teal-300 decoration-2 font-bold">GAD MASOZERA</span>
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <span class="flex h-3 w-3 relative">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-3 w-3 bg-teal-400"></span>
                    </span>
                    <span class="bg-emerald-800/50 border border-emerald-500/30 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wider uppercase text-emerald-200">
                        Production Live Server
                    </span>
                </div>
            </div>
        </header>

        <!-- Main Body -->
        <main class="max-w-5xl mx-auto px-6 py-10">
            
            <!-- Key Metrics Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-t-4 border-emerald-600 hover:shadow-md transition duration-300">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">USSD Code</p>
                    <p class="text-2xl font-black text-slate-700 mt-1 font-mono tracking-tight text-emerald-600">*384*61254#</p>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-t-4 border-orange-500 hover:shadow-md transition duration-300">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Platform Status</p>
                    <p class="text-2xl font-black text-emerald-600 mt-1">Active / Secure</p>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-t-4 border-blue-500 hover:shadow-md transition duration-300">
                    <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Law Core Modules</p>
                    <p class="text-2xl font-black text-slate-700 mt-1">7 Full Codes</p>
                </div>
            </div>

            <!-- Search Area Header -->
            <div class="mb-10 text-center md:text-left">
                <h2 class="text-2xl font-extrabold text-slate-800 tracking-tight">Amategeko y'u Rwanda n'Ibihano birimo</h2>
                <p class="text-slate-500 text-sm mt-1">Andika ijambo ushaka (Urugero: ubujura, permis, akazi) cyangwa igihano ubyungurure ako kanya.</p>
                
                <!-- Live Search Bar -->
                <div class="mt-5 max-w-xl relative">
                    <input type="text" id="searchInput" onkeyup="filterLaws()" placeholder="Shakisha amategeko hano... / Search laws here..." 
                           class="w-full bg-white border border-slate-200 rounded-2xl py-4 pl-12 pr-4 shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-slate-700 placeholder-slate-400 font-medium transition">
                    <svg class="h-5 w-5 text-slate-400 absolute left-4 top-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                    </svg>
                </div>
            </div>

            <!-- Laws Container Cards -->
            <div id="lawsContainer" class="space-y-6">
                <!-- Laws will be dynamically generated by Javascript with filtering here -->
            </div>

            <!-- No Results Feedback -->
            <div id="noResults" class="hidden text-center py-12 bg-white rounded-2xl border border-dashed border-slate-200">
                <p class="text-slate-400 font-medium text-lg">Ntacyo twabonye kuri iryo jambo! / No laws found matching your search.</p>
