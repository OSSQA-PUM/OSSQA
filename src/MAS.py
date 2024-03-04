
def analyze_sbom(sbom: dict, requirements: list[float]):
    score_dict = SSFAnalyser.analyse(sbom)
    score = FSC(score_dict, requirements)
    return score


def get_old_results(sbom: dict):
    name = sbom['metadata']['name']+ sbom['metadata']['version']
    old_results = BackendAPI.get_old_results(name)
    return old_results
    pass
