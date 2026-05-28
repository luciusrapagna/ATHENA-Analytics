class MethodologicalAdvisor:

    def __init__(self):

        self.explanations = {

            "enamed": {
                "estatistica": "Resumir o desempenho geral dos estudantes por média, mediana, dispersão e variação.",
                "anova": "Comparar o desempenho entre períodos, turmas ou grupos acadêmicos.",
                "pressupostos_posthoc": "Verificar normalidade, homogeneidade e identificar quais grupos diferem após o teste global.",
                "pca": "Identificar padrões de desempenho entre grandes áreas e reduzir a dimensionalidade dos resultados.",
                "kmeans": "Detectar perfis de estudantes ou turmas com padrões semelhantes de desempenho.",
                "graficos": "Visualizar diferenças entre grupos e facilitar a interpretação institucional.",
                "relatorio_word": "Gerar relatório científico automático com resultados e interpretação."
            },

            "educacao": {
                "estatistica": "Descrever desempenho, frequência, percepção, satisfação ou indicadores educacionais.",
                "anova": "Comparar médias entre turmas, cursos, períodos, metodologias ou grupos.",
                "pressupostos_posthoc": "Garantir validade estatística dos testes e indicar diferenças específicas entre grupos.",
                "pca": "Reduzir múltiplos indicadores educacionais em componentes interpretáveis.",
                "kmeans": "Agrupar estudantes, turmas ou cursos com perfis semelhantes.",
                "graficos": "Comunicar padrões educacionais de forma visual.",
                "relatorio_word": "Documentar achados em formato acadêmico."
            },

            "educacao_medica": {
                "estatistica": "Sintetizar desempenho acadêmico e indicadores formativos.",
                "anova": "Comparar desempenho entre períodos, ciclos, turmas ou estratégias pedagógicas.",
                "pressupostos_posthoc": "Verificar pressupostos da ANOVA e aplicar Tukey ou Dunn quando necessário.",
                "pca": "Identificar padrões integrados entre áreas médicas e competências.",
                "kmeans": "Detectar perfis de estudantes, turmas ou ciclos formativos.",
                "graficos": "Produzir evidências visuais para gestão pedagógica.",
                "relatorio_word": "Gerar relatório institucional e científico."
            },

            "epidemiologia": {
                "estatistica": "Descrever casos, taxas, incidência, prevalência e distribuição temporal ou espacial.",
                "anova": "Comparar indicadores epidemiológicos entre municípios, anos, grupos ou regiões.",
                "pressupostos_posthoc": "Avaliar validade dos testes e localizar diferenças entre grupos.",
                "pca": "Reduzir variáveis socioambientais ou epidemiológicas correlacionadas.",
                "kmeans": "Agrupar territórios ou períodos com perfis epidemiológicos semelhantes.",
                "umap": "Revelar agrupamentos não lineares em dados epidemiológicos complexos.",
                "hdbscan": "Detectar clusters epidemiológicos sem definir previamente o número de grupos.",
                "graficos": "Visualizar padrões temporais, espaciais e comparativos.",
                "relatorio_word": "Gerar síntese técnica dos achados epidemiológicos."
            },

            "ecologia": {
                "estatistica": "Descrever abundância, biomassa, riqueza, diversidade e variabilidade ecológica.",
                "pca": "Explorar gradientes ambientais e padrões multivariados.",
                "similaridade": "Avaliar semelhança entre amostras, locais ou comunidades usando matrizes ecológicas.",
                "umap": "Detectar padrões não lineares em comunidades ecológicas.",
                "hdbscan": "Identificar grupos ecológicos naturais e possíveis outliers.",
                "graficos": "Representar padrões ecológicos de forma interpretável.",
                "relatorio_word": "Documentar os resultados ecológicos automaticamente."
            },

            "oceanografia": {
                "estatistica": "Descrever variáveis oceanográficas como temperatura, salinidade, oxigênio, clorofila e nutrientes.",
                "pca": "Identificar gradientes oceanográficos e reduzir variáveis ambientais correlacionadas.",
                "similaridade": "Comparar estações, campanhas ou massas d’água com base em similaridade multivariada.",
                "umap": "Revelar padrões não lineares em séries oceanográficas complexas.",
                "hdbscan": "Detectar agrupamentos naturais de estações ou condições oceanográficas.",
                "graficos": "Visualizar gradientes e padrões ambientais.",
                "relatorio_word": "Gerar relatório técnico-científico oceanográfico."
            },

            "citometria_ambiental": {
                "estatistica": "Descrever abundância celular, fluorescência, FSC/SSC e variáveis citométricas.",
                "pca": "Identificar padrões globais entre populações celulares ou sinais de fluorescência.",
                "similaridade": "Comparar amostras ambientais por composição citométrica e estrutura microbiana.",
                "umap": "Separar populações ou assinaturas citométricas complexas.",
                "hdbscan": "Detectar agrupamentos celulares ou ambientais sem número fixo de clusters.",
                "graficos": "Gerar visualizações de padrões celulares e ambientais.",
                "relatorio_word": "Documentar interpretações citométricas ambientais."
            },

            "generic": {
                "estatistica": "Descrever as variáveis principais do conjunto de dados.",
                "anova": "Comparar grupos quando houver variável categórica adequada.",
                "pressupostos_posthoc": "Verificar pressupostos e diferenças específicas entre grupos.",
                "pca": "Explorar padrões multivariados gerais.",
                "kmeans": "Agrupar observações com características semelhantes.",
                "graficos": "Facilitar a interpretação visual dos resultados.",
                "relatorio_word": "Gerar relatório automático dos achados."
            }
        }

    def explain_plan(self, domain, analyses):

        domain = domain if domain in self.explanations else "generic"

        print("\n===================================")
        print("ATHENA METHODOLOGICAL ADVISOR")
        print("===================================")
        print(f"\nDomínio detectado: {domain.upper()}")

        for analysis in analyses:

            explanation = self.explanations.get(
                domain,
                self.explanations["generic"]
            ).get(
                analysis,
                "Análise complementar recomendada para exploração do conjunto de dados."
            )

            print(f"\nPor que {analysis}?")
            print(f"→ {explanation}")

        print("\nDeseja executar este plano?")
        print("[1] Sim")
        print("[2] Personalizar")

        choice = input("\nOpção: ").strip()

        return choice
