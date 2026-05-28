from src.core.domain_detector import detect_domain
from src.core.analysis_recommender import recommend_analyses


def route_pipeline(df):
    domain = detect_domain(df)

    print(f"\nDomínio detectado: {domain}")

    analyses = recommend_analyses(
        df,
        domain=domain
    )

    return {
        "domain": domain,
        "recommended_analyses": analyses,
        "status": "pipeline executado"
    }