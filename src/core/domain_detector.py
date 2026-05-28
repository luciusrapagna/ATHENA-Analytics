def detect_domain(df):
    columns = [str(c).lower() for c in df.columns]

    domain_keywords = {
        "enamed": [
            "aluno", "turma", "período", "periodo", "acertos",
            "clínica médica", "pediatria", "cirurgia",
            "gineco", "saúde coletiva", "enamed", "teste de progresso"
        ],
        "epidemiology": [
            "casos", "incidência", "incidencia", "prevalência",
            "prevalencia", "óbitos", "obitos", "risco",
            "município", "municipio", "sexo", "idade"
        ],
        "ecology": [
            "espécie", "especie", "abundância", "abundancia",
            "riqueza", "diversidade", "shannon", "biomassa",
            "local", "estação", "estacao"
        ],
        "biomarkers": [
            "gst", "cat", "sod", "ache", "lpo", "mda",
            "proteína", "proteina", "biomarcador", "enzima"
        ],
        "environmental": [
            "temperatura", "ph", "salinidade", "oxigênio",
            "oxigenio", "turbidez", "nitrato", "fosfato",
            "metal", "mercúrio", "mercurio"
        ],
        "oceanography": [
            "salinidade", "clorofila", "batimetria", "corrente",
            "vento", "onda", "upwelling", "ressurgência",
            "ressurgencia"
        ],
        "medical_education": [
            "disciplina", "competência", "competencia", "habilidade",
            "nota", "avaliação", "avaliacao", "docente",
            "discente", "módulo", "modulo"
        ]
    }

    scores = {}

    for domain, keywords in domain_keywords.items():
        score = 0

        for col in columns:
            for keyword in keywords:
                if keyword in col:
                    score += 1

        scores[domain] = score

    best_domain = max(scores, key=scores.get)

    if scores[best_domain] == 0:
        return "general"

    return best_domain