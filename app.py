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
    "🎬 Curiosidades":12, "🔪 Histórias/Crimes":18, "📽️ Documentário":20,
    "🎥 Resumo de Filmes":15, "🙏 Religião":10, "💪 Motivacional":9,
    "🎵 Música/Relax":4, "🎮 Games":8, "⚽ Esportes":14,
    "🚗 Carros":26, " Tecnologia/IA":35, "💊 Saúde":22, "💰 Finanças":55,
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

# ═══════════════ CSS IDENTIDADE BEGINS (Verde + Dourado) ═══════════════
CSS_BEGINS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

* { font-family: 'Inter', 'Segoe UI', sans-serif !important; }

.gradio-container { 
    max-width: 1150px !important; 
    margin: auto !important; 
    background-color: #0a2e1e; 
}

/* HEADER PRINCIPAL */
.ac-header { 
    background: linear-gradient(135deg, #0a2e1e 0%, #0d4a30 40%, #1a6b4a 100%); 
    border-radius: 24px; 
    padding: 50px 30px; 
    text-align: center; 
    margin-bottom: 30px; 
    color: white; 
    border: 2px solid #d4af37; 
    box-shadow: 0 10px 50px rgba(212,175,55,0.25), inset 0 0 60px rgba(16,185,129,0.1); 
    position: relative;
    overflow: hidden;
}
.ac-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(212,175,55,0.08) 0%, transparent 70%);
    animation: shimmer 8s infinite linear;
}
@keyframes shimmer {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.ac-header h1 { 
    margin: 0; 
    font-size: 42px; 
    font-weight: 900; 
    letter-spacing: -1px;
    color: #f5f5f0;
    position: relative;
}
.ac-header h1 .begins { 
    color: #d4af37; 
    text-shadow: 0 0 20px rgba(212,175,55,0.5);
}
.ac-header .creator { 
    font-size: 13px; 
    color: #d4af37; 
    font-weight: 700; 
    margin-top: 12px; 
    text-transform: uppercase; 
    letter-spacing: 2px;
    position: relative;
}
.ac-header .subtitle { 
    margin: 14px 0 0; 
    font-size: 17px; 
    opacity: 0.95; 
    color: #e8f5ef; 
    position: relative;
}
.ac-header .badge { 
    display: inline-block; 
    background: rgba(212,175,55,0.15); 
    padding: 8px 20px; 
    border-radius: 24px; 
    font-size: 12px; 
    margin-top: 18px; 
    border: 1px solid rgba(212,175,55,0.4); 
    color: #f4c430;
    font-weight: 600;
    position: relative;
}

/* ESTATÍSTICAS TOPO */
.ac-stats{display:flex;gap:14px;margin-bottom:24px}
.ac-stat{
    flex:1;
    background: linear-gradient(135deg, #0d4a30, #0a2e1e);
    padding:20px;
    border-radius:14px;
    text-align:center;
    border:1px solid #1a6b4a;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.ac-stat strong{display:block;font-size:28px;color:#d4af37;font-weight:800}
.ac-stat span{color:#a8d5c0;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}

/* CARDS DE CANAL */
.ac-card{
    background: linear-gradient(135deg, #0d4a30, #0a2e1e);
    border-radius:16px;
    margin:18px 0;
    overflow:hidden;
    border:1px solid #1a6b4a; 
    transition: all 0.3s;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.ac-card:hover{
    transform: translateY(-4px); 
    border-color: #d4af37;
    box-shadow: 0 8px 30px rgba(212,175,55,0.2);
}
.ac-card-head{
    padding:18px 22px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-bottom:1px solid #1a6b4a;
    background: rgba(10,46,30,0.8);
}
.ac-card-head h3{margin:0;font-size:18px;color:#f5f5f0;font-weight:700}
.ac-badge{padding:6px 16px;border-radius:24px;font-size:11px;font-weight:700;letter-spacing:0.5px}
.ac-badge-rocket{background:linear-gradient(135deg,#10b981,#059669);color:#fff;box-shadow:0 2px 10px rgba(16,185,129,0.4)}
.ac-badge-up{background:linear-gradient(135deg,#f4c430,#d4af37);color:#0a2e1e}
.ac-badge-sleep{background:#64748b;color:#fff}

.ac-card-body{padding:20px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.ac-stat-mini{
    background: rgba(10,46,30,0.6);
    padding:12px;
    border-radius:10px;
    text-align:center;
    border:1px solid #1a6b4a;
}
.ac-stat-mini .lbl{font-size:10px;color:#a8d5c0;text-transform:uppercase;font-weight:600;letter-spacing:0.5px}
.ac-stat-mini .val{font-size:17px;font-weight:700;color:#f5f5f0;margin-top:4px}

.ac-money{
    background:linear-gradient(135deg,#0d4a30,#1a6b4a);
    padding:16px 22px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-top:1px solid #1a6b4a;
    border-bottom:1px solid #1a6b4a;
}
.ac-money strong{font-size:22px;color:#d4af37;font-weight:800}

.ac-bombas{
    padding:16px 22px;
    background: rgba(212,175,55,0.05);
    border-top:1px solid #1a6b4a;
}
.ac-bombas h4{
    margin:0 0 12px;
    color:#d4af37;
    font-size:12px;
    text-transform:uppercase; 
    letter-spacing: 1.5px;
    font-weight:700;
}
.ac-bomba{
    padding:10px 0;
    font-size:14px;
    border-bottom:1px dashed #1a6b4a;
    color:#e8f5ef;
}
.ac-bomba:last-child{border:none}
.ac-bomba a{color:#10b981;text-decoration:none;font-weight:600}
.ac-bomba a:hover{color:#d4af37}
.ac-bomba .v{color:#d4af37;font-weight:800;margin-right:10px}

.ac-foot{
    padding:14px;
    text-align:center;
    background: rgba(10,46,30,0.6);
}
.ac-foot a{color:#d4af37;text-decoration:none;font-weight:700;font-size:13px;letter-spacing:0.5px}
.ac-foot a:hover{color:#f4c430}

.ac-empty{
    text-align:center;
    padding:60px 20px;
    background: linear-gradient(135deg, #0d4a30, #0a2e1e);
    border-radius:16px;
    color:#a8d5c0; 
    border: 1px solid #1a6b4a;
}

/* GERADOR DE TÍTULOS */
.title-gen-box { 
    background: linear-gradient(135deg, #0d4a30, #0a2e1e); 
    padding: 24px; 
    border-radius: 14px; 
    border: 1px solid #d4af37; 
    margin-top: 10px;
    box-shadow: 0 4px 20px rgba(212,175,55,0.15);
}
.title-gen-item { 
    background: rgba(10,46,30,0.7); 
    padding: 14px 18px; 
    border-radius: 10px; 
    margin-bottom: 10px; 
    border-left: 4px solid #d4af37; 
    color: #f5f5f0; 
    font-size: 15px;
    font-weight: 500;
    transition: all 0.2s;
}
.title-gen-item:hover {
    background: rgba(212,175,55,0.1);
    transform: translateX(4px);
}

/* RODAPÉ */
.footer-creator { 
    text-align:center; 
    padding: 40px 30px; 
    color: #a8d5c0; 
    font-size: 13px; 
    border-top: 1px solid #1a6b4a; 
    margin-top: 50px; 
    background: rgba(10,46,30,0.4);
    border-radius: 0 0 24px 24px;
}
.footer-creator strong { color: #d4af37; font-weight:800; }
.footer-creator .begins-mark { 
    display: inline-block; 
    color: #d4af37; 
    font-weight: 900; 
    font-size: 18px; 
    letter-spacing: 2px;
    margin-bottom: 8px;
}

/* BOTÕES PRIMÁRIOS */
button.primary {
    background: linear-gradient(135deg, #0d4a30, #1a6b4a) !important;
    border: 2px solid #d4af37 !important;
    color: #d4af37 !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    transition: all 0.3s !important;
}
button.primary:hover {
    background: linear-gradient(135deg, #1a6b4a, #0d4a30) !important;
    box-shadow: 0 0 25px rgba(212,175,55,0.4) !important;
    transform: translateY(-2px);
}
</style>"""

def render_cards(resultados):
    html = [CSS_BEGINS,'<div class="ac-wrap">']
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
<div class="ac-stat-mini"><div class="lbl"> Views/vídeo</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">🔥 Taxa viral</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">📊 Mediana</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div style="font-size:10px;opacity:.8;color:#a8d5c0;font-weight:600">GANHO POR VÍDEO</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right;font-size:11px;color:#a8d5c0;font-weight:600">Total do canal<br><strong style="font-size:18px">{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>''')
            if r['bombas']:
                html.append('<div class="ac-bombas"><h4>🧬 Modelos para copiar</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:65]}{"..." if len(b["titulo"])>65 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">🔗 ABRIR CANAL NO YOUTUBE →</a></div></div>')
    html.append('</div>')
    return "".join(html)

# ═══════════════ FUNÇÃO CAÇADOR ═══════════════
def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return "<div style='padding:40px;text-align:center;color:#f87171'>️ Digite o que você quer caçar!</div>", None
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div style='padding:40px;text-align:center;color:#f87171'> Nada encontrado. Tente outra palavra.</div>", None
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
        a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado",""))
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

# ═══════════════ FUNÇÃO ANALISADOR ═══════════════
def analisar_canal_ui(url_canal, nicho_label, vids, estrangeiro):
    if not url_canal or not url_canal.strip():
        return "<div style='padding:40px;text-align:center;color:#f87171'>️ Cole o link do canal!</div>"
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

# ═══════════════ GERADOR DE TÍTULOS VIRAIS ═══════════════
def gerar_titulos(nicho, palavra_chave):
    if not palavra_chave:
        return "⚠️ Digite uma palavra-chave (ex: 'carros abandonados', 'casos criminais')."
    
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
    
    html = f'<div class="title-gen-box"><h3 style="color:#d4af37; margin-top:0; font-weight:800;"> 7 TÍTULOS DE ALTA CONVERSÃO PARA: "{kw}"</h3>'
    for t in titulos:
        html += f'<div class="title-gen-item">{t}</div>'
    html += '<p style="color:#a8d5c0; font-size:13px; margin-top:18px; border-top:1px solid #1a6b4a; padding-top:14px;">💎 <strong style="color:#d4af37">Dica de Murilo Silva (Canal Begins):</strong> Combine estes títulos com thumbnails de alto contraste — rosto com expressão forte + seta vermelha + texto curto em até 3 palavras. A taxa de clique pode dobrar.</p></div>'
    return html

# ═══════════════ INTERFACE BEGINS ═══════════════
with gr.Blocks(title="Begins · Assistente do Criador", theme=gr.themes.Base()) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1>🐘 <span class="begins">BEGINS</span> · Assistente do Criador</h1>
        <div class="creator">Murilo Silva · Criador de Conteúdo do Canal Begins</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube.</p>
        <span class="badge">✨ Versão 4.0 · Ideias Práticas · Renda Extra · Crescimento no Zero</span>
    </div>
    """)
    
    with gr.Tabs():
        with gr.Tab("🕵️ Caçador de Canais"):
            gr.Markdown("### 🔍 Encontre canais que estão estourando e modele o sucesso")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label="🎯 O que caçar?", placeholder="Ex: histórias de terror, carros abandonados, true crime...")
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho")
            with gr.Row():
                qtd = gr.Slider(3,20,value=8,step=1,label=" Quantos canais")
                vids_caca = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos por canal")
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label=" Inscritos mín.")
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label="👥 Inscritos máx.")
            estrangeiro = gr.Checkbox(True, label="🌍 Público estrangeiro (paga 3x mais)")
            btn = gr.Button("🚀 INICIAR CAÇADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label="📥 Baixar Relatório Begins (CSV)")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv])

        with gr.Tab("🔎 Analisar Canal Específico"):
            gr.Markdown("### 🔗 Cole o link de um canal para uma auditoria completa")
            url_analise = gr.Textbox(label="📎 Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="💰 Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="🌍 Canal em inglês/espanhol?")
            btn2 = gr.Button("📊 AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=out2)

        with gr.Tab("🧠 Gerador de Títulos Virais"):
            gr.Markdown("### ✍️ Crie títulos que o algoritmo do YouTube é obrigado a recomendar")
            gr.Markdown("Baseado nas fórmulas de copywriting dos maiores canais Dark do mundo.")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="🎯 Palavra-chave ou Tema do Vídeo", placeholder="Ex: navio fantasma, loteria não reclamada, mansão abandonada")
            btn_gen = gr.Button("✨ GERAR TÍTULOS DE ALTA CONVERSÃO", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab("💡 Guia & Estratégia"):
            gr.Markdown("""
            ### 📖 Como usar o Begins · Assistente do Criador
            
            **1. 🕵️ Caçador de Canais:** Digite o tema, escolha o nicho e clique em INICIAR CAÇADA. Foque nos canais marcados com 🚀 ESTOURANDO.
            **2. 🔎 Analisador:** Já tem um concorrente? Cole o link e veja a média real de views (esqueça o número total de inscritos, olhe a mediana!).
            **3. 🧠 Gerador de Títulos:** Use esta aba para criar títulos infalíveis baseados no tema que você escolheu.
            
            **💎 Dicas de Ouro de Murilo Silva (Canal Begins):**
            - Busque em inglês (`true crime`, `abandoned places`) para achar canais que pagam 3x mais (RPM alto).
            - Taxa viral acima de **1.0x** significa que o YouTube está entregando o vídeo para não-inscritos. É ouro puro.
            - Modele a estrutura (gancho, ritmo, edição) dos vídeos na seção "Modelos para copiar", mas **nunca copie o roteiro palavra por palavra**.
            - **Comece pequeno:** canais com 10k-100k inscritos são mais fáceis de superar do que os gigantes.
            """)

    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div><br>
        <strong>O ponto de partida para o seu novo negócio.</strong><br><br>
        Desenvolvido por <strong>Murilo Silva</strong> · Criador de Conteúdo do Canal Begins<br>
        <span style="font-size:11px; opacity:0.7">💡 Ideias Práticas · 💰 Renda Extra · 📈 Crescimento no Zero</span><br>
        <span style="font-size:10px; opacity:0.5; margin-top:10px; display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

# ═══════════════ LINHA MÁGICA PRO RENDER ═══════════════
app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
