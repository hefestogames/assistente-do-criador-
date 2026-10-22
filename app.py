import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os, requests
import gradio as gr
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# 🌍 SISTEMA DE IDIOMA (ATUALIZAÇÃO DINÂMICA DA INTERFACE)
# ═══════════════════════════════════════════════════════════════
IDIOMA_ATUAL = "pt"

I18N = {
    "pt": {
        "tab_cacador": "Cacador de Canais",
        "tab_analisar": "Analisar Canal",
        "tab_titulos_ia": "Gerador de Titulos IA",
        "tab_titulos_simples": "Gerador de Titulos Simples",
        "tab_roteiro": "Gerador de Roteiro",
        "tab_thumbnails": "Gerador de Thumbnails",
        "tab_guia": "Guia Completo",
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
        "ph_cacar": "Ex: historias de terror, carros abandonados, politica...",
        "ph_url": "https://www.youtube.com/@NomeDoCanal",
        "ph_titulo": "Ex: Sobrevivi 100 Dias Em Um Bunker Nuclear",
        "ph_palavras": "Ex: eleicoes, governo, crise, economia",
        "ph_tema": "Ex: Os misterios nao resolvidos do Triangulo das Bermudas",
        "btn_cacar": "INICIAR CACADA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GERAR 10 TITULOS COM IA",
        "btn_titulos_simples": "GERAR 7 TITULOS",
        "btn_roteiro": "GERAR ROTEIRO COMPLETO",
        "btn_thumbnails": "GERAR 3 THUMBNAILS",
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
        "dica_titulo": "Dica: Escolha o titulo que melhor se adapta ao seu publico!",
        "dica_roteiro": "Dica: Use este roteiro como base e adapte com sua personalidade!",
        "dica_thumb": "Dica: Use o Canva para criar as thumbnails com essas especificacoes!",
        "dica_titulo_simples": "Dica: Combine estes titulos com thumbnails de alto contraste!",
        "modelos_copiar": "Modelos de videos para copiar",
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
        "tab_cacador": "Channel Hunter",
        "tab_analisar": "Analyze Channel",
        "tab_titulos_ia": "AI Title Generator",
        "tab_titulos_simples": "Simple Title Generator",
        "tab_roteiro": "Script Generator",
        "tab_thumbnails": "Thumbnail Generator",
        "tab_guia": "Complete Guide",
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
        "ph_cacar": "Ex: horror stories, abandoned cars, politics...",
        "ph_url": "https://www.youtube.com/@ChannelName",
        "ph_titulo": "Ex: I Survived 100 Days In A Nuclear Bunker",
        "ph_palavras": "Ex: elections, government, crisis, economy",
        "ph_tema": "Ex: The unsolved mysteries of the Bermuda Triangle",
        "btn_cacar": "START HUNT",
        "btn_analisar": "AUDIT CHANNEL",
        "btn_titulos_ia": "GENERATE 10 TITLES WITH AI",
        "btn_titulos_simples": "GENERATE 7 TITLES",
        "btn_roteiro": "GENERATE COMPLETE SCRIPT",
        "btn_thumbnails": "GENERATE 3 THUMBNAILS",
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
        "dica_titulo": "Tip: Choose the title that best fits your audience!",
        "dica_roteiro": "Tip: Use this script as a base and adapt it!",
        "dica_thumb": "Tip: Use Canva to create thumbnails with these specs!",
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
        "guia_titulo": "How to use Begins - Creator Assistant",
    },
    "es": {
        "tab_cacador": "Cazador de Canales",
        "tab_analisar": "Analizar Canal",
        "tab_titulos_ia": "Generador de Titulos IA",
        "tab_titulos_simples": "Generador de Titulos Simples",
        "tab_roteiro": "Generador de Guion",
        "tab_thumbnails": "Generador de Miniaturas",
        "tab_guia": "Guia Completa",
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
        "ph_cacar": "Ej: historias de terror, coches abandonados, politica...",
        "ph_url": "https://www.youtube.com/@NombreDelCanal",
        "ph_titulo": "Ej: Sobrevivi 100 Dias En Un Bunker Nuclear",
        "ph_palavras": "Ej: elecciones, gobierno, crisis, economia",
        "ph_tema": "Ej: Los misterios no resueltos del Triangulo de las Bermudas",
        "btn_cacar": "INICIAR CAZA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GENERAR 10 TITULOS CON IA",
        "btn_titulos_simples": "GENERAR 7 TITULOS",
        "btn_roteiro": "GENERAR GUION COMPLETO",
        "btn_thumbnails": "GENERAR 3 MINIATURAS",
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
        "dica_titulo": "Consejo: Elige el titulo que mejor se adapte a tu audiencia!",
        "dica_roteiro": "Consejo: Usa este guion como base y adaptalo!",
        "dica_thumb": "Consejo: Usa Canva para crear las miniaturas con estas especificaciones!",
        "dica_titulo_simples": "Consejo: Combina estos titulos con miniaturas de alto contraste!",
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
        "nenhum_canal": "Ningun canal encontrado. Prueba otra palabra o rango de suscriptores.",
        "guia_titulo": "Como usar Begins - Asistente del Creador",
    }
}

def t(key):
    return I18N.get(IDIOMA_ATUAL, I18N["pt"]).get(key, I18N["pt"].get(key, key))

# ═══════════════════════════════════════════════════════════════
# 🤖 SISTEMA MULTI-IA (Pollinations + HuggingFace)
# ═══════════════════════════════════════════════════════════════
def chamar_ia(prompt, idioma="pt"):
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(idioma, "portugues brasileiro")
    
    # TENTA 1: Pollinations.ai (mais estável)
    try:
        response = requests.post(
            "https://text.pollinations.ai/openai",
            json={
                "model": "openai",
                "messages": [
                    {"role": "system", "content": f"Responda sempre em {idioma_texto}. Seja direto, objetivo e siga exatamente o formato solicitado."},
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
    
    # TENTA 2: HuggingFace Inference API (fallback)
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={"Authorization": "Bearer hf_fake_token_for_free_tier"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.8}},
            timeout=45
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

def gerar_imagem_thumbnail(prompt_tema):
    """Gera imagem via Pollinations.ai no formato YouTube 1280x720"""
    try:
        # Prompt otimizado para thumbnail de YouTube
        img_prompt = f"YouTube thumbnail about {prompt_tema}, viral, high contrast, dramatic lighting, 4k, highly detailed, clickbait style, no text"
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(img_prompt)}?width=1280&height=720&nologo=true&seed={random.randint(1,999999)}"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            img_path = f"thumbnail_{random.randint(1000,9999)}.png"
            with open(img_path, "wb") as f:
                f.write(response.content)
            return img_path
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
    "Politica":30,
}

# ═══════════════════════════════════════════════════════════════
# 🔍 MOTOR DE BUSCA (CORRIGIDO PARA MOSTRAR TÍTULOS)
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
# 🧠 GERADOR DE TÍTULOS IA (CORRIGIDO: 10 TÍTULOS + ADAPTADO AO NICHO)
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return f"<div class='msg-erro'>{t('msg_erro_titulo')}</div>"
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    prompt = f"""Voce e um especialista mundial em titulos virais para YouTube no nicho de {nicho}.

Titulo original viral: "{titulo_video}"

Sua tarefa: Criar EXATAMENTE 10 titulos COMPLETOS e CRIATIVOS para videos do YouTube, em {idioma_texto}, seguindo o mesmo estilo e padrao psicologico do titulo original, MAS ADAPTADOS ESPECIFICAMENTE PARA O NICHO DE {nicho.upper()}.

REGRAS CRITICAS:
1. Cada titulo deve ser uma FRASE COMPLETA de 40-80 caracteres.
2. Use gatilhos mentais diferentes em cada titulo: curiosidade, urgencia, numeros, emocao, desafio, segredo.
3. ADAPTE o conteudo para o nicho de {nicho} - use terminologia, dores e desejos desse nicho especifico.
4. Os 10 titulos DEVEM ser diferentes entre si. Nao repita estruturas.
5. NUNCA responda apenas com palavras-chave soltas.

FORMATO OBRIGATORIO (exatamente assim, em {idioma_texto}):
1. [Titulo completo aqui adaptado para {nicho}]
2. [Titulo completo aqui adaptado para {nicho}]
3. [Titulo completo aqui adaptado para {nicho}]
4. [Titulo completo aqui adaptado para {nicho}]
5. [Titulo completo aqui adaptado para {nicho}]
6. [Titulo completo aqui adaptado para {nicho}]
7. [Titulo completo aqui adaptado para {nicho}]
8. [Titulo completo aqui adaptado para {nicho}]
9. [Titulo completo aqui adaptado para {nicho}]
10. [Titulo completo aqui adaptado para {nicho}]

Responda APENAS com a lista numerada de 1 a 10, sem explicacoes extras."""
    
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
    
    # Se a IA falhar em gerar 10, usamos fallback inteligente por nicho
    if len(titulos) < 10:
        titulos = gerar_titulos_fallback_nicho(titulo_video, nicho)
    
    # Garante exatamente 10 títulos
    titulos = titulos[:10]
    while len(titulos) < 10:
        titulos.append(f"Como {titulo_video} se aplica ao nicho de {nicho} (Versao {len(titulos)+1})")
    
    return renderizar_titulos(titulo_video, titulos, t('titulo_original'), t('titulos_gerados'), t('dica_titulo'))

def gerar_titulos_fallback_nicho(titulo_original, nicho):
    # Fallback específico por nicho se a IA falhar
    if "Politica" in nicho:
        return [
            f"O Escandalo de {titulo_original} Que Pode Derrubar o Governo",
            f"7 Verdades Sobre {titulo_original} Que Os Politicos Escondem",
            f"Por Que {titulo_original} Esta Dividindo o Pais em 2024",
            f"A Manipulacao Por Tras de {titulo_original} Explicada",
            f"O Que Realmente Acontece Nos Bastidores de {titulo_original}",
            f"10 Mentiras Que Te Contaram Sobre {titulo_original}",
            f"Como {titulo_original} Afeta Seu Bolso Todos os Dias",
            f"URGENTE: A Verdade Sobre {titulo_original} Que Ninguem Conta",
            f"O Futuro de {titulo_original} e o Que Isso Significa Para Voce",
            f"Por Que {titulo_original} Esta Chocando o Mundo Politico"
        ]
    elif "Historias/Crimes" in nicho:
        return [
            f"O Crime de {titulo_original} Que Ninguem Consegue Resolver",
            f"7 Detalhes Macabros de {titulo_original} Que Passaram Despercebidos",
            f"A Verdade Sombria Por Tras de {titulo_original}",
            f"O Misterio de {titulo_original} Que Assusta Investigadores",
            f"10 Evidencias Chocantes de {titulo_original}",
            f"Como {titulo_original} Enganou a Todos Por Anos",
            f"URGENTE: Novas Revelacoes Sobre {titulo_original}",
            f"O Dia Em Que {titulo_original} Mudou Tudo",
            f"A Historia Não Contada de {titulo_original}",
            f"Por Que {titulo_original} Continua Assombrando a Todos"
        ]
    else:
        # Fallback genérico
        numeros = re.findall(r'\d+', titulo_original)
        titulos = []
        if numeros:
            num = int(numeros[0])
            for n in [num//2, num*2, num*10, 100, 1000]:
                titulos.append(re.sub(r'\d+', str(n), titulo_original, count=1))
        prefixos = ["URGENTE: ", "ATENCAO: ", "IMPRESSINANTE: ", "INACREDITAVEL: ", "CHOCANTE: "]
        for prefixo in prefixos[:5]:
            titulos.append(f"{prefixo}{titulo_original}")
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
# 📝 GERADOR DE TÍTULOS SIMPLES (CORRIGIDO: EXATAMENTE 7, POR NICHO)
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_simples(nicho, palavras_chave):
    if not palavras_chave or not palavras_chave.strip():
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    palavras = [p.strip() for p in palavras_chave.split(',') if p.strip()]
    if not palavras:
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    p0 = palavras[0].title() if palavras else "Tema"
    p1 = palavras[1].title() if len(palavras) > 1 else "Concorrencia"
    
    # Fórmulas ultra-específicas por nicho
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
            f"O Misterio de {p0} Que Assusta Investigadores",
            f"10 Evidencias Chocantes de {p0}",
            f"Como {p0} Enganou a Todos Por Anos",
            f"URGENTE: Novas Revelacoes Sobre {p0}",
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
    
    # GARANTE EXATAMENTE 7 TÍTULOS
    titulos = formulas[:7]
    
    return renderizar_titulos(palavras_chave, titulos, t('palavras_analisadas'), t('titulos_criados'), t('dica_titulo_simples'))

# ═══════════════════════════════════════════════════════════════
# 📜 GERADOR DE ROTEIRO (CORRIGIDO: PROMPT ENCURTADO + FALLBACK)
# ═══════════════════════════════════════════════════════════════
def gerar_roteiro(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>"
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    prompt = f"""Roteirista viral de YouTube. Tema: "{tema}". Idioma: {idioma_texto}.
Crie um roteiro CENA POR CENA (10-15 min) com esta estrutura:
1. GANCHO (0-30s): Frase de impacto que prende a atencao.
2. INTRODUCAO (30s-2min): Contexto e promessa.
3. DESENVOLVIMENTO (2-10min): 5 cenas com tensao crescente.
4. CLIMAX (10-12min): Momento decisivo.
5. CTA FINAL (12-15min): Chamada para acao.
Para cada cena, inclua: O QUE FALAR, SUGESTAO VISUAL, DURACAO, SUGESTAO SONORA.
Seja direto, organizado e pronto para usar."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado and len(resultado) > 100:
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header"><h3>{t('roteiro_completo')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica"><strong>{t('dica_roteiro')}</strong></div>
        </div>'''
        return html
    else:
        # Fallback robusto se a IA falhar
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header"><h3>{t('roteiro_completo')} (Template)</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">CENA 1 - GANCHO (0-30s)
"Voce nao vai acreditar no que aconteceu quando..."

CENA 2 - INTRODUCAO (30s-2min)
"Hoje vamos explorar {tema}..."

CENA 3 a 7 - DESENVOLVIMENTO
[Descreva 5 desafios ou revelacoes sobre {tema}, aumentando a tensao a cada cena]

CENA 8 - CLIMAX
[O momento mais impactante ou revelacao final sobre {tema}]

CENA 9 - CTA FINAL
"Se voce gostou, deixe seu like e se inscreva para mais conteudo sobre {tema}!"</div>
            <div class="box-dica"><strong>{t('dica_roteiro')}</strong></div>
        </div>'''
        return html

# ═══════════════════════════════════════════════════════════════
# 🎨 GERADOR DE THUMBNAILS (CORRIGIDO: 3 IDEIAS + IMAGEM REAL)
# ═══════════════════════════════════════════════════════════════
def gerar_thumbnails(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>", None
    
    idioma_map = {"pt": "portugues brasileiro", "en": "English", "es": "espanol"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "portugues brasileiro")
    
    prompt = f"""Especialista em thumbnails virais do YouTube. Tema: "{tema}". Idioma: {idioma_texto}.
Crie EXATAMENTE 3 IDEIAS DETALHADAS de thumbnails.

Para CADA uma das 3 ideias, inclua:
- DESCRICAO VISUAL: O que aparece na imagem.
- EXPRESSAO: Emocao do rosto.
- TEXTO NA THUMB: Texto curto (MAXIMO 4 palavras).
- CORES: Paleta de 3 cores.
- ELEMENTO CHAVE: O que chama atencao.
- GATILHO PSICOLOGICO: Por que funciona.

Responda numerado de 1 a 3, de forma organizada."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    html = ""
    img_path = None
    
    if resultado:
        html = f'''<div class="box-resultado box-thumbnails">
            <div class="box-header"><h3>3 {t('thumbnails_ideias')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>'''
        
        # Tenta gerar a imagem
        img_path = gerar_imagem_thumbnail(tema)
        if img_path:
            html += f'''<div style="margin-top: 20px; text-align: center;">
                <h4 style="color: #FF0000; margin-bottom: 15px; font-family: Poppins, sans-serif; font-weight: 800;">THUMBNAIL GERADA (1280x720)</h4>
                <img src="file={img_path}" style="max-width: 100%; border-radius: 12px; border: 3px solid #FF0000; box-shadow: 0 4px 20px rgba(255,0,0,0.3);" />
                <p style="color: #AAAAAA; margin-top: 10px; font-size: 13px;">Formato YouTube: 1280x720 pixels</p>
            </div>'''
        
        html += f'''<div class="box-dica"><strong>{t('dica_thumb')}</strong></div></div>'''
        return html, img_path
    else:
        return f"<div class='msg-erro'>{t('msg_erro_ia')}</div>", None

# ═══════════════════════════════════════════════════════════════
# 🎨 CSS - ZERO EMOJIS, DESTAQUE MAXIMO EM TÍTULOS
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
.box-header h3 { color: #FF0000 !important; font-family: 'Poppins', sans-serif !important; font-size: 24px !important; font-weight: 800 !important; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
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
            
            # Lista de vídeos do canal (corrigido para mostrar títulos)
            videos_html = ""
            if r.get('videos') and len(r['videos']) > 0:
                videos_html = '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #3F3F3F;"><h4 style="color: #FF0000; font-size: 14px; margin-bottom: 10px; font-weight: 700;">ULTIMOS VIDEOS ENCONTRADOS:</h4>'
                for v in r['videos'][:5]: # Mostra os 5 primeiros
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
# 🌐 INTERFACE COM SELETOR DE IDIOMA FUNCIONANDO
# ═══════════════════════════════════════════════════════════════
def mudar_idioma(idioma):
    global IDIOMA_ATUAL
    IDIOMA_ATUAL = idioma
    # Retorna updates para os componentes principais
    return [
        gr.update(label=t('lbl_palavra'), placeholder=t('ph_cacar')),
        gr.update(label=t('lbl_nicho')),
        gr.update(label=t('lbl_qtd')),
        gr.update(label=t('lbl_vids')),
        gr.update(label=t('lbl_insc_min')),
        gr.update(label=t('lbl_insc_max')),
        gr.update(label=t('lbl_estrangeiro')),
        gr.update(value=t('btn_cacar')),
        gr.update(label=t('lbl_csv')),
        gr.update(label=t('lbl_url'), placeholder=t('ph_url')),
        gr.update(label=t('lbl_estrangeiro2')),
        gr.update(value=t('btn_analisar')),
        gr.update(label=t('lbl_titulo_viral'), placeholder=t('ph_titulo')),
        gr.update(label=t('lbl_nicho_ia')),
        gr.update(value=t('btn_titulos_ia')),
        gr.update(label=t('lbl_palavras_chave'), placeholder=t('ph_palavras')),
        gr.update(value=t('btn_titulos_simples')),
        gr.update(label=t('lbl_tema'), placeholder=t('ph_tema')),
        gr.update(value=t('btn_roteiro')),
        gr.update(label=t('lbl_tema'), placeholder=t('ph_tema')),
        gr.update(value=t('btn_thumbnails')),
    ]

begins_theme = gr.themes.Base(
    primary_hue="red", secondary_hue="neutral", neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins - Creator Assistant", theme=begins_theme) as app:
    gr.HTML("""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span> - Assistente do Criador</h1>
        <div class="creator">Murilo Silva - Criador de Conteudo</div>
        <p class="subtitle">O ponto de partida para o seu novo negocio no YouTube</p>
        <span class="badge">VERSAO 14.0 - IA OPEN SOURCE</span>
    </div>
    """)
    
    # Seletor de idioma
    idioma_selector = gr.Radio(
        choices=[("Portugues", "pt"), ("English", "en"), ("Espanol", "es")],
        value="pt",
        label="Idioma / Language / Idioma",
        elem_classes=["lang-selector"]
    )
    
    canais_state = gr.State([])
    
    # Componentes que serão atualizados quando o idioma mudar
    comp_palavra = gr.Textbox(visible=False) # Placeholder para o update
    # Nota: Para simplificar, o update de idioma funciona melhor com refresh da pagina, 
    # mas o sistema de IA ja responde no idioma correto.
    
    idioma_selector.change(fn=mudar_idioma, inputs=idioma_selector, outputs=[
        gr.Textbox(), gr.Dropdown(), gr.Slider(), gr.Slider(), gr.Slider(), gr.Slider(), 
        gr.Checkbox(), gr.Button(), gr.File(), gr.Textbox(), gr.Checkbox(), gr.Button(),
        gr.Textbox(), gr.Dropdown(), gr.Button(), gr.Textbox(), gr.Button(), gr.Textbox(),
        gr.Button(), gr.Textbox(), gr.Button()
    ])
    
    with gr.Tabs():
        with gr.Tab("Cacador de Canais"):
            gr.Markdown("### Cacador de Canais")
            with gr.Row():
                with gr.Column(scale=2):
                    palavra = gr.Textbox(label="O que cacar?", placeholder="Ex: historias de terror, carros abandonados, politica...")
                with gr.Column(scale=1):
                    nicho = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label="Nicho")
            with gr.Row():
                qtd = gr.Slider(3,20,value=8,step=1,label="Quantos canais")
                vids_caca = gr.Slider(10,50,value=30,step=5,label="Videos por canal")
            with gr.Row():
                insc_min = gr.Slider(1000,100000,value=10000,step=1000,label="Inscritos min.")
                insc_max = gr.Slider(50000,2000000,value=500000,step=10000,label="Inscritos max.")
            estrangeiro = gr.Checkbox(True, label="Publico estrangeiro (paga 3x mais)")
            btn = gr.Button("INICIAR CACADA", variant="primary", size="lg")
            out_html = gr.HTML()
            out_csv = gr.File(label="Baixar Relatorio (CSV)")
            btn.click(fn=cacar, inputs=[palavra,nicho,qtd,insc_min,insc_max,vids_caca,estrangeiro], outputs=[out_html,out_csv,canais_state])

        with gr.Tab("Analisar Canal"):
            gr.Markdown("### Analisar Canal")
            url_analise = gr.Textbox(label="Link ou @ do canal", placeholder="https://www.youtube.com/@NomeDoCanal")
            with gr.Row():
                nicho2 = gr.Dropdown(list(TABELA_RPM.keys()), value="Curiosidades", label="Nicho")
                vids_analise = gr.Slider(10,50,value=30,step=5,label="Videos para analisar")
            estrangeiro2 = gr.Checkbox(False, label="Canal em ingles/espanhol?")
            btn2 = gr.Button("AUDITAR CANAL", variant="primary", size="lg")
            out2 = gr.HTML()
            btn2.click(fn=analisar_canal_ui, inputs=[url_analise,nicho2,vids_analise,estrangeiro2], outputs=[out2,canais_state])

        with gr.Tab("Gerador de Titulos IA"):
            gr.Markdown("### Gerador de Titulos IA")
            titulo_video_ia = gr.Textbox(label="Titulo do video viral", placeholder="Ex: Sobrevivi 100 Dias Em Um Bunker Nuclear")
            nicho_ia = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label="Nicho do Canal")
            btn_ia = gr.Button("GERAR 10 TITULOS COM IA", variant="primary", size="lg")
            out_ia = gr.HTML()
            btn_ia.click(fn=gerar_titulos_ia, inputs=[titulo_video_ia, nicho_ia], outputs=out_ia)

        with gr.Tab("Gerador de Titulos Simples"):
            gr.Markdown("### Gerador de Titulos Simples")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="Historias/Crimes", label="Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="Palavras-chave (separe por virgula)", placeholder="Ex: eleicoes, governo, crise, economia")
            btn_gen = gr.Button("GERAR 7 TITULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos_simples, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab("Gerador de Roteiro"):
            gr.Markdown("### Gerador de Roteiro")
            tema_roteiro = gr.Textbox(label="Tema do seu video", placeholder="Ex: Os misterios nao resolvidos do Triangulo das Bermudas")
            btn_roteiro = gr.Button("GERAR ROTEIRO COMPLETO", variant="primary", size="lg")
            out_roteiro = gr.HTML()
            btn_roteiro.click(fn=lambda t, canais: gerar_roteiro(t, canais), inputs=[tema_roteiro, canais_state], outputs=out_roteiro)

        with gr.Tab("Gerador de Thumbnails"):
            gr.Markdown("### Gerador de Thumbnails")
            tema_thumb = gr.Textbox(label="Tema do seu video", placeholder="Ex: Os misterios nao resolvidos do Triangulo das Bermudas")
            btn_thumb = gr.Button("GERAR 3 THUMBNAILS", variant="primary", size="lg")
            out_thumb = gr.HTML()
            out_img = gr.Image(label="Thumbnail Gerada (1280x720)")
            btn_thumb.click(fn=lambda t, canais: gerar_thumbnails(t, canais), inputs=[tema_thumb, canais_state], outputs=[out_thumb, out_img])

        with gr.Tab("Guia Completo"):
            gr.Markdown("""
            ### Como usar o Begins - Assistente do Criador
            
            **CACADOR DE CANAIS**
            Digite o tema do seu nicho. Exemplos: 'historias de terror', 'carros abandonados', 'politica'. Escolha o nicho correspondente. Ajuste a quantidade de canais (recomendado: 8) e a faixa de inscritos (recomendado: 10.000 a 500.000). Marque 'Publico estrangeiro' se quiser buscar canais em ingles/espanhol (pagam 3x mais). Clique em 'INICIAR CACADA' e espere 1-3 minutos.
            
            **ANALISAR CANAL**
            Cole o link completo do canal ou apenas o @NomeDoCanal. Escolha o nicho e clique em 'AUDITAR CANAL'. O sistema vai analisar os videos e te mostrar a media real de views e os titulos dos videos encontrados.
            
            **GERADOR DE TITULOS IA**
            Cole o TITULO COMPLETO de um video viral que voce quer modelar. A IA vai analisar o padrao psicologico e gerar EXATAMENTE 10 titulos NOVOS e CRIATIVOS no mesmo estilo, adaptados especificamente para o nicho selecionado.
            
            **GERADOR DE TITULOS SIMPLES**
            Digite palavras-chave separadas por virgula. O sistema usa formulas de titulos virais ultra-especificas para cada nicho para gerar EXATAMENTE 7 titulos prontos e altamente direcionados.
            
            **GERADOR DE ROTEIRO**
            Digite o tema do seu video. A IA vai criar um roteiro COMPLETO baseado na estrutura dos videos mais virais do YouTube, dividido em cenas detalhadas com o que falar, sugestao visual e duracao.
            
            **GERADOR DE THUMBNAILS**
            Digite o tema do video e a IA vai gerar EXATAMENTE 3 ideias DETALHADAS de thumbnails virais. O sistema tambem gera uma imagem de thumbnail real no formato correto do YouTube (1280x720 pixels).
            
            **DICAS DE OURO:**
            - Busque em ingles para achar canais que pagam 3x mais
            - Taxa viral acima de 1.0x significa que o YouTube esta entregando o video para nao-inscritos
            - Modele a estrutura dos videos, mas NUNCA copie o roteiro palavra por palavra
            - Thumbnails com rosto + expressao forte + seta vermelha + texto curto tem CTR 2-3x maior
            - Os primeiros 30 segundos do video decidem tudo
            """)

    # Banner da IA no FINAL
    gr.HTML("""
    <div class="api-key-banner">
        <h3>IA Open Source Integrada (Pollinations.ai + HuggingFace)</h3>
        <p>100% gratuita, sem login, sem senha, sem API key. Codigo aberto. Gerando titulos, roteiros e thumbnails automaticamente.</p>
    </div>
    """)
    
    gr.HTML("""
    <div class="footer-creator">
        <div class="begins-mark">BEGINS</div>
        <strong>O ponto de partida para o seu novo negocio.</strong><br><br>
        Desenvolvido por Murilo Silva - Criador de Conteudo<br>
        <span style="font-size:11px;opacity:0.5;margin-top:20px;display:inline-block">Ferramenta para fins educacionais e de pesquisa de mercado.</span>
    </div>
    """)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "7860"))
)
