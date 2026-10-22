import yt_dlp, re, statistics, csv, datetime, warnings, time, random, os, requests
import gradio as gr
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# 🌍 SISTEMA DE INTERNACIONALIZAÇÃO (PT / EN / ES)
# ══════════════════════════════════════════════════════════════
IDIOMA_ATUAL = "pt"

I18N = {
    "pt": {
        "header_title": "BEGINS · Assistente do Criador",
        "header_creator": "Murilo Silva · Criador de Conteúdo",
        "header_subtitle": "O ponto de partida para o seu novo negócio no YouTube",
        "header_badge": "VERSÃO 12.0 · IA OPEN SOURCE",
        "tab_cacador": "🕵️ Caçador de Canais",
        "tab_analisar": "🔎 Analisar Canal",
        "tab_titulos_ia": " Gerador de Títulos IA",
        "tab_titulos_simples": "📝 Gerador de Títulos Simples",
        "tab_roteiro": "📜 Gerador de Roteiro",
        "tab_thumbnails": " Gerador de Thumbnails",
        "tab_guia": "💡 Guia Completo",
        "footer_text": "O ponto de partida para o seu novo negócio.",
        "footer_dev": "Desenvolvido por Murilo Silva · Criador de Conteúdo",
        "footer_disclaimer": "Ferramenta para fins educacionais e de pesquisa de mercado.",
        "lang_label": " Idioma",
        "lang_pt": "Português",
        "lang_en": "English",
        "lang_es": "Español",
        "banner_ia_title": "🤖 IA Open Source Integrada (Pollinations.ai)",
        "banner_ia_text": "100% gratuita, sem login, sem senha, sem API key. Código aberto. Gerando títulos, roteiros e thumbnails automaticamente.",
        "btn_cacar": "INICIAR CAÇADA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GERAR 10 TÍTULOS COM IA",
        "btn_titulos_simples": "GERAR 7 TÍTULOS",
        "btn_roteiro": "GERAR ROTEIRO COMPLETO",
        "btn_thumbnails": "GERAR 3 THUMBNAILS",
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
        "lbl_tema": "Tema do seu vídeo",
        "ph_cacar": "Ex: histórias de terror, carros abandonados, true crime...",
        "ph_url": "https://www.youtube.com/@NomeDoCanal",
        "ph_titulo": "Ex: I Survived 100 Days In Nuclear Bunker, Win $500,000",
        "ph_palavras": "Ex: cachorro, dinheiro, trabalho, gratis",
        "ph_tema": "Ex: Os mistérios não resolvidos do Triângulo das Bermudas",
        "lbl_csv": "Baixar Relatório (CSV)",
        "msg_erro_vazio": "⚠️ Digite o que você quer caçar!",
        "msg_erro_nada": " Nada encontrado. Tente outra palavra.",
        "msg_erro_url": "⚠️ Cole o link do canal!",
        "msg_erro_canal": "❌ Canal não encontrado. Verifique o link.",
        "msg_erro_titulo": "⚠️ Digite o título de um vídeo viral!",
        "msg_erro_tema": "️ Digite o tema do seu vídeo!",
        "msg_erro_palavras": "️ Digite palavras-chave válidas separadas por vírgula!",
        "msg_erro_ia": "❌ Erro ao gerar conteúdo. Tente novamente.",
        "titulo_original": "TÍTULO ORIGINAL ANALISADO",
        "titulos_gerados": "TÍTULOS GERADOS PELA IA",
        "palavras_analisadas": "PALAVRAS-CHAVE ANALISADAS",
        "titulos_criados": "TÍTULOS CRIADOS",
        "roteiro_completo": "ROTEIRO COMPLETO",
        "thumbnails_ideias": "IDEIAS DE THUMBNAILS",
        "dica_titulo": "💎 Dica: Escolha o título que melhor se adapta ao seu público e combine com uma thumbnail impactante!",
        "dica_roteiro": "💡 Dica: Use este roteiro como base e adapte com sua personalidade!",
        "dica_thumb": "💡 Dica: Use o Canva (grátis) para criar as thumbnails com essas especificações!",
        "dica_titulo_simples": "💎 Dica: Combine estes títulos com thumbnails de alto contraste para maximizar o CTR!",
        "modelos_copiar": "🧬 Modelos para copiar",
        "abrir_youtube": "🔗 Abrir canal no YouTube →",
        "ganho_video": "GANHO POR VÍDEO",
        "total_canal": "TOTAL DO CANAL",
        "inscritos": "👥 Inscritos",
        "views_video": "📈 Views/vídeo",
        "taxa_viral": " Taxa viral",
        "mediana": "📊 Mediana",
        "estourando": "ESTOURANDO",
        "saudavel": "Saudável",
        "estagnado": "Estagnado",
        "canais": "Canais",
        "estourando_label": "Estourando",
        "ganho_medio": "Ganho médio/vídeo",
        "nenhum_canal": " Nenhum canal encontrado. Tente outra palavra ou faixa de inscritos.",
        "guia_titulo": "Como usar o Begins · Assistente do Criador",
        "guia_passo1_titulo": "1. 🕵️ Caçador de Canais",
        "guia_passo1_texto": "Digite o tema do seu nicho no campo 'O que caçar?'. Exemplos: 'histórias de terror', 'carros abandonados', 'true crime'. Escolha o nicho correspondente no menu ao lado (isso define quanto o YouTube paga por 1.000 views). Ajuste a quantidade de canais (recomendado: 8) e a faixa de inscritos (recomendado: 10.000 a 500.000 para achar canais em crescimento). Marque 'Público estrangeiro' se quiser buscar canais em inglês/espanhol (pagam 3x mais). Clique em 'INICIAR CAÇADA' e espere 1-3 minutos. Foque nos canais marcados com  ESTOURANDO — esses são os que o YouTube está entregando para não-inscritos.",
        "guia_passo2_titulo": "2. 🔎 Analisar Canal",
        "guia_passo2_texto": "Já tem um concorrente em mente? Cole o link completo do canal (ex: https://www.youtube.com/@NomeDoCanal) ou apenas o @NomeDoCanal. Escolha o nicho e clique em 'AUDITAR CANAL'. O sistema vai analisar os últimos 30 vídeos e te mostrar a média real de views, a mediana (que é mais importante que a média) e os vídeos que mais bombaram. Use isso para modelar a estrutura dos vídeos de sucesso.",
        "guia_passo3_titulo": "3. 🧠 Gerador de Títulos IA",
        "guia_passo3_texto": "Cole o TÍTULO COMPLETO de um vídeo viral que você quer modelar (ex: 'I Survived 100 Days In Nuclear Bunker, Win $500,000'). A IA vai analisar o padrão psicológico (gatilhos mentais, curiosidade, urgência, números, emoção) e gerar 10 títulos NOVOS e CRIATIVOS no mesmo estilo. Cada título terá entre 40-80 caracteres e usará gatilhos diferentes. Escolha o que melhor se adapta ao seu público.",
        "guia_passo4_titulo": "4. 📝 Gerador de Títulos Simples",
        "guia_passo4_texto": "Digite palavras-chave separadas por vírgula (ex: 'cachorro, dinheiro, trabalho, gratis'). O sistema usa 18 fórmulas de títulos virais comprovadas (baseadas em canais como MrBeast, Manual do Mundo, etc.) para gerar 7 títulos prontos. Fórmulas incluem: listas com números, perguntas provocativas, desafios, comparações, segredos revelados, transformações pessoais. Não precisa de IA — funciona instantaneamente.",
        "guia_passo5_titulo": "5. 📜 Gerador de Roteiro Cena por Cena",
        "guia_passo5_texto": "Digite o tema do seu vídeo (ex: 'Os mistérios não resolvidos do Triângulo das Bermudas'). A IA vai criar um roteiro COMPLETO baseado na estrutura dos vídeos mais virais do YouTube (padrão MrBeast). O roteiro é dividido em:  GANCHO (0-30s) — frase impactante que prende a atenção; 🎬 INTRODUÇÃO (30s-2min) — contexto e promessa; 📖 DESENVOLVIMENTO (2-10min) — 5-7 cenas com escalating tension; 💥 CLÍMAX (10-12min) — momento decisivo; 📣 CTA FINAL (12-15min) — chamada para ação. Cada cena inclui: o que falar, sugestão visual e duração.",
        "guia_passo6_titulo": "6. 🎨 Gerador de Thumbnails",
        "guia_passo6_texto": "Digite o tema do vídeo e a IA vai gerar 3 ideias DETALHADAS de thumbnails virais. Cada ideia inclui: descrição visual completa, expressão facial sugerida, texto para colocar na thumb (máx 4 palavras), paleta de cores, elemento chave (seta, círculo, contraste) e o gatilho psicológico que faz funcionar. Use o Canva (grátis) para criar as thumbnails seguindo essas especificações.",
        "guia_dicas_titulo": "💎 Dicas de Ouro de Murilo Silva:",
        "guia_dica1": "Busque em inglês (true crime, abandoned places) para achar canais que pagam 3x mais (RPM alto).",
        "guia_dica2": "Taxa viral acima de 1.0x significa que o YouTube está entregando o vídeo para não-inscritos. É ouro puro.",
        "guia_dica3": "Modele a estrutura (gancho, ritmo, edição) dos vídeos, mas NUNCA copie o roteiro palavra por palavra.",
        "guia_dica4": "Thumbnails com rosto + expressão forte + seta vermelha + texto curto (3 palavras) têm CTR 2-3x maior.",
        "guia_dica5": "Os primeiros 30 segundos do vídeo decidem tudo. Use o gancho do roteiro sem cortar.",
    },
    "en": {
        "header_title": "BEGINS · Creator Assistant",
        "header_creator": "Murilo Silva · Content Creator",
        "header_subtitle": "The starting point for your new YouTube business",
        "header_badge": "VERSION 12.0 · OPEN SOURCE AI",
        "tab_cacador": "🕵️ Channel Hunter",
        "tab_analisar": "🔎 Analyze Channel",
        "tab_titulos_ia": "🧠 AI Title Generator",
        "tab_titulos_simples": " Simple Title Generator",
        "tab_roteiro": "📜 Script Generator",
        "tab_thumbnails": "🎨 Thumbnail Generator",
        "tab_guia": "💡 Complete Guide",
        "footer_text": "The starting point for your new business.",
        "footer_dev": "Developed by Murilo Silva · Content Creator",
        "footer_disclaimer": "Tool for educational and market research purposes.",
        "lang_label": " Language",
        "lang_pt": "Português",
        "lang_en": "English",
        "lang_es": "Español",
        "banner_ia_title": "🤖 Open Source AI Integrated (Pollinations.ai)",
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
        "msg_erro_vazio": "️ Type what you want to hunt!",
        "msg_erro_nada": "❌ Nothing found. Try another word.",
        "msg_erro_url": "⚠️ Paste the channel link!",
        "msg_erro_canal": "❌ Channel not found. Check the link.",
        "msg_erro_titulo": "⚠️ Type a viral video title!",
        "msg_erro_tema": "⚠️ Type your video theme!",
        "msg_erro_palavras": "️ Type valid keywords separated by comma!",
        "msg_erro_ia": "❌ Error generating content. Try again.",
        "titulo_original": "ORIGINAL TITLE ANALYZED",
        "titulos_gerados": "AI GENERATED TITLES",
        "palavras_analisadas": "ANALYZED KEYWORDS",
        "titulos_criados": "CREATED TITLES",
        "roteiro_completo": "COMPLETE SCRIPT",
        "thumbnails_ideias": "THUMBNAIL IDEAS",
        "dica_titulo": "💎 Tip: Choose the title that best fits your audience and combine with an impactful thumbnail!",
        "dica_roteiro": "💡 Tip: Use this script as a base and adapt it with your personality!",
        "dica_thumb": "💡 Tip: Use Canva (free) to create thumbnails with these specifications!",
        "dica_titulo_simples": "💎 Tip: Combine these titles with high-contrast thumbnails to maximize CTR!",
        "modelos_copiar": "🧬 Models to copy",
        "abrir_youtube": " Open channel on YouTube →",
        "ganho_video": "EARNINGS PER VIDEO",
        "total_canal": "CHANNEL TOTAL",
        "inscritos": "👥 Subscribers",
        "views_video": "📈 Views/video",
        "taxa_viral": " Viral rate",
        "mediana": " Median",
        "estourando": "VIRAL",
        "saudavel": "Healthy",
        "estagnado": "Stagnant",
        "canais": "Channels",
        "estourando_label": "Viral",
        "ganho_medio": "Avg earnings/video",
        "nenhum_canal": "😕 No channel found. Try another word or subscriber range.",
        "guia_titulo": "How to use Begins · Creator Assistant",
        "guia_passo1_titulo": "1. 🕵️ Channel Hunter",
        "guia_passo1_texto": "Type your niche theme in the 'What to hunt?' field. Examples: 'horror stories', 'abandoned cars', 'true crime'. Choose the corresponding niche in the side menu (this defines how much YouTube pays per 1,000 views). Adjust the number of channels (recommended: 8) and subscriber range (recommended: 10,000 to 500,000 to find growing channels). Check 'Foreign audience' if you want to search English/Spanish channels (they pay 3x more). Click 'START HUNT' and wait 1-3 minutes. Focus on channels marked with 🚀 VIRAL — these are the ones YouTube is delivering to non-subscribers.",
        "guia_passo2_titulo": "2. 🔎 Analyze Channel",
        "guia_passo2_texto": "Already have a competitor in mind? Paste the full channel link (ex: https://www.youtube.com/@ChannelName) or just @ChannelName. Choose the niche and click 'AUDIT CHANNEL'. The system will analyze the last 30 videos and show you the real average views, the median (which is more important than the average) and the videos that exploded the most. Use this to model the structure of successful videos.",
        "guia_passo3_titulo": "3. 🧠 AI Title Generator",
        "guia_passo3_texto": "Paste the COMPLETE TITLE of a viral video you want to model (ex: 'I Survived 100 Days In Nuclear Bunker, Win $500,000'). The AI will analyze the psychological pattern (mental triggers, curiosity, urgency, numbers, emotion) and generate 10 NEW and CREATIVE titles in the same style. Each title will have between 40-80 characters and use different triggers. Choose the one that best fits your audience.",
        "guia_passo4_titulo": "4. 📝 Simple Title Generator",
        "guia_passo4_texto": "Type keywords separated by commas (ex: 'dog, money, work, free'). The system uses 18 proven viral title formulas (based on channels like MrBeast, etc.) to generate 7 ready-made titles. Formulas include: numbered lists, provocative questions, challenges, comparisons, revealed secrets, personal transformations. No AI needed — works instantly.",
        "guia_passo5_titulo": "5. 📜 Scene-by-Scene Script Generator",
        "guia_passo5_texto": "Type your video theme (ex: 'The unsolved mysteries of the Bermuda Triangle'). The AI will create a COMPLETE script based on the structure of the most viral YouTube videos (MrBeast pattern). The script is divided into: 🎣 HOOK (0-30s) — impactful phrase that grabs attention; 🎬 INTRODUCTION (30s-2min) — context and promise;  DEVELOPMENT (2-10min) — 5-7 scenes with escalating tension;  CLIMAX (10-12min) — decisive moment; 📣 FINAL CTA (12-15min) — call to action. Each scene includes: what to say, visual suggestion and duration.",
        "guia_passo6_titulo": "6. 🎨 Thumbnail Generator",
        "guia_passo6_texto": "Type the video theme and the AI will generate 3 DETAILED viral thumbnail ideas. Each idea includes: complete visual description, suggested facial expression, text to put on the thumb (max 4 words), color palette, key element (arrow, circle, contrast) and the psychological trigger that makes it work. Use Canva (free) to create the thumbnails following these specifications.",
        "guia_dicas_titulo": "💎 Golden Tips from Murilo Silva:",
        "guia_dica1": "Search in English (true crime, abandoned places) to find channels that pay 3x more (high RPM).",
        "guia_dica2": "Viral rate above 1.0x means YouTube is delivering the video to non-subscribers. It's pure gold.",
        "guia_dica3": "Model the structure (hook, rhythm, editing) of videos, but NEVER copy the script word for word.",
        "guia_dica4": "Thumbnails with face + strong expression + red arrow + short text (3 words) have 2-3x higher CTR.",
        "guia_dica5": "The first 30 seconds of the video decide everything. Use the hook from the script without cutting.",
    },
    "es": {
        "header_title": "BEGINS · Asistente del Creador",
        "header_creator": "Murilo Silva · Creador de Contenido",
        "header_subtitle": "El punto de partida para tu nuevo negocio en YouTube",
        "header_badge": "VERSIÓN 12.0 · IA OPEN SOURCE",
        "tab_cacador": "🕵️ Cazador de Canales",
        "tab_analisar": "🔎 Analizar Canal",
        "tab_titulos_ia": "🧠 Generador de Títulos IA",
        "tab_titulos_simples": "📝 Generador de Títulos Simples",
        "tab_roteiro": "📜 Generador de Guion",
        "tab_thumbnails": "🎨 Generador de Miniaturas",
        "tab_guia": "💡 Guía Completa",
        "footer_text": "El punto de partida para tu nuevo negocio.",
        "footer_dev": "Desarrollado por Murilo Silva · Creador de Contenido",
        "footer_disclaimer": "Herramienta para fines educativos e investigación de mercado.",
        "lang_label": "🌐 Idioma",
        "lang_pt": "Português",
        "lang_en": "English",
        "lang_es": "Español",
        "banner_ia_title": "🤖 IA Open Source Integrada (Pollinations.ai)",
        "banner_ia_text": "100% gratuita, sin login, sin contraseña, sin API key. Código abierto. Generando títulos, guiones y miniaturas automáticamente.",
        "btn_cacar": "INICIAR CAZA",
        "btn_analisar": "AUDITAR CANAL",
        "btn_titulos_ia": "GENERAR 10 TÍTULOS CON IA",
        "btn_titulos_simples": "GENERAR 7 TÍTULOS",
        "btn_roteiro": "GENERAR GUION COMPLETO",
        "btn_thumbnails": "GENERAR 3 MINIATURAS",
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
        "lbl_tema": "Tema de tu video",
        "ph_cacar": "Ej: historias de terror, coches abandonados, true crime...",
        "ph_url": "https://www.youtube.com/@NombreDelCanal",
        "ph_titulo": "Ej: Sobreviví 100 Días En Un Búnker Nuclear, Gana $500,000",
        "ph_palavras": "Ej: perro, dinero, trabajo, gratis",
        "ph_tema": "Ej: Los misterios no resueltos del Triángulo de las Bermudas",
        "lbl_csv": "Descargar Reporte (CSV)",
        "msg_erro_vazio": "⚠️ ¡Escribe lo que quieres cazar!",
        "msg_erro_nada": "❌ Nada encontrado. Prueba otra palabra.",
        "msg_erro_url": "⚠️ ¡Pega el link del canal!",
        "msg_erro_canal": " Canal no encontrado. Verifica el link.",
        "msg_erro_titulo": "⚠️ ¡Escribe el título de un video viral!",
        "msg_erro_tema": "⚠️ ¡Escribe el tema de tu video!",
        "msg_erro_palavras": "⚠️ ¡Escribe palabras clave válidas separadas por coma!",
        "msg_erro_ia": "❌ Error al generar contenido. Intenta de nuevo.",
        "titulo_original": "TÍTULO ORIGINAL ANALIZADO",
        "titulos_gerados": "TÍTULOS GENERADOS POR IA",
        "palavras_analisadas": "PALABRAS CLAVE ANALIZADAS",
        "titulos_criados": "TÍTULOS CREADOS",
        "roteiro_completo": "GUION COMPLETO",
        "thumbnails_ideias": "IDEAS DE MINIATURAS",
        "dica_titulo": "💎 Consejo: ¡Elige el título que mejor se adapte a tu audiencia y combínalo con una miniatura impactante!",
        "dica_roteiro": " Consejo: ¡Usa este guion como base y adáptalo con tu personalidad!",
        "dica_thumb": "💡 Consejo: ¡Usa Canva (gratis) para crear las miniaturas con estas especificaciones!",
        "dica_titulo_simples": "💎 Consejo: ¡Combina estos títulos con miniaturas de alto contraste para maximizar el CTR!",
        "modelos_copiar": "🧬 Modelos para copiar",
        "abrir_youtube": "🔗 Abrir canal en YouTube →",
        "ganho_video": "GANANCIA POR VIDEO",
        "total_canal": "TOTAL DEL CANAL",
        "inscritos": "👥 Suscriptores",
        "views_video": "📈 Vistas/video",
        "taxa_viral": "🔥 Tasa viral",
        "mediana": "📊 Mediana",
        "estourando": "VIRAL",
        "saudavel": "Saludable",
        "estagnado": "Estancado",
        "canais": "Canales",
        "estourando_label": "Viral",
        "ganho_medio": "Ganancia promedio/video",
        "nenhum_canal": "😕 Ningún canal encontrado. Prueba otra palabra o rango de suscriptores.",
        "guia_titulo": "Cómo usar Begins · Asistente del Creador",
        "guia_passo1_titulo": "1. ️ Cazador de Canales",
        "guia_passo1_texto": "Escribe el tema de tu nicho en el campo '¿Qué cazar?'. Ejemplos: 'historias de terror', 'coches abandonados', 'true crime'. Elige el nicho correspondiente en el menú lateral (esto define cuánto paga YouTube por 1.000 vistas). Ajusta la cantidad de canales (recomendado: 8) y el rango de suscriptores (recomendado: 10.000 a 500.000 para encontrar canales en crecimiento). Marca 'Audiencia extranjera' si quieres buscar canales en inglés/español (pagan 3x más). Haz clic en 'INICIAR CAZA' y espera 1-3 minutos. Enfócate en los canales marcados con 🚀 VIRAL — esos son los que YouTube está entregando a no-suscriptores.",
        "guia_passo2_titulo": "2. 🔎 Analizar Canal",
        "guia_passo2_texto": "¿Ya tienes un competidor en mente? Pega el link completo del canal (ej: https://www.youtube.com/@NombreDelCanal) o solo @NombreDelCanal. Elige el nicho y haz clic en 'AUDITAR CANAL'. El sistema analizará los últimos 30 videos y te mostrará el promedio real de vistas, la mediana (que es más importante que el promedio) y los videos que más explotaron. Usa esto para modelar la estructura de los videos exitosos.",
        "guia_passo3_titulo": "3.  Generador de Títulos IA",
        "guia_passo3_texto": "Pega el TÍTULO COMPLETO de un video viral que quieres modelar (ej: 'Sobreviví 100 Días En Un Búnker Nuclear, Gana $500,000'). La IA analizará el patrón psicológico (gatillos mentales, curiosidad, urgencia, números, emoción) y generará 10 títulos NUEVOS y CREATIVOS en el mismo estilo. Cada título tendrá entre 40-80 caracteres y usará gatillos diferentes. Elige el que mejor se adapte a tu audiencia.",
        "guia_passo4_titulo": "4. 📝 Generador de Títulos Simples",
        "guia_passo4_texto": "Escribe palabras clave separadas por comas (ej: 'perro, dinero, trabajo, gratis'). El sistema usa 18 fórmulas de títulos virales comprobadas (basadas en canales como MrBeast, etc.) para generar 7 títulos listos. Las fórmulas incluyen: listas numeradas, preguntas provocativas, desafíos, comparaciones, secretos revelados, transformaciones personales. No necesita IA — funciona instantáneamente.",
        "guia_passo5_titulo": "5. 📜 Generador de Guion Escena por Escena",
        "guia_passo5_texto": "Escribe el tema de tu video (ej: 'Los misterios no resueltos del Triángulo de las Bermudas'). La IA creará un guion COMPLETO basado en la estructura de los videos más virales de YouTube (patrón MrBeast). El guion se divide en: 🎣 GANCHO (0-30s) — frase impactante que atrapa la atención; 🎬 INTRODUCCIÓN (30s-2min) — contexto y promesa;  DESARROLLO (2-10min) — 5-7 escenas con tensión creciente; 💥 CLÍMAX (10-12min) — momento decisivo; 📣 CTA FINAL (12-15min) — llamada a la acción. Cada escena incluye: qué decir, sugerencia visual y duración.",
        "guia_passo6_titulo": "6. 🎨 Generador de Miniaturas",
        "guia_passo6_texto": "Escribe el tema del video y la IA generará 3 ideas DETALLADAS de miniaturas virales. Cada idea incluye: descripción visual completa, expresión facial sugerida, texto para poner en la miniatura (máx 4 palabras), paleta de colores, elemento clave (flecha, círculo, contraste) y el gatillo psicológico que hace que funcione. Usa Canva (gratis) para crear las miniaturas siguiendo estas especificaciones.",
        "guia_dicas_titulo": "💎 Consejos de Oro de Murilo Silva:",
        "guia_dica1": "Busca en inglés (true crime, abandoned places) para encontrar canales que pagan 3x más (RPM alto).",
        "guia_dica2": "Tasa viral superior a 1.0x significa que YouTube está entregando el video a no-suscriptores. Es oro puro.",
        "guia_dica3": "Modela la estructura (gancho, ritmo, edición) de los videos, pero NUNCA copies el guion palabra por palabra.",
        "guia_dica4": "Las miniaturas con rostro + expresión fuerte + flecha roja + texto corto (3 palabras) tienen CTR 2-3x mayor.",
        "guia_dica5": "Los primeros 30 segundos del video lo deciden todo. Usa el gancho del guion sin cortar.",
    }
}

def t(key):
    """Retorna texto traduzido baseado no idioma atual"""
    return I18N.get(IDIOMA_ATUAL, I18N["pt"]).get(key, I18N["pt"].get(key, key))

# ═══════════════════════════════════════════════════════════════
# 🤖 SISTEMA DE IA (Pollinations.ai - 100% grátis, sem login)
# ═══════════════════════════════════════════════════════════════
def chamar_ia(prompt, idioma="pt"):
    """Chama Pollinations.ai com prompt otimizado"""
    try:
        response = requests.post(
            "https://text.pollinations.ai/openai",
            json={
                "model": "openai",
                "messages": [
                    {"role": "system", "content": f"Responda sempre em {idioma}. Seja direto e objetivo."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 3000
            },
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Erro IA: {e}")
    return None

# ═══════════════════════════════════════════════════════════════
#  UTILITÁRIOS
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
    " Curiosidades":12, "🔪 Histórias/Crimes":18, "️ Documentário":20,
    " Resumo de Filmes":15, " Religião":10, "💪 Motivacional":9,
    "🎵 Música/Relax":4, "🎮 Games":8, "⚽ Esportes":14,
    "🚗 Carros":26, "🤖 Tecnologia/IA":35, "💊 Saúde":22, "💰 Finanças":55,
    "🎙️ Cortes de Podcast":8, "🧘 Meditação":6, "₿ Finanças Cripto":45,
    "📱 Shorts/TikTok":5, "🎯 Marketing Digital":40, "🏋️ Fitness":18,
    "🍳 Receitas":14, "🐶 Pets":16, "✈️ Viagens":28,
    "👻 Sobrenatural":22, "📚 Autoajuda":16, "🎭 Fofoca/Celebridades":10,
}

# ═══════════════════════════════════════════════════════════════
# 🔍 MOTOR DE BUSCA (YouTube via yt-dlp)
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

# ═══════════════════════════════════════════════════════════════
# 🧠 GERADOR DE TÍTULOS IA (REFINADO)
# ═══════════════════════════════════════════════════════════════
def gerar_titulos_ia(titulo_video, nicho):
    if not titulo_video or not titulo_video.strip():
        return f"<div class='msg-erro'>{t('msg_erro_titulo')}</div>"
    
    idioma_map = {"pt": "português brasileiro", "en": "English", "es": "español"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "português brasileiro")
    
    prompt = f"""Você é um especialista mundial em títulos virais para YouTube no nicho de {nicho}.

Título original viral: "{titulo_video}"

Sua tarefa: Criar EXATAMENTE 10 títulos COMPLETOS e CRIATIVOS para vídeos do YouTube, em {idioma_texto}, seguindo o mesmo estilo e padrão psicológico do título original.

REGRAS CRÍTICAS:
1. Cada título deve ser uma FRASE COMPLETA de 40-80 caracteres
2. Use gatilhos mentais diferentes em cada título: curiosidade, urgência, números, emoção, desafio, segredo, transformação
3. Mantenha o mesmo tom e estilo do original
4. Varie os gatilhos entre os 10 títulos
5. NUNCA responda apenas com palavras-chave soltas

FORMATO OBRIGATÓRIO (exatamente assim, em {idioma_texto}):
1. [Título completo aqui com 40-80 caracteres]
2. [Título completo aqui com 40-80 caracteres]
... até 10

EXEMPLO DE TÍTULO VÁLIDO: "I Survived 100 Days In A Nuclear Bunker, Win $500,000"
EXEMPLO DE TÍTULO INVÁLIDO: "sobrevivência, bunker, desafio"

Responda APENAS com a lista numerada de 1 a 10, sem explicações extras."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        titulos = extrair_titulos(resultado)
        if len(titulos) < 5:
            titulos = gerar_titulos_fallback(titulo_video, nicho)
    else:
        titulos = gerar_titulos_fallback(titulo_video, nicho)
    
    return renderizar_titulos(titulo_video, titulos, t('titulo_original'), t('titulos_gerados'), t('dica_titulo'))

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
    prefixos = ["🚨 URGENTE: ", "⚠️ ATENÇÃO: ", "💥 IMPRESSIONANTE: ", "🔥 INACREDITÁVEL: ", "😱 CHOCANTE: "]
    for prefixo in prefixos[:5]:
        novo = f"{prefixo}{titulo_original}"
        if len(novo) <= 100:
            titulos.append(novo)
    titulos.append(f"Você Conseguiria Sobreviver a Isso? {titulo_original}")
    titulos.append(f"Por Que {titulo_original} Está Chocando o Mundo?")
    return titulos[:10]

def renderizar_titulos(titulo_original, titulos, label_original, label_gerados, dica):
    html = f'''<div class="box-resultado box-titulos">
        <div class="box-header"><span class="box-icon">📊</span><h3>{label_original}</h3></div>
        <div class="box-conteudo">{titulo_original}</div>
        <div class="box-header" style="margin-top: 25px;"><span class="box-icon">🎯</span><h3>{len(titulos)} {label_gerados}</h3></div>'''
    for i, titulo in enumerate(titulos[:10], 1):
        html += f'''<div class="titulo-item"><span class="titulo-num">{i}.</span><span class="titulo-texto">{titulo}</span></div>'''
    html += f'''<div class="box-dica"><strong>{dica}</strong></div></div>'''
    return html

# ═══════════════════════════════════════════════════════════════
# 📝 GERADOR DE TÍTULOS SIMPLES (REFINADO - 18 FÓRMULAS)
# ══════════════════════════════════════════════════════════════
def gerar_titulos_simples(nicho, palavras_chave):
    if not palavras_chave or not palavras_chave.strip():
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    palavras = [p.strip() for p in palavras_chave.split(',') if p.strip()]
    if not palavras:
        return f"<div class='msg-erro'>{t('msg_erro_palavras')}</div>"
    
    p0 = palavras[0].title() if palavras else "Tema"
    p1 = palavras[1].title() if len(palavras) > 1 else "Concorrência"
    p2 = palavras[2].title() if len(palavras) > 2 else "Segredo"
    
    formulas = [
        f"7 Segredos Sobre {p0} Que Vão Mudar Sua Vida Para Sempre",
        f"10 Maneiras de Ganhar Dinheiro com {p0} (Funciona em 2024)",
        f"Por Que {p0} Está Fazendo Pessoas Ficarem Ricas Rapidamente?",
        f"Você Sabia Que {p0} Pode Te Fazer Ganhar {p1}?",
        f" URGENTE: O Que Está Acontecendo com {p0} Vai Te Chocar!",
        f"⚠️ ATENÇÃO: Não Ignore Isso Sobre {p0} em 2024!",
        f"{p0} vs {p1}: Qual é Melhor? (Teste Definitivo)",
        f"$1 vs $1,000,000 em {p0} - A Diferença é Absurda!",
        f"Sobrevivi 30 Dias Fazendo {p0} - O Resultado Foi Inacreditável!",
        f"Tentei {p0} Por 7 Dias e Isso Aconteceu...",
        f"5 Erros Que Você Comete com {p0} (E Como Evitar)",
        f"Top 10 Dicas de {p0} Que Ninguém Te Conta",
        f"O Segredo Obscuro de {p0} Que as Empresas Não Querem Que Você Saiba",
        f"A Verdade Sobre {p0} Que Está Sendo Escondida de Você",
        f"Como {p0} Transformou Minha Vida em Apenas 30 Dias",
        f"De Zero a Herói: Minha Jornada com {p0}",
        f"O Que Acontece Quando Você {p0} Todos os Dias?",
        f"Por Que Milhões de Pessoas Estão Obcecadas por {p0}?",
    ]
    
    titulos = [t for t in formulas if 30 <= len(t) <= 100][:10]
    
    if len(titulos) < 7:
        for p in palavras[:3]:
            titulos.append(f"Guia Completo de {p.title()} para Iniciantes em 2024")
            titulos.append(f"Como Começar com {p.title()} do Zero (Passo a Passo)")
    
    return renderizar_titulos(palavras_chave, titulos[:10], t('palavras_analisadas'), t('titulos_criados'), t('dica_titulo_simples'))

# ═══════════════════════════════════════════════════════════════
#  GERADOR DE ROTEIRO CENA POR CENA (BASEADO EM MRBEAST)
# ═══════════════════════════════════════════════════════════════
def gerar_roteiro(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>"
    
    idioma_map = {"pt": "português brasileiro", "en": "English", "es": "español"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "português brasileiro")
    
    canais_str = ""
    if canais_info and len(canais_info) > 0:
        canais_str = "\nCanais de referência analisados:\n"
        for c in canais_info[:5]:
            canais_str += f"- {c.get('nome','Canal')}: {fmt(c.get('media_rec',0))} views/vídeo\n"
            for b in c.get('bombas', [])[:2]:
                canais_str += f"  • Vídeo viral: {b.get('titulo','')} ({fmt(b.get('views',0))} views)\n"
    
    # Estrutura baseada nos vídeos virais do MrBeast (dados reais do CSV)
    prompt = f"""Você é o MELHOR roteirista de vídeos virais do YouTube, especialista no padrão MrBeast.

TEMA DO VÍDEO: "{tema}"
{canais_str}

Crie um ROTEIRO COMPLETO CENA POR CENA para um vídeo de 10-15 minutos, em {idioma_texto}, baseado na estrutura dos vídeos mais virais do YouTube (padrão MrBeast com 200M+ views).

ESTRUTURA OBRIGATÓRIA (use EXATAMENTE estes blocos):

 CENA 1 - GANCHO (0-30 segundos)
- Frase de impacto que PRENDE a atenção nos primeiros 3 segundos
- Revele o stakes (o que está em jogo)
- Prometa algo extraordinário
- Duração: 30s

🎬 CENA 2 - INTRODUÇÃO (30s - 2min)
- Contextualize o tema
- Apresente as regras do desafio/conceito
- Mostre o prêmio ou objetivo final
- Duração: 1min30s

📖 CENA 3 - PRIMEIRO OBSTÁCULO (2min - 4min)
- Primeiro desafio/surpresa
- Mostre reação emocional dos participantes
- Duração: 2min

📖 CENA 4 - ESCALADA DE TENSÃO (4min - 6min)
- Aumente a dificuldade
- Elimine participantes ou aumente stakes
- Duração: 2min

 CENA 5 - PONTO DE VIRADA (6min - 8min)
- Momento inesperado que muda tudo
- Reação emocional forte
- Duração: 2min

📖 CENA 6 - PREPARAÇÃO PARA O CLÍMAX (8min - 10min)
- Últimos competidores/desafio final se aproximando
- Tensão máxima
- Duração: 2min

💥 CENA 7 - CLÍMAX (10min - 12min)
- Momento decisivo
- Resolução do desafio principal
- Reação emocional máxima
- Duração: 2min

🏆 CENA 8 - PREMIAÇÃO (12min - 13min30s)
- Entrega do prêmio
- Reação do vencedor
- Duração: 1min30s

📣 CENA 9 - CTA FINAL (13min30s - 15min)
- Chamada para like, inscrição e próximo vídeo
- Teaser do próximo vídeo
- Duração: 1min30s

Para CADA CENA, inclua:
-  O QUE FALAR: texto sugerido pronto para narrar
- 🎥 SUGESTÃO VISUAL: o que mostrar na tela (cenas, ângulos, gráficos)
- ️ DURAÇÃO: tempo exato da cena
- 🎵 SUGESTÃO SONORA: tipo de música/efeito sonoro

Responda de forma ORGANIZADA, CLARA e PRONTA PARA USAR. Use linguagem ENVOLVENTE e DIRETA. Escreva em {idioma_texto}."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        html = f'''<div class="box-resultado box-roteiro">
            <div class="box-header"><span class="box-icon">📝</span><h3>{t('roteiro_completo')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica"><strong>{t('dica_roteiro')}</strong></div>
        </div>'''
        return html
    else:
        return f"<div class='msg-erro'>{t('msg_erro_ia')}</div>"

# ═══════════════════════════════════════════════════════════════
# 🎨 GERADOR DE THUMBNAILS (APENAS 3, CORRIGIDO)
# ═══════════════════════════════════════════════════════════════
def gerar_thumbnails(tema, canais_info):
    if not tema or not tema.strip():
        return f"<div class='msg-erro'>{t('msg_erro_tema')}</div>"
    
    idioma_map = {"pt": "português brasileiro", "en": "English", "es": "español"}
    idioma_texto = idioma_map.get(IDIOMA_ATUAL, "português brasileiro")
    
    canais_str = ""
    if canais_info and len(canais_info) > 0:
        canais_str = "\nEstilo dos canais de referência:\n"
        for c in canais_info[:3]:
            canais_str += f"- {c.get('nome','Canal')}: taxa viral {c.get('taxa',0):.2f}x\n"
    
    prompt = f"""Você é o MELHOR especialista em thumbnails virais do YouTube.

TEMA DO VÍDEO: "{tema}"
{canais_str}

Crie EXATAMENTE 3 IDEIAS DETALHADAS de thumbnails que gerem alta taxa de clique (CTR), em {idioma_texto}.

Para CADA uma das 3 ideias, inclua TODOS estes elementos:

IDEIA 1:
- 🖼️ DESCRIÇÃO VISUAL: Descreva exatamente o que aparece na imagem (pessoas, objetos, cenário, composição)
-  EXPRESSÃO: Emoção do rosto (se houver pessoa) - seja específico
-  TEXTO NA THUMB: Texto curto (MÁXIMO 4 palavras) em destaque - escreva o texto exato
- 🎨 CORES: Paleta de 3 cores específicas (ex: vermelho, amarelo, preto)
- ⚡ ELEMENTO CHAVE: O que chama atenção (seta, círculo, contraste, brilho)
- 🎯 GATILHO PSICOLÓGICO: Por que essa thumb funciona (curiosidade, urgência, medo, ganância)

IDEIA 2:
(mesma estrutura detalhada)

IDEIA 3:
(mesma estrutura detalhada)

Responda de forma ORGANIZADA, numerada de 1 a 3, em {idioma_texto}."""
    
    resultado = chamar_ia(prompt, IDIOMA_ATUAL)
    
    if resultado:
        html = f'''<div class="box-resultado box-thumbnails">
            <div class="box-header"><span class="box-icon">🎨</span><h3>3 {t('thumbnails_ideias')}</h3></div>
            <div class="box-tema"><strong>Tema:</strong> {tema}</div>
            <div class="box-conteudo-texto">{resultado}</div>
            <div class="box-dica"><strong>{t('dica_thumb')}</strong></div>
        </div>'''
        return html
    else:
        return f"<div class='msg-erro'>{t('msg_erro_ia')}</div>"

# ═══════════════════════════════════════════════════════════════
# 🎨 CSS - PALETA YOUTUBE + VISUAL LIMPO
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
        html.append(f'<div class="msg-erro">{t("nenhum_canal")}</div>')
    else:
        est = sum(1 for r in resultados if r["status"]=="ESTOURANDO")
        gm = sum(r["ganho_video"] for r in resultados)/len(resultados)
        html.append(f'''<div class="stats-container">
            <div class="stat-card"><strong>{len(resultados)}</strong><span>{t("canais")}</span></div>
            <div class="stat-card"><strong>{est} 🚀</strong><span>{t("estourando_label")}</span></div>
            <div class="stat-card"><strong>{brl(gm)}</strong><span>{t("ganho_medio")}</span></div>
        </div>''')
        for r in resultados:
            bc = "rocket" if r["status"]=="ESTOURANDO" else ("up" if r["status"]=="Saudável" else "sleep")
            status_text = t("estourando") if r["status"]=="ESTOURANDO" else (t("saudavel") if r["status"]=="Saudável" else t("estagnado"))
            html.append(f'''<div class="ac-card"><div class="ac-card-head"><h3>{r['emoji']} {r['nome']}</h3><span class="ac-badge ac-badge-{bc}">{status_text}</span></div>
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
    a["status"], a["emoji"] = ("ESTOURANDO","🚀") if tx>=1.0 else (("Saudável","📈") if tx>=0.3 else ("Estagnado","😴"))
    a["rpm"] = RPM; a["ganho_video"] = a["media_rec"]/1000*RPM
    return render_cards([a]), [a]

# ══════════════════════════════════════════════════════════════
# 🌐 INTERFACE COM SELETOR DE IDIOMA
# ═══════════════════════════════════════════════════════════════
def mudar_idioma(idioma):
    global IDIOMA_ATUAL
    IDIOMA_ATUAL = idioma
    return gr.update()

begins_theme = gr.themes.Base(
    primary_hue="red", secondary_hue="neutral", neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
)

with gr.Blocks(title="Begins · Creator Assistant", theme=begins_theme) as app:
    gr.HTML(f"""
    <div class="ac-header">
        <h1><span class="begins">BEGINS</span> · Assistente do Criador</h1>
        <div class="creator">Murilo Silva · Criador de Conteúdo</div>
        <p class="subtitle">O ponto de partida para o seu novo negócio no YouTube</p>
        <span class="badge">VERSÃO 12.0 · IA OPEN SOURCE</span>
    </div>
    """)
    
    # Seletor de idioma
    with gr.Row():
        idioma_selector = gr.Radio(
            choices=["pt", "en", "es"],
            value="pt",
            label=" Language / Idioma / Idioma",
            elem_classes=["lang-selector"]
        )
    
    canais_state = gr.State([])
    
    idioma_selector.change(fn=mudar_idioma, inputs=idioma_selector, outputs=gr.HTML())
    
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
            gr.Markdown("### Crie títulos baseados em palavras-chave usando fórmulas virais")
            with gr.Row():
                with gr.Column(scale=1):
                    nicho_gen = gr.Dropdown(list(TABELA_RPM.keys()), value="🔪 Histórias/Crimes", label="Nicho do Canal")
                with gr.Column(scale=2):
                    kw_gen = gr.Textbox(label="Palavras-chave (separe por vírgula)", placeholder="Ex: cachorro, dinheiro, trabalho, gratis")
            btn_gen = gr.Button("GERAR 7 TÍTULOS", variant="primary", size="lg")
            out_gen = gr.HTML()
            btn_gen.click(fn=gerar_titulos_simples, inputs=[nicho_gen, kw_gen], outputs=out_gen)

        with gr.Tab(" Gerador de Roteiro"):
            gr.Markdown("### Gere um roteiro COMPLETO CENA POR CENA baseado em vídeos virais")
            tema_roteiro = gr.Textbox(label="Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_roteiro = gr.Button("GERAR ROTEIRO COMPLETO", variant="primary", size="lg")
            out_roteiro = gr.HTML()
            btn_roteiro.click(fn=lambda t, canais: gerar_roteiro(t, canais), inputs=[tema_roteiro, canais_state], outputs=out_roteiro)

        with gr.Tab("🎨 Gerador de Thumbnails"):
            gr.Markdown("### Crie 3 ideias detalhadas de thumbnails virais")
            tema_thumb = gr.Textbox(label="Tema do seu vídeo", placeholder="Ex: Os mistérios não resolvidos do Triângulo das Bermudas")
            btn_thumb = gr.Button("GERAR 3 THUMBNAILS", variant="primary", size="lg")
            out_thumb = gr.HTML()
            btn_thumb.click(fn=lambda t, canais: gerar_thumbnails(t, canais), inputs=[tema_thumb, canais_state], outputs=out_thumb)

        with gr.Tab("💡 Guia Completo"):
            gr.Markdown(f"""
            ### {t('guia_titulo')}
            
            **{t('guia_passo1_titulo')}**
            
            {t('guia_passo1_texto')}
            
            **{t('guia_passo2_titulo')}**
            
            {t('guia_passo2_texto')}
            
            **{t('guia_passo3_titulo')}**
            
            {t('guia_passo3_texto')}
            
            **{t('guia_passo4_titulo')}**
            
            {t('guia_passo4_texto')}
            
            **{t('guia_passo5_titulo')}**
            
            {t('guia_passo5_texto')}
            
            **{t('guia_passo6_titulo')}**
            
            {t('guia_passo6_texto')}
            
            **{t('guia_dicas_titulo')}**
            
            - {t('guia_dica1')}
            - {t('guia_dica2')}
            - {t('guia_dica3')}
            - {t('guia_dica4')}
            - {t('guia_dica5')}
            """)

    # Banner da IA no FINAL (como pedido)
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
