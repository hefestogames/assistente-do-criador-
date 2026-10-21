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
    "🎬 Curiosidades":12,"🔪 Histórias/Crimes":18,"📽️ Documentário":20,
    "🎥 Resumo de Filmes":15,"🙏 Religião":10,"💪 Motivacional":9,
    "🎵 Música/Relax":4,"🎮 Games":8,"⚽ Esportes":14,
    "🚗 Carros":26," Tecnologia/IA":35,"💊 Saúde":22,"💰 Finanças":55,
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

# ═══════════════ CSS DOS CARDS ═══════════════
CSS_CARDS = """<style>
.ac-wrap{font-family:'Segoe UI',sans-serif;max-width:950px;margin:0 auto;color:#e2e8f0}
.ac-stats{display:flex;gap:12px;margin-bottom:20px}
.ac-stat{flex:1;background:#1e293b;padding:16px;border-radius:12px;text-align:center;border:1px solid #334155}
.ac-stat strong{display:block;font-size:26px;color:#60a5fa}.ac-stat span{color:#94a3b8;font-size:12px}
.ac-card{background:#1e293b;border-radius:14px;margin:16px 0;overflow:hidden;border:1px solid #334155}
.ac-card-head{padding:16px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #334155;background:#0f172a}
.ac-card-head h3{margin:0;font-size:17px;color:#f1f5f9}
.ac-badge{padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700}
.ac-badge-rocket{background:#10b981;color:#fff}.ac-badge-up{background:#f59e0b;color:#000}.ac-badge-sleep{background:#ef4444;color:#fff}
.ac-card-body{padding:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.ac-stat-mini{background:#0f172a;padding:10px;border-radius:8px;text-align:center}
.ac-stat-mini .lbl{font-size:10px;color:#64748b;text-transform:uppercase}.ac-stat-mini .val{font-size:16px;font-weight:600;color:#e2e8f0;margin-top:4px}
.ac-money{background:linear-gradient(135deg,#059669,#10b981);padding:14px 20px;display:flex;justify-content:space-between;align-items:center}
.ac-money strong{font-size:20px;color:#fff}
.ac-bombas{padding:14px 20px;border-top:1px solid #334155}
.ac-bombas h4{margin:0 0 10px;color:#fbbf24;font-size:12px;text-transform:uppercase}
.ac-bomba{padding:8px 0;font-size:13px;border-bottom:1px dashed #334155;color:#cbd5e1}
.ac-bomba:last-child{border:none}
.ac-bomba a{color:#60a5fa;text-decoration:none}.ac-bomba .v{color:#34d399;font-weight:700;margin-right:8px}
.ac-foot{padding:12px;text-align:center;background:#0f172a}
.ac-foot a{color:#60a5fa;text-decoration:none;font-weight:600;font-size:13px}
.ac-empty{text-align:center;padding:60px 20px;background:#1e293b;border-radius:14px;color:#94a3b8}
</style>"""

def render_cards(resultados):
    html = [CSS_CARDS,'<div class="ac-wrap">']
    if not resultados:
        html.append('<div class="ac-empty"><h3>😕 Nenhum canal encontrado</h3><p>Tente outra palavra ou faixa de inscritos.</p></div>')
    else:
        est = sum(1 for r in resultados if r["status"]=="ESTOURANDO")
        gm = sum(r["ganho_video"] for r in resultados)/len(resultados)
        html.append(f'<div class="ac-stats"><div class="ac-stat"><strong>{len(resultados)}</strong><span>Canais</span></div><div class="ac-stat"><strong>{est} 🚀</strong><span>Estourando</span></div><div class="ac-stat"><strong>{brl(gm)}</strong><span>Ganho médio/vídeo</span></div></div>')
        for r in resultados:
            bc = "rocket" if r["status"]=="ESTOURANDO" else ("up" if r["status"]=="Saudável" else "sleep")
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['emoji']} {r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{r['status']}</span></div>
<div class="ac-card-body">
<div class="ac-stat-mini"><div class="lbl">👥 Inscritos</div><div class="val">{fmt(r['inscritos'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">📈 Views/vídeo</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl"> Taxa viral</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">📊 Mediana</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div style="font-size:10px;opacity:.8;color:#d1fae5">GANHO POR VÍDEO</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right;font-size:11px;color:#d1fae5">Total do canal<br><strong style="font-size:16px">{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>''')
            if r['bombas']:
                html.append('<div class="ac-bombas"><h4>🧬 Modelos para copiar</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:65]}{"..." if len(b["titulo"])>65 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">🔗 Abrir canal no YouTube →</a></div></div>')
    html.append('</div>')
    return "".join(html)

# ══════════════ FUNÇÃO CAÇADOR ═══════════════
def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return "<div style='padding:40px;text-align:center;color:#f87171'>⚠️ Digite o que você quer caçar!</div>", None
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div style='padding:40px;text-align:center;color:#f87171'>❌ Nada encontrado. Tente outra palavra.</div>", None
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
        a["status"], a["emoji"] = ("ESTOURANDO","") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
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
                  "ganho_total":round((r["views_totais"] or sum(v['views'] for v in r['videos']))/1000*r["rpm"],2),
                  "data":datetime.date.today().isoformat()} for r in resultados]
        csv_path = f"assistente_criador_{datetime.date.today().isoformat()}.csv"
        with open(csv_path,"w",newline="",encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=dados[0].keys()); w.writeheader(); w.writerows(dados)
    return render_cards(resultados), csv_path

# ═══════════════ FUNÇÃO ANALISADOR ═══════════════
def analisar_canal_ui(url_canal, nicho_label, vids, estrangeiro):
    if not url_canal or not url_canal.strip():
        return "<div style='padding:40px;text-align:center;color:#f87171'>⚠️ Cole o link do canal!</div>"
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return "<div style='padding:40px;text-align:center;color:#f87171'>❌ Canal não encontrado. Verifique o link.</div>"
    tx = a["taxa"] or 0
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a])

# ═══════════════ INTERFACE ═══════════════
custom_css = """
.gradio-container { max-width: 1100px !important; margin: auto !important; }
.ac-header { background: linear-gradient(135deg, #1e3a8a, #7c3aed); border-radius: 20px; padding: 40px 30px; text-align: center; margin-bottom: 30px; color: white; }
.ac-header h1 { margin: 0; font-size: 40px; font-weight: 800; }
.ac-header .subtitle { margin: 12px 0 0; font-size: 16px; opacity: 0.9; color: #c7d2fe; }
.ac-header .badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 12px; margin-top: 16px; }
"""

with gr.Blocks(title="Assistente do Criador", theme=gr.themes.Base(), css=custom_css) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1>🎬 Assistente do Criador</h1>
        <p class="subtitle">Seu radar inteligente para descobrir canais dark que estão estourando</p>
        <span class="badge">✨ 100% Gratuito · Powered by YouTube</span>
    </div>
    """)
    with gr.Tabs():
        with gr.Tab("🕵️ Caçador de Canais"):
            gr.Markdown("### 🔍 Encontre canais que estão estourando")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label="🎯 O que caçar?", placeholder="Ex: histórias de terror, carros abandonados, true crime...")
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value=" Histórias/Crimes", label="💰 Nicho")
            with gr.Row():
                qtd = gr.Slider(3,20,value=8,step=1,label="📊 Quantos canais")
                vids_caca = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos por canal")
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label="👥 Inscritos mín.")
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label="👥 Inscritos máx.")
            estrangeiro = gr.Checkbox(True, label="🌍 Público estrangeiro (paga 3x mais)")
            btn = gr.Button("🚀 INICIAR CAÇADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label="📥 Planilha")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv])

        with gr.Tab("🔎 Analisar Canal Específico"):
            gr.Markdown("### 🔗 Cole o link de um canal")
            url_analise = gr.Textbox(label="📎 Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="💰 Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="🌍 Canal em inglês/espanhol?")
            btn2 = gr.Button("📊 ANALISAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=out2)

        with gr.Tab("💡 Guia"):
            gr.Markdown("""
            ###  Como usar
            **🕵️ Caçador**: digite o tema, escolha o nicho, clique em INICIAR CAÇADA.
            **🔎 Analisador**: cole o link de um canal e veja tudo sobre ele.
            **💰 Dicas**: busque em inglês para achar canais que pagam 3x mais. Taxa viral acima de 1.0x = ESTOURANDO 🚀
            """)

    gr.HTML('<div style="text-align:center;padding:30px;color:#64748b;font-size:13px">🎬 Assistente do Criador · v2.0</div>')

# ═══════════════ LINHA MÁGICA PRO RENDER ═══════════════
app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
