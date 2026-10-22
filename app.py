import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os, requests
import gradio as gr
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# 🌍 SISTEMA DE IDIOMA
# ═══════════════════════════════════════════════════════════════
IDIOMA_ATUAL = "pt"

I18N = {
    "pt": {
        "tab_cacador": "Caçador de Canais",
        "tab_analisar": "Analisar Canal",
        "tab_titulos_ia": "Gerador de Títulos IA",
        "tab_titulos_simples": "Gerador de Títulos Simples",
        "tab_guia": "Guia",
        "lbl_palavra": "O que caçar?",
        "lbl_nicho": "Nicho",
        "lbl_qtd": "Quantos canais",
        "lbl_vids": "Vídeos por canal",
        "lbl_insc_min": "Inscritos mín.",
        "lbl_insc_max": "Inscritos máx.",
        "lbl_estrangeiro": "Público estrangeiro (paga 3x mais)",
        "lbl_url": "Link ou @ do canal",
        "lbl_estrangeiro2": "Canal em inglês/espanhol?",
        "lbl_titulo_viral": "Título do vídeo viral",
        "lbl_nicho_ia": "Nicho do Canal",
        "lbl_palavras_chave": "Palavras-chave (separe por vírgula)",
        "ph_cacar": "Ex: histórias de terror, carros abandonados, política...",
        "ph_url": "https://www.youtube.com/@NomeDoCanal",
        "ph_titulo": "Ex: Sobrevivi 100 Dias Em Um Bunker Nuclear",
        "ph_palavras": "Ex: eleições, governo, crise, economia",
        "btn_cacar": "INICIAR CAÇADA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GERAR 10 TÍTULOS COM IA",
        "btn_titulos_simples": "GERAR 7 TÍTULOS",
        "lbl_csv": "Baixar Relatório (CSV)",
        "msg_erro_vazio": "Digite o que você quer caçar!",
        "msg_erro_nada": "Nada encontrado. Tente outra palavra.",
        "msg_erro_url": "Cole o link do canal!",
        "msg_erro_canal": "Canal não encontrado. Verifique o link.",
        "msg_erro_titulo": "Digite o título de um vídeo viral!",
        "msg_erro_palavras": "Digite palavras-chave válidas separadas por vírgula!",
        "msg_erro_ia": "Erro ao gerar conteúdo. Tente novamente.",
        "titulo_original": "TÍTULO ORIGINAL ANALISADO",
        "titulos_gerados": "TÍTULOS GERADOS PELA IA",
        "palavras_analisadas": "PALAVRAS-CHAVE ANALISADAS",
        "titulos_criados": "TÍTULOS CRIADOS",
        "dica_titulo": "Dica: Escolha o título que melhor se adapta ao seu público!",
        "dica_titulo_simples": "Dica: Combine estes títulos com thumbnails de alto contraste!",
        "modelos_copiar": "Modelos de vídeos para copiar",
        "abrir_youtube": "Abrir canal no YouTube",
        "ganho_video": "GANHO POR VÍDEO",
        "total_canal": "TOTAL DO CANAL",
        "inscritos": "Inscritos",
        "views_video": "Views/vídeo",
        "taxa_viral": "Taxa viral",
        "mediana": "Mediana",
        "estourando": "ESTOURANDO",
        "saudavel": "Saudável",
        "estagnado": "Estagnado",
        "canais": "Canais",
        "estourando_label": "Estourando",
        "ganho_medio": "Ganho médio/vídeo",
        "nenhum_canal": "Nenhum canal encontrado. Tente outra palavra ou faixa de inscritos.",
    },
    "en": {
        "tab_cacador": "Channel Hunter",
        "tab_analisar": "Analyze Channel",
        "tab_titulos_ia": "AI Title Generator",
        "tab_titulos_simples": "Simple Title Generator",
        "tab_guia": "Guide",
        "lbl_palavra": "What to hunt?",
        "lbl_nicho": "Niche",
        "lbl_qtd": "How many channels",
        "lbl_vids": "Videos per channel",
        "lbl_insc_min": "Min subscribers",
        "lbl_insc_max": "Max subscribers",
        "lbl_estrangeiro": "Foreign audience (pays 3x more)",
        "lbl_url": "Channel link or @",
        "lbl_estrangeiro2": "Channel in English/Spanish?",
        "lbl_titulo_viral": "Viral video title",
        "lbl_nicho_ia": "Channel Niche",
        "lbl_palavras_chave": "Keywords (separate with comma)",
        "ph_cacar": "Ex: horror stories, abandoned cars, politics...",
        "ph_url": "https://www.youtube.com/@ChannelName",
        "ph_titulo": "Ex: I Survived 100 Days In A Nuclear Bunker",
        "ph_palavras": "Ex: elections, government, crisis, economy",
        "btn_cacar": "START HUNT",
        "btn_analisar": "AUDIT CHANNEL",
        "btn_titulos_ia": "GENERATE 10 TITLES WITH AI",
        "btn_titulos_simples": "GENERATE 7 TITLES",
        "lbl_csv": "Download Report (CSV)",
        "msg_erro_vazio": "Type what you want to hunt!",
        "msg_erro_nada": "Nothing found. Try another word.",
        "msg_erro_url": "Paste the channel link!",
        "msg_erro_canal": "Channel not found. Check the link.",
        "msg_erro_titulo": "Type a viral video title!",
        "msg_erro_palavras": "Type valid keywords separated by comma!",
        "msg_erro_ia": "Error generating content. Try again.",
        "titulo_original": "ORIGINAL TITLE ANALYZED",
        "titulos_gerados": "AI GENERATED TITLES",
        "palavras_analisadas": "ANALYZED KEYWORDS",
        "titulos_criados": "CREATED TITLES",
        "dica_titulo": "Tip: Choose the title that best fits your audience!",
        "dica_titulo_simples": "Tip: Combine these titles with high-contrast thumbnails!",
        "modelos_copiar": "Video models to copy",
        "abrir_youtube": "Open channel on YouTube",
        "ganho_video": "EARNINGS PER VIDEO",
        "total_canal": "CHANNEL TOTAL",
        "inscritos": "Subscribers",
        "views_video": "Views/video",
        "taxa_viral": "Viral rate",
        "mediana": "Median",
        "estourando": "VIRAL",
        "saudavel": "Healthy",
        "estagnado": "Stagnant",
        "canais": "Channels",
        "estourando_label": "Viral",
        "ganho_medio": "Avg earnings/video",
        "nenhum_canal": "No channel found. Try another word or subscriber range.",
    },
    "es": {
        "tab_cacador": "Cazador de Canales",
        "tab_analisar": "Analizar Canal",
        "tab_titulos_ia": "Generador de Títulos IA",
        "tab_titulos_simples": "Generador de Títulos Simples",
        "tab_guia": "Guía",
        "lbl_palavra": "¿Qué cazar?",
        "lbl_nicho": "Nicho",
        "lbl_qtd": "Cuántos canales",
        "lbl_vids": "Videos por canal",
        "lbl_insc_min": "Suscriptores mín.",
        "lbl_insc_max": "Suscriptores máx.",
        "lbl_estrangeiro": "Audiencia extranjera (paga 3x más)",
        "lbl_url": "Link o @ del canal",
        "lbl_estrangeiro2": "¿Canal en inglés/español?",
        "lbl_titulo_viral": "Título del video viral",
        "lbl_nicho_ia": "Nicho del Canal",
        "lbl_palavras_chave": "Palabras clave (separar con coma)",
        "ph_cacar": "Ej: historias de terror, coches abandonados, política...",
        "ph_url": "https://www.youtube.com/@NombreDelCanal",
        "ph_titulo": "Ej: Sobreviví 100 Días En Un Búnker Nuclear",
        "ph_palavras": "Ej: elecciones, gobierno, crisis, economía",
        "btn_cacar": "INICIAR CAZA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GENERAR 10 TÍTULOS CON IA",
        "btn_titulos_simples": "GENERAR 7 TÍTULOS",
        "lbl_csv": "Descargar Reporte (CSV)",
        "msg_erro_vazio": "¡Escribe lo que quieres cazar!",
        "msg_erro_nada": "Nada encontrado. Prueba otra palabra.",
        "msg_erro_url": "¡Pega el link del canal!",
        "msg_erro_canal": "Canal no encontrado. Verifica el link.",
        "msg_erro_titulo": "¡Escribe el título de un video viral!",
        "msg_erro_palavras": "¡Escribe palabras clave válidas separadas por coma!",
        "msg_erro_ia": "Error al generar contenido. Intenta de nuevo.",
        "titulo_original": "TÍTULO ORIGINAL ANALIZADO",
        "titulos_gerados": "TÍTULOS GENERADOS POR IA",
        "palavras_analisadas": "PALABRAS CLAVE ANALIZADAS",
        "titulos_criados": "TÍTULOS CREADOS",
        "dica_titulo": "Consejo: ¡Elige el título que mejor se adapte a tu audiencia!",
        "dica_titulo_simples": "Consejo: ¡Combina estos títulos con miniaturas de alto contraste!",
        "modelos_copiar": "Modelos de videos para copiar",
        "abrir_youtube": "Abrir canal en YouTube",
        "ganho_video": "GANANCIA POR VIDEO",
        "total_canal": "TOTAL DEL CANAL",
        "inscritos": "Suscriptores",
        "views_video": "Vistas/video",
        "taxa_viral": "Tasa viral",
        "mediana": "Mediana",
        "estourando": "VIRAL",
        "saudavel": "Saludable",
        "estagnado": "Estancado",
        "canais": "Canales",
        "estourando_label": "Viral",
        "ganho_medio": "Ganancia promedio/video",
        "nenhum_canal": "Ningún canal encontrado. Prueba otra palabra o rango de suscriptores.",
    }
}

def t(key):
    return I18N.get(IDIOMA_ATUAL, I18N["pt"]).get(key, I18N["pt"].get(key, key))

# ═══════════════════════════════════════════════════════════════
# 🤖 SISTEMA IA (Pollinations.ai)
# ═══════════════════════════════════════════════════════════════
def chamar_ia(prompt, idioma="pt"):
    idioma_map = {"pt": "português brasileiro", "en": "English", "es": "español"}
    idioma_texto = idioma_map.get(idioma, "português brasileiro")
    
    try:
        response = requests.post(
            "https://text.pollinations.ai/openai",
            json={
                "model": "openai",
                "messages": [
                    {"role": "system", "content": f"Responda sempre em {idioma_texto}. Seja direto e objetivo."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 2500
            },
            timeout=45
        )
        if response.status_code == 200:
            data = response.json()
            resultado = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if resultado and len(resultado) > 50:
                return resultado
    except:
        pass
    
    return None

# ═══════════════════════════════════════════════════════════════
# 🛠️ UTILITÁRIOS
# ═══════════════════════════════════════════════════════════════
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
    "Curiosidades":12, "Histórias/Crimes":18, "Documentário":20,
    "Resumo de Filmes":15, "Religião":10, "Motivacional":9,
    "Música/Relax":4, "Games":8, "Esportes":14,
    "Carros":26, "Tecnologia/IA":35, "Saúde":22, "Finanças":55,
    "Cortes de Podcast":8, "Meditação":6, "Finanças Cripto":45,
    "Shorts/TikTok":5, "Marketing Digital":40, "Fitness":18,
    "Receitas":14, "Pets":16, "Viagens":28,
    "Sobrenatural":22, "Autoajuda":16, "Fofoca/Celebridades":10,
    "Política":30,
}

# ═══════════════════════════════════════════════════════════════
# 🔍 MOTOR DE BUSCA
# ═══════════════════════════════════════════════════════════════
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
            "playlist_items":f"1-{max_vids}","ignoreerrors":True,"retries":3}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url_v, download=False) or {}
    except: return None
    
    vids = [e for e in (info.get("entries") or []) if e]
    
    if not vids or len(vids) < 5:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info2 = ydl.extract_info(url.rstrip("/")+"/shorts", download=False) or {}
            vids_shorts = [e for e in (info2.get("entries") or []) if e]
            vids = vids + vids_shorts
        except:
            pass
    
    if not vids:
        return None
    
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

# ═══════════════════════════════════════════════════════════════
# 🧠 GERADOR DE TÍTULOS IA
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return f"<div class='msg-erro'>{t('msg_erro_titulo')}</div>"
    
    idioma_map = {"pt": "português brasileiro", "en": "English", "es": "español"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "português brasileiro")
    
    prompt = f"""Você é um especialista em títulos virais para YouTube no nicho de {nicho}.

Título original viral: "{titulo_video}"

Sua tarefa: Criar EXATAMENTE 10 títulos COMPLETOS e CRIATIVOS para vídeos do YouTube, em {idioma_texto}, adaptados para o nicho de {nicho.upper()}.

REGRAS:
1. Cada título deve ser uma FRASE COMPLETA de 40-80 caracteres.
2. Use gatilhos mentais diferentes: curiosidade, urgência, números, emoção.
3. Adapte o conteúdo para o nicho de {nicho}.
4. Os 10 títulos DEVEM ser diferentes entre si.

FORMATO OBRIGATÓRIO:
1. [Título completo aqui]
2. [Título completo aqui]
... até 10

Responda APENAS com a lista numerada de 1 a 10."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    titulos = []
    if resultado:
        linhas = resultado.split('\n')
        for linha in linhas:
            linha = linha.strip()
            match = re.match(r'^\d+[\.\)]\s*(.+)', linha)
            if match:
                titulo = match.group(1).strip()
                if len(titulo) >= 30 and len(titulo) <= 100:
                    if re.search(r'[A-ZÀ-Ýa-zà-ý]', titulo) and len(titulo.split()) >= 5:
                        titulos.append(titulo)
    
    if len(titulos) < 10:
        titulos = gerar_titulos_fallback_nicho(titulo_video, nicho)
    
    titulos = titulos[:10]
    while len(titulos) < 10:
        titulos.append(f"Como {titulo_video} se aplica ao nicho de {nicho} (Versão {len(titulos)+1})")
    
    return renderizar_titulos(titulo_video, titulos, t('titulo_original'), t('titulos_gerados'), t('dica_titulo'))

def gerar_titulos_fallback_nicho(titulo_original, nicho):
    if "Política" in nicho:
        return [
            f"O Escândalo de {titulo_original} Que Pode Derrubar o Governo",
            f"7 Verdades Sobre {titulo_original} Que Os Políticos Escondem",
            f"Por Que {titulo_original} Está Dividindo o País em 2024",
            f"A Manipulação Por Tras de {titulo_original} Explicada",
            f"O Que Realmente Acontece Nos Bastidores de {titulo_original}",
            f"10 Mentiras Que Te Contaram Sobre {titulo_original}",
            f"Como {titulo_original} Afeta Seu Bolso Todos os Dias",
            f"URGENTE: A Verdade Sobre {titulo_original}",
            f"O Futuro de {titulo_original} e o Que Isso Significa",
            f"Por Que {titulo_original} Está Chocando o Mundo Político"
        ]
    elif "Histórias/Crimes" in nicho:
        return [
            f"O Crime de {titulo_original} Que Ninguém Consegue Resolver",
            f"7 Detalhes Macabros de {titulo_original}",
            f"A Verdade Sombria Por Tras de {titulo_original}",
            f"O Mistério de {titulo_original} Que Assusta Investigadores",
            f"10 Evidências Chocantes de {titulo_original}",
            f"Como {titulo_original} Enganou a Todos Por Anos",
            f"URGENTE: Novas Revelações Sobre {titulo_original}",
            f"O Dia Em Que {titulo_original} Mudou Tudo",
            f"A História Não Contada de {titulo_original}",
            f"Por Que {titulo_original} Continua Assombrando a Todos"
        ]
    else:
        numeros = re.findall(r'\d+', titulo_original)
        titulos = []
        if numeros:
            num = int(numeros[0])
            for n in [num//2, num*2, num*10, 100, 1000]:
                titulos.append(re.sub(r'\d+', str(n), titulo_original, count=1))
        prefixos = ["URGENTE: ", "ATENÇÃO: ", "IMPRESSINANTE: ", "INACREDITÁVEL: ", "CHOCANTE: "]
        for prefixo in prefixos[:5]:
            titulos.append(f"{prefixo}{titulo_original}")
        titulos.append(f"Você Conseguiria Sobreviver a Isso? {titulo_original}")
        titulos.append(f"Por Que {titulo_original} Está Chocando o Mundo?")
        return titulos[:10]

def renderizar_titulos(titulo_original, titulos, label_original, label_gerados, dica):
    html = f'''<div class="box-resultado box-titulos">
        <div class="box-header"><h3>{label_original}</h3></div>
        <div class="box-conteudo">{titulo_original}</div>
        <div class="box-header" style="margin-top: 25px;"><h3>{len(titulos)} {label_gerados}</h3></div>'''
    for i, titulo in enumerate(titulos[:10], 1):
        html += f'''<div class="titulo-item"><span class="titulo-num">{i}.</span><span class="titulo-texto">{titulo}</span></div>'''
    html += f'''<div class="box-dica"><strong>{dica}</strong></div></div>'''
    return html

# ═══════════════════════════════════════════════════════════════
# 📝 GERADOR DE TÍTULOS SIMPLES
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_simples(nicho, palavras_chave):
    if not palavras_chave or not palavras_chave.strip():
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    palavras = [p.strip() for p in palavras_chave.split(',') if p.strip()]
    if not palavras:
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    p0 = palavras[0].title() if palavras else "Tema"
    p1 = palavras[1].title() if len(palavras) > 1 else "Concorrência"
    
    formulas_por_nicho = {
        "Política": [
            f"O Escândalo de {p0} Que Pode Derrubar o Governo",
            f"7 Verdades Sobre {p0} Que Os Políticos Escondem",
            f"Por Que {p0} Está Dividindo o País em 2024",
            f"A Manipulação Por Tras de {p0} Explicada",
            f"O Que Realmente Acontece Nos Bastidores de {p0}",
            f"10 Mentiras Que Te Contaram Sobre {p0}",
            f"Como {p0} Afeta Seu Bolso Todos os Dias",
        ],
        "Histórias/Crimes": [
            f"O Crime de {p0} Que Ninguém Consegue Resolver",
            f"7 Detalhes Macabros de {p0}",
            f"A Verdade Sombria Por Tras de {p0}",
            f"O Mistério de {p0} Que Assusta Investigadores",
            f"10 Evidências Chocantes de {p0}",
            f"Como {p0} Enganou a Todos Por Anos",
            f"URGENTE: Novas Revelações Sobre {p0}",
        ],
        "Finanças": [
            f"7 Maneiras de Ganhar Dinheiro com {p0} em 2024",
            f"Como {p0} Pode Te Fazer Rico em 5 Anos",
            f"O Segredo de {p0} Que Milionários Não Contam",
            f"Por Que {p0} Está Fazendo Pessoas Comuns Ficarem Ricas",
            f"10 Erros Financeiros Que Você Comete com {p0}",
            f"Como Começar com {p0} do Zero (Guia Completo)",
            f"A Verdade Sobre {p0} Que Os Bancos Escondem",
        ],
        "Tecnologia/IA": [
            f"Como {p0} Vai Mudar o Mundo em 2024",
            f"7 Ferramentas de {p0} Que Você Precisa Conhecer",
            f"O Futuro de {p0} Que Ninguém Está Vendo",
            f"Por Que {p0} Está Substituindo Profissões Inteiras",
            f"10 Usos Incríveis de {p0} Que Você Não Imaginava",
            f"Como Começar com {p0} Hoje Mesmo (Passo a Passo)",
            f"A Verdade Sobre {p0} Que As Big Techs Escondem",
        ],
    }
    
    formulas = formulas_por_nicho.get(nicho, [
        f"7 Segredos Sobre {p0} Que Vão Mudar Sua Vida",
        f"10 Maneiras de Ganhar Dinheiro com {p0}",
        f"Por Que {p0} Está Fazendo Pessoas Ficarem Ricas",
        f"Você Sabia Que {p0} Pode Te Fazer Ganhar {p1}?",
        f"URGENTE: O Que Está Acontecendo com {p0}",
        f"ATENÇÃO: Não Ignore Isso Sobre {p0} em 2024",
        f"{p0} vs {p1}: Qual é Melhor?",
    ])
    
    titulos = formulas[:7]
    
    return renderizar_titulos(palavras_chave, titulos, t('palavras_analisadas'), t('titulos_criados'), t('dica_titulo_simples'))

# ═══════════════════════════════════════════════════════════════
#  CSS - INTERFACE LIMPA E SIMPLES
# ═══════════════════════════════════════════════════════════════
CSS_YOUTUBE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
body, .gradio-container, .main, .wrap, .gradio-app { 
    background: #0F0F0F !important; color: #F1F1F1 !important;
}

.ac-header {
    background: #0F0F0F; border-bottom: 4px solid #FF0000;
    padding: 50px 40px; text-align: center; margin-bottom: 40px;
    max-width: 1200px; margin-left: auto; margin-right: auto;
}
.ac-header h1 {
    font-family: 'Poppins', sans-serif !important; font-size: 56px !important;
    font-weight: 900 !important; color: #FFFFFF !important; margin: 0;
}
.ac-header h1 .begins { color: #FF0000 !important; }
.ac-header .creator { font-size: 16px; color: #AAAAAA; margin-top: 15px; font-weight: 500; }
.ac-header .subtitle { font-size: 18px; color: #F1F1F1; margin-top: 10px; font-weight: 400; }
.ac-header .badge {
    display: inline-block; background: #FF0000; color: #FFFFFF;
    padding: 8px 20px; border-radius: 20px; font-size: 13px;
    font-weight: 700; margin-top: 20px; text-transform: uppercase;
}

.stats-container { display: flex; gap: 20px; margin: 40px auto; justify-content: center; max-width: 1200px; }
.stat-card {
    flex: 1; max-width: 320px; background: #282828; padding: 30px;
    border-radius: 12px; text-align: center; border: 1px solid #3F3F3F;
}
.stat-card strong {
    display: block; font-family: 'Poppins', sans-serif !important;
    font-size: 48px !important; color: #FF0000 !important; font-weight: 900; margin-bottom: 10px;
}
.stat-card span { color: #AAAAAA; font-size: 13px !important; font-weight: 600; text-transform: uppercase; }

.ac-card {
    background: #282828; border-radius: 12px; margin: 25px auto;
    overflow: hidden; border: 1px solid #3F3F3F; max-width: 1200px;
}
.ac-card:hover { border-color: #FF0000; }
.ac-card-head {
    padding: 25px 30px; display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #3F3F3F; background: #1F1F1F;
}
.ac-card-head h3 {
    margin: 0; font-family: 'Poppins', sans-serif !important;
    font-size: 22px !important; color: #FFFFFF !important; font-weight: 700;
}
.ac-badge { padding: 8px 18px; border-radius: 20px; font-size: 12px !important; font-weight: 700; text-transform: uppercase; }
.ac-badge-rocket { background: #FF0000; color: #FFFFFF !important; }
.ac-badge-up { background: #FFD700; color: #0F0F0F !important; }
.ac-badge-sleep { background: #606060; color: #FFFFFF !important; }

.ac-card-body { padding: 25px 30px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.ac-stat-mini { background: #1F1F1F; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #3F3F3F; }
.ac-stat-mini .lbl { font-size: 11px !important; color: #AAAAAA !important; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }
.ac-stat-mini .val { font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 700; color: #FFFFFF !important; }

.ac-money { background: #FF0000; padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; }
.ac-money strong { font-family: 'Poppins', sans-serif !important; font-size: 32px !important; color: #FFFFFF !important; font-weight: 900; }
.ac-money .label { font-size: 11px !important; color: #FFFFFF !important; font-weight: 600; text-transform: uppercase; }

.ac-bombas { padding: 25px 30px; background: #1F1F1F; border-top: 1px solid #3F3F3F; }
.ac-bombas h4 { margin: 0 0 15px; color: #FF0000 !important; font-size: 14px !important; text-transform: uppercase; font-weight: 700; }
.ac-bomba { padding: 12px 15px; font-size: 14px !important; border-bottom: 1px solid #3F3F3F; color: #F1F1F1 !important; background: #282828; border-radius: 6px; margin-bottom: 8px; }
.ac-bomba:last-child { border-bottom: none; }
.ac-bomba a { color: #3EA6FF !important; text-decoration: none !important; font-weight: 600; }
.ac-bomba a:hover { text-decoration: underline !important; }
.ac-bomba .v { color: #FF0000 !important; font-weight: 700; margin-right: 12px; font-size: 16px !important; }

.ac-foot { padding: 20px; text-align: center; background: #1F1F1F; border-top: 1px solid #3F3F3F; }
.ac-foot a {
    color: #FF0000 !important; text-decoration: none !important; font-weight: 700;
    font-size: 14px !important; text-transform: uppercase;
    display: inline-block; padding: 12px 30px; border: 2px solid #FF0000;
    border-radius: 20px;
}
.ac-foot a:hover { background: #FF0000; color: #FFFFFF !important; }

.box-resultado { background: #282828; border-radius: 12px; padding: 30px; margin: 30px auto; max-width: 1200px; border: 1px solid #3F3F3F; }
.box-titulos { border-left: 4px solid #FF0000; }
.box-header h3 { color: #FF0000 !important; font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 800 !important; margin: 0; text-transform: uppercase; }
.box-conteudo { background: #1F1F1F; padding: 20px; border-radius: 8px; color: #F1F1F1; font-size: 16px; font-weight: 500; border: 1px solid #3F3F3F; }
.box-dica { margin-top: 25px; padding: 15px 20px; background: #1F1F1F; border-radius: 8px; color: #AAAAAA; font-size: 14px; border-left: 3px solid #FFD700; }
.box-dica strong { color: #FFD700; }
.titulo-item { background: #1F1F1F; padding: 18px 20px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #FF0000; display: flex; align-items: flex-start; gap: 15px; }
.titulo-num { color: #FF0000; font-weight: 700; font-size: 16px; min-width: 25px; }
.titulo-texto { color: #F1F1F1; font-size: 15px; font-weight: 500; line-height: 1.5; }
.msg-erro { padding: 40px; text-align: center; color: #FF0000; font-size: 18px; font-weight: 600; background: #282828; border-radius: 12px; border: 1px solid #FF0000; margin: 30px auto; max-width: 800px; }

.footer-creator { text-align: center; padding: 50px 30px; color: #AAAAAA !important; font-size: 14px !important; border-top: 1px solid #3F3F3F; margin-top: 60px; background: #0F0F0F; }
.footer-creator strong { color: #FFFFFF !important; font-weight: 700; font-size: 16px !important; }
.footer-creator .begins-mark { display: inline-block; color: #FF0000 !important; font-weight: 900; font-size: 36px !important; margin-bottom: 15px; text-transform: uppercase; font-family: 'Poppins', sans-serif; }

.gr-box, .gr-input, .gr-dropdown, .gr-slider, .gr-textbox { background: #282828 !important; border: 1px solid #3F3F3F !important; color: #F1F1F1 !important; border-radius: 8px !important; }
.gr-input, .gr-textbox input { color: #F1F1F1 !important; font-size: 15px !important; font-weight: 500; background: #1F1F1F !important; }
.gr-dropdown .wrap { background: #282828 !important; border: 1px solid #3F3F3F !important; }
.gr-dropdown .wrap span { color: #F1F1F1 !important; font-size: 14px !important; font-weight: 500; }
.gr-button-primary {
    background: #FF0000 !important; border: none !important; color: #FFFFFF !important;
    font-weight: 700 !important; font-size: 16px !important;
    text-transform: uppercase; padding: 16px 40px !important; border-radius: 20px !important;
}
.gr-button-primary:hover { background: #CC0000 !important; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255,0,0,0.4) !important; }
.gr-tabs .selected { border-bottom: 3px solid #FF0000 !important; color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; }
.gr-tabs .unselected { color: #AAAAAA !important; font-size: 15px !important; }
.gr-markdown h3 { color: #FF0000 !important; font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 800; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; }
.gr-markdown p { color: #AAAAAA !important; font-size: 15px; line-height: 1.6; }
</style>
"""

def render_cards(resultados):
    html = [CSS_YOUTUBE,'<div class="ac-wrap">']
    if not resultados:
        html.append(f'<div class="msg-erro">{t("nenhum_canal")}</div>')
    else:
        est = sum(1 for r in resultados if r["status"]=="ESTOURANDO")
        gm = sum(r["ganho_video"] for r in resultados)/len(resultados)
        html.append(f'''<div class="stats-container">
            <div class="stat-card"><strong>{len(resultados)}</strong><span>{t("canais")}</span></div>
            <div class="stat-card"><strong>{est}</strong><span>{t("estourando_label")}</span></div>
            <div class="stat-card"><strong>{brl(gm)}</strong><span>{t("ganho_medio")}</span></div>
        </div>''')
        for r in resultados:
            bc = "rocket" if r["status"]=="ESTOURANDO" else ("up" if r["status"]=="Saudavel" else "sleep")
            status_text = t("estourando") if r["status"]=="ESTOURANDO" else (t("saudavel") if r["status"]=="Saudavel" else t("estagnado"))
            
            videos_html = ""
            if r.get('videos') and len(r['videos']) > 0:
                videos_html = '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #3F3F3F;"><h4 style="color: #FF0000; font-size: 14px; margin-bottom: 10px; font-weight: 700;">ÚLTIMOS VÍDEOS ENCONTRADOS:</h4>'
                for v in r['videos'][:5]:
                    videos_html += f'<div style="font-size: 13px; color: #F1F1F1; margin-bottom: 6px; padding: 8px; background: #282828; border-radius: 6px;"><strong style="color: #3EA6FF;">{fmt(v["views"])} views</strong> - {v["titulo"][:80]}{"..." if len(v["titulo"])>80 else ""}</div>'
                videos_html += '</div>'
            
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{status_text}</span></div>
<div class="ac-card-body">
<div class="ac-stat-mini"><div class="lbl">{t("inscritos")}</div><div class="val">{fmt(r['inscritos'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("views_video")}</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("taxa_viral")}</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("mediana")}</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div class="label">{t("ganho_video")}</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right"><div class="label">{t("total_canal")}</div><strong>{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>
{videos_html}''')
            if r['bombas']:
                html.append(f'<div class="ac-bombas"><h4>{t("modelos_copiar")}</h4>')
                for b in r['bombas']:
                    html.append(f'<div class="ac-bomba"><span class="v">{fmt(b["views"])}</span><a href="{b["url"]}" target="_blank">{b["titulo"][:70]}{"..." if len(b["titulo"])>70 else ""}</a></div>')
                html.append('</div>')
            html.append(f'<div class="ac-foot"><a href="{r["url"]}" target="_blank">{t("abrir_youtube")}</a></div></div>')
    html.append('</div>')
    return "".join(html)

def cacar(palavra, nicho_label, qtd, insc_min, insc_max, vids, estrangeiro):
    if not palavra or not palavra.strip():
        return f"<div class='msg-erro'>{t('msg_erro_vazio')}</div>", None, []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    vids_achados = buscar_videos(palavra, 50)
    if not vids_achados:
        return f"<div class='msg-erro'>{t('msg_erro_nada')}</div>", None, []
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
        a["status"] = ("ESTOURANDO") if tx>=1.0 else (("Saudavel") if tx>=0.3 else ("Estagnado"))
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
        return f"<div class='msg-erro'>{t('msg_erro_url')}</div>", []
    RPM = TABELA_RPM.get(nicho_label,12) * (3.2 if estrangeiro else 1.0)
    url = url_canal.strip()
    if url.startswith("@"): url = "https://www.youtube.com/" + url
    elif not url.startswith("http"):
        url = "https://www.youtube.com/channel/"+url if url.startswith("UC") else "https://www.youtube.com/"+url
    a = analisar_canal(url, int(vids))
    if a is None:
        return f"<div class='msg-erro'>{t('msg_erro_canal')}</div>", []
    tx = a["taxa"] or 0
    a["status"] = ("ESTOURANDO") if tx>=1.0 else (("Saudavel") if tx>=0.3 else ("Estagnado"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a]), [a]

# ═══════════════════════════════════════════════════════════════
# 🌐 INTERFACE
# ═══════════════════════════════════════════════════════════════
begins_theme = gr.themes.Base(
    primary_hue="red", secondary_hue="neutral", neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins - Creator Assistant", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span> - Assistente do Criador</h1>
        <div class="creator">Murilo Silva - Criador de Conteúdo</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">VERSÃO 15.0 - IA OPEN SOURCE</span>
    </div>
    """)
    
    # Seletor de idioma
    idioma_selector = gr.Radio(
        choices=[("Português", "pt"), ("English", "en"), ("Español", "es")],
        value="pt",
        label="Idioma / Language / Idioma",
        elem_classes=["lang-selector"]
    )
    
    canais_state = gr.State([])
    
    with gr.Tabs():
        with gr.Tab(t('tab_cacador')):
            gr.Markdown(f"### {t('tab_cacador')}")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label=t('lbl_palavra'), placeholder=t('ph_cacar'))
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value="Histórias/Crimes", label=t('lbl_nicho'))
            with gr.Row():
                qtd = gr.Slider(3,20,value=8,step=1,label=t('lbl_qtd'))
                vids_caca = gr.Slider(10,50,value=30,step=5,label=t('lbl_vids'))
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label=t('lbl_insc_min'))
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label=t('lbl_insc_max'))
            estrangeiro = gr.Checkbox(True, label=t('lbl_estrangeiro'))
            btn = gr.Button(t('btn_cacar'), variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label=t('lbl_csv'))
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv,canais_state])

        with gr.Tab(t('tab_analisar')):
            gr.Markdown(f"### {t('tab_analisar')}")
            url_analise = gr.Textbox(label=t('lbl_url'), placeholder=t('ph_url'))
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="Curiosidades", label=t('lbl_nicho'))
                vids_analise = gr.Slider(10,50,value=30,step=5,label=t('lbl_vids'))
            estrangeiro2 = gr.Checkbox(False, label=t('lbl_estrangeiro2'))
            btn2 = gr.Button(t('btn_analisar'), variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=[out2,canais_state])

        with gr.Tab(t('tab_titulos_ia')):
            gr.Markdown(f"### {t('tab_titulos_ia')}")
            titulo_video_ia = gr.Textbox(label=t('lbl_titulo_viral'), placeholder=t('ph_titulo'))
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="Histórias/Crimes", label=t('lbl_nicho_ia'))
            btn_ia = gr.Button(t('btn_titulos_ia'), variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=gerar_titulos_ia, inputs=[titulo_video_ia, nicho_ia], outputs=out_ia)

        with gr.Tab(t('tab_titulos_simples')):
            gr.Markdown(f"### {t('tab_titulos_simples')}")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="Histórias/Crimes", label=t('lbl_nicho_ia'))
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label=t('lbl_palavras_chave'), placeholder=t('ph_palavras'))
            btn_gen = gr.Button(t('btn_titulos_simples'), variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos_simples, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab(t('tab_guia')):
            gr.Markdown(f"""
            ### {t('tab_guia')}
            
            **CAÇADOR DE CANAIS**
            Digite o tema do seu nicho. Exemplos: 'histórias de terror', 'carros abandonados', 'política'. Escolha o nicho correspondente. Ajuste a quantidade de canais (recomendado: 8) e a faixa de inscritos (recomendado: 10.000 a 500.000). Marque 'Público estrangeiro' se quiser buscar canais em inglês/espanhol (pagam 3x mais). Clique em 'INICIAR CAÇADA' e espere 1-3 minutos.
            
            **ANALISAR CANAL**
            Cole o link completo do canal ou apenas o @NomeDoCanal. Escolha o nicho e clique em 'AUDITAR CANAL'. O sistema vai analisar os vídeos e te mostrar a média real de views e os títulos dos vídeos encontrados.
            
            **GERADOR DE TÍTULOS IA**
            Cole o TÍTULO COMPLETO de um vídeo viral que você quer modelar. A IA vai analisar o padrão psicológico e gerar EXATAMENTE 10 títulos NOVOS e CRIATIVOS no mesmo estilo, adaptados especificamente para o nicho selecionado.
            
            **GERADOR DE TÍTULOS SIMPLES**
            Digite palavras-chave separadas por vírgula. O sistema usa fórmulas de títulos virais ultra-específicas para cada nicho para gerar EXATAMENTE 7 títulos prontos e altamente direcionados.
            
            **DICAS DE OURO:**
            - Busque em inglês para achar canais que pagam 3x mais
            - Taxa viral acima de 1.0x significa que o YouTube está entregando o vídeo para não-inscritos
            - Modele a estrutura dos vídeos, mas NUNCA copie o roteiro palavra por palavra
            - Thumbnails com rosto + expressão forte + seta vermelha + texto curto tem CTR 2-3x maior
            - Os primeiros 30 segundos do vídeo decidem tudo
            """)

    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div>
        <strong>O ponto de partida para o seu novo negócio.</strong><br><br>
        Desenvolvido por Murilo Silva - Criador de Conteúdo<br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
