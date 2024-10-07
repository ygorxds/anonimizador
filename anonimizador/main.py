import spacy
import re
import pandas as pd
import streamlit as st
from spacy.util import filter_spans

# Carregar o modelo de linguagem em português
nlp = spacy.load("pt_core_news_sm")

def mask_entities_and_contacts(text):
    """
    Esta função anonimiza informações sensíveis em um texto fornecido.

    Args:
        text (str): O texto a ser processado.

    Returns:
        tuple: Texto anonimizado, lista de entidades encontradas e o objeto doc do spaCy.
    """
    doc = nlp(text)
    spans = []
    entities_found = []

    # Iterar sobre as entidades reconhecidas pelo modelo do spaCy
    for ent in doc.ents:
        if ent.label_ in ["PER", "ORG", "LOC", "GPE"]:  # Labels em português
            spans.append((ent.start_char, ent.end_char))
            entities_found.append({'text': ent.text, 'label': ent.label_})

    # Padrões para CPF, CNPJ, RG, telefones, emails, passaporte e cartão de crédito
    patterns = [
        # Padrão para CPF com e sem pontuação, e com ou sem "CPF" ou "CPF:"
        {'label': 'CPF', 'pattern': r'\b(?:CPF[:\s]*)?(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})\b'},
        # Padrão para RG com e sem pontuação
        {'label': 'RG', 'pattern': r'\b(?:RG[:\s]*)?(?:\d{2}\.\d{3}\.\d{3}-\d{1}|\d{9})\b'},
        {'label': 'CNPJ', 'pattern': r'\b(?:CNPJ[:\s]*)?\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'},
        {'label': 'TELEFONE', 'pattern': r'\b(?:telefone[:\s]*)?(\(?\d{2}\)?\s*)?9?\d{4}-\d{4}\b'},
        {'label': 'EMAIL', 'pattern': r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b'},
        {'label': 'PASSAPORTE', 'pattern': r'\b[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]\b'},  # Padrão para passaportes internacionais comuns
        {'label': 'CARTÃO DE CRÉDITO', 'pattern': r'\b(?:\d{4}[-\s]?){3}\d{4}\b'},  # Padrão para cartões de crédito
    ]

    new_ents = list(doc.ents)
    for item in patterns:
        for match in re.finditer(item['pattern'], text, flags=re.IGNORECASE):
            span = doc.char_span(match.start(), match.end(), label=item['label'])
            if span is not None:
                new_ents.append(span)
                entities_found.append({'text': span.text, 'label': span.label_})
                spans.append((span.start_char, span.end_char))

    filtered_ents = filter_spans(new_ents)
    doc.ents = filtered_ents

    spans = sorted(spans, key=lambda x: x[0])
    merged_spans = []
    for span in spans:
        if not merged_spans:
            merged_spans.append(span)
        else:
            last_span = merged_spans[-1]
            if span[0] <= last_span[1]:
                new_span = (last_span[0], max(last_span[1], span[1]))
                merged_spans[-1] = new_span
            else:
                merged_spans.append(span)

    masked_text = ''
    last_idx = 0
    for start, end in merged_spans:
        masked_text += text[last_idx:start]
        masked_text += '********'
        last_idx = end
    masked_text += text[last_idx:]

    return masked_text, entities_found, doc


def process_spreadsheet(file):
    """
    Processa uma planilha carregada e anonimiza as informações sensíveis.

    Args:
        file: Arquivo de planilha carregado pelo usuário.

    Returns:
        DataFrame: DataFrame com os dados anonimizados.
    """
    # Ler o arquivo dependendo de sua extensão
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        st.error("Formato de arquivo não suportado. Por favor, carregue um arquivo .xlsx ou .csv.")
        return None

    anonymized_df = df.copy()

    for col in anonymized_df.columns:
        anonymized_df[col] = anonymized_df[col].apply(
            lambda x: mask_entities_and_contacts(str(x))[0] if isinstance(x, str) else x
        )

    return anonymized_df


def main():
    st.title("Anonimizador de Informações Sensíveis")
    st.write("Este aplicativo anonimiza informações pessoais em planilhas.")

    uploaded_file = st.file_uploader("Carregar planilha", type=["xlsx", "csv"])
    if uploaded_file is not None:
        anonymized_df = process_spreadsheet(uploaded_file)
        if anonymized_df is not None:
            st.subheader("Planilha Anonimizada")
            st.dataframe(anonymized_df)

            # Salvar a planilha anonimizada como um arquivo Excel temporário
            output_name = "planilha_anonimizada.xlsx"
            anonymized_df.to_excel(output_name, index=False)

            # Oferecer o download do arquivo anonimizado
            with open(output_name, "rb") as file:
                st.download_button(
                    label="Baixar Planilha Anonimizada",
                    data=file.read(),
                    file_name=output_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        else:
            st.warning("Erro ao processar a planilha. Verifique o formato do arquivo.")

if __name__ == "__main__":
    main()
