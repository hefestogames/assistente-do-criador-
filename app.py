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
    "🚗 Carros":26, "🤖 Tecnologia/IA":35, "💊 Saúde":22, "💰 Finanças":55,
    "🎙️ Cortes de Podcast":8, "🧘 Meditação":6, "₿ Finanças Cripto":45,
    "📱 Shorts/TikTok":5, "🎯 Marketing Digital":40, "🏋️ Fitness":18,
    "🍳 Receitas":14, "🐶 Pets":16, "✈️ Viagens":28,
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

# ═══════════════ GERADOR DE TÍTULOS COM IA (POR TÍTULO, SEM ERROS) ═══════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:20px;font-family:Poppins,sans-serif'>⚠️ Digite o título de um vídeo viral!</div>"
    
    try:
        numeros = re.findall(r'\d+', titulo_video)
        titulos_ia = []
        
        # Padrão 1: Mudar números
        if numeros:
            num_base = int(numeros[0])
            for mult in [0.5, 2, 10, 100]:
                novo_num = max(1, int(num_base * mult))
                novo_titulo = re.sub(r'\d+', str(novo_num), titulo_video, count=1)
                titulos_ia.append(f"🔢 {novo_titulo}")
        
        # Padrão 2: Trocar valores monetários
        if "$" in titulo_video or "R$" in titulo_video:
            valores = ["$1", "$100", "$1,000", "$10,000", "$100,000", "$1,000,000"]
            for valor in valores[:5]:
                novo_titulo = re.sub(r'[\$R\$][\d,\.]+', valor, titulo_video)
                if novo_titulo != titulo_video:
                    titulos_ia.append(f"💰 {novo_titulo}")
        
        # Padrão 3: Trocar períodos de tempo
        tempos = ["24 Horas", "7 Dias", "30 Dias", "100 Dias", "1 Ano"]
        for tempo in tempos:
            novo_titulo = re.sub(r'\d+\s*(dias?|horas?|minutos?)', tempo, titulo_video, flags=re.I)
            if novo_titulo != titulo_video:
                titulos_ia.append(f"⏱️ {novo_titulo}")
        
        # Padrão 4: Adicionar urgência
        if len(titulos_ia) < 10:
            titulos_ia.append(f"🚨 URGENTE: {titulo_video}")
            titulos_ia.append(f"⚠️ ATENÇÃO: {titulo_video}")
            titulos_ia.append(f"💥 IMPRESSIONANTE: {titulo_video}")
        
        # Remover duplicatas e limitar a 10
        titulos_ia = list(dict.fromkeys(titulos_ia))[:10]
        
        html = f'''
        <div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 30px; border-radius: 20px; border: 3px solid #f97316; margin-top: 20px; box-shadow: 0 8px 40px rgba(249,115,22,0.4);">
            <h3 style="color: #fde047 !important; font-size: 24px !important; font-weight: 900; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; font-family: 'Poppins', sans-serif;">
                📊 Título Original Analisado
            </h3>
            <p style="color: #ffffff; font-size: 18px; font-weight: 600; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; border-left: 4px solid #f97316;">
                {titulo_video}
            </p>
            <h3 style="color: #f97316 !important; font-size: 24px !important; font-weight: 800; margin-top: 30px; text-transform: uppercase; letter-spacing: 2px; font-family: 'Poppins', sans-serif;">
                🎯 10 TÍTULOS GERADOS PELA IA:
            </h3>
        '''
        
        for i, titulo in enumerate(titulos_ia, 1):
            html += f'''
            <div style="background: linear-gradient(135deg, #0f0f1e, #1e1b4b); padding: 18px 25px; border-radius: 12px; margin-bottom: 12px; border-left: 6px solid #f97316; color: #ffffff !important; font-size: 16px !important; font-weight: 600; box-shadow: 0 4px 20px rgba(124,58,237,0.3); transition: all 0.3s;">
                <span style="color: #fde047; font-weight: 800; margin-right: 10px;">{i}.</span> {titulo}
            </div>
            '''
        
        html += '''
            <p style="color: #c4b5fd; font-size: 16px; margin-top: 25px; padding-top: 20px; border-top: 3px solid #6d28d9; text-align: center;">
                <strong style="color: #fde047; font-size: 18px;">💎 Dica:</strong> Escolha o título que melhor se adapta ao seu público e combine com uma thumbnail impactante!
            </p>
        </div>
        '''
        return html
    except Exception as e:
        return f"❌ Erro ao gerar títulos: {str(e)}"

def gerar_titulos_simples(nicho, palavra_chave):
    if not palavra_chave:
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:20px;font-family:Poppins,sans-serif'>⚠️ Digite uma palavra-chave.</div>"
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
    html = f'<div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 30px; border-radius: 20px; border: 3px solid #f97316; margin-top: 20px;">'
    html += f'<h3 style="color: #fde047 !important; font-size: 24px !important; font-weight: 900; margin-top: 0; font-family: Poppins, sans-serif;">💡 7 TÍTULOS PARA: "{kw}"</h3>'
    for t in titulos:
        html += f'<div style="background: linear-gradient(135deg, #0f0f1e, #1e1b4b); padding: 18px 25px; border-radius: 12px; margin-bottom: 12px; border-left: 6px solid #f97316; color: #ffffff !important; font-size: 16px !important; font-weight: 600;">{t}</div>'
    html += '</div>'
    return html

# ═══════════════ CSS MODERNO E VIBRANTE ═══════════════
CSS_BEGINS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@400;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
body, .gradio-container, .main, .wrap, .gradio-app { 
    background: linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 50%, #16213E 100%) !important; 
    color: #ffffff !important;
}

.ac-header { 
    background: linear-gradient(135deg, #6D28D9 0%, #7C3AED 50%, #A78BFA 100%); 
    border-radius: 20px; padding: 50px 40px; text-align: center; margin: 20px auto 40px; 
    border: 4px solid #F97316; box-shadow: 0 0 80px rgba(249,115,22,0.6), 0 15px 60px rgba(124,58,237,0.5); 
    position: relative; max-width: 1200px;
}
.ac-header::before {
    content: '⚠ ALERTA DE OPORTUNIDADE ⚠';
    position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
    background: #F97316; color: #0F0F1E; padding: 6px 24px; font-size: 12px; font-weight: 900;
    letter-spacing: 3px; font-family: 'Poppins', sans-serif; border-radius: 20px;
}
.ac-header h1 { 
    margin: 0; font-family: 'Poppins', sans-serif !important; font-size: 64px !important; 
    font-weight: 900 !important; color: #FDE047 !important;
    text-shadow: 0 0 40px rgba(253,224,71,0.8), 0 4px 12px rgba(0,0,0,0.8); letter-spacing: 2px;
}
.ac-header .begins { 
    color: #F97316 !important; display: block; font-family: 'Montserrat', sans-serif !important;
    font-size: 72px !important; margin-bottom: 10px; font-weight: 900; text-shadow: 0 0 50px rgba(249,115,22,0.9);
}
.ac-header .creator { 
    font-family: 'Montserrat', sans-serif !important; font-size: 18px !important; color: #FED7AA !important; 
    font-weight: 700 !important; margin-top: 15px; letter-spacing: 2px;
}
.ac-header .subtitle { margin: 15px 0 0; font-size: 16px !important; color: #ffffff !important; font-weight: 600; letter-spacing: 1px; }
.ac-header .badge { 
    display: inline-block; background: linear-gradient(135deg, #F97316, #FB923C); padding: 10px 25px; 
    border-radius: 25px; font-size: 13px !important; margin-top: 20px; color: #0F0F1E !important;
    font-weight: 800 !important; font-family: 'Poppins', sans-serif; box-shadow: 0 4px 20px rgba(249,115,22,0.5);
}

.stats-container { display: flex; gap: 20px; margin-bottom: 40px; justify-content: center; max-width: 1200px; margin-left: auto; margin-right: auto; }
.stat-card {
    flex: 1; max-width: 320px; background: linear-gradient(135deg, #6D28D9, #7C3AED); padding: 30px;
    border-radius: 20px; text-align: center; border: 3px solid #F97316; box-shadow: 0 8px 40px rgba(124,58,237,0.5);
}
.stat-card strong {
    display: block; font-family: 'Poppins', sans-serif !important; font-size: 52px !important;
    color: #FDE047 !important; font-weight: 900; margin-bottom: 10px; text-shadow: 0 0 30px rgba(253,224,71,0.6);
}
.stat-card span { color: #FED7AA; font-size: 14px !important; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-family: 'Montserrat', sans-serif; }

.ac-card { 
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #1E1B4B 100%); border-radius: 20px; 
    margin: 25px auto; overflow: hidden; border: 3px solid #8B5CF6; box-shadow: 0 10px 50px rgba(139,92,246,0.4);
    max-width: 1200px; transition: all 0.3s;
}
.ac-card:hover { transform: translateY(-5px) scale(1.01); box-shadow: 0 15px 70px rgba(249,115,22,0.6); border-color: #F97316; }
.ac-card-head { 
    padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; 
    border-bottom: 3px solid #6D28D9; background: linear-gradient(135deg, #0F0F1E, #1E1B4B);
}
.ac-card-head h3 { margin: 0; font-family: 'Poppins', sans-serif !important; font-size: 26px !important; color: #ffffff !important; font-weight: 800; }
.ac-badge { padding: 10px 20px; border-radius: 20px; font-size: 13px !important; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; font-family: 'Montserrat', sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
.ac-badge-rocket { background: linear-gradient(135deg, #F97316, #EA580C); color: #ffffff !important; box-shadow: 0 4px 20px rgba(249,115,22,0.5); }
.ac-badge-up { background: linear-gradient(135deg, #FDE047, #FBBF24); color: #0F0F1E !important; }
.ac-badge-sleep { background: linear-gradient(135deg, #64748B, #475569); color: #ffffff !important; }

.ac-card-body { padding: 25px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.ac-stat-mini { background: linear-gradient(135deg, #0F0F1E, #1E1B4B); padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #6D28D9; box-shadow: 0 4px 20px rgba(109,40,217,0.3); }
.ac-stat-mini .lbl { font-size: 12px !important; color: #C4B5FD !important; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; margin-bottom: 8px; font-family: 'Montserrat', sans-serif; }
.ac-stat-mini .val { font-family: 'Poppins', sans-serif !important; font-size: 30px !important; font-weight: 900; color: #FDE047 !important; text-shadow: 0 0 20px rgba(253,224,71,0.5); }

.ac-money { background: linear-gradient(135deg, #6D28D9, #7C3AED); padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; border-top: 3px solid #6D28D9; border-bottom: 3px solid #6D28D9; }
.ac-money strong { font-family: 'Poppins', sans-serif !important; font-size: 38px !important; color: #FDE047 !important; font-weight: 900; text-shadow: 0 0 30px rgba(253,224,71,0.6); }
.ac-money .label { font-size: 12px !important; color: #E9D5FF !important; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-family: 'Montserrat', sans-serif; }

.ac-bombas { padding: 25px 30px; background: rgba(249,115,22,0.1); border-top: 3px solid #6D28D9; }
.ac-bombas h4 { margin: 0 0 15px; color: #F97316 !important; font-size: 18px !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; font-family: 'Poppins', sans-serif; }
.ac-bomba { padding: 15px; font-size: 15px !important; border-bottom: 2px dashed #6D28D9; color: #ffffff !important; background: rgba(15,15,30,0.6); border-radius: 8px; margin-bottom: 10px; }
.ac-bomba:last-child { border: none; }
.ac-bomba a { color: #A78BFA !important; text-decoration: none; font-weight: 700; font-size: 15px !important; }
.ac-bomba a:hover { color: #F97316 !important; text-decoration: underline; }
.ac-bomba .v { color: #FDE047 !important; font-weight: 900; margin-right: 15px; font-size: 18px !important; font-family: 'Poppins', sans-serif; }

.ac-foot { padding: 20px; text-align: center; background: linear-gradient(135deg, #0F0F1E, #1E1B4B); }
.ac-foot a { color: #F97316 !important; text-decoration: none; font-weight: 800; font-size: 16px !important; letter-spacing: 1px; text-transform: uppercase; display: inline-block; padding: 12px 35px; border: 2px solid #F97316; border-radius: 12px; transition: all 0.3s; font-family: 'Montserrat', sans-serif; }
.ac-foot a:hover { background: #F97316; color: #0F0F1E !important; transform: scale(1.05); box-shadow: 0 0 30px rgba(249,115,22,0.6); }

.footer-creator { text-align: center; padding: 50px 30px; color: #A78BFA !important; font-size: 14px !important; border-top: 3px solid #6D28D9; margin-top: 60px; background: linear-gradient(135deg, #0F0F1E, #1E1B4B); border-radius: 0 0 20px 20px; }
.footer-creator strong { color: #FDE047 !important; font-weight: 900; font-size: 16px !important; font-family: 'Poppins', sans-serif; }
.footer-creator .begins-mark { display: inline-block; color: #F97316 !important; font-weight: 900; font-size: 40px !important; letter-spacing: 3px; margin-bottom: 15px; text-transform: uppercase; font-family: 'Montserrat', sans-serif; text-shadow: 0 0 30px rgba(249,115,22,0.6); }

.gr-box, .gr-input, .gr-dropdown, .gr-slider, .gr-textbox { background: linear-gradient(135deg, #1E1B4B, #312E81) !important; border: 2px solid #8B5CF6 !important; color: #ffffff !important; border-radius: 12px !important; }
.gr-input, .gr-textbox input { color: #ffffff !important; font-size: 16px !important; font-weight: 600; font-family: 'Inter', sans-serif; }
.gr-dropdown .wrap { background: linear-gradient(135deg, #1E1B4B, #312E81) !important; border: 2px solid #8B5CF6 !important; }
.gr-dropdown .wrap span { color: #ffffff !important; font-size: 15px !important; font-weight: 600; font-family: 'Inter', sans-serif; }
.gr-button-primary { 
    background: linear-gradient(135deg, #F97316, #EA580C) !important; border: 3px solid #F97316 !important; color: #0F0F1E !important; 
    font-weight: 900 !important; letter-spacing: 2px !important; font-size: 18px !important; text-transform: uppercase;
    padding: 18px 40px !important; border-radius: 12px !important; box-shadow: 0 8px 40px rgba(249,115,22,0.6) !important;
    transition: all 0.3s !important; font-family: 'Poppins', sans-serif;
}
.gr-button-primary:hover { background: linear-gradient(135deg, #FB923C, #F97316) !important; transform: translateY(-3px) scale(1.05); box-shadow: 0 12px 60px rgba(249,115,22,0.8) !important; }
.gr-tabs .selected { border-bottom: 4px solid #F97316 !important; color: #F97316 !important; font-weight: 800 !important; font-size: 16px !important; font-family: 'Poppins', sans-serif; }
.gr-tabs .unselected { color: #A78BFA !important; font-size: 16px !important; font-family: 'Montserrat', sans-serif; }
.gr-markdown h3 { color: #F97316 !important; font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 800; }
</style>
"""

def render_cards(resultados):
    html = [CSS_BEGINS,'<div class="ac-wrap">']
    if not resultados:
        html.append('<div style="text-align:center;padding:80px 20px;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;color:#ffffff;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;"><h3 style="font-family:Poppins,sans-serif;font-size:32px;color:#FDE047;margin-bottom:20px">😕 Nenhum canal encontrado</h3><p style="font-size:18px;color:#C4B5FD">Tente outra palavra ou faixa de inscritos.</p></div>')
    else:
        est = sum(1 for r in resultados if r["status"]=="ESTOURANDO")
        gm = sum(r["ganho_video"] for r in resultados)/len(resultados)
        html.append(f'''<div class="stats-container">
            <div class="stat-card"><strong>{len(resultados)}</strong><span>Canais</span></div>
            <div class="stat-card"><strong>{est} 🚀</strong><span>Estourando</span></div>
            <div class="stat-card"><strong>{brl(gm)}</strong><span>Ganho médio/vídeo</span></div>
        </div>''')
        for r in resultados:
            bc = "rocket" if r["status"]=="ESTOURANDO" else ("up" if r["status"]=="Saudável" else "sleep")
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['emoji']} {r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{r['status']}</span></div>
<div class="ac-card-body">
<div class="ac-stat-mini"><div class="lbl">👥 Inscritos</div><div class="val">{fmt(r['inscritos'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">📈 Views/vídeo</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">🔥 Taxa viral</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">📊 Mediana</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div class="label">GANHO POR VÍDEO</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right"><div class="label">TOTAL DO CANAL</div><strong>{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>''')
            if r['bombas']:
                html.append('<div class="ac-bombas"><h4>🧬 Modelos para copiar</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:70]}{"..." if len(b["titulo"])>70 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">🔗 ABRIR CANAL NO YOUTUBE →</a></div></div>')
    html.append('</div>')
    return "".join(html)

def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>⚠️ Digite o que você quer caçar!</div>", None
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>❌ Nada encontrado. Tente outra palavra.</div>", None
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
        a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
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
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>⚠️ Cole o link do canal!</div>"
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>❌ Canal não encontrado. Verifique o link.</div>"
    tx = a["taxa"] or 0
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a])

# ═══════════════ INTERFACE ═══════════════
begins_theme = gr.themes.Base(
    primary_hue="orange", secondary_hue="purple", neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins · Assistente do Criador", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">🐘 BEGINS</span>Assistente doCriador</h1>
        <div class="creator">Murilo Silva · Criador de Conteúdo</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">✨ Versão 8.0 · Com IA Generativa</span>
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
                qtd = gr.Slider(3,20,value=8,step=1,label="📊 Quantos canais")
                vids_caca = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos por canal")
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label="👥 Inscritos mín.")
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label="👥 Inscritos máx.")
            estrangeiro = gr.Checkbox(True, label="🌍 Público estrangeiro (paga 3x mais)")
            btn = gr.Button("🚀 INICIAR CAÇADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label="📥 Baixar Relatório Begins (CSV)")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv])

        with gr.Tab("🔎 Analisar Canal"):
            gr.Markdown("### 🔗 Cole o link de um canal para uma auditoria completa")
            url_analise = gr.Textbox(label="📎 Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="💰 Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="🌍 Canal em inglês/espanhol?")
            btn2 = gr.Button("📊 AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=out2)

        with gr.Tab("🧠 Gerador de Títulos IA"):
            gr.Markdown("### ✍️ Cole o TÍTULO de um vídeo que estourou e receba 10 ideias no mesmo estilo")
            gr.Markdown("A IA analisa o padrão do texto e gera variações otimizadas (sem erros de bloqueio do YouTube).")
            titulo_video_ia = gr.Textbox(label="📝 Título do vídeo viral", placeholder="Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000")
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho do Canal")
            btn_ia = gr.Button("✨ GERAR 10 TÍTULOS COM IA", variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=gerar_titulos_ia, inputs=[titulo_video_ia, nicho_ia], outputs=out_ia)

        with gr.Tab("📝 Gerador de Títulos"):
            gr.Markdown("### 📝 Crie títulos baseados em fórmulas virais comprovadas")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="🎯 Palavra-chave ou Tema do Vídeo", placeholder="Ex: navio fantasma, loteria não reclamada, mansão abandonada")
            btn_gen = gr.Button("📝 GERAR 7 TÍTULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos_simples, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab("💡 Guia"):
            gr.Markdown("""
            ### 📖 Como usar o Begins · Assistente do Criador
            
            **1. 🕵️ Caçador de Canais:** Digite o tema, escolha o nicho e clique em INICIAR CAÇADA. Foque nos canais marcados com 🚀 ESTOURANDO.
            **2. 🔎 Analisador:** Já tem um concorrente? Cole o link e veja a média real de views (esqueça o número total de inscritos, olhe a mediana!).
            **3. 🧠 Gerador de Títulos IA:** Cole o TÍTULO de um vídeo viral e receba 10 ideias de títulos no mesmo estilo.
            **4. 📝 Gerador de Títulos:** Use fórmulas comprovadas para criar títulos baseados em palavras-chave.
            
            **💎 Dicas de Ouro de Murilo Silva:**
            - Busque em inglês (`true crime`, `abandoned places`) para achar canais que pagam 3x mais (RPM alto).
            - Taxa viral acima de **1.0x** significa que o YouTube está entregando o vídeo para não-inscritos. É ouro puro.
            - Modele a estrutura (gancho, ritmo, edição) dos vídeos na seção "Modelos para copiar", mas **nunca copie o roteiro palavra por palavra**.
            """)

    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">🐘 BEGINS</div>
        <strong>O ponto de partida para o seu novo negócio.</strong><br><br>
        Desenvolvido por <strong>Murilo Silva</strong> · Criador de Conteúdo<br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
