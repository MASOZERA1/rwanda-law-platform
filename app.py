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

# PREMIER PREMIUM DARK UI BASE ON YOUR DESIGN (MUHOZA CLAUDE portal)
HTML_PAGE = """<!DOCTYPE html>
<html lang="rw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MUHOZA CLAUDE - Rwandan Law Portal</title>
    <script src="https://jsdelivr.net"></script>
</head>
<body class="bg-[#121212] font-sans text-slate-200 antialiased min-h-screen">
    
    <!-- Top Custom Header Header from your image -->
    <div class="bg-gradient-to-r from-emerald-700 via-[#1e293b] to-emerald-800 text-center py-4 font-bold text-lg text-amber-300 border-b-2 border-emerald-500 shadow-md">
        Amategeko y'u Rwanda ku baturage bose
    </div>

    <main class="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row gap-8">
        
        <!-- Left Side Profile Card (Your exact design with Gold frame) -->
        <div class="w-full md:w-1/3 bg-[#1e1e1e] p-6 rounded-2xl border-2 border-amber-400/80 shadow-lg text-center h-fit">
            <div class="w-full bg-[#121212] border border-cyan-400 py-2 rounded-xl inline-block mb-4 max-w-[200px] mx-auto text-cyan-300 font-bold tracking-wider text-xs">
                📸 MUHOZA CLAUDE
            </div>
            <h2 class="text-2xl font-black text-amber-400 tracking-tight mt-2 uppercase">MUHOZA CLAUDE</h2>
            <p class="text-slate-300 text-sm leading-relaxed mt-4 font-medium px-2">
                Kaze kuri MUHOZA CLAUDE Law Portal. Uru rubuga rwateguriwe gufusha abaturarwanda, abanyamategeko, n'abacamanza kubona amategeko agenga u Rwanda binyuze mu gushyira amategeko mu kiganza cya buri muntu.
            </p>
            <div class="mt-6 pt-4 border-t border-slate-700/50">
                <span class="bg-emerald-950 text-emerald-400 border border-emerald-500/30 px-4 py-1.5 rounded-full text-xs font-bold font-mono">
                    USSD: *384*61254#
                </span>
            </div>
        </div>

        <!-- Right Side Main Law Hub (Your Dark UI with Hammer and Live Filter) -->
        <div class="w-full md:w-2/3 bg-[#1a1a1a] p-6 md:p-8 rounded-2xl border border-emerald-500/30 shadow-md flex flex-col items-center">
            
            <!-- Gavel Icon from your design -->
            <div class="text-center mb-4">
                <span class="text-5xl block animate-bounce">🔨</span>
                <h3 class="text-lg font-bold text-slate-100 mt-3">Kanda ku itegeko usome ibikubiyemo</h3>
            </div>

            <!-- Live Smart Search input Filter -->
            <div class="w-full max-w-xl mb-8 relative">
                <input type="text" id="searchInput" onkeyup="filterSystem()" placeholder="Shakisha itegeko... (Urugero: Ubujura, Permis)" 
                       class="w-full bg-[#121212] border border-slate-700 rounded-xl py-3.5 px-5 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 font-medium transition shadow-inner">
            </div>

            <!-- Laws Lists Cards from your design grid -->
            <div class="w-full space-y-4" id="lawsContainer">
                
                <!-- Law Card 1 -->
                <div class="law-card bg-[#121212] border-l-4 border-cyan-400 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition hover:border-emerald-500 hover:bg-[#1a1a1a]">
                    <div>
                        <h4 class="font-bold text-base text-slate-200 tracking-tight">Itegeko Nshinga rya Repubulika y'u Rwanda</h4>
                        <p class="text-xs text-slate-500 font-medium mt-1 font-mono">Constitution of Rwanda</p>
                    </div>
                    <button onclick="alert('Ingingo ya 1: Umuryango nyarwanda uteye imbere. IBIHANO: Ikintu cyose kinyuranyije na ryo nta gaciro kiba gifite.')" class="text-xs text-cyan-400 hover:underline font-bold whitespace-nowrap cursor-pointer">Soma byose (External) ›</button>
                </div>

                <!-- Law Card 2 -->
                <div class="law-card bg-[#121212] border-l-4 border-cyan-400 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition hover:border-emerald-500 hover:bg-[#1a1a1a]">
                    <div>
                        <h4 class="font-bold text-base text-slate-200 tracking-tight">Itegeko ry'Ibyaha n'Ibano (Penal Code)</h4>
                        <p class="text-xs text-slate-500 font-medium mt-1 font-mono">Penal Code of Rwanda</p>
                    </div>
                    <button onclick="alert('Ingingo ya 120 (Ubujura): IBIHANO: Igifungo kuva ku mezi 6 kugeza ku myaka 2 n'amande ari hagati ya 100,000 Frw na 500,000 Frw.')" class="text-xs text-cyan-400 hover:underline font-bold whitespace-nowrap cursor-pointer">Soma byose (External) ›</button>
                </div>

                <!-- Law Card 3 -->
                <div class="law-card bg-[#121212] border-l-4 border-cyan-400 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition hover:border-emerald-500 hover:bg-[#1a1a1a]">
                    <div>
                        <h4 class="font-bold text-base text-slate-200 tracking-tight">Itegeko ry'Umuryango n'Abantu (Family Law)</h4>
                        <p class="text-xs text-slate-500 font-medium mt-1 font-mono">Family Law</p>
                    </div>
                    <button onclick="alert('Ingingo ya 35 (Ishyingirwa): Ishyingirwa ryemewe n\'amategeko ni irisezeranyijwe imbere y\'ubuyobozi bwa Leta.')" class="text-xs text-cyan-400 hover:underline font-bold whitespace-nowrap cursor-pointer">Soma byose (External) ›</button>
                </div>

                <!-- Law Card 4 -->
                <div class="law-card bg-[#121212] border-l-4 border-cyan-400 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition hover:border-emerald-500 hover:bg-[#1a1a1a]">
                    <div>
                        <h4 class="font-bold text-base text-slate-200 tracking-tight">Itegeko ry'Umurimo mu Rwanda (Labor Law)</h4>
                        <p class="text-xs text-slate-500 font-medium mt-1 font-mono">Labor Law</p>
                    </div>
                    <button onclick="alert('Ingingo ya 28: Integuza y\'ukwezi imbere yo kwirukana umukozi.')" class="text-xs text-cyan-400 hover:underline font-bold whitespace-nowrap cursor-pointer">Soma byose (External) ›</button>
                </div>

                <!-- Law Card 5 -->
                <div class="law-card bg-[#121212] border-l-4 border-cyan-400 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition hover:border-emerald-500 hover:bg-[#1a1a1a]">
                    <div>
                        <h4 class="font-bold text-base text-slate-200 tracking-tight">Amategeko y'Umuhanda n'Ibyapa (Traffic Regulations)</h4>
                        <p class="text-xs text-slate-500 font-medium mt-1 font-mono">Traffic Rules</p>
                    </div>
                    <button onclick="alert('Ingingo ya 14: Gutwara ikinyabiziga nta permis bihanishwa amande ya 50,000 Frw.')" class="text-xs text-cyan-400 hover:underline font-bold whitespace-nowrap cursor-pointer">Soma byose (External) ›</button>
                </div>

            </div>

            <!-- No Results Feedback -->
            <div id="noResults" class="hidden text-center py-8 text-slate-500 font-medium text-sm">
                Ntacyo twabonye kuri iryo jambo! / No laws found matching.
            </div>

        </div>
    </main>

    <script>
        function filterSystem() {
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            const cards = document.getElementsByClassName('law-card');
            let foundAny = false;

            for (let card of cards) {
                const text = card.innerText.toLowerCase();
                if (text.includes(query)) {
                    card.classList.remove('hidden');
                    foundAny = true;
                } else {
                    card.classList.add('hidden');
                }
            }

            if (!foundAny && query !== "") {
                document.getElementById('noResults').classList.remove('hidden');
            } else {
                document.getElementById('noResults').classList.add('hidden');
            }
        }
    </script>
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
        return "CON Ikaze kuri Rwanda Law App (By GAD MASOZERA / MUHOZA CLAUDE)!\nHitamo ururimi / Choose language:\n1. Kinyarwanda\n2. English"
    elif len(steps) == 1:
        return "CON Hitamo Icyiciro:\n1. Itegeko Nshinga\n2. Itegeko ry'Ibyaha\n3. Itegeko ry'Umuryango\n4. Itegeko ry'Umurimo\n5. Amategeko y'Umuhanda"
    elif len(steps) == 2:
        category = steps
