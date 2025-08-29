import streamlit as st
import google.generativeai as genai
import time

# Configura chave da API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("📝 Gerador de Roteiros de Vídeo com Gemini")

# Função de "streaming fake"
def mostrar_com_streaming(texto):
    placeholder = st.empty()
    exibido = ""
    for char in texto:
        exibido += char
        placeholder.markdown(exibido)
        time.sleep(0.001)  # velocidade da "digitação"
    return exibido

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

    secoes_escolhidas = [
        "Introdução",
        "Unboxing ou o que vem na caixa",
        "Preço",
        "Pontos positivos",
        "Pontos negativos",
        "Vale a pena?",
        "Conclusão com CTA"
    ]

    gerar = st.button("🎬 Gerar Roteiro com Gemini")

    if gerar:
        secoes_texto = "\n".join([f"- {sec}" for sec in secoes_escolhidas])

        prompt = f"""
Crie um roteiro em formato de **tópicos** para um vídeo de YouTube sobre o produto **"{nome_produto}"**.

O roteiro deve servir como lembrete dos pontos que o criador de conteúdo deve comentar, **sem ser um texto palavra por palavra**.  
⚠️ Não inclua timings por seção.

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

### Seções obrigatórias no roteiro:
{secoes_texto}

### Instruções importantes para a IA:
- Analise todas as informações (título, nome do produto, descrição, transcrição e ideias gerais).  
- Deduzir automaticamente o tipo de produto (ex: notebook, smartphone, headset, monitor, etc).  
- Além das seções obrigatórias, adicione tópicos **relevantes e específicos para o tipo de produto**.  
- Sempre usar linguagem natural, fluida e direta.  
- Cada item deve ser um lembrete claro do que o criador de conteúdo deve falar.  
"""

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        st.subheader("📑 Roteiro Gerado")
        roteiro_final = mostrar_com_streaming(response.text)

        # Botão para copiar
        st.text_area("✂️ Copiar Roteiro:", roteiro_final, height=300)
        st.info("Você pode selecionar e copiar o roteiro acima.")

elif tipo_video == "Comparação de produtos":
    st.subheader("🔀 Comparação de Produtos")

    produto1 = st.text_area("📝 Roteiro do Produto 1 (já existente)")
    produto2 = st.text_area("📝 Roteiro do Produto 2 (já existente)")
    publico_alvo = st.text_input("Público-alvo")
    objetivo = st.text_input("Objetivo da comparação (ex: descobrir qual é melhor para jogos)")

    gerar_comp = st.button("🎬 Gerar Roteiro de Comparação com Gemini")

    if gerar_comp:
        prompt = f"""
Compare dois produtos com base nos roteiros abaixo, criando um novo roteiro de vídeo em formato de tópicos.  
⚠️ Não inclua timings por seção.

### Público-alvo: {publico_alvo}
### Objetivo da comparação: {objetivo}

### Roteiro do Produto 1:
{produto1}

### Roteiro do Produto 2:
{produto2}

### Instruções importantes para a IA:
- Analise o contexto e deduza automaticamente os pontos fortes e fracos de cada produto.  
- Adicione tópicos específicos e relevantes de acordo com o tipo de produto (ex: bateria para notebook, som para headset, câmeras para smartphone).  
- Estruture a comparação de forma clara, com pontos lado a lado quando possível.  
- Use linguagem natural, tópicos diretos e lembretes claros do que o criador deve comentar.  
"""

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        st.subheader("📑 Roteiro Gerado")
        roteiro_final = mostrar_com_streaming(response.text)

        # Botão para copiar
        st.text_area("✂️ Copiar Roteiro:", roteiro_final, height=300)
        st.info("Você pode selecionar e copiar o roteiro acima.")
