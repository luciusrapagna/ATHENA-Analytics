class AutoInterpretationEngine:

    def generate_basic_interpretation(
        self,
        numeric_columns
    ):

        interpretation = []

        interpretation.append(
            "Os resultados demonstraram variabilidade entre as variáveis numéricas avaliadas."
        )

        interpretation.append(
            f"Foram detectadas {len(numeric_columns)} variáveis quantitativas para análise estatística."
        )

        interpretation.append(
            "As análises automáticas executadas pelo ATHENA incluíram estatística descritiva, agrupamentos multivariados e exploração dimensional."
        )

        return "\n\n".join(interpretation)
