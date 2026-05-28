class AnalysisSelector:

    def __init__(self):
        self.available_analyses = {
            "1": "estatistica",
            "2": "anova",
            "3": "pca",
            "4": "kmeans",
            "5": "graficos",
            "6": "relatorio_word",
            "7": "umap",
            "8": "hdbscan",
            "9": "exportacao"
        }

        self.assisted_default = [
            "estatistica",
            "anova",
            "pca",
            "kmeans",
            "graficos",
            "relatorio_word"
        ]

    def show_modes(self):

        print("\n===================================")
        print("ATHENA ANALYTICS - MODO DE ANÁLISE")
        print("===================================")
        print("[1] Automático - executa tudo")
        print("[2] Assistido - ATHENA sugere e você confirma/escolhe")
        print("[3] Expert - você escolhe manualmente")

        choice = input("\nEscolha o modo: ").strip()

        if choice == "2":
            return self.assisted_mode()

        if choice == "3":
            return self.expert_mode()

        return self.auto_mode()

    def auto_mode(self):

        print("\nModo automático selecionado.")
        return {
            "mode": "auto",
            "analyses": list(self.available_analyses.values())
        }

    def assisted_mode(self):

        print("\nModo assistido selecionado.")
        print("\nSugestão do ATHENA:")
        print(self.assisted_default)

        confirm = input(
            "\nDigite S para aceitar a sugestão ou N para escolher manualmente: "
        ).strip().lower()

        if confirm == "s":
            analyses = self.assisted_default

        else:
            analyses = self.choose_analyses()

        return {
            "mode": "assisted",
            "analyses": analyses
        }

    def expert_mode(self):

        print("\nModo expert selecionado.")
        analyses = self.choose_analyses()

        return {
            "mode": "expert",
            "analyses": analyses
        }

    def choose_analyses(self):

        print("\nEscolha as análises:")

        for key, value in self.available_analyses.items():
            print(f"[{key}] {value}")

        selected = input(
            "\nDigite os números separados por vírgula. Exemplo: 1,3,6: "
        ).strip()

        selected_keys = [
            item.strip()
            for item in selected.split(",")
            if item.strip() in self.available_analyses
        ]

        analyses = [
            self.available_analyses[key]
            for key in selected_keys
        ]

        print("\nAnálises realmente selecionadas:")
        print(analyses)

        return analyses
