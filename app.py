import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os, requests
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
    " Curiosidades":12, "🔪 Histórias/Crimes":18, "📽️ Documentário":20,
    " Resumo de Filmes":15, " Religião":10, "💪 Motivacional":9,
    "🎵 Música/Relax":4, "🎮 Games":8, "⚽ Esportes":14,
    "🚗 Carros":26, "🤖 Tecnologia/IA":35, " Saúde":22, "💰 Finanças":55,
    "🎙️ Cortes de Podcast":8, "🧘 Meditação":6, "₿ Finanças Cripto":45,
    "📱 Shorts/TikTok":5, "🎯 Marketing Digital":40, "🏋️ Fitness":18,
    "🍳 Receitas":14, " Pets":16, "✈️ Viagens":28,
    "👻 Sobrenatural":22, "📚 Autoajuda":16, "🎭 Fofoca/Celebridades":10,
}

# ═══════════════ IA OPEN SOURCE: POLLINATIONS.AI ═══════════════
# 100% grátis, sem login, sem API key, código aberto
# Docs: https://github.com/pollinations/pollinations
def chamar_ia(prompt, modelo="openai"):
    """Chama Pollinations.ai - IA gratuita sem chave"""
    try:
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        params = {"model": modelo, "json": "false"}
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
    except:
        pass
    
    # Fallback: POST method (mais robusto)
    try:
        response = requests.post(
            "https://text.pollinations.ai/openai",
            json={
                "model": modelo,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except:
        pass
    
    return None

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
                            key=lambda x:x["views"],reverse=True)[:5]}

# ═══════════════ GERADORES COM IA ═══════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return "<div class='msg-erro'>⚠️ Digite o título de um vídeo viral!</div>"
    
    prompt = f"""Você é um especialista em títulos virais para YouTube no nicho de {nicho}.
    
Título original viral: "{titulo_video}"

Analise o padrão psicológico deste título (gatilhos mentais, curiosidade, urgência, números, emoção) e gere EXATAMENTE 10 títulos NOVAS e CRIATIVAS seguindo o mesmo estilo, mas com variações inteligentes.

Regras:
- Cada título deve ser único e criativo
- Use gatilhos mentais diferentes em cada um
- Varie entre: curiosidade, urgência, números, emoção, desafio, segredo
- Mantenha o mesmo estilo e tom do original
- Responda APENAS com a lista numerada, uma por linha, sem explicações extras
- Formato: 1. Título aqui"""
    
    resultado = chamar_ia(prompt)
    
    if resultado:
        titulos = [linha.strip() for linha in resultado.split('\n') if linha.strip() and re.match(r'^\d+[\.\)]', linha.strip())]
        if not titulos:
            titulos = [linha.strip() for linha in resultado.split('\n') if linha.strip() and len(linha.strip()) > 20][:10]
    else:
        titulos = gerar_titulos_fallback(titulo_video)
    
    html = f'''<div class="box-resultado box-titulos">
        <div class="box-header">
            <span class="box-icon">📊</span>
            <h3>TÍTULO ORIGINAL ANALISADO</h3>
        </div>
        <div class="box-conteudo">{titulo_video}</div>
        <div class="box-header" style="margin-top: 25px;">
            <span class="box-icon">🎯</span>
            <h3>10 TÍTULOS GERADOS PELA IA</h3>
        </div>'''
    
    for i, titulo in enumerate(titulos[:10], 1):
        titulo_limpo = re.sub(r'^\d+[\.\)]\s*', '', titulo)
        html += f'''<div class="titulo-item">
            <span class="titulo-num">{i}.</span>
            <span class="titulo-texto">{titulo_limpo}</span>
        </div>'''
    
    html += '''<div class="box-dica">
        <strong>💎 Dica:</strong> Escolha o título que melhor se adapta ao seu público e combine com uma thumbnail impactante!
    </div></div>'''
    return html

def gerar_titulos_fallback(titulo):
    numeros = re.findall(r'\d+', titulo)
    titulos = []
    if numeros:
        num = int(numeros[0])
        for n in [num//2, num*2, num*10, 100, 1000]:
            titulos.append(re.sub(r'\d+', str(n), titulo, count=1))
    titulos.extend([
        f"🚨 URGENTE: {titulo}",
        f"️ ATENÇÃO: {titulo}",
        f"💥 IMPRESSIONANTE: {titulo}",
        f"🔥 O SEGREDO: {titulo}",
        f"😱 INACREDITÁVEL: {titulo}",
    ])
    return list(dict.fromkeys(titulos))[:10]

def gerar_roteiro(tema, canais_info):
    if not tema or not tema.strip():
        return "<div class='msg-erro'>⚠️ Digite o tema do seu vídeo!</div>"
    
    canais_str = ""
    if canais_info and len(canais_info) > 0:
        canais_str = "\nCanais de referência analisados:\n"
        for c in canais_info[:5]:
            canais_str += f"- {c.get('nome','Canal')}: {fmt(c.get('media_rec',0))} views/vídeo\n"
            for b in c.get('bombas', [])[:2]:
                canais_str += f"  • Vídeo viral: {b.get('titulo','')} ({fmt(b.get('views',0))} views)\n"
    
    prompt = f"""Você é um roteirista especialista em canais Dark do YouTube no nicho de {tema}.
{canais_str}
Crie um ROTEIRO COMPLETO e ESTRUTURADO para um vídeo de 8-12 minutos sobre: "{tema}"

Estrutura obrigatória:
1.  GANCHO (0-30s): Frase impactante que prende a atenção
2.  INTRODUÇÃO (30s-1min): Contexto e promessa do vídeo
3.  DESENVOLVIMENTO (1-9min): 5-7 blocos de conteúdo com transições
4. 💥 CLÍMAX (9-11min): Momento mais impactante
5.  CTA FINAL (11-12min): Chamada para ação (like, inscrição, próximo vídeo)

Para cada bloco do desenvolvimento, inclua:
- O que falar (texto sugerido)
- Sugestão de imagem/cena
- Duração estimada

Responda de forma organizada, clara e pronta para usar. Use linguagem envolvente e direta."""
    
    resultado = chamar_ia(prompt)
    
    if resultado:
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header">
                <span class="box-icon">📝</span>
                <h3>ROTEIRO COMPLETO</h3>
            </div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica">
                <strong>💡 Dica:</strong> Use este roteiro como base e adapte com sua personalidade!
            </div>
        </div>'''
        return html
    else:
        return "<div class='msg-erro'>❌ Erro ao gerar roteiro. Tente novamente.</div>"

def gerar_thumbnails(tema, canais_info):
    if not tema or not tema.strip():
        return "<div class='msg-erro'>⚠️ Digite o tema do seu vídeo!</div>"
    
    canais_str = ""
    if canais_info and len(canais_info) > 0:
        canais_str = "\nEstilo dos canais de referência:\n"
        for c in canais_info[:3]:
            canais_str += f"- {c.get('nome','Canal')}: taxa viral {c.get('taxa',0):.2f}x\n"
    
    prompt = f"""Você é um especialista em thumbnails virais para YouTube.
Tema do vídeo: "{tema}"
{canais_str}
Crie 5 IDEIAS DETALHADAS de thumbnails que gerem alta taxa de clique (CTR).

Para cada ideia, inclua:
1. 🖼️ DESCRIÇÃO VISUAL: O que aparece na imagem (pessoas, objetos, cenário)
2. 😱 EXPRESSÃO: Emoção do rosto (se houver pessoa)
3.  TEXTO NA THUMB: Texto curto (máx 4 palavras) em destaque
4.  CORES: Paleta de cores sugerida
5. ⚡ ELEMENTO CHAVE: O que chama atenção (seta, círculo, contraste)
6. 🎯 GATILHO PSICOLÓGICO: Por que essa thumb funciona

Responda de forma organizada, numerada de 1 a 5."""
    
    resultado = chamar_ia(prompt)
    
    if resultado:
        html = f'''<div class="box-resultado box-thumbnails">
            <div class="box-header">
                <span class="box-icon">🎨</span>
                <h3>5 IDEIAS DE THUMBNAILS</h3>
            </div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica">
                <strong>💡 Dica:</strong> Use o Canva (grátis) para criar as thumbnails com essas especificações!
            </div>
        </div>'''
        return html
    else:
        return "<div class='msg-erro'>❌ Erro ao gerar thumbnails. Tente novamente.</div>"

# ═══════════════ CSS - PALETA YOUTUBE ═══════════════
CSS_YOUTUBE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
body, .gradio-container, .main, .wrap, .gradio-app { 
    background: #0F0F0F !important; color: #F1F1F1 !important;
}

.ac-header {
    background: #0F0F0F; border-bottom: 3px solid #FF0000;
    padding: 50px 40px; text-align: center; margin-bottom: 40px;
    max-width: 1200px; margin-left: auto; margin-right: auto;
}
.ac-header h1 {
    font-family: 'Poppins', sans-serif !important; font-size: 56px !important;
    font-weight: 900 !important; color: #FFFFFF !important; margin: 0; letter-spacing: -1px;
}
.ac-header h1 .begins { color: #FF0000 !important; }
.ac-header .creator { font-size: 16px; color: #AAAAAA; margin-top: 15px; font-weight: 500; }
.ac-header .subtitle { font-size: 18px; color: #F1F1F1; margin-top: 10px; font-weight: 400; }
.ac-header .badge {
    display: inline-block; background: #FF0000; color: #FFFFFF;
    padding: 8px 20px; border-radius: 20px; font-size: 13px;
    font-weight: 700; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px;
}

.api-key-banner {
    background: #282828; border: 1px solid #3F3F3F; border-radius: 12px;
    padding: 25px 30px; margin: 30px auto; max-width: 1200px;
}
.api-key-banner h3 {
    color: #FF0000 !important; font-family: 'Poppins', sans-serif !important;
    font-size: 18px !important; font-weight: 700 !important; margin: 0 0 10px 0;
}
.api-key-banner p { color: #AAAAAA !important; font-size: 14px !important; margin: 0; }
.api-key-banner a { color: #3EA6FF !important; text-decoration: none !important; font-weight: 600 !important; }

.stats-container { display: flex; gap: 20px; margin: 40px auto; justify-content: center; max-width: 1200px; }
.stat-card {
    flex: 1; max-width: 320px; background: #282828; padding: 30px;
    border-radius: 12px; text-align: center; border: 1px solid #3F3F3F;
}
.stat-card strong {
    display: block; font-family: 'Poppins', sans-serif !important;
    font-size: 48px !important; color: #FF0000 !important; font-weight: 900; margin-bottom: 10px;
}
.stat-card span { color: #AAAAAA; font-size: 13px !important; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

.ac-card {
    background: #282828; border-radius: 12px; margin: 25px auto;
    overflow: hidden; border: 1px solid #3F3F3F; max-width: 1200px; transition: all 0.3s;
}
.ac-card:hover { border-color: #FF0000; box-shadow: 0 4px 20px rgba(255,0,0,0.2); }
.ac-card-head {
    padding: 25px 30px; display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #3F3F3F; background: #1F1F1F;
}
.ac-card-head h3 {
    margin: 0; font-family: 'Poppins', sans-serif !important;
    font-size: 22px !important; color: #FFFFFF !important; font-weight: 700;
}
.ac-badge { padding: 8px 18px; border-radius: 20px; font-size: 12px !important; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.ac-badge-rocket { background: #FF0000; color: #FFFFFF !important; }
.ac-badge-up { background: #FFD700; color: #0F0F0F !important; }
.ac-badge-sleep { background: #606060; color: #FFFFFF !important; }

.ac-card-body { padding: 25px 30px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.ac-stat-mini { background: #1F1F1F; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #3F3F3F; }
.ac-stat-mini .lbl { font-size: 11px !important; color: #AAAAAA !important; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px; }
.ac-stat-mini .val { font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 700; color: #FFFFFF !important; }

.ac-money { background: #FF0000; padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; }
.ac-money strong { font-family: 'Poppins', sans-serif !important; font-size: 32px !important; color: #FFFFFF !important; font-weight: 900; }
.ac-money .label { font-size: 11px !important; color: #FFFFFF !important; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; }

.ac-bombas { padding: 25px 30px; background: #1F1F1F; border-top: 1px solid #3F3F3F; }
.ac-bombas h4 { margin: 0 0 15px; color: #FF0000 !important; font-size: 14px !important; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.ac-bomba { padding: 12px 15px; font-size: 14px !important; border-bottom: 1px solid #3F3F3F; color: #F1F1F1 !important; background: #282828; border-radius: 6px; margin-bottom: 8px; }
.ac-bomba:last-child { border-bottom: none; }
.ac-bomba a { color: #3EA6FF !important; text-decoration: none !important; font-weight: 600; }
.ac-bomba a:hover { text-decoration: underline !important; }
.ac-bomba .v { color: #FF0000 !important; font-weight: 700; margin-right: 12px; font-size: 16px !important; }

.ac-foot { padding: 20px; text-align: center; background: #1F1F1F; border-top: 1px solid #3F3F3F; }
.ac-foot a {
    color: #FF0000 !important; text-decoration: none !important; font-weight: 700;
    font-size: 14px !important; letter-spacing: 1px; text-transform: uppercase;
    display: inline-block; padding: 12px 30px; border: 2px solid #FF0000;
    border-radius: 20px; transition: all 0.3s;
}
.ac-foot a:hover { background: #FF0000; color: #FFFFFF !important; }

.box-resultado { background: #282828; border-radius: 12px; padding: 30px; margin: 30px auto; max-width: 1200px; border: 1px solid #3F3F3F; }
.box-titulos { border-left: 4px solid #FF0000; }
.box-roteiro { border-left: 4px solid #3EA6FF; }
.box-thumbnails { border-left: 4px solid #FF0000; }
.box-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.box-header h3 { color: #FFFFFF !important; font-family: 'Poppins', sans-serif !important; font-size: 20px !important; font-weight: 700 !important; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
.box-icon { font-size: 28px; }
.box-conteudo { background: #1F1F1F; padding: 20px; border-radius: 8px; color: #F1F1F1; font-size: 16px; font-weight: 500; border: 1px solid #3F3F3F; }
.box-tema { background: #1F1F1F; padding: 15px 20px; border-radius: 8px; color: #AAAAAA; font-size: 14px; margin-bottom: 20px; border: 1px solid #3F3F3F; }
.box-conteudo-texto { color: #F1F1F1; font-size: 15px; line-height: 1.8; white-space: pre-wrap; padding: 20px; background: #1F1F1F; border-radius: 8px; border: 1px solid #3F3F3F; }
.box-dica { margin-top: 25px; padding: 15px 20px; background: #1F1F1F; border-radius: 8px; color: #AAAAAA; font-size: 14px; border-left: 3px solid #FFD700; }
.box-dica strong { color: #FFD700; }
.titulo-item { background: #1F1F1F; padding: 18px 20px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #FF0000; display: flex; align-items: flex-start; gap: 15px; }
.titulo-num { color: #FF0000; font-weight: 700; font-size: 16px; min-width: 25px; }
.titulo-texto { color: #F1F1F1; font-size: 15px; font-weight: 500; line-height: 1.5; }
.msg-erro { padding: 40px; text-align: center; color: #FF0000; font-size: 18px; font-weight: 600; background: #282828; border-radius: 12px; border: 1px solid #FF0000; margin: 30px auto; max-width: 800px; }

.footer-creator { text-align: center; padding: 50px 30px; color: #AAAAAA !important; font-size: 14px !important; border-top: 1px solid #3F3F3F; margin-top: 60px; background: #0F0F0F; }
.footer-creator strong { color: #FFFFFF !important; font-weight: 700; font-size: 16px !important; }
.footer-creator .begins-mark { display: inline-block; color: #FF0000 !important; font-weight: 900; font-size: 36px !important; letter-spacing: 2px; margin-bottom: 15px; text-transform: uppercase; font-family: 'Poppins', sans-serif; }

.gr-box, .gr-input, .gr-dropdown, .gr-slider, .gr-textbox { background: #282828 !important; border: 1px solid #3F3F3F !important; color: #F1F1F1 !important; border-radius: 8px !important; }
.gr-input, .gr-textbox input { color: #F1F1F1 !important; font-size: 15px !important; font-weight: 500; background: #1F1F1F !important; }
.gr-dropdown .wrap { background: #282828 !important; border: 1px solid #3F3F3F !important; }
.gr-dropdown .wrap span { color: #F1F1F1 !important; font-size: 14px !important; font-weight: 500; }
.gr-button-primary {
    background: #FF0000 !important; border: none !important; color: #FFFFFF !important;
    font-weight: 700 !important; letter-spacing: 1px !important; font-size: 16px !important;
    text-transform: uppercase; padding: 16px 40px !important; border-radius: 20px !important; transition: all 0.3s !important;
}
.gr-button-primary:hover { background: #CC0000 !important; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255,0,0,0.4) !important; }
.gr-tabs .selected { border-bottom: 3px solid #FF0000 !important; color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; }
.gr-tabs .unselected { color: #AAAAAA !important; font-size: 15px !important; }
.gr-markdown h3 { color: #FFFFFF !important; font-family: 'Poppins', sans-serif !important; font-size: 22px !important; font-weight: 700; margin-top: 30px; margin-bottom: 15px; }
.gr-markdown p { color: #AAAAAA !important; font-size: 15px; line-height: 1.6; }
</style>
"""

def render_cards(resultados):
    html = [CSS_YOUTUBE,'<div class="ac-wrap">']
    if not resultados:
        html.append('<div class="msg-erro">😕 Nenhum canal encontrado. Tente outra palavra ou faixa de inscritos.</div>')
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
                html.append('<div class="ac-bombas"><h4> Modelos para copiar</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:70]}{"..." if len(b["titulo"])>70 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">🔗 Abrir canal no YouTube →</a></div></div>')
    html.append('</div>')
    return "".join(html)

def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return "<div class='msg-erro'>⚠️ Digite o que você quer caçar!</div>", None, []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div class='msg-erro'>❌ Nada encontrado. Tente outra palavra.</div>", None, []
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
    return render_cards(resultados), csv_path, resultados

def analisar_canal_ui(url_canal, nicho_label, vids, estrangeiro):
    if not url_canal or not url_canal.strip():
        return "<div class='msg-erro'>⚠️ Cole o link do canal!</div>", []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return "<div class='msg-erro'>❌ Canal não encontrado. Verifique o link.</div>", []
    tx = a["taxa"] or 0
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a]), [a]

# ═══════════════ INTERFACE ═══════════════
begins_theme = gr.themes.Base(
    primary_hue="red", secondary_hue="neutral", neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins · Assistente do Criador", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span> · Assistente do Criador</h1>
        <div class="creator">Murilo Silva · Criador de Conteúdo</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">Versão 11.0 · IA Open Source</span>
    </div>
    """)
    
    gr.HTML("""
    <div class="api-key-banner">
        <h3>🤖 IA Open Source Integrada (Pollinations.ai)</h3>
        <p>100% gratuita, sem login, sem senha, sem API key. Código aberto. Gerando títulos, roteiros e thumbnails automaticamente.</p>
    </div>
    """)
    
    canais_state = gr.State([])
    
    with gr.Tabs():
        with gr.Tab("🕵️ Caçador de Canais"):
            gr.Markdown("### Encontre canais que estão estourando")
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
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv,canais_state])

        with gr.Tab("🔎 Analisar Canal"):
            gr.Markdown("### Cole o link de um canal para auditoria completa")
            url_analise = gr.Textbox(label="Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="Canal em inglês/espanhol?")
            btn2 = gr.Button("AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=[out2,canais_state])

        with gr.Tab("🧠 Gerador de Títulos IA"):
            gr.Markdown("### Cole o TÍTULO de um vídeo viral e receba 10 ideias criativas")
            titulo_video_ia = gr.Textbox(label="Título do vídeo viral", placeholder="Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000")
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="Nicho do Canal")
            btn_ia = gr.Button("GERAR 10 TÍTULOS COM IA", variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=gerar_titulos_ia, inputs=[titulo_video_ia, nicho_ia], outputs=out_ia)

        with gr.Tab("📝 Gerador de Títulos Simples"):
            gr.Markdown("### Crie títulos baseados em fórmulas virais")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value=" Histórias/Crimes", label="Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="Palavra-chave ou Tema", placeholder="Ex: navio fantasma, loteria não reclamada")
            btn_gen = gr.Button("GERAR 7 TÍTULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=lambda n, k: gerar_titulos_ia(k, n), inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab(" Gerador de Roteiro"):
            gr.Markdown("### Gere um roteiro completo baseado no seu tema")
            tema_roteiro = gr.Textbox(label="Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_roteiro = gr.Button("GERAR ROTEIRO COMPLETO", variant="primary", size="lg")
            out_roteiro = gr.HTML()
            btn_roteiro.click(fn=lambda t, canais: gerar_roteiro(t, canais), inputs=[tema_roteiro, canais_state], outputs=out_roteiro)

        with gr.Tab("🎨 Gerador de Thumbnails"):
            gr.Markdown("### Crie ideias de thumbnails virais")
            tema_thumb = gr.Textbox(label="Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_thumb = gr.Button("GERAR 5 THUMBNAILS", variant="primary", size="lg")
            out_thumb = gr.HTML()
            btn_thumb.click(fn=lambda t, canais: gerar_thumbnails(t, canais), inputs=[tema_thumb, canais_state], outputs=out_thumb)

        with gr.Tab("💡 Guia"):
            gr.Markdown("""
            ### Como usar o Begins · Assistente do Criador
            
            **1. 🕵️ Caçador de Canais:** Digite o tema, escolha o nicho e clique em INICIAR CAÇADA. Foque nos canais marcados com 🚀 ESTOURANDO.
            
            **2. 🔎 Analisador:** Já tem um concorrente? Cole o link e veja a média real de views.
            
            **3. 🧠 Gerador de Títulos IA:** Cole o TÍTULO de um vídeo viral e receba 10 ideias criativas da IA.
            
            **4. 📜 Gerador de Roteiro:** Use esta aba para gerar um roteiro completo baseado no seu tema.
            
            **5. 🎨 Gerador de Thumbnails:** Crie 5 ideias detalhadas de thumbnails virais.
            
            **Dicas de Murilo Silva:**
            - Busque em inglês (`true crime`, `abandoned places`) para achar canais que pagam 3x mais.
            - Taxa viral acima de **1.0x** significa que o YouTube está entregando o vídeo para não-inscritos.
            - Modele a estrutura dos vídeos, mas **nunca copie o roteiro palavra por palavra**.
            """)

    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div>
        <strong>O ponto de partida para o seu novo negócio.</strong><br><br>
        Desenvolvido por <strong>Murilo Silva</strong> · Criador de Conteúdo<br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
