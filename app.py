import streamlit as st

st.title("📝 Gerador de Prompt para Roteiros de Vídeo")

# Tipo do vídeo
tipo_video = st.selectbox("Tipo do vídeo", ["Unboxing / Review", "Comparação de produtos"])

if tipo_video == "Unboxing / Review":
    st.subheader("🧩 Informações sobre o produto")

    titulo_video = st.text_input("Título do vídeo")
    nome_produto = st.text_input("Nome do produto")
    valor_compra = st.text_input("Valor da compra")
    onde_comprou = st.text_input("Onde comprou?")
    valeu_a_pena = st.radio("O produto valeu a pena?", ["Sim", "Não", "Em partes"])

    pontos_positivos = st.text_area("Pontos positivos")
    pontos_negativos = st.text_area("Pontos negativos")
    descricao_fabricante = st.text_area("Descrição do produto (fabricante)")
    transcricao_youtube = st.text_area("Transcrição de outro vídeo sobre o produto")
    ideias_gerais = st.text_area("Ideias gerais para o vídeo")

    # Seções obrigatórias em todo roteiro
    secoes_escolhidas = [
        "Introdução",
        "Unboxing ou o que vem na caixa",
        "Preço",
        "Pontos positivos",
        "Pontos negativos",
        "Vale a pena?",
        "Conclusão com CTA"
    ]

    gerar = st.button("📋 Gerar Prompt")

    if gerar:
        secoes_texto = "\n".join([f"- {sec}" for sec in secoes_escolhidas])

        prompt = f"""
Crie um roteiro em formato de **tópicos** para um vídeo de YouTube sobre o produto **"{nome_produto}"**.

O roteiro deve servir como lembrete dos pontos que o criador de conteúdo deve comentar, **sem ser um texto palavra por palavra**.

### Informações:
- Título do vídeo: {titulo_video}
- Valor da compra: {valor_compra}
- Onde comprou: {onde_comprou}
- Valeu a pena?: {valeu_a_pena}

### Pontos positivos:
{pontos_positivos}

### Pontos negativos:
{pontos_negativos}

### Descrição do fabricante:
{descricao_fabricante}

### Transcrição de outro vídeo:
{transcricao_youtube}

### Ideias gerais:
{ideias_gerais}

### Seções desejadas no roteiro:
{secoes_texto}

Use linguagem natural, fluida e direta. Cada item deve ser um lembrete claro do que o criador de conteúdo deve falar.
"""

        st.subheader("🧠 Prompt Gerado")
        st.code(prompt, language="markdown")
        st.info("Copie este prompt e cole no ChatGPT para gerar seu roteiro!")

elif tipo_video == "Comparação de produtos":
    st.subheader("🔀 Comparação de Produtos")

    produto1 = st.text_area("📝 Roteiro do Produto 1 (já existente)")
    produto2 = st.text_area("📝 Roteiro do Produto 2 (já existente)")
    publico_alvo = st.text_input("Público-alvo")
    objetivo = st.text_input("Objetivo da comparação (ex: descobrir qual é melhor para jogos)")

    gerar_comp = st.button("📋 Gerar Prompt de Comparação")

    if gerar_comp:
        prompt = f"""
Compare dois produtos com base nos roteiros abaixo, criando um novo roteiro de vídeo em formato de tópicos.

### Público-alvo: {publico_alvo}
### Objetivo da comparação: {objetivo}

### Roteiro do Produto 1:
{produto1}

### Roteiro do Produto 2:
{produto2}

Crie um roteiro comparativo para vídeo do YouTube, com linguagem natural, tópicos diretos e lembretes do que o criador deve comentar.
"""
        st.subheader("🧠 Prompt Gerado")
        st.code(prompt, language="markdown")
        st.info("Copie este prompt e cole no ChatGPT para gerar seu roteiro!")
