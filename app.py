import os
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

LAW_DATABASE = {
    "1": "Itegeko Nshinga: Umuryango nyarwanda uteye imbere. IBIHANO: Ikintu cyose kinyuranyije na ryo nta gaciro kiba gifite imbere y'amategeko (Null and void).",
    "2": "Itegeko ry'Ibyaha: Ubujura buhanishwa igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande kuva kuri 100k kugeza kuri 500k Frw.",
    "3": "Itegeko ry'Umuryango: Ishyingirwa ryemewe n'amategeko ni irisezeranyijwe imbere y'ubuyobozi bwa Leta.",
    "4": "Itegeko ry'Umurimo: Integuza y'ukwezi imbere yo kwirukana umukozi. Umukoresha wishe iri tegeko ategekwa kwishyura umushahara w'ukwezi.",
    "5": "Amategeko y'Umuhanda: Gutwara ikinyabiziga nta permis bihanishwa amande ya 50,000 Frw no gufatira ikinyabiziga."
}

# PREMIUM HTML DASHBOARD IN A SAFE FLASK STRING
HTML_PAGE = """<!DOCTYPE html>
<html lang="rw">
<head>
    <meta charset="UTF-8">
    <title>Rwanda Law - GAD MASOZERA</title>
    <script src="https://jsdelivr.net"></script>
</head>
<body class="bg-slate-100 font-sans text-slate-800 antialiased min-h-screen">
    <header class="bg-gradient-to-r from-emerald-800 to-teal-700 text-white shadow-xl sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-5 flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <h1 class="text-3xl font-black tracking-tight">🇷🇼 Rwanda Law Access Hub</h1>
                <p class="text-emerald-100 text-sm mt-1 font-medium">Developed by <span class="underline font-bold">GAD MASOZERA</span></p>
            </div>
            <div class="bg-emerald-900/60 border border-emerald-500/30 px-5 py-2 rounded-full text-xs font-bold uppercase text-emerald-200">Innovative Server Live</div>
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
                <p class="text-xs font-bold uppercase tracking-wider text-slate-400">System Engine</p>
                <p class="text-2xl font-black text-slate-700 mt-1">Active Hub</p>
            </div>
        </div>

        <div class="mb-6 flex flex-col sm:flex-row gap-4 justify-between items-center">
            <h2 class="text-2xl font-extrabold text-slate-800 tracking-tight">Amategeko y'u Rwanda n'Ibihano (Urwego rushya rwa GAD MASOZERA)</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-4">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-base font-bold text-slate-900 mb-3">📑 Urutonde rw'Amategeko</h3>
                    <p class="text-sm text-slate-600 mb-2">1. Itegeko Nshinga (Constitution)</p>
                    <p class="text-sm text-slate-600 mb-2">2. Itegeko ry'Ibyaha (Penal Code)</p>
                    <p class="text-sm text-slate-600 mb-2">3. Itegeko ry'Umuryango (Family Law)</p>
                    <p class="text-sm text-slate-600 mb-2">4. Itegeko ry'Umurimo (Labor Law)</p>
                    <p class="text-sm text-slate-600 mb-2">5. Amategeko y'Umuhanda (Traffic Rules)</p>
                </div>
            </div>

            <div class="md:col-span-2 space-y-6">
                <div class="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200/60 border-l-6 border-emerald-600">
                    <h2 class="text-xl font-black text-slate-900">⚖️ Itegeko Nshinga rya Repubulika y'u Rwanda</h2>
                    <p class="text-slate-700 mt-4 leading-relaxed font-medium">Ingingo ya 1: Umuryango nyarwanda uteye imbere ku bumwe n'ubwiyunge. Ingingo ya 10: Demokarasi n'uburenganzira bwa muntu ntibwogerwa.</p>
                    <div class="bg-rose-50 border border-rose-100 p-4 rounded-xl mt-4">
                        <p class="text-rose-900 font-bold">IBIHANO: Ikintu cyose, itegeko cyangwa gikorwa kinyuranyije n'Itegeko Nshinga nta gaciro kiba gifite imbere y'amategeko.</p>
                    </div>
                </div>

                <div class="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200/60 border-l-6 border-emerald-600">
                    <h2 class="text-xl font-black text-slate-900">🚨 Itegeko ry'Ibyaha n'Ibano (Penal Code)</h2>
                    <p class="text-slate-700 mt-4 leading-relaxed font-medium">Ingingo ya 120 (Ubujura): Gufata ikintu cy'undi utabyemerewe. Ingingo ya 166: Gukubita cyangwa gukomeretsa ku bushake.</p>
                    <div class="bg-rose-50 border border-rose-100 p-4 rounded-xl mt-4">
                        <p class="text-rose-900 font-bold">IBIHANO: Ubujura buhanishwa igifungo kuva kuzi 6 kugeza ku myaka 2 n'amande kuva kuri 100,000 Frw kugeza kuri 500,000 Frw.</p>
                    </div>
                </div>

                <div class="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200/60 border-l-6 border-emerald-600">
                    <h2 class="text-xl font-black text-slate-900">🚗 Amategeko y'Umuhanda n'Ibyapa (Traffic Regulations)</h2>
                    <p class="text-slate-700 mt-4 leading-relaxed font-medium">Ingingo ya 14: Gutwara ikinyabiziga nta permis cyangwa uruhushya rwo gutwara rwemewe.</p>
                    <div class="bg-rose-50 border border-rose-100 p-4 rounded-xl mt-4">
                        <p class="text-rose-900 font-bold">IBIHANO: Gutwara nta permis bihanishwa amande ya 50,000 Frw no gufatira ikinyabiziga n'igipolisi.</p>
                    </div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>"""

@app.route("/", methods=["GET"])
def dashboard():
    return render_template_string(HTML_PAGE)

@app.route("/ussd", methods=["POST"])
def ussd_handler():
    text_input = request.form.get("text", "")
    steps = text_input.split('*') if text_input else []
    
    if text_input == "":
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English"
    elif len(steps) == 1:
        return "CON Hitamo Icyiciro:\n1. Itegeko Nshinga\n2. Itegeko ry'Ibyaha\n3. Itegeko ry'Umuryango\n4. Itegeko ry'Umurimo\n5. Amategeko y'Umuhanda"
    elif len(steps) == 2:
        category = steps[1]
        if category in LAW_DATABASE:
            return f"END {LAW_DATABASE[category]}"
        return "END Category Not Found."
    return "END System error."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
