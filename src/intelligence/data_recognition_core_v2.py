from src.domains.flow_environmental_keywords import FLOW_ENVIRONMENTAL_KEYWORDS
import pandas as pd
import numpy as np


class DataRecognitionCoreV2:

    def __init__(self):
        self.trash_patterns = [
            "unnamed", "sem nome", "index", "level_0"
        ]

        self.id_patterns = [
            "id", "codigo", "código", "matricula", "matrícula",
            "aluno", "nome", "cpf", "ra", "registro"
        ]

        self.group_patterns = [
            "grupo", "turma", "periodo", "período", "curso",
            "instituicao", "instituição", "sexo", "gênero", "genero",
            "local", "area", "área", "tratamento", "classe",
            "categoria", "semestre", "ano", "campus", "turno"
        ]

        self.education_patterns = [
            "nota", "média", "media", "desempenho", "acerto",
            "acertos", "percentual", "frequência", "frequencia",
            "evasão", "evasao", "retenção", "retencao",
            "aprovação", "aprovacao", "reprovação", "reprovacao",
            "disciplina", "competência", "competencia",
            "habilidade", "currículo", "curriculo", "matriz",
            "percepção", "percepcao", "satisfação", "satisfacao",
            "engajamento", "aprendizagem", "metodologia",
            "pbl", "tbl", "simulado", "enade", "enamed",
            "teste de progresso", "progresso", "avaliação",
            "avaliacao", "extensão", "extensao", "monitoria",
            "internato", "ciclo básico", "ciclo basico",
            "ciclo clínico", "ciclo clinico"
        ]

        self.domain_keywords = {
            "educacao": self.education_patterns,

            "educacao_medica": [
                "medicina", "enamed", "enade", "teste de progresso",
                "simulado", "internato", "pbl", "tbl",
                "clínica médica", "clinica medica", "pediatria",
                "cirurgia", "gineco", "obstetrícia",
                "saúde coletiva", "bases biomédicas",
                "competência médica", "habilidade médica"
            ],

            "avaliacao_institucional": [
                "cpa", "avaliação institucional", "avaliacao institucional",
                "satisfação", "satisfacao", "percepção", "percepcao",
                "docente", "discente", "infraestrutura",
                "coordenação", "coordenacao", "curso", "instituição"
            ],

            "saude_mental_discente": [
                "ansiedade", "estresse", "burnout", "depressão",
                "depressao", "qualidade de vida", "bem-estar",
                "sono", "procrastinação", "procrastinacao",
                "coping", "resiliência", "resiliencia"
            ],

            "extensao_universitaria": [
                "extensão", "extensao", "projeto integrador",
                "comunidade", "território", "territorio",
                "ubs", "sus", "pse", "ação extensionista",
                "acao extensionista", "ensino-serviço-comunidade"
            ],

            "enamed": [
                "clínica médica", "clinica medica", "pediatria",
                "cirurgia", "gineco", "obstetrícia",
                "saúde coletiva", "periodo", "período", "turma"
            ],

            "epidemiologia": [
                "casos", "incidência", "incidencia", "prevalência",
                "prevalencia", "mortalidade", "letalidade",
                "município", "municipio", "ano", "semana epidemiológica"
            ],

            "ecologia": [
                "espécie", "especie", "abundância", "abundancia",
                "biomassa", "diversidade", "riqueza", "local",
                "ponto", "estação", "estacao"
            ],

            "oceanografia": [
                "temperatura", "salinidade", "oxigênio", "oxigenio",
                "profundidade", "ph", "clorofila", "nutrientes",
                "estação", "estacao"
            ]
        }

    def normalize_name(self, name):
        return str(name).strip().lower()

    def identify_trash_columns(self, df):
        return [
            col for col in df.columns
            if any(p in self.normalize_name(col) for p in self.trash_patterns)
            or df[col].isna().all()
        ]

    def identify_id_columns(self, df):
        return [
            col for col in df.columns
            if any(p in self.normalize_name(col) for p in self.id_patterns)
        ]

    def identify_numeric_columns(self, df):
        return df.select_dtypes(include=[np.number]).columns.tolist()

    def identify_categorical_columns(self, df):
        return df.select_dtypes(include=["object", "category"]).columns.tolist()

    def identify_group_candidates(self, df):
        candidates = []

        for col in df.columns:
            col_norm = self.normalize_name(col)
            unique_count = df[col].nunique(dropna=True)

            if any(p in col_norm for p in self.group_patterns):
                candidates.append({
                    "column": col,
                    "reason": "nome compatível com agrupamento",
                    "unique_values": int(unique_count)
                })

            elif 2 <= unique_count <= 25 and df[col].dtype == "object":
                candidates.append({
                    "column": col,
                    "reason": "baixa cardinalidade categórica",
                    "unique_values": int(unique_count)
                })

        return candidates

    def detect_best_group_column(self, df):
        candidates = self.identify_group_candidates(df)

        if not candidates:
            return None

        priority = [
            "período", "periodo", "turma", "curso", "semestre",
            "grupo", "instituição", "instituicao", "campus",
            "turno", "sexo", "gênero", "genero"
        ]

        for p in priority:
            for c in candidates:
                if p in self.normalize_name(c["column"]):
                    return c["column"]

        return candidates[0]["column"]

    def detect_domain(self, df):
        columns_text = " ".join([self.normalize_name(c) for c in df.columns])

        scores = {}

        for domain, keywords in self.domain_keywords.items():
            scores[domain] = sum(
                1 for keyword in keywords
                if keyword in columns_text
            )

        best_domain = max(scores, key=scores.get)

        if scores[best_domain] == 0:
            return {
                "domain": "generic",
                "confidence": 0,
                "scores": scores
            }

        confidence = scores[best_domain] / max(
            1, len(self.domain_keywords[best_domain])
        )

        return {
            "domain": best_domain,
            "confidence": round(confidence, 3),
            "scores": scores
        }

    def classify_educational_variables(self, df):
        categories = {
            "performance_variables": [],
            "attendance_variables": [],
            "perception_variables": [],
            "curricular_variables": [],
            "mental_health_variables": [],
            "extension_variables": []
        }

        mapping = {
            "performance_variables": [
                "nota", "média", "media", "desempenho",
                "acerto", "acertos", "percentual", "score"
            ],
            "attendance_variables": [
                "frequência", "frequencia", "presença",
                "presenca", "faltas"
            ],
            "perception_variables": [
                "percepção", "percepcao", "satisfação",
                "satisfacao", "opinião", "opiniao",
                "avaliação", "avaliacao"
            ],
            "curricular_variables": [
                "disciplina", "competência", "competencia",
                "habilidade", "matriz", "currículo", "curriculo",
                "ciclo", "período", "periodo"
            ],
            "mental_health_variables": [
                "ansiedade", "estresse", "burnout", "depressão",
                "depressao", "sono", "bem-estar"
            ],
            "extension_variables": [
                "extensão", "extensao", "projeto integrador",
                "comunidade", "ubs", "sus", "pse"
            ]
        }

        for col in df.columns:
            col_norm = self.normalize_name(col)

            for category, keywords in mapping.items():
                if any(k in col_norm for k in keywords):
                    categories[category].append(col)

        return categories

    def recommend_educational_analyses(self, df):
        edu_vars = self.classify_educational_variables(df)
        group_col = self.detect_best_group_column(df)

        recommendations = []

        if edu_vars["performance_variables"]:
            recommendations += [
                "estatística descritiva de desempenho",
                "ranking por turma/período",
                "boxplot de desempenho por grupo",
                "ANOVA ou Kruskal-Wallis entre grupos",
                "análise de risco acadêmico"
            ]

        if edu_vars["attendance_variables"]:
            recommendations += [
                "correlação entre frequência e desempenho",
                "análise de faltas por turma/período"
            ]

        if edu_vars["perception_variables"]:
            recommendations += [
                "análise de satisfação/percepção discente",
                "escala Likert por domínio",
                "mapa de calor de percepção"
            ]

        if edu_vars["mental_health_variables"]:
            recommendations += [
                "análise de saúde mental discente",
                "correlação entre sofrimento psíquico e desempenho",
                "comparação por período/turma"
            ]

        if edu_vars["extension_variables"]:
            recommendations += [
                "análise de impacto extensionista",
                "indicadores ensino-serviço-comunidade",
                "síntese de produtos extensionistas"
            ]

        if group_col:
            recommendations.append(f"estratificação automática por {group_col}")

        return recommendations

    def classify_columns(self, df):
        trash = self.identify_trash_columns(df)
        ids = self.identify_id_columns(df)
        numeric = self.identify_numeric_columns(df)
        categorical = self.identify_categorical_columns(df)
        group = self.detect_best_group_column(df)

        dependent_candidates = [
            col for col in numeric
            if col not in trash and col not in ids
        ]

        return {
            "trash_columns": trash,
            "id_columns": ids,
            "numeric_columns": numeric,
            "categorical_columns": categorical,
            "group_column": group,
            "dependent_candidates": dependent_candidates,
            "educational_variables": self.classify_educational_variables(df)
        }

    def data_quality_report(self, df):
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_total": int(df.isna().sum().sum()),
            "missing_percent": round(float(df.isna().sum().sum() / df.size * 100), 2),
            "duplicated_rows": int(df.duplicated().sum())
        }

    def run(self, df):
        domain = self.detect_domain(df)

        return {
            "domain_detection": domain,
            "column_classification": self.classify_columns(df),
            "group_candidates": self.identify_group_candidates(df),
            "educational_analysis_recommendations": self.recommend_educational_analyses(df),
            "data_quality": self.data_quality_report(df)
        }


