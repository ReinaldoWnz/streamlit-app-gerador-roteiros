import streamlit as st
import openai
import datetime

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Gerador de Roteiros de Vídeo Automatizado")

# Tipos de vídeo
tipo_video = st.selectbox("Tipo do vídeo", ["Unboxing / Review", "Comparação de produtos"])

# Estruturas por tipo de produto
estruturas_por_tipo = {
    "Headset / Fone de Ouvido": [
        "Unboxing",
        "Design e conforto",
        "Conectividade e compatibilidade",
        "Qualidade de som",
        "Cancelamento de ruído (ANC)",
        "Microfone (teste rápido)",
        "Bateria e autonomia",
        "Experiência de uso (músicas, chamadas, jogos)"
    ],
    "Mouse": [
        "Unboxing",
        "Design e ergonomia",
        "Sensor e DPI",
        "Conectividade",
        "Software e personalização",
        "Experiência em jogos ou uso geral",
        "Bateria (se for wireless)"
    ],
    "Teclado": [
        "Unboxing",
        "Layout e tipo de switch",
        "Iluminação (RGB)",
        "Conectividade",
        "Software (se tiver)",
        "Experiência de digitação ou jogos"
    ],
    "Monitor": [
        "Unboxing e montagem",
        "Design e conexões",
        "Tela (resolução, tipo de painel, taxa de atualização)",
        "Qualidade de imagem (brilho, contraste, cores)",
        "Uso em jogos / trabalho"
    ],
    "Smartphone": [
        "Unboxing",
        "Design e tela",
        "Sistema e desempenho",
        "Câmeras (teste rápido)",
        "Bateria e carregamento",
        "Experiência geral"
    ],
    "Notebook": [
        "Unboxing",
        "Design e tela",
        "Teclado, portas e conectividade",
        "Desempenho e temperatura",
        "Bateria",
        "Experiência de uso geral"
    ]
}

def gerar_roteiro_unboxing():
    # Controle de estado para tipo de produto (para atualizar seções)
    if 'tipo_produto_anterior' not in st.session_state:
        st.session_state.tipo_produto_anterior = None

    tipo_produto = st.selectbox("Tipo de produto", list(estruturas_por_tipo.keys()))

    if st.session_state.tipo_produto_anterior != tipo_produto:
        st.session_state.tipo_produto_anterior = tipo_produto
        secoes_base = ["Introdução"] + estruturas_por_tipo[tipo_produto] + ["Pontos positivos", "Pontos negativos", "Vale a pena?", "Conclusão com CTA"]
        for secao in secoes_base:
            st.session_state[f"secao_{secao}"] = True

    with st.form("form_roteiro"):
        titulo_video = st.text_input("Título do vídeo")
        nome_produto = st.text_input("Nome do produto")
        data_compra = st.date_input("Data da compra", value=datetime.date.today())
        valor_compra = st.text_input("Valor da compra")
        onde_comprou = st.text_input("Onde comprou")
        publico_alvo = st.text_input("Público-alvo do vídeo")
        valeu_a_pena = st.radio("O produto valeu a pena?", ["Sim", "Não", "Em partes"])

        pontos_positivos = st.text_area("Pontos positivos")
        pontos_negativos = st.text_area("Pontos negativos")

        descricao_fabricante = st.text_area("Descrição do produto (fabricante)")
        transcricao_youtube = st.text_area("Transcrição de outro vídeo sobre o produto")
        ideias_gerais = st.text_area("Ideias gerais para o vídeo")

        gerar = st.form_submit_button("Gerar Roteiro")

    st.markdown("**Seções que você quer incluir no roteiro:**")
    secoes_base = ["Introdução"] + estruturas_por_tipo[tipo_produto] + ["Pontos positivos", "Pontos negativos", "Vale a pena?", "Conclusão com CTA"]

    secoes_escolhidas = []
    for secao in secoes_base:
        checked = st.session_state.get(f"secao_{secao}", True)
        incluir = st.checkbox(secao, value=checked, key=f"secao_{secao}")
        if incluir:
            secoes_escolhidas.append(secao)

    if gerar:
        with st.spinner("Gerando roteiro..."):
            secoes_texto = "\n".join([f"- {sec}" for sec in secoes_escolhidas])

            prompt = f"""
            Crie um roteiro em formato de tópicos para um vídeo de YouTube sobre o produto "{nome_produto}". O roteiro deve funcionar como um lembrete dos pontos que o criador de conteúdo precisa comentar, e não como um script palavra por palavra.

            Informações adicionais:
            - Título do vídeo: {titulo_video}
            - Tipo de produto: {tipo_produto}
            - Data da compra: {data_compra}
            - Valor da compra: {valor_compra}
            - Onde comprou: {onde_comprou}
            - Público-alvo: {publico_alvo}
            - Valeu a pena?: {valeu_a_pena}

            Pontos positivos:
            {pontos_positivos}

            Pontos negativos:
            {pontos_negativos}

            Descrição do fabricante:
            {descricao_fabricante}

            Transcrição de outro criador:
            {transcricao_youtube}

            Ideias gerais:
            {ideias_gerais}

            As seções do roteiro devem ser:
            {secoes_texto}

            Seja direto e claro em cada tópico.
            """

            try:
                resposta = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "..."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                roteiro = resposta.choices[0].message.content

                st.subheader("Roteiro Gerado (em tópicos)")
                st.code(roteiro, language="markdown")
                st.caption("Copie o texto acima para seu editor ou roteiro.")

            except Exception as e:
                st.error(f"Erro ao gerar o roteiro: {e}")

def gerar_roteiro_comparacao():
    with st.form("form_comparacao"):
        roteiro_1 = st.text_area("Roteiro do Produto 1")
        roteiro_2 = st.text_area("Roteiro do Produto 2")
        gerar = st.form_submit_button("Gerar Roteiro Comparativo")

    if gerar:
        with st.spinner("Gerando roteiro comparativo..."):
            prompt = f"""
            Você é um especialista em criar roteiros para vídeos de comparação de produtos. Abaixo estão dois roteiros de produtos que serão comparados:

            Produto 1:
            {roteiro_1}

            Produto 2:
            {roteiro_2}

            Crie um roteiro comparativo em formato de tópicos para um vídeo no YouTube, destacando as diferenças, pontos fortes e fracos de cada produto, e uma conclusão indicando qual produto vale mais a pena. Seja direto e claro em cada ponto.
            """

            try:
                resposta = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é um especialista em roteiros..."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                roteiro = resposta.choices[0].message.content

                st.subheader("Roteiro Comparativo Gerado (em tópicos)")
                st.code(roteiro, language="markdown")
                st.caption("Copie o texto acima para seu editor ou roteiro.")

            except Exception as e:
                st.error(f"Erro ao gerar o roteiro: {e}")

# Mostrar formulário conforme tipo do vídeo
if tipo_video == "Unboxing / Review":
    gerar_roteiro_unboxing()
elif tipo_video == "Comparação de produtos":
    gerar_roteiro_comparacao()
