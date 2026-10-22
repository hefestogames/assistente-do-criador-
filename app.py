import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os
import gradio as gr
warnings.filterwarnings("ignore")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

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
    "🎙️ Cortes de Podcast":8, "🧘 Meditação":6, "₿ Finanças Cripto":45,
    "📱 Shorts/TikTok":5, "🎯 Marketing Digital":40, "️ Fitness":18,
    " Receitas":14, "🐶 Pets":16, "✈️ Viagens":28,
    "👻 Sobrenatural":22, "📚 Autoajuda":16, "🎭 Fofoca/Celebridades":10,
}

# ═══════════════ IA REAL (GEMINI) COM FALLBACK ═══════════════
def chamar_ia(prompt, api_key):
    """Chama o Google Gemini tentando múltiplos modelos"""
    if not api_key or not api_key.strip():
        return None
    try:
        genai.configure(api_key=api_key.strip())
        # Tenta modelos em ordem (do mais novo para o mais antigo)
        modelos = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]
        for modelo in modelos:
            try:
                model = genai.GenerativeModel(modelo)
                response = model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.8, "max_output_tokens": 2048}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                continue
        return None
    except Exception as e:
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

# ═══════════════ GERADORES COM IA REAL ═══════════════
def gerar_titulos_ia(titulo_video, nicho, api_key):
    if not titulo_video or not titulo_video.strip():
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:20px;font-family:Poppins,sans-serif'>️ Digite o título de um vídeo viral!</div>"
    
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
    
    resultado = chamar_ia(prompt, api_key)
    
    if resultado:
        titulos = [linha.strip() for linha in resultado.split('\n') if linha.strip() and re.match(r'^\d+[\.\)]', linha.strip())]
        if not titulos:
            titulos = [linha.strip() for linha in resultado.split('\n') if linha.strip() and len(linha.strip()) > 20][:10]
    else:
        titulos = gerar_titulos_fallback(titulo_video)
    
    html = f'''<div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 30px; border-radius: 20px; border: 3px solid #f97316; margin-top: 20px; box-shadow: 0 8px 40px rgba(249,115,22,0.4);">
        <h3 style="color: #fde047 !important; font-size: 24px !important; font-weight: 900; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; font-family: Poppins, sans-serif;">📊 Título Original Analisado</h3>
        <p style="color: #ffffff; font-size: 18px; font-weight: 600; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; border-left: 4px solid #f97316;">{titulo_video}</p>
        <h3 style="color: #f97316 !important; font-size: 24px !important; font-weight: 800; margin-top: 30px; text-transform: uppercase; letter-spacing: 2px; font-family: Poppins, sans-serif;">🎯 10 TÍTULOS GERADOS PELA IA:</h3>'''
    
    for i, titulo in enumerate(titulos[:10], 1):
        titulo_limpo = re.sub(r'^\d+[\.\)]\s*', '', titulo)
        html += f'''<div style="background: linear-gradient(135deg, #0f0f1e, #1e1b4b); padding: 18px 25px; border-radius: 12px; margin-bottom: 12px; border-left: 6px solid #f97316; color: #ffffff !important; font-size: 16px !important; font-weight: 600; box-shadow: 0 4px 20px rgba(124,58,237,0.3);">
            <span style="color: #fde047; font-weight: 800; margin-right: 10px;">{i}.</span> {titulo_limpo}
        </div>'''
    
    html += '''<p style="color: #c4b5fd; font-size: 16px; margin-top: 25px; padding-top: 20px; border-top: 3px solid #6d28d9; text-align: center;">
        <strong style="color: #fde047; font-size: 18px;">💎 Dica:</strong> Escolha o título que melhor se adapta ao seu público e combine com uma thumbnail impactante!
    </p></div>'''
    return html

def gerar_titulos_fallback(titulo):
    """Fallback caso a IA não esteja disponível"""
    numeros = re.findall(r'\d+', titulo)
    titulos = []
    if numeros:
        num = int(numeros[0])
        for n in [num//2, num*2, num*10, 100, 1000]:
            titulos.append(re.sub(r'\d+', str(n), titulo, count=1))
    titulos.extend([
        f"🚨 URGENTE: {titulo}",
        f"⚠️ ATENÇÃO: {titulo}",
        f"💥 IMPRESSIONANTE: {titulo}",
        f"🔥 O SEGREDO: {titulo}",
        f"😱 INACREDITÁVEL: {titulo}",
    ])
    return list(dict.fromkeys(titulos))[:10]

def gerar_roteiro(tema, canais_info, api_key):
    if not tema or not tema.strip():
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:20px;font-family:Poppins,sans-serif'>⚠️ Digite o tema do seu vídeo!</div>"
    
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
2. 🎬 INTRODUÇÃO (30s-1min): Contexto e promessa do vídeo
3. 📖 DESENVOLVIMENTO (1-9min): 5-7 blocos de conteúdo com transições
4. 💥 CLÍMAX (9-11min): Momento mais impactante
5. 📣 CTA FINAL (11-12min): Chamada para ação (like, inscrição, próximo vídeo)

Para cada bloco do desenvolvimento, inclua:
- O que falar (texto sugerido)
- Sugestão de imagem/cena
- Duração estimada

Responda de forma organizada, clara e pronta para usar. Use linguagem envolvente e direta."""
    
    resultado = chamar_ia(prompt, api_key)
    
    if resultado:
        html = f'''<div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 30px; border-radius: 20px; border: 3px solid #10b981; margin-top: 20px; box-shadow: 0 8px 40px rgba(16,185,129,0.4);">
            <h3 style="color: #10b981 !important; font-size: 26px !important; font-weight: 900; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; font-family: Poppins, sans-serif;">📝 ROTEIRO COMPLETO</h3>
            <p style="color: #ffffff; font-size: 16px; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; border-left: 4px solid #10b981; margin-bottom: 20px;"><strong>Tema:</strong> {tema}</p>
            <div style="color: #ffffff; font-size: 15px; line-height: 1.7; white-space: pre-wrap; font-family: Inter, sans-serif;">{resultado}</div>
            <p style="color: #a7f3d0; font-size: 14px; margin-top: 25px; padding-top: 15px; border-top: 2px solid #10b981; text-align: center;">
                <strong>💡 Dica:</strong> Use este roteiro como base e adapte com sua personalidade!
            </p>
        </div>'''
        return html
    else:
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:18px'>❌ Erro ao gerar roteiro. Verifique sua chave API ou tente novamente.</div>"

def gerar_thumbnails(tema, canais_info, api_key):
    if not tema or not tema.strip():
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:20px;font-family:Poppins,sans-serif'>⚠️ Digite o tema do seu vídeo!</div>"
    
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
3. 📝 TEXTO NA THUMB: Texto curto (máx 4 palavras) em destaque
4. 🎨 CORES: Paleta de cores sugerida
5. ⚡ ELEMENTO CHAVE: O que chama atenção (seta, círculo, contraste)
6. 🎯 GATILHO PSICOLÓGICO: Por que essa thumb funciona

Responda de forma organizada, numerada de 1 a 5."""
    
    resultado = chamar_ia(prompt, api_key)
    
    if resultado:
        html = f'''<div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 30px; border-radius: 20px; border: 3px solid #ec4899; margin-top: 20px; box-shadow: 0 8px 40px rgba(236,72,153,0.4);">
            <h3 style="color: #ec4899 !important; font-size: 26px !important; font-weight: 900; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; font-family: Poppins, sans-serif;"> 5 IDEIAS DE THUMBNAILS</h3>
            <p style="color: #ffffff; font-size: 16px; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; border-left: 4px solid #ec4899; margin-bottom: 20px;"><strong>Tema:</strong> {tema}</p>
            <div style="color: #ffffff; font-size: 15px; line-height: 1.7; white-space: pre-wrap; font-family: Inter, sans-serif;">{resultado}</div>
            <p style="color: #fbcfe8; font-size: 14px; margin-top: 25px; padding-top: 15px; border-top: 2px solid #ec4899; text-align: center;">
                <strong> Dica:</strong> Use o Canva (grátis) para criar as thumbnails com essas especificações!
            </p>
        </div>'''
        return html
    else:
        return "<div style='padding:40px;text-align:center;color:#F97316;font-size:18px'>❌ Erro ao gerar thumbnails. Verifique sua chave API ou tente novamente.</div>"

# ═══════════════ CSS MODERNO ═══════════════
CSS_BEGINS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@400;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
body, .gradio-container, .main, .wrap, .gradio-app { 
    background: linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 50%, #16213E 100%) !important; 
    color: #ffffff !important;
}

.api-key-banner {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border: 2px solid #f97316;
    border-radius: 15px;
    padding: 20px;
    margin: 20px auto;
    max-width: 1200px;
    box-shadow: 0 4px 20px rgba(249,115,22,0.3);
}
.api-key-banner h3 {
    color: #fde047 !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin: 0 0 10px 0;
}
.api-key-banner p {
    color: #c4b5fd !important;
    font-size: 14px !important;
    margin: 0 0 15px 0;
}
.api-key-banner a {
    color: #f97316 !important;
    font-weight: 700 !important;
    text-decoration: underline !important;
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
<div class="ac-stat-mini"><div class="lbl"> Views/vídeo</div><div class="val">{fmt(r['media_rec'])}</div></div>
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
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>️ Digite o que você quer caçar!</div>", None, []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>❌ Nada encontrado. Tente outra palavra.</div>", None, []
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
    return render_cards(resultados), csv_path, resultados

def analisar_canal_ui(url_canal, nicho_label, vids, estrangeiro):
    if not url_canal or not url_canal.strip():
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>⚠️ Cole o link do canal!</div>", []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return "<div style='padding:60px;text-align:center;color:#F97316;font-size:24px;font-weight:700;background:linear-gradient(135deg,#1E1B4B,#312E81);border-radius:20px;border:3px solid #F97316;box-shadow:0 10px 50px rgba(249,115,22,0.5);margin:40px auto;max-width:800px;font-family:Poppins,sans-serif'>❌ Canal não encontrado. Verifique o link.</div>", []
    tx = a["taxa"] or 0
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a]), [a]

# ══════════════ INTERFACE ═══════════════
begins_theme = gr.themes.Base(
    primary_hue="orange", secondary_hue="purple", neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins · Assistente do Criador", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">🐘 BEGINS</span>Assistente do Criador</h1>
        <div class="creator">Murilo Silva · Criador de Conteúdo</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">✨ Versão 9.1 · Com IA Real Gemini</span>
    </div>
    """)
    
    gr.HTML("""
    <div class="api-key-banner">
        <h3>🔑 CHAVE API DO GOOGLE GEMINI (GRÁTIS)</h3>
        <p>Obtenha sua chave gratuita em: <a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com/app/apikey</a> — Necessária para usar a IA real nos geradores.</p>
    </div>
    """)
    
    api_key_input = gr.Textbox(
        label="🔑 Cole sua chave API do Gemini aqui (começa com AIza... ou AQ...)",
        placeholder="AIzaSy... ou AQ.Ab8...",
        type="password"
    )
    
    canais_state = gr.State([])
    
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
            btn = gr.Button(" INICIAR CAÇADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label=" Baixar Relatório Begins (CSV)")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv,canais_state])

        with gr.Tab(" Analisar Canal"):
            gr.Markdown("### 🔗 Cole o link de um canal para uma auditoria completa")
            url_analise = gr.Textbox(label="📎 Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="🎬 Curiosidades", label="💰 Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="🎬 Vídeos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="🌍 Canal em inglês/espanhol?")
            btn2 = gr.Button("📊 AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=[out2,canais_state])

        with gr.Tab("🧠 Gerador de Títulos IA"):
            gr.Markdown("### ✍️ Cole o TÍTULO de um vídeo viral e receba 10 ideias criativas")
            gr.Markdown("A IA REAL (Gemini) analisa o padrão e gera títulos únicos e criativos.")
            titulo_video_ia = gr.Textbox(label="📝 Título do vídeo viral", placeholder="Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000")
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho do Canal")
            btn_ia = gr.Button("✨ GERAR 10 TÍTULOS COM IA", variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=lambda t, n, k: gerar_titulos_ia(t, n, k), inputs=[titulo_video_ia, nicho_ia, api_key_input], outputs=out_ia)

        with gr.Tab("📝 Gerador de Títulos Simples"):
            gr.Markdown("### 📝 Crie títulos baseados em fórmulas virais comprovadas")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="💰 Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="🎯 Palavra-chave ou Tema do Vídeo", placeholder="Ex: navio fantasma, loteria não reclamada, mansão abandonada")
            btn_gen = gr.Button("📝 GERAR 7 TÍTULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=lambda n, k: gerar_titulos_ia(k, n, ""), inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab("📜 Gerador de Roteiro"):
            gr.Markdown("###  Gere um roteiro completo baseado no seu tema e canais de referência")
            gr.Markdown("A IA cria um roteiro estruturado com gancho, desenvolvimento e CTA.")
            tema_roteiro = gr.Textbox(label="🎯 Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_roteiro = gr.Button("📜 GERAR ROTEIRO COMPLETO", variant="primary", size="lg")
            out_roteiro = gr.HTML()
            btn_roteiro.click(fn=lambda t, k, canais: gerar_roteiro(t, canais, k), inputs=[tema_roteiro, api_key_input, canais_state], outputs=out_roteiro)

        with gr.Tab("🎨 Gerador de Thumbnails"):
            gr.Markdown("### 🎨 Crie ideias de thumbnails virais para seu vídeo")
            gr.Markdown("A IA sugere 5 thumbnails detalhadas com descrição visual, cores e gatilhos psicológicos.")
            tema_thumb = gr.Textbox(label=" Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_thumb = gr.Button(" GERAR 5 THUMBNAILS", variant="primary", size="lg")
            out_thumb = gr.HTML()
            btn_thumb.click(fn=lambda t, k, canais: gerar_thumbnails(t, canais, k), inputs=[tema_thumb, api_key_input, canais_state], outputs=out_thumb)

        with gr.Tab(" Guia"):
            gr.Markdown("""
            ### 📖 Como usar o Begins · Assistente do Criador
            
            **1. 🔑 Primeiro passo:** Obtenha sua chave API gratuita do Gemini em [aistudio.google.com](https://aistudio.google.com/app/apikey) e cole no campo no topo.
            
            **2. ️ Caçador de Canais:** Digite o tema, escolha o nicho e clique em INICIAR CAÇADA. Foque nos canais marcados com 🚀 ESTOURANDO.
            
            **3. 🔎 Analisador:** Já tem um concorrente? Cole o link e veja a média real de views.
            
            **4. 🧠 Gerador de Títulos IA:** Cole o TÍTULO de um vídeo viral e receba 10 ideias criativas da IA real.
            
            **5. 📜 Gerador de Roteiro:** Após caçar canais, use esta aba para gerar um roteiro completo baseado no seu tema.
            
            **6. 🎨 Gerador de Thumbnails:** Crie 5 ideias detalhadas de thumbnails virais.
            
            **💎 Dicas de Ouro de Murilo Silva:**
            - Busque em inglês (`true crime`, `abandoned places`) para achar canais que pagam 3x mais.
            - Taxa viral acima de **1.0x** significa que o YouTube está entregando o vídeo para não-inscritos.
            - Modele a estrutura dos vídeos, mas **nunca copie o roteiro palavra por palavra**.
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
