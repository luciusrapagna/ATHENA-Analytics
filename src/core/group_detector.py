def detect_group_column(df):

    possible_group_names = [

        "grupo",
        "group",

        "turma",
        "classe",

        "período",
        "periodo",

        "tratamento",

        "espécie",
        "especie",

        "local",

        "campus",

        "instituição",
        "instituicao",

        "cluster",

        "sexo",

        "categoria"
    ]

    for column in df.columns:

        col = str(column).lower()

        for keyword in possible_group_names:

            if keyword in col:
                return column

    return None