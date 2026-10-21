import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os
import gradio as gr
warnings.filterwarnings("ignore")

# ═══════════════ UTILITÁRIOS ═══════════════
PADRAO_NUM = re.compile(r"(\d+(?:[.,]\d+)?)\s*(bilh[oõ]es?|bilh[aã]o|milh[oõ]es?|milh[aã]o|mil|mi|m|b|k)?", re.I)
MAPA_MULT = {"bilhoes":1e9,"bilhao":1e9,"b":1e9,"milhoes":1e6,"milhao":1e6,"mi":1e6,"m":1e6,"mil":1e3,"k":1e3}

def fmt(n):
    if n is None: return "—"
    n=int(n)
    if n>=1e9: return f"{n/1e9:.1f} bi"
    if n>=1e6: return f"{n/1e6:.2f} mi"
    if n>=1e3: return f"{n/1e3:.1f} mil"
    return str(n)

def brl(v):
    if v is None: return "—"
    return "R$ " + f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

TABELA_RPM = {
    " Curiosidades":12, "🔪 Histórias/Crimes":18, "️ Documentário":20,
    " Resumo de Filmes":15, " Religião":10, " Motivacional":9,
    "🎵 Música/Relax":4, "🎮 Games":8, "⚽ Esportes":14,
    "🚗 Carros":26, "🤖 Tecnologia/IA":35, "💊 Saúde":22, "💰 Finanças":55,
}

# ═══════════════ MOTOR DE BUSCA ═══════════════
def buscar_videos(query, max_results=50):
    opts = {"quiet":True,"no_warnings":True,"skip_download":True,"extract_flat":True,
            "playlist_items":f"1-{max_results}","ignoreerrors":True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False) or {}
        return [e for e in (info.get("entries") or []) if e]
    except: return []

def analisar_canal(url, max_vids=30):
    url_v = url.rstrip("/") + "/videos"
    opts = {"quiet":True,"no_warnings":True,"skip_download":True,"extract_flat":"in_playlist",
            "playlist_items":f"1-{max_vids}","ignoreerrors":True,"retries":2}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url_v, download=False) or {}
    except: return None
    vids = [e for e in (info.get("entries") or []) if e]
    if not vids:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info2 = ydl.extract_info(url.rstrip("/")+"/shorts", download=False) or {}
            vids = [e for e in (info2.get("entries") or []) if e]
            if not vids: return None
        except: return None
    ins = info.get("channel_follower_count")
    videos = [{"id":e.get("id"),"titulo":(e.get("title") or "").strip(),
               "views":int(e.get("view_count") or 0),"dur":e.get("duration"),
               "url":f"https://www.youtube.com/watch?v={e.get('id')}"} for e in vids]
    views = [v["views"] for v in videos if v["views"]]
    if not views: return None
    rec = views[:10]
    return {"nome":info.get("channel") or info.get("uploader") or "—","url":url,
            "inscritos":ins,"views_totais":info.get("view_count"),"videos":videos,
            "media_rec":statistics.mean(rec),"mediana":statistics.median(views),
            "taxa":(statistics.mean(rec)/ins) if ins else None,
            "bombas":sorted([v for v in videos if v["views"]>statistics.median(views)*2.5],
                            key=lambda x:x["views"],reverse=True)[:3]}

# ═══════════════ CSS NOVO (VERMELHO + BRANCO + CINZA) ═══════════════
CSS_BEGINS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Norican&family=Inter:wght@400;600;700;800;900&display=swap');

* { 
    font-family: 'Inter', sans-serif !important; 
    box-sizing: border-box;
}

body, .gradio-container, .main, .wrap, .gradio-app { 
    background: #282828 !important; 
    color: #ffffff !important;
}

/* HEADER */
.ac-header { 
    background: linear-gradient(135deg, #1a1a1a 0%, #282828 50%, #1a1a1a 100%); 
    border-radius: 0; 
    padding: 50px 40px; 
    text-align: center; 
    margin: 0 auto 40px; 
    border-bottom: 6px solid #ff0000; 
    border-top: 2px solid #ff0000;
    box-shadow: 0 10px 40px rgba(255,0,0,0.3); 
    max-width: 1200px;
    position: relative;
}
.ac-header::before {
    content: '⚠ ALERTA DE OPORTUNIDADE ⚠';
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: #ff0000;
    color: #ffffff;
    padding: 4px 20px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    font-family: 'Inter', sans-serif;
}
.ac-header h1 { 
    margin: 0; 
    font-family: 'Kaushan Script', cursive !important;
    font-size: 72px !important; 
    font-weight: 400 !important; 
    color: #ff0000 !important;
    text-shadow: 3px 3px 0 #000000, 0 0 30px rgba(255,0,0,0.5);
    letter-spacing: 2px;
}
.ac-header .begins { 
    color: #ffffff !important;
    display: block;
    font-family: 'Norican', cursive !important;
    font-size: 80px !important;
    margin-bottom: 5px;
    text-shadow: 4px 4px 0 #ff0000, 0 0 40px rgba(255,0,0,0.6);
}
.ac-header .creator { 
    font-family: 'Norican', cursive !important;
    font-size: 22px !important; 
    color: #ffffff !important; 
    font-weight: 400 !important; 
    margin-top: 15px; 
    letter-spacing: 1px;
}
.ac-header .subtitle { 
    margin: 15px 0 0; 
    font-size: 18px !important; 
    color: #bbbbbb !important;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.ac-header .badge { 
    display: inline-block; 
    background: #ff0000; 
    padding: 10px 25px; 
    border-radius: 0; 
    font-size: 13px !important; 
    margin-top: 20px; 
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    border: 2px solid #ffffff;
}

/* ESTATÍSTICAS */
.stats-container {
    display: flex;
    gap: 20px;
    margin-bottom: 40px;
    justify-content: center;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}
.stat-card {
    flex: 1;
    max-width: 320px;
    background: #1a1a1a;
    padding: 30px;
    text-align: center;
    border-left: 6px solid #ff0000;
    border-right: 2px solid #aaaaaa;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.stat-card strong {
    display: block;
    font-family: 'Norican', cursive !important;
    font-size: 52px !important;
    color: #ff0000 !important;
    font-weight: 400;
    margin-bottom: 10px;
    text-shadow: 2px 2px 0 #000000;
}
.stat-card span {
    color: #bbbbbb;
    font-size: 14px !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
}

/* CARDS DE CANAL */
.ac-card { 
    background: #1a1a1a;
    border-radius: 0; 
    margin: 25px auto; 
    overflow: hidden; 
    border-left: 8px solid #ff0000;
    border-right: 2px solid #aaaaaa;
    border-top: 2px solid #aaaaaa;
    border-bottom: 2px solid #aaaaaa;
    max-width: 1200px;
    transition: all 0.3s;
}
.ac-card:hover { 
    transform: translateX(5px); 
    box-shadow: -8px 8px 0 #ff0000;
}
.ac-card-head { 
    padding: 25px 30px; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    border-bottom: 2px solid #ff0000; 
    background: #282828;
}
.ac-card-head h3 { 
    margin: 0; 
    font-family: 'Kaushan Script', cursive !important;
    font-size: 32px !important; 
    color: #ffffff !important; 
    font-weight: 400;
}
.ac-badge { 
    padding: 10px 20px; 
    font-size: 13px !important; 
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    border: 2px solid;
}
.ac-badge-rocket { 
    background: #ff0000; 
    color: #ffffff !important;
    border-color: #ffffff;
}
.ac-badge-up { 
    background: #ffffff; 
    color: #282828 !important;
    border-color: #ff0000;
}
.ac-badge-sleep { 
    background: #aaaaaa; 
    color: #282828 !important;
    border-color: #282828;
}

.ac-card-body { 
    padding: 25px; 
    display: grid; 
    grid-template-columns: repeat(4, 1fr); 
    gap: 15px; 
    background: #1a1a1a;
}
.ac-stat-mini { 
    background: #282828;
    padding: 20px; 
    text-align: center; 
    border: 1px solid #aaaaaa;
}
.ac-stat-mini .lbl { 
    font-size: 11px !important; 
    color: #bbbbbb !important; 
    text-transform: uppercase; 
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
}
.ac-stat-mini .val { 
    font-family: 'Norican', cursive !important;
    font-size: 32px !important; 
    font-weight: 400; 
    color: #ffffff !important;
}

.ac-money { 
    background: #ff0000;
    padding: 25px 30px; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    border-top: 2px solid #ffffff;
    border-bottom: 2px solid #ffffff;
}
.ac-money strong { 
    font-family: 'Norican', cursive !important;
    font-size: 40px !important; 
    color: #ffffff !important; 
    font-weight: 400;
    text-shadow: 2px 2px 0 #000000;
}
.ac-money .label {
    font-size: 12px !important;
    color: #ffffff !important;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.ac-bombas { 
    padding: 25px 30px; 
    background: #282828;
    border-top: 2px solid #aaaaaa;
}
.ac-bombas h4 { 
    margin: 0 0 15px; 
    color: #ff0000 !important; 
    font-size: 16px !important; 
    text-transform: uppercase; 
    letter-spacing: 3px; 
    font-weight: 800;
}
.ac-bomba { 
    padding: 15px; 
    font-size: 15px !important; 
    border-bottom: 1px dashed #aaaaaa; 
    color: #ffffff !important;
    background: #1a1a1a;
    margin-bottom: 10px;
    border-left: 4px solid #ff0000;
}
.ac-bomba:last-child { border-bottom: none; }
.ac-bomba a { 
    color: #ffffff !important; 
    text-decoration: none; 
    font-weight: 700;
    font-size: 15px !important;
}
.ac-bomba a:hover { 
    color: #ff0000 !important;
    text-decoration: underline;
}
.ac-bomba .v { 
    color: #ff0000 !important; 
    font-weight: 900; 
    margin-right: 15px;
    font-size: 18px !important;
}

.ac-foot { 
    padding: 20px; 
    text-align: center; 
    background: #1a1a1a;
    border-top: 2px solid #aaaaaa;
}
.ac-foot a { 
    color: #ffffff !important; 
    text-decoration: none; 
    font-weight: 800; 
    font-size: 16px !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    display: inline-block;
    padding: 12px 35px;
    background: #ff0000;
    border: 2px solid #ffffff;
    transition: all 0.3s;
}
.ac-foot a:hover { 
    background: #ffffff;
    color: #ff0000 !important;
}

/* GERADOR DE TÍTULOS */
.title-gen-box { 
    background: #1a1a1a; 
    padding: 30px; 
    border-left: 8px solid #ff0000;
    border-right: 2px solid #aaaaaa;
    border-top: 2px solid #aaaaaa;
    border-bottom: 2px solid #aaaaaa;
    margin-top: 20px;
}
.title-gen-box h3 {
    font-family: 'Kaushan Script', cursive !important;
    color: #ff0000 !important;
    font-size: 32px !important;
    font-weight: 400;
    margin-top: 0;
}
.title-gen-item { 
    background: #282828; 
    padding: 18px 25px; 
    margin-bottom: 12px; 
    border-left: 4px solid #ff0000; 
    color: #ffffff !important; 
    font-size: 16px !important;
    font-weight: 600;
    transition: all 0.3s;
}
.title-gen-item:hover {
    background: #ff0000;
    transform: translateX(10px);
}

/* RODAPÉ */
.footer-creator { 
    text-align: center; 
    padding: 50px 30px; 
    color: #bbbbbb !important; 
    font-size: 14px !important; 
    border-top: 6px solid #ff0000; 
    margin-top: 60px; 
    background: #1a1a1a;
}
.footer-creator strong { 
    color: #ffffff !important; 
    font-weight: 800;
    font-size: 18px !important;
}
.footer-creator .begins-mark { 
    display: inline-block; 
    font-family: 'Kaushan Script', cursive !important;
    color: #ff0000 !important; 
    font-size: 48px !important;
    margin-bottom: 15px;
}

/* COMPONENTES GRADIO */
.gr-box, .gr-input, .gr-dropdown, .gr-slider, .gr-textbox { 
    background: #1a1a1a !important; 
    border: 2px solid #aaaaaa !important; 
    color: #ffffff !important;
    border-radius: 0 !important;
}
.gr-input, .gr-textbox input {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600;
    background: #282828 !important;
}
.gr-dropdown .wrap { 
    background: #1a1a1a !important; 
    border: 2px solid #aaaaaa !important;
}
.gr-dropdown .wrap span { 
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 600;
}
.gr-button-primary { 
    background: #ff0000 !important; 
    border: 3px solid #ffffff !important; 
    color: #ffffff !important; 
    font-weight: 900 !important; 
    letter-spacing: 3px !important;
    font-size: 18px !important;
    text-transform: uppercase;
    padding: 18px 40px !important;
    border-radius: 0 !important;
    box-shadow: 0 4px 0 #000000 !important;
    transition: all 0.1s !important;
}
.gr-button-primary:hover { 
    background: #ffffff !important; 
    color: #ff0000 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #000000 !important;
}
.gr-button-primary:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #000000 !important;
}
.gr-tabs .selected { 
    border-bottom: 4px solid #ff0000 !important; 
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    background: #ff0000 !important;
    padding: 10px 20px;
}
.gr-tabs .unselected { 
    color: #bbbbbb !important;
    font-size: 16px !important;
    background: #282828 !important;
    padding: 10px 20px;
}
.gr-slider .label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.gr-check label {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 600;
}
.gr-markdown, .gr-markdown p, .gr-markdown h3 {
    color: #ffffff !important;
}
.gr-markdown h3 {
    color: #ff0000 !important;
    font-family: 'Kaushan Script', cursive !important;
    font-size: 28px !important;
}
</style>
"""

def render_cards(resultados):
    html = [CSS_BEGINS,'<div class="ac-wrap">']
    if not resultados:
        html.append('<div style="text-align:center;padding:80px 20px;background:#1a1a1a;border-left:8px solid #ff0000;border-right:2px solid #aaaaaa;border-top:2px solid #aaaaaa;border-bottom:2px solid #aaaaaa;margin:40px auto;max-width:800px;"><h3 style="font-family:Kaushan Script,cursive;font-size:36px;color:#ff0000;margin-bottom:20px">Nenhum canal encontrado</h3><p style="font-size:18px;color:#bbbbbb">Tente outra palavra ou faixa de inscritos.</p></div>')
    else:
        est = sum(1 for r in resultados if r["status"]=="ESTOURANDO")
        gm = sum(r["ganho_video"] for r in resultados)/len(resultados)
        html.append(f'''<div class="stats-container">
            <div class="stat-card"><strong>{len(resultados)}</strong><span>Canais</span></div>
            <div class="stat-card"><strong>{est}</strong><span>Estourando</span></div>
            <div class="stat-card"><strong>{brl(gm)}</strong><span>Ganho médio/vídeo</span></div>
        </div>''')
        for r in resultados:
            bc = "rocket" if r["status"]=="ESTOURANDO" else ("up" if r["status"]=="Saudável" else "sleep")
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['emoji']} {r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{r['status']}</span></div>
<div class="ac-card-body">
<div class="ac-stat-mini"><div class="lbl">Inscritos</div><div class="val">{fmt(r['inscritos'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">Views/vídeo</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">Taxa viral</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">Mediana</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div class="label">Ganho por vídeo</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right"><div class="label">Total do canal</div><strong>{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>''')
            if r['bombas']:
                html.append('<div class="ac-bombas"><h4>Modelos para copiar</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:70]}{"..." if len(b["titulo"])>70 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">Abrir canal no YouTube →</a></div></div>')
    html.append('</div>')
    return "".join(html)

# ═══════════════ FUNÇÕES ═══════════════
def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return "<div style='padding:60px;text-align:center;color:#ff0000;font-size:22px;font-weight:700;background:#1a1a1a;border-left:8px solid #ff0000;border-right:2px solid #aaaaaa;border-top:2px solid #aaaaaa;border-bottom:2px solid #aaaaaa;margin:40px auto;max-width:800px;font-family:Kaushan Script,cursive'>Digite o que você quer caçar!</div>", None
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div style='padding:60px;text-align:center;color:#ff0000;font-size:22px;font-weight:700;background:#1a1a1a;border-left:8px solid #ff0000;border-right:2px solid #aaaaaa;border-top:2px solid #aaaaaa;border-bottom:2px solid #aaaaaa;margin:40px auto;max-width:800px;font-family:Kaushan Script,cursive'>Nada encontrado. Tente outra palavra.</div>", None
    canais = {}
    for v in vids_achados:
        uc = v.get("channel_url") or v.get("uploader_url")
        if uc and uc not in canais: canais[uc] = v.get("channel") or v.get("uploader")
    resultados = []
    for url in list(canais.keys())[:int(qtd)*2]:
        a = analisar_canal(url, int(vids))
        if a is None: continue
        ins = a["inscritos"]
        if ins is None or ins<insc_min or ins>insc_max: continue
        tx = a["taxa"] or 0
        a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","") if tx>=0.3 else ("Estagnado","😴"))
        a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
        resultados.append(a)
        if len(resultados)>=int(qtd): break
        time.sleep(random.uniform(0.4,1.0))
    resultados.sort(key=lambda x: x.get("taxa",0) or 0, reverse=True)

    csv_path = None
    if resultados:
        dados = [{"canal":r["nome"],"url":r["url"],"inscritos":r["inscritos"],"status":r["status"],
                  "taxa":round(r["taxa"] or 0,3),"media_views":int(r["media_rec"]),"mediana":int(r["mediana"]),
                  "views_totais":r["views_totais"],"ganho_video":round(r["ganho_video"],2),
                  "ganho_total":round((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r["rpm"],2),
                  "data":datetime.date.today().isoformat()} for r in resultados]
        csv_path = f"Relatorio_Begins_{datetime.date.today().isoformat()}.csv"
        with open(csv_path,"w",newline="",encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=dados[0].keys()); w.writeheader(); w.writerows(dados)
    return render_cards(resultados), csv_path

def analisar_canal_ui(url_canal, nicho_label, vids, estrangeiro):
    if not url_canal or not url_canal.strip():
        return "<div style='padding:60px;text-align:center;color:#ff0000;font-size:22px;font-weight:700;background:#1a1a1a;border-left:8px solid #ff0000;border-right:2px solid #aaaaaa;border-top:2px solid #aaaaaa;border-bottom:2px solid #aaaaaa;margin:40px auto;max-width:800px;font-family:Kaushan Script,cursive'>Cole o link do canal!</div>"
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return "<div style='padding:60px;text-align:center;color:#ff0000;font-size:22px;font-weight:700;background:#1a1a1a;border-left:8px solid #ff0000;border-right:2px solid #aaaaaa;border-top:2px solid #aaaaaa;border-bottom:2px solid #aaaaaa;margin:40px auto;max-width:800px;font-family:Kaushan Script,cursive'>Canal não encontrado. Verifique o link.</div>"
    tx = a["taxa"] or 0
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a])

def gerar_titulos(nicho, palavra_chave):
    if not palavra_chave:
        return "<div style='padding:40px;text-align:center;color:#ff0000;font-size:20px'>Digite uma palavra-chave (ex: 'carros abandonados', 'casos criminais').</div>"
    kw = palavra_chave.strip().title()
    titulos = [
        f"🚨 A Verdade Sombria Sobre {kw} Que Ninguém Te Conta",
        f"💰 Como {kw} Está Fazendo Criadores de Conteúdo Ficarem Milionários",
        f"⚠️ 7 Fatos Assustadores Sobre {kw} (O Número 4 Vai Te Chocar)",
        f"📉 Por Que {kw} Está Falindo Rapidamente em 2024",
        f"👑 O Segredo Por Trás do Sucesso de {kw} (Estudo de Caso)",
        f"🔥 Top 10 Maiores Mistérios de {kw} Resolvidos",
        f"💀 Eu Investi 30 Dias Estudando {kw} e o Resultado Foi Assustador"
    ]
    html = f'<div class="title-gen-box"><h3>7 TÍTULOS DE ALTA CONVERSÃO PARA: "{kw}"</h3>'
    for t in titulos:
        html += f'<div class="title-gen-item">{t}</div>'
    html += '<p style="color:#bbbbbb;font-size:16px;margin-top:25px;padding-top:20px;border-top:2px solid #aaaaaa"><strong style="color:#ff0000;font-size:18px">Dica de Murilo Silva:</strong><br>Combine estes títulos com thumbnails de alto contraste — rosto com expressão forte + seta vermelha + texto curto em até 3 palavras.</p></div>'
    return html

# ═══════════════ INTERFACE ═══════════════
begins_theme = gr.themes.Base(
    primary_hue="red",
    secondary_hue="neutral",
    neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins · Assistente do Criador", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span>Assistente do Criador</h1>
        <div class="creator">Murilo Silva</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">Versão 7.0</span>
    </div>
    """)
    
    with gr.Tabs():
        with gr.Tab("🕵️ Caçador de Canais"):
            gr.Markdown("### Encontre canais que estão estourando e modele o sucesso")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label="O que caçar?", placeholder="Ex: histórias de terror, carros abandonados, true crime...")
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="Nicho")
            with gr.Row():
                qtd = gr.Slider(3,20,value=8,step=1,label="Quantos canais")
                vids_caca = gr.Slider(10,50,value=30,step=5,label="Vídeos por canal")
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label="Inscritos mín.")
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label="Inscritos máx.")
            estrangeiro = gr.Checkbox(True, label="Público estrangeiro (paga 3x mais)")
            btn = gr.Button("INICIAR CAÇADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label="Baixar Relatório (CSV)")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv])

        with gr.Tab("🔎 Analisar Canal"):
            gr.Markdown("### Cole o link de um canal para uma auditoria completa")
            url_analise = gr.Textbox(label="Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="Canal em inglês/espanhol?")
            btn2 = gr.Button("AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=out2)

        with gr.Tab("🧠 Gerador de Títulos"):
            gr.Markdown("### Crie títulos que o algoritmo do YouTube é obrigado a recomendar")
            gr.Markdown("Baseado nas fórmulas de copywriting dos maiores canais Dark do mundo.")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value=" Histórias/Crimes", label="Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="Palavra-chave ou Tema do Vídeo", placeholder="Ex: navio fantasma, loteria não reclamada, mansão abandonada")
            btn_gen = gr.Button("GERAR TÍTULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab("💡 Guia"):
            gr.Markdown("""
            ### Como usar o Begins
            
            **1. Caçador de Canais:** Digite o tema, escolha o nicho e clique em INICIAR CAÇADA. Foque nos canais marcados como ESTOURANDO.
            **2. Analisador:** Já tem um concorrente? Cole o link e veja a média real de views (esqueça o número total de inscritos, olhe a mediana!).
            **3. Gerador de Títulos:** Use esta aba para criar títulos infalíveis baseados no tema que você escolheu.
            
            **Dicas de Murilo Silva:**
            - Busque em inglês (`true crime`, `abandoned places`) para achar canais que pagam 3x mais (RPM alto).
            - Taxa viral acima de **1.0x** significa que o YouTube está entregando o vídeo para não-inscritos. É ouro puro.
            - Modele a estrutura (gancho, ritmo, edição) dos vídeos na seção "Modelos para copiar", mas **nunca copie o roteiro palavra por palavra**.
            """)

    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div><br>
        <strong>O ponto de partida para o seu novo negócio.</strong><br><br>
        Desenvolvido por <strong>Murilo Silva</strong><br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
