RESULT_TYPES = {
    "explorer": {
        "name": "자유로운 탐험가", "english": "THE ADVENTURER",
        "description": "새로운 경험을 즐기고 호기심이 많아요. 정해진 길보다는 자신만의 길을 찾는 것을 좋아하고, 예상하지 못한 순간에서도 즐거움을 발견하는 편이에요.",
        "keywords": ["호기심", "자유로움", "도전"], "quote": "세상에는 아직 발견하지 못한 길이 너무 많아!"
    },
    "observer": {
        "name": "차분한 관찰자", "english": "THE OBSERVER",
        "description": "주변을 세심하게 살피고 충분히 생각한 뒤 움직여요. 혼자만의 시간과 익숙한 안정감 속에서 자신만의 리듬을 찾는 편이에요.",
        "keywords": ["신중함", "섬세함", "차분함"], "quote": "천천히 바라보면 더 많은 것이 보여."
    },
    "supporter": {
        "name": "따뜻한 조력자", "english": "THE SUPPORTER",
        "description": "사람들의 마음을 잘 살피고 관계 속에서 따뜻함을 나눠요. 함께하는 순간을 소중히 여기며 주변에 편안한 분위기를 만들어 주는 편이에요.",
        "keywords": ["공감", "배려", "친밀함"], "quote": "함께라면 어떤 길도 조금 더 따뜻해져."
    },
    "strategist": {
        "name": "계획적인 전략가", "english": "THE STRATEGIST",
        "description": "목표를 세우고 차근차근 실행하는 것을 좋아해요. 문제를 만났을 때 원인을 파악하고 현실적인 해결 방법을 찾는 데 강점이 있어요.",
        "keywords": ["계획성", "논리", "집중력"], "quote": "좋은 길은 작은 계획에서 시작돼."
    },
    "dreamer": {
        "name": "감성적인 몽상가", "english": "THE DREAMER",
        "description": "일상 속에서도 자신만의 의미와 아름다움을 발견해요. 변화하는 분위기를 유연하게 받아들이고 상상력을 더해 특별한 순간을 만드는 편이에요.",
        "keywords": ["감수성", "상상력", "유연함"], "quote": "평범한 하루에도 작은 마법은 숨어 있어."
    },
}

def calculate_result(answers):
    # 각 문항은 특정 성향 축을 측정합니다. 5문항 결과를 합산해 가장 가까운 유형을 결정합니다.
    scores = {key: 0 for key in RESULT_TYPES}
    mapping = [
        {"A": "observer", "B": "supporter"},
        {"A": "strategist", "B": "explorer"},
        {"A": "strategist", "B": "supporter"},
        {"A": "observer", "B": "explorer"},
        {"A": "strategist", "B": "dreamer"},
    ]
    for index, answer in enumerate(answers[:5]):
        scores[mapping[index][answer]] += 1
    # 동점일 경우 마지막 응답과 가장 관련 있는 유형을 우선합니다.
    highest = max(scores.values())
    tied = [key for key, value in scores.items() if value == highest]
    if len(tied) > 1 and answers:
        last_pick = mapping[min(len(answers), 5)-1][answers[min(len(answers), 5)-1]]
        if last_pick in tied:
            winner = last_pick
        else:
            winner = tied[0]
    else:
        winner = tied[0]
    return RESULT_TYPES[winner]
