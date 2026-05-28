from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


class SemanticScientificEngine:

    def __init__(self):

        print("[ATHENA AI] Carregando modelo semântico...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.scientific_concepts = {

            "educacao_medica": [
                "desempenho acadêmico",
                "teste de progresso",
                "ENAMED",
                "PBL",
                "TBL",
                "competência médica",
                "avaliação institucional",
                "aprendizagem"
            ],

            "epidemiologia": [
                "incidência",
                "prevalência",
                "mortalidade",
                "casos",
                "risco epidemiológico"
            ],

            "ecologia": [
                "diversidade",
                "abundância",
                "riqueza de espécies",
                "ecossistema",
                "biomassa"
            ],

            "oceanografia": [
                "salinidade",
                "temperatura",
                "clorofila",
                "produtividade primária",
                "nutrientes"
            ],

            "citometria_ambiental": [
                "citometria de fluxo",
                "fitoplâncton",
                "bacterioplâncton",
                "fluorescência",
                "chlorophyll fluorescence",
                "microbial abundance"
            ]
        }

        self.concept_embeddings = {}

        for domain, concepts in self.scientific_concepts.items():

            self.concept_embeddings[domain] = (
                self.model.encode(concepts)
            )

    def detect_semantic_domain(
        self,
        columns
    ):

        column_text = " ".join(columns)

        column_embedding = self.model.encode(
            [column_text]
        )

        scores = {}

        for domain, embeddings in (
            self.concept_embeddings.items()
        ):

            similarity = cosine_similarity(
                column_embedding,
                embeddings
            )

            scores[domain] = float(
                np.mean(similarity)
            )

        best_domain = max(
            scores,
            key=scores.get
        )

        return {
            "semantic_domain": best_domain,
            "confidence": round(
                scores[best_domain],
                4
            ),
            "all_scores": scores
        }

    def infer_column_meaning(
        self,
        columns
    ):

        interpretations = {}

        semantic_library = {

            "desempenho": [
                "nota",
                "score",
                "acertos",
                "percentual"
            ],

            "agrupamento": [
                "turma",
                "grupo",
                "período",
                "campus"
            ],

            "variável ambiental": [
                "salinity",
                "temperature",
                "oxygen",
                "chlorophyll"
            ],

            "citometria": [
                "fsc",
                "ssc",
                "fluorescence",
                "mfi"
            ]
        }

        for col in columns:

            col_embedding = self.model.encode(
                [col]
            )

            best_match = None
            best_score = -1

            for concept, examples in (
                semantic_library.items()
            ):

                example_embeddings = (
                    self.model.encode(examples)
                )

                similarity = cosine_similarity(
                    col_embedding,
                    example_embeddings
                )

                score = float(
                    np.mean(similarity)
                )

                if score > best_score:
                    best_score = score
                    best_match = concept

            interpretations[col] = {
                "semantic_meaning": best_match,
                "confidence": round(best_score, 4)
            }

        return interpretations

    def run(self, df):

        columns = [
            str(c)
            for c in df.columns
        ]

        return {

            "semantic_domain_detection":
                self.detect_semantic_domain(
                    columns
                ),

            "semantic_column_interpretation":
                self.infer_column_meaning(
                    columns
                )
        }
