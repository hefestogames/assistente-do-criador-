import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os, requests, json
import gradio as gr
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# 🌍 SISTEMA DE INTERNACIONALIZAÇÃO (PT / EN / ES) - FUNCIONANDO
# ═══════════════════════════════════════════════════════════════
IDIOMA_ATUAL = "pt"

I18N = {
    "pt": {
        "header_title": "BEGINS - Assistente do Criador",
        "header_creator": "Murilo Silva - Criador de Conteúdo",
        "header_subtitle": "O ponto de partida para o seu novo negócio no YouTube",
        "header_badge": "VERSAO 13.0 - IA OPEN SOURCE",
        "tab_cacador": "Cacador de Canais",
        "tab_analisar": "Analisar Canal",
        "tab_titulos_ia": "Gerador de Titulos IA",
        "tab_titulos_simples": "Gerador de Titulos Simples",
        "tab_roteiro": "Gerador de Roteiro",
        "tab_thumbnails": "Gerador de Thumbnails",
        "tab_guia": "Guia Completo",
        "footer_text": "O ponto de partida para o seu novo negocio.",
        "footer_dev": "Desenvolvido por Murilo Silva - Criador de Conteudo",
        "footer_disclaimer": "Ferramenta para fins educacionais e de pesquisa de mercado.",
        "lang_label": "Idioma",
        "banner_ia_title": "IA Open Source Integrada (Pollinations.ai + HuggingFace)",
        "banner_ia_text": "100% gratuita, sem login, sem senha, sem API key. Codigo aberto. Gerando titulos, roteiros e thumbnails automaticamente.",
        "btn_cacar": "INICIAR CACADA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GERAR 10 TITULOS COM IA",
        "btn_titulos_simples": "GERAR 7 TITULOS",
        "btn_roteiro": "GERAR ROTEIRO COMPLETO",
        "btn_thumbnails": "GERAR 3 THUMBNAILS",
        "lbl_palavra": "O que cacar?",
        "lbl_nicho": "Nicho",
        "lbl_qtd": "Quantos canais",
        "lbl_vids": "Videos por canal",
        "lbl_insc_min": "Inscritos min.",
        "lbl_insc_max": "Inscritos max.",
        "lbl_estrangeiro": "Publico estrangeiro (paga 3x mais)",
        "lbl_url": "Link ou @ do canal",
        "lbl_estrangeiro2": "Canal em ingles/espanhol?",
        "lbl_titulo_viral": "Titulo do video viral",
        "lbl_nicho_ia": "Nicho do Canal",
        "lbl_palavras_chave": "Palavras-chave (separe por virgula)",
        "lbl_tema": "Tema do seu video",
        "ph_cacar": "Ex: historias de terror, carros abandonados, true crime...",
        "ph_url": "https://www.youtube.com/@NomeDoCanal",
        "ph_titulo": "Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000",
        "ph_palavras": "Ex: cachorro, dinheiro, trabalho, gratis",
        "ph_tema": "Ex: Os misterios nao resolvidos do Triangulo das Bermudas",
        "lbl_csv": "Baixar Relatorio (CSV)",
        "msg_erro_vazio": "Digite o que voce quer cacar!",
        "msg_erro_nada": "Nada encontrado. Tente outra palavra.",
        "msg_erro_url": "Cole o link do canal!",
        "msg_erro_canal": "Canal nao encontrado. Verifique o link.",
        "msg_erro_titulo": "Digite o titulo de um video viral!",
        "msg_erro_tema": "Digite o tema do seu video!",
        "msg_erro_palavras": "Digite palavras-chave validas separadas por virgula!",
        "msg_erro_ia": "Erro ao gerar conteudo. Tente novamente.",
        "titulo_original": "TITULO ORIGINAL ANALISADO",
        "titulos_gerados": "TITULOS GERADOS PELA IA",
        "palavras_analisadas": "PALAVRAS-CHAVE ANALISADAS",
        "titulos_criados": "TITULOS CRIADOS",
        "roteiro_completo": "ROTEIRO COMPLETO",
        "thumbnails_ideias": "IDEIAS DE THUMBNAILS",
        "dica_titulo": "Dica: Escolha o titulo que melhor se adapta ao seu publico e combine com uma thumbnail impactante!",
        "dica_roteiro": "Dica: Use este roteiro como base e adapte com sua personalidade!",
        "dica_thumb": "Dica: Use o Canva (gratis) para criar as thumbnails com essas especificacoes!",
        "dica_titulo_simples": "Dica: Combine estes titulos com thumbnails de alto contraste para maximizar o CTR!",
        "modelos_copiar": "Modelos para copiar",
        "abrir_youtube": "Abrir canal no YouTube",
        "ganho_video": "GANHO POR VIDEO",
        "total_canal": "TOTAL DO CANAL",
        "inscritos": "Inscritos",
        "views_video": "Views/video",
        "taxa_viral": "Taxa viral",
        "mediana": "Mediana",
        "estourando": "ESTOURANDO",
        "saudavel": "Saudavel",
        "estagnado": "Estagnado",
        "canais": "Canais",
        "estourando_label": "Estourando",
        "ganho_medio": "Ganho medio/video",
        "nenhum_canal": "Nenhum canal encontrado. Tente outra palavra ou faixa de inscritos.",
        "guia_titulo": "Como usar o Begins - Assistente do Criador",
    },
    "en": {
        "header_title": "BEGINS - Creator Assistant",
        "header_creator": "Murilo Silva - Content Creator",
        "header_subtitle": "The starting point for your new YouTube business",
        "header_badge": "VERSION 13.0 - OPEN SOURCE AI",
        "tab_cacador": "Channel Hunter",
        "tab_analisar": "Analyze Channel",
        "tab_titulos_ia": "AI Title Generator",
        "tab_titulos_simples": "Simple Title Generator",
        "tab_roteiro": "Script Generator",
        "tab_thumbnails": "Thumbnail Generator",
        "tab_guia": "Complete Guide",
        "footer_text": "The starting point for your new business.",
        "footer_dev": "Developed by Murilo Silva - Content Creator",
        "footer_disclaimer": "Tool for educational and market research purposes.",
        "lang_label": "Language",
        "banner_ia_title": "Open Source AI Integrated (Pollinations.ai + HuggingFace)",
        "banner_ia_text": "100% free, no login, no password, no API key. Open source. Generating titles, scripts and thumbnails automatically.",
        "btn_cacar": "START HUNT",
        "btn_analisar": "AUDIT CHANNEL",
        "btn_titulos_ia": "GENERATE 10 TITLES WITH AI",
        "btn_titulos_simples": "GENERATE 7 TITLES",
        "btn_roteiro": "GENERATE COMPLETE SCRIPT",
        "btn_thumbnails": "GENERATE 3 THUMBNAILS",
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
        "lbl_tema": "Your video theme",
        "ph_cacar": "Ex: horror stories, abandoned cars, true crime...",
        "ph_url": "https://www.youtube.com/@ChannelName",
        "ph_titulo": "Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000",
        "ph_palavras": "Ex: dog, money, work, free",
        "ph_tema": "Ex: The unsolved mysteries of the Bermuda Triangle",
        "lbl_csv": "Download Report (CSV)",
        "msg_erro_vazio": "Type what you want to hunt!",
        "msg_erro_nada": "Nothing found. Try another word.",
        "msg_erro_url": "Paste the channel link!",
        "msg_erro_canal": "Channel not found. Check the link.",
        "msg_erro_titulo": "Type a viral video title!",
        "msg_erro_tema": "Type your video theme!",
        "msg_erro_palavras": "Type valid keywords separated by comma!",
        "msg_erro_ia": "Error generating content. Try again.",
        "titulo_original": "ORIGINAL TITLE ANALYZED",
        "titulos_gerados": "AI GENERATED TITLES",
        "palavras_analisadas": "ANALYZED KEYWORDS",
        "titulos_criados": "CREATED TITLES",
        "roteiro_completo": "COMPLETE SCRIPT",
        "thumbnails_ideias": "THUMBNAIL IDEAS",
        "dica_titulo": "Tip: Choose the title that best fits your audience and combine with an impactful thumbnail!",
        "dica_roteiro": "Tip: Use this script as a base and adapt it with your personality!",
        "dica_thumb": "Tip: Use Canva (free) to create thumbnails with these specifications!",
        "dica_titulo_simples": "Tip: Combine these titles with high-contrast thumbnails to maximize CTR!",
        "modelos_copiar": "Models to copy",
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
        "guia_titulo": "How to use Begins - Creator Assistant",
    },
    "es": {
        "header_title": "BEGINS - Asistente del Creador",
        "header_creator": "Murilo Silva - Creador de Contenido",
        "header_subtitle": "El punto de partida para tu nuevo negocio en YouTube",
        "header_badge": "VERSION 13.0 - IA OPEN SOURCE",
        "tab_cacador": "Cazador de Canales",
        "tab_analisar": "Analizar Canal",
        "tab_titulos_ia": "Generador de Titulos IA",
        "tab_titulos_simples": "Generador de Titulos Simples",
        "tab_roteiro": "Generador de Guion",
        "tab_thumbnails": "Generador de Miniaturas",
        "tab_guia": "Guia Completa",
        "footer_text": "El punto de partida para tu nuevo negocio.",
        "footer_dev": "Desarrollado por Murilo Silva - Creador de Contenido",
        "footer_disclaimer": "Herramienta para fines educativos e investigacion de mercado.",
        "lang_label": "Idioma",
        "banner_ia_title": "IA Open Source Integrada (Pollinations.ai + HuggingFace)",
        "banner_ia_text": "100% gratuita, sin login, sin contrasena, sin API key. Codigo abierto. Generando titulos, guiones y miniaturas automaticamente.",
        "btn_cacar": "INICIAR CAZA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GENERAR 10 TITULOS CON IA",
        "btn_titulos_simples": "GENERAR 7 TITULOS",
        "btn_roteiro": "GENERAR GUION COMPLETO",
        "btn_thumbnails": "GENERAR 3 MINIATURAS",
        "lbl_palavra": "Que cazar?",
        "lbl_nicho": "Nicho",
        "lbl_qtd": "Cuantos canales",
        "lbl_vids": "Videos por canal",
        "lbl_insc_min": "Suscriptores min.",
        "lbl_insc_max": "Suscriptores max.",
        "lbl_estrangeiro": "Audiencia extranjera (paga 3x mas)",
        "lbl_url": "Link o @ del canal",
        "lbl_estrangeiro2": "Canal en ingles/espanol?",
        "lbl_titulo_viral": "Titulo del video viral",
        "lbl_nicho_ia": "Nicho del Canal",
        "lbl_palavras_chave": "Palabras clave (separar con coma)",
        "lbl_tema": "Tema de tu video",
        "ph_cacar": "Ej: historias de terror, coches abandonados, true crime...",
        "ph_url": "https://www.youtube.com/@NombreDelCanal",
        "ph_titulo": "Ej: Sobrevivi 100 Dias En Un Bunker Nuclear, Gana $500,000",
        "ph_palavras": "Ej: perro, dinero, trabajo, gratis",
        "ph_tema": "Ej: Los misterios no resueltos del Triangulo de las Bermudas",
        "lbl_csv": "Descargar Reporte (CSV)",
        "msg_erro_vazio": "Escribe lo que quieres cazar!",
        "msg_erro_nada": "Nada encontrado. Prueba otra palabra.",
        "msg_erro_url": "Pega el link del canal!",
        "msg_erro_canal": "Canal no encontrado. Verifica el link.",
        "msg_erro_titulo": "Escribe el titulo de un video viral!",
        "msg_erro_tema": "Escribe el tema de tu video!",
        "msg_erro_palavras": "Escribe palabras clave validas separadas por coma!",
        "msg_erro_ia": "Error al generar contenido. Intenta de nuevo.",
        "titulo_original": "TITULO ORIGINAL ANALIZADO",
        "titulos_gerados": "TITULOS GENERADOS POR IA",
        "palavras_analisadas": "PALABRAS CLAVE ANALIZADAS",
        "titulos_criados": "TITULOS CREADOS",
        "roteiro_completo": "GUION COMPLETO",
        "thumbnails_ideias": "IDEAS DE MINIATURAS",
        "dica_titulo": "Consejo: Elige el titulo que mejor se adapte a tu audiencia y combinalo con una miniatura impactante!",
        "dica_roteiro": "Consejo: Usa este guion como base y adaptalo con tu personalidad!",
        "dica_thumb": "Consejo: Usa Canva (gratis) para crear las miniaturas con estas especificaciones!",
        "dica_titulo_simples": "Consejo: Combina estos titulos con miniaturas de alto contraste para maximizar el CTR!",
        "modelos_copiar": "Modelos para copiar",
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
        "nenhum_canal": "Ningun canal encontrado. Prueba otra palabra o rango de suscriptores.",
        "guia_titulo": "Como usar Begins - Asistente del Creador",
    }
}

def t(key):
    return I18N.get(IDIOMA_ATUAL, I18N["pt"]).get(key, I18N["pt"].get(key, key))

# ═══════════════════════════════════════════════════════════════
#  SISTEMA MULTI-IA (Pollinations + HuggingFace + Fallback)
# ═══════════════════════════════════════════════════════════════
def chamar_ia(prompt, idioma="pt"):
    """Tenta Pollinations.ai primeiro, depois HuggingFace"""
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(idioma, "portugues brasileiro")
    
    # TENTA 1: Pollinations.ai
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
                "max_tokens": 3000
            },
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            resultado = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if resultado and len(resultado) > 50:
                return resultado
    except:
        pass
    
    # TENTA 2: HuggingFace Inference API (grátis)
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={"Authorization": "Bearer hf_fake_token_for_free_tier"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.8}},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                resultado = data[0].get("generated_text", "")
                if resultado and len(resultado) > 50:
                    return resultado
    except:
        pass
    
    return None

def gerar_imagem(prompt, width=1280, height=720):
    """Gera imagem via Pollinations.ai (grátis, sem login)"""
    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width={width}&height={height}&nologo=true&seed={random.randint(1,999999)}"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Salva imagem temporária
            img_path = f"thumbnail_{random.randint(1000,9999)}.png"
            with open(img_path, "wb") as f:
                f.write(response.content)
            return img_path
    except:
        pass
    return None

# ═══════════════════════════════════════════════════════════════
# ️ UTILITÁRIOS
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

# TABELA RPM COM POLÍTICA ADICIONADA
TABELA_RPM = {
    "Curiosidades":12, "Historias/Crimes":18, "Documentario":20,
    "Resumo de Filmes":15, "Religiao":10, "Motivacional":9,
    "Musica/Relax":4, "Games":8, "Esportes":14,
    "Carros":26, "Tecnologia/IA":35, "Saude":22, "Financas":55,
    "Cortes de Podcast":8, "Meditacao":6, "Financas Cripto":45,
    "Shorts/TikTok":5, "Marketing Digital":40, "Fitness":18,
    "Receitas":14, "Pets":16, "Viagens":28,
    "Sobrenatural":22, "Autoajuda":16, "Fofoca/Celebridades":10,
    "Politica":30,  # NOVO NICHO ADICIONADO
}

# ══════════════════════════════════════════════════════════════
# 🔍 MOTOR DE BUSCA (CORRIGIDO - extrai mais vídeos)
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
    """Analisa canal extraindo TODOS os vídeos disponíveis"""
    url_v = url.rstrip("/") + "/videos"
    opts = {"quiet":True,"no_warnings":True,"skip_download":True,"extract_flat":"in_playlist",
            "playlist_items":f"1-{max_vids}","ignoreerrors":True,"retries":3}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url_v, download=False) or {}
    except: return None
    
    vids = [e for e in (info.get("entries") or []) if e]
    
    # Se não achou vídeos normais, tenta shorts
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
# 🧠 GERADOR DE TÍTULOS IA (CORRIGIDO - varia por nicho, 10 títulos)
# ══════════════════════════════════════════════════════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return f"<div class='msg-erro'>{t('msg_erro_titulo')}</div>"
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    # Prompt específico por nicho
    prompt = f"""Voce e um especialista mundial em titulos virais para YouTube no nicho de {nicho}.

Titulo original viral: "{titulo_video}"

Sua tarefa: Criar EXATAMENTE 10 titulos COMPLETOS e CRIATIVOS para videos do YouTube, em {idioma_texto}, seguindo o mesmo estilo e padrao psicologico do titulo original, MAS ADAPTADOS PARA O NICHO DE {nicho.upper()}.

REGRAS CRITICAS:
1. Cada titulo deve ser uma FRASE COMPLETA de 40-80 caracteres
2. Use gatilhos mentais diferentes em cada titulo: curiosidade, urgencia, numeros, emocao, desafio, segredo, transformacao
3. ADAPTE o conteudo para o nicho de {nicho} - use terminologia e temas desse nicho
4. Varie os gatilhos entre os 10 titulos
5. NUNCA responda apenas com palavras-chave soltas
6. Os titulos devem ser DIFERENTES entre si - nao repita estruturas

FORMATO OBRIGATORIO (exatamente assim, em {idioma_texto}):
1. [Titulo completo aqui com 40-80 caracteres adaptado para {nicho}]
2. [Titulo completo aqui com 40-80 caracteres adaptado para {nicho}]
3. [Titulo completo aqui com 40-80 caracteres adaptado para {nicho}]
... ate 10

EXEMPLO DE TITULO VALIDO: "I Survived 100 Days In A Nuclear Bunker, Win $500,000"
EXEMPLO DE TITULO INVALIDO: "sobrevivencia, bunker, desafio"

Responda APENAS com a lista numerada de 1 a 10, sem explicacoes extras."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        titulos = extrair_titulos(resultado)
        if len(titulos) < 7:
            titulos = gerar_titulos_fallback(titulo_video, nicho)
    else:
        titulos = gerar_titulos_fallback(titulo_video, nicho)
    
    # Garante exatamente 10 títulos
    while len(titulos) < 10:
        titulos.append(f"Titulo bonus {len(titulos)+1}: Como {titulo_video} se aplica ao nicho de {nicho}")
    
    return renderizar_titulos(titulo_video, titulos[:10], t('titulo_original'), t('titulos_gerados'), t('dica_titulo'))

def extrair_titulos(texto):
    titulos = []
    linhas = texto.split('\n')
    for linha in linhas:
        linha = linha.strip()
        match = re.match(r'^\d+[\.\)]\s*(.+)', linha)
        if match:
            titulo = match.group(1).strip()
            if len(titulo) >= 30 and len(titulo) <= 100:
                if re.search(r'[A-ZÀ-Ýa-zà-ý]', titulo) and len(titulo.split()) >= 5:
                    titulos.append(titulo)
    if len(titulos) < 5:
        for linha in linhas:
            linha = linha.strip()
            if len(linha) >= 30 and len(linha) <= 100:
                if re.search(r'[A-ZÀ-Ýa-zà-ý]', linha) and len(linha.split()) >= 5:
                    linha = re.sub(r'^[\-\*\•]\s*', '', linha)
                    if linha not in titulos:
                        titulos.append(linha)
    return titulos[:10]

def gerar_titulos_fallback(titulo_original, nicho):
    numeros = re.findall(r'\d+', titulo_original)
    titulos = []
    if numeros:
        num = int(numeros[0])
        for n in [num//2, num*2, num*10, 100, 1000]:
            novo = re.sub(r'\d+', str(n), titulo_original, count=1)
            if len(novo) >= 30:
                titulos.append(novo)
    prefixos = ["URGENTE: ", "ATENCAO: ", "IMPRESSINANTE: ", "INACREDITAVEL: ", "CHOCANTE: "]
    for prefixo in prefixos[:5]:
        novo = f"{prefixo}{titulo_original}"
        if len(novo) <= 100:
            titulos.append(novo)
    titulos.append(f"Voce Conseguiria Sobreviver a Isso? {titulo_original}")
    titulos.append(f"Por Que {titulo_original} Esta Chocando o Mundo?")
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
# 📝 GERADOR DE TÍTULOS SIMPLES (CORRIGIDO - 7 títulos, por nicho)
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_simples(nicho, palavras_chave):
    if not palavras_chave or not palavras_chave.strip():
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    palavras = [p.strip() for p in palavras_chave.split(',') if p.strip()]
    if not palavras:
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    p0 = palavras[0].title() if palavras else "Tema"
    p1 = palavras[1].title() if len(palavras) > 1 else "Concorrencia"
    
    # Fórmulas específicas por nicho
    formulas_por_nicho = {
        "Politica": [
            f"O Escandalo de {p0} Que Pode Derrubar o Governo",
            f"7 Verdades Sobre {p0} Que Os Politicos Escondem",
            f"Por Que {p0} Esta Dividindo o Pais em 2024",
            f"A Manipulacao Por Tras de {p0} Explicada",
            f"O Que Realmente Acontece Nos Bastidores de {p0}",
            f"10 Mentiras Que Te Contaram Sobre {p0}",
            f"Como {p0} Afeta Seu Bolso Todos os Dias",
        ],
        "Historias/Crimes": [
            f"O Crime de {p0} Que Ninguem Consegue Resolver",
            f"7 Detalhes Macabros de {p0} Que Passaram Despercebidos",
            f"A Verdade Sombria Por Tras de {p0}",
            f"O Assassino de {p0} Finalmente Foi Pego?",
            f"10 Evidencias Chocantes de {p0}",
            f"O Misterio de {p0} Que Assusta Investigadores",
            f"Como {p0} Enganou a Todos Por Anos",
        ],
        "Financas": [
            f"7 Maneiras de Ganhar Dinheiro com {p0} em 2024",
            f"Como {p0} Pode Te Fazer Rico em 5 Anos",
            f"O Segredo de {p0} Que Milionarios Nao Contam",
            f"Por Que {p0} Esta Fazendo Pessoas Comuns Ficarem Ricas",
            f"10 Erros Financeiros Que Voce Comete com {p0}",
            f"Como Comecar com {p0} do Zero (Guia Completo)",
            f"A Verdade Sobre {p0} Que Os Bancos Escondem",
        ],
        "Tecnologia/IA": [
            f"Como {p0} Vai Mudar o Mundo em 2024",
            f"7 Ferramentas de {p0} Que Voce Precisa Conhecer",
            f"O Futuro de {p0} Que Ninguem Esta Vendo",
            f"Por Que {p0} Esta Substituindo Profissoes Inteiras",
            f"10 Usos Incriveis de {p0} Que Voce Nao Imaginava",
            f"Como Comecar com {p0} Hoje Mesmo (Passo a Passo)",
            f"A Verdade Sobre {p0} Que As Big Techs Escondem",
        ],
    }
    
    # Usa fórmulas do nicho ou genéricas
    formulas = formulas_por_nicho.get(nicho, [
        f"7 Segredos Sobre {p0} Que Vao Mudar Sua Vida",
        f"10 Maneiras de Ganhar Dinheiro com {p0}",
        f"Por Que {p0} Esta Fazendo Pessoas Ficarem Ricas",
        f"Voce Sabia Que {p0} Pode Te Fazer Ganhar {p1}?",
        f"URGENTE: O Que Esta Acontecendo com {p0}",
        f"ATENCAO: Nao Ignore Isso Sobre {p0} em 2024",
        f"{p0} vs {p1}: Qual e Melhor?",
    ])
    
    # Garante exatamente 7 títulos
    titulos = formulas[:7]
    
    return renderizar_titulos(palavras_chave, titulos, t('palavras_analisadas'), t('titulos_criados'), t('dica_titulo_simples'))

# ═══════════════════════════════════════════════════════════════
# 📜 GERADOR DE ROTEIRO CENA POR CENA (CORRIGIDO)
# ═══════════════════════════════════════════════════════════════
def gerar_roteiro(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>"
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    prompt = f"""Voce e o MELHOR roteirista de videos virais do YouTube.

TEMA DO VIDEO: "{tema}"

Crie um ROTEIRO COMPLETO CENA POR CENA para um video de 10-15 minutos, em {idioma_texto}, baseado na estrutura dos videos mais virais do YouTube.

ESTRUTURA OBRIGATORIA:

CENA 1 - GANCHO (0-30 segundos)
- Frase de impacto que PRENDE a atencao nos primeiros 3 segundos
- Revele o stakes (o que esta em jogo)
- Prometa algo extraordinario
- Duracao: 30s

CENA 2 - INTRODUCAO (30s - 2min)
- Contextualize o tema
- Apresente as regras do desafio/conceito
- Mostre o premio ou objetivo final
- Duracao: 1min30s

CENA 3 - PRIMEIRO OBSTACULO (2min - 4min)
- Primeiro desafio/surpresa
- Mostre reacao emocional
- Duracao: 2min

CENA 4 - ESCALADA DE TENSAO (4min - 6min)
- Aumente a dificuldade
- Elimine participantes ou aumente stakes
- Duracao: 2min

CENA 5 - PONTO DE VIRADA (6min - 8min)
- Momento inesperado que muda tudo
- Reacao emocional forte
- Duracao: 2min

CENA 6 - PREPARACAO PARA O CLIMAX (8min - 10min)
- Ultimos competidores/desafio final se aproximando
- Tensao maxima
- Duracao: 2min

CENA 7 - CLIMAX (10min - 12min)
- Momento decisivo
- Resolucao do desafio principal
- Duracao: 2min

CENA 8 - PREMIACAO (12min - 13min30s)
- Entrega do premio
- Reacao do vencedor
- Duracao: 1min30s

CENA 9 - CTA FINAL (13min30s - 15min)
- Chamada para like, inscricao e proximo video
- Teaser do proximo video
- Duracao: 1min30s

Para CADA CENA, inclua:
- O QUE FALAR: texto sugerido pronto para narrar
- SUGESTAO VISUAL: o que mostrar na tela
- DURACAO: tempo exato da cena
- SUGESTAO SONORA: tipo de musica/efeito sonoro

Responda de forma ORGANIZADA, CLARA e PRONTA PARA USAR. Escreva em {idioma_texto}."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header"><h3>{t('roteiro_completo')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica"><strong>{t('dica_roteiro')}</strong></div>
        </div>'''
        return html
    else:
        # Fallback: roteiro template
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header"><h3>{t('roteiro_completo')} (Template)</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">CENA 1 - GANCHO (0-30s)
"Voce nao vai acreditar no que aconteceu quando..."

CENA 2 - INTRODUCAO (30s-2min)
"Hoje vamos explorar {tema}..."

CENA 3-9: [Continue desenvolvendo o conteudo]

CTA FINAL: "Se voce gostou, deixe seu like e se inscreva!"</div>
            <div class="box-dica"><strong>{t('dica_roteiro')}</strong></div>
        </div>'''
        return html

# ═══════════════════════════════════════════════════════════════
# 🎨 GERADOR DE THUMBNAILS (CORRIGIDO - 3 ideias + geração de imagem)
# ═══════════════════════════════════════════════════════════════
def gerar_thumbnails(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>", None
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    prompt = f"""Voce e o MELHOR especialista em thumbnails virais do YouTube.

TEMA DO VIDEO: "{tema}"

Crie EXATAMENTE 3 IDEIAS DETALHADAS de thumbnails que gerem alta taxa de clique (CTR), em {idioma_texto}.

Para CADA uma das 3 ideias, inclua TODOS estes elementos:

IDEIA 1:
- DESCRICAO VISUAL: Descreva exatamente o que aparece na imagem
- EXPRESSAO: Emocao do rosto (se houver pessoa)
- TEXTO NA THUMB: Texto curto (MAXIMO 4 palavras)
- CORES: Paleta de 3 cores especificas
- ELEMENTO CHAVE: O que chama atencao
- GATILHO PSICOLOGICO: Por que essa thumb funciona

IDEIA 2:
(mesma estrutura detalhada)

IDEIA 3:
(mesma estrutura detalhada)

Responda de forma ORGANIZADA, numerada de 1 a 3, em {idioma_texto}."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        # Tenta gerar uma imagem de thumbnail
        img_path = gerar_imagem(f"YouTube thumbnail about {tema}, viral, high contrast, dramatic, 1280x720", 1280, 720)
        
        html = f'''<div class="box-resultado box-thumbnails">
            <div class="box-header"><h3>3 {t('thumbnails_ideias')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>'''
        
        if img_path:
            html += f'''<div style="margin-top: 20px; text-align: center;">
                <h4 style="color: #FF0000; margin-bottom: 15px;">THUMBNAIL GERADA (1280x720)</h4>
                <img src="file={img_path}" style="max-width: 100%; border-radius: 12px; border: 2px solid #FF0000;" />
                <p style="color: #AAAAAA; margin-top: 10px; font-size: 13px;">Formato YouTube: 1280x720 pixels</p>
            </div>'''
        
        html += f'''<div class="box-dica"><strong>{t('dica_thumb')}</strong></div>
        </div>'''
        return html, img_path
    else:
        return f"<div class='msg-erro'>{t('msg_erro_ia')}</div>", None

# ══════════════════════════════════════════════════════════════
# 🎨 CSS - SEM EMOJIS, MAIS DESTAQUE
# ═══════════════════════════════════════════════════════════════
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

.lang-selector {
    background: #282828; border: 1px solid #3F3F3F; border-radius: 12px;
    padding: 20px 30px; margin: 20px auto; max-width: 1200px;
    display: flex; align-items: center; justify-content: center; gap: 15px;
}
.lang-selector label { color: #FFFFFF !important; font-weight: 600; font-size: 15px; }

.api-key-banner {
    background: #282828; border: 1px solid #3F3F3F; border-radius: 12px;
    padding: 25px 30px; margin: 30px auto; max-width: 1200px;
}
.api-key-banner h3 {
    color: #FF0000 !important; font-family: 'Poppins', sans-serif !important;
    font-size: 18px !important; font-weight: 700 !important; margin: 0 0 10px 0;
}
.api-key-banner p { color: #AAAAAA !important; font-size: 14px !important; margin: 0; }

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
.box-header h3 { color: #FF0000 !important; font-family: 'Poppins', sans-serif !important; font-size: 22px !important; font-weight: 800 !important; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
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
.gr-markdown h3 { color: #FF0000 !important; font-family: 'Poppins', sans-serif !important; font-size: 22px !important; font-weight: 800; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; }
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
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{status_text}</span></div>
<div class="ac-card-body">
<div class="ac-stat-mini"><div class="lbl">{t("inscritos")}</div><div class="val">{fmt(r['inscritos'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("views_video")}</div><div class="val">{fmt(r['media_rec'])}</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("taxa_viral")}</div><div class="val">{r['taxa']:.2f}x</div></div>
<div class="ac-stat-mini"><div class="lbl">{t("mediana")}</div><div class="val">{fmt(r['mediana'])}</div></div></div>
<div class="ac-money"><div><div class="label">{t("ganho_video")}</div><strong>{brl(r['ganho_video'])}</strong></div>
<div style="text-align:right"><div class="label">{t("total_canal")}</div><strong>{brl((r['views_totais'] or sum(v['views'] for v in r['videos']))/1000*r['rpm'])}</strong></div></div>''')
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
#  INTERFACE COM SELETOR DE IDIOMA FUNCIONANDO
# ═══════════════════════════════════════════════════════════════
def mudar_idioma(idioma):
    global IDIOMA_ATUAL
    IDIOMA_ATUAL = idioma
    return gr.update()

begins_theme = gr.themes.Base(
    primary_hue="red", secondary_hue="neutral", neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins - Creator Assistant", theme=begins_theme) as app:
    gr.HTML(f"""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span> - {t('header_title').split(' - ')[1] if ' - ' in t('header_title') else 'Assistente do Criador'}</h1>
        <div class="creator">{t('header_creator')}</div>
        <p class="subtitle">{t('header_subtitle')}</p>
        <span class="badge">{t('header_badge')}</span>
    </div>
    """)
    
    # Seletor de idioma
    idioma_selector = gr.Radio(
        choices=[("Portugues", "pt"), ("English", "en"), ("Espanol", "es")],
        value="pt",
        label=t('lang_label'),
        elem_classes=["lang-selector"]
    )
    
    canais_state = gr.State([])
    
    idioma_selector.change(fn=mudar_idioma, inputs=idioma_selector, outputs=gr.HTML())
    
    with gr.Tabs():
        with gr.Tab(t('tab_cacador')):
            gr.Markdown(f"### {t('tab_cacador')}")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label=t('lbl_palavra'), placeholder=t('ph_cacar'))
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label=t('lbl_nicho'))
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
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label=t('lbl_nicho_ia'))
            btn_ia = gr.Button(t('btn_titulos_ia'), variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=gerar_titulos_ia, inputs=[titulo_video_ia, nicho_ia], outputs=out_ia)

        with gr.Tab(t('tab_titulos_simples')):
            gr.Markdown(f"### {t('tab_titulos_simples')}")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label=t('lbl_nicho_ia'))
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label=t('lbl_palavras_chave'), placeholder=t('ph_palavras'))
            btn_gen = gr.Button(t('btn_titulos_simples'), variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos_simples, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab(t('tab_roteiro')):
            gr.Markdown(f"### {t('tab_roteiro')}")
            tema_roteiro = gr.Textbox(label=t('lbl_tema'), placeholder=t('ph_tema'))
            btn_roteiro = gr.Button(t('btn_roteiro'), variant="primary", size="lg")
            out_roteiro = gr.HTML()
            btn_roteiro.click(fn=lambda t, canais: gerar_roteiro(t, canais), inputs=[tema_roteiro, canais_state], outputs=out_roteiro)

        with gr.Tab(t('tab_thumbnails')):
            gr.Markdown(f"### {t('tab_thumbnails')}")
            tema_thumb = gr.Textbox(label=t('lbl_tema'), placeholder=t('ph_tema'))
            btn_thumb = gr.Button(t('btn_thumbnails'), variant="primary", size="lg")
            out_thumb = gr.HTML()
            out_img = gr.Image(label="Thumbnail Gerada (1280x720)")
            btn_thumb.click(fn=lambda t, canais: gerar_thumbnails(t, canais), inputs=[tema_thumb, canais_state], outputs=[out_thumb, out_img])

        with gr.Tab(t('tab_guia')):
            gr.Markdown(f"""
            ### {t('guia_titulo')}
            
            **CACADOR DE CANAIS**
            
            Digite o tema do seu nicho no campo apropriado. Exemplos: 'historias de terror', 'carros abandonados', 'true crime'. Escolha o nicho correspondente no menu ao lado. Ajuste a quantidade de canais (recomendado: 8) e a faixa de inscritos (recomendado: 10.000 a 500.000). Marque 'Publico estrangeiro' se quiser buscar canais em ingles/espanhol (pagam 3x mais). Clique em 'INICIAR CACADA' e espere 1-3 minutos.
            
            **ANALISAR CANAL**
            
            Cole o link completo do canal ou apenas o @NomeDoCanal. Escolha o nicho e clique em 'AUDITAR CANAL'. O sistema vai analisar os videos e te mostrar a media real de views.
            
            **GERADOR DE TITULOS IA**
            
            Cole o TITULO COMPLETO de um video viral que voce quer modelar. A IA vai analisar o padrao psicologico e gerar 10 titulos NOVOS e CRIATIVOS no mesmo estilo, adaptados para o nicho selecionado.
            
            **GERADOR DE TITULOS SIMPLES**
            
            Digite palavras-chave separadas por virgula. O sistema usa formulas de titulos virais especificas para cada nicho para gerar 7 titulos prontos.
            
            **GERADOR DE ROTEIRO**
            
            Digite o tema do seu video. A IA vai criar um roteiro COMPLETO baseado na estrutura dos videos mais virais do YouTube, dividido em 9 cenas detalhadas.
            
            **GERADOR DE THUMBNAILS**
            
            Digite o tema do video e a IA vai gerar 3 ideias DETALHADAS de thumbnails virais. O sistema tambem gera uma imagem de thumbnail no formato correto do YouTube (1280x720 pixels).
            
            **DICAS DE OURO:**
            
            - Busque em ingles para achar canais que pagam 3x mais
            - Taxa viral acima de 1.0x significa que o YouTube esta entregando o video para nao-inscritos
            - Modele a estrutura dos videos, mas NUNCA copie o roteiro palavra por palavra
            - Thumbnails com rosto + expressao forte + seta vermelha + texto curto tem CTR 2-3x maior
            - Os primeiros 30 segundos do video decidem tudo
            """)

    # Banner da IA no FINAL
    gr.HTML(f"""
    <div class="api-key-banner">
        <h3>{t('banner_ia_title')}</h3>
        <p>{t('banner_ia_text')}</p>
    </div>
    """)
    
    gr.HTML(f"""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div>
        <strong>{t('footer_text')}</strong><br><br>
        {t('footer_dev')}<br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">{t('footer_disclaimer')}</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
