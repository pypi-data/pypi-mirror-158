import dataclasses
import json
import rbo
from typing import Dict, List

from esqa.save import Ranking


@dataclasses.dataclass
class FailedRanking:
    name: str
    similarity: float
    ranking_pair: List[tuple]


def load_rankings(path: str) -> Dict:
    with open(path) as f:
        rankings = json.load(f)
    results = {}
    for ranking in rankings:
        results[ranking["name"]] = Ranking(
            ranking["name"], ranking["request"], ranking["ranking"]
        )
    return results


def _extract(ranking: Ranking, target_field: str) -> List[str]:
    return [e["source"][target_field] for e in ranking.ranking]


def _compare(ranking_a, ranking_b):
    return rbo.rbo.RankingSimilarity(ranking_a, ranking_b).rbo()


def _generate(
    ranking_a: Ranking, ranking_b: Ranking, similarity: float, target_field: str
):
    return FailedRanking(
        name=ranking_a.name,
        similarity=similarity,
        ranking_pair=list(
            zip(_extract(ranking_a, target_field), _extract(ranking_b, target_field))
        ),
    )


def compare_rankings(
    rankings_a: Dict[str, Ranking],
    rankings_b: Dict[str, Ranking],
    threshold: float,
    target_field: str,
) -> List[FailedRanking]:
    results = []
    for ranking_name in rankings_a:
        similarity = _compare(
            _extract(rankings_a[ranking_name], target_field),
            _extract(rankings_b[ranking_name], target_field),
        )
        if similarity > threshold:
            continue
        results.append(
            _generate(
                rankings_a[ranking_name],
                rankings_b[ranking_name],
                similarity,
                target_field,
            )
        )
    return results
