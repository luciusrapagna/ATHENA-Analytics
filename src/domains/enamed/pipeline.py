from src.core.analysis_recommender import recommend_analyses


def run_enamed_pipeline(df):

    print("\nPipeline ENAMED iniciado")

    analyses = recommend_analyses(
        df,
        domain="enamed"
    )

    return {
        "domain": "enamed",
        "recommended_analyses": analyses
    }