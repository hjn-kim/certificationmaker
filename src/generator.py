"""Content generation logic using Gemini API for certification prep books."""

from src.gemini_client import generate_content


PROMPTS = {
    "outline": (
        "당신은 자격증 시험 전문가입니다. '{cert}' 자격증 시험에 대한 대비서의 목차를 작성해주세요.\n"
        "다음 형식으로 작성해주세요:\n"
        "- 총 5~8개의 챕터로 구성\n"
        "- 각 챕터에는 2~4개의 소단원 포함\n"
        "- 마지막 챕터는 반드시 '기출문제 및 모의고사'로 구성\n\n"
        "형식:\n"
        "제1장: [챕터명]\n"
        "  1.1 [소단원명]\n"
        "  1.2 [소단원명]\n"
        "...\n\n"
        "목차만 출력하고 다른 설명은 하지 마세요."
    ),
    "theory": (
        "당신은 '{cert}' 자격증 시험 전문 강사입니다.\n"
        "다음 챕터에 대한 이론 내용을 상세하게 작성해주세요:\n\n"
        "챕터: {chapter}\n\n"
        "작성 지침:\n"
        "- 시험에 자주 출제되는 핵심 개념을 중심으로 설명\n"
        "- 각 소단원별로 명확한 제목을 붙이고 내용을 작성\n"
        "- 중요한 용어나 공식은 별도로 강조\n"
        "- 이해를 돕는 예시를 포함\n"
        "- 실무 관점에서의 설명도 추가\n"
        "- 마크다운 기호(*, #, ``` 등)를 사용하지 말고 일반 텍스트로만 작성\n"
        "- 소제목은 [소제목] 형식으로, 강조는 <<강조내용>> 형식으로 표시\n"
    ),
    "questions": (
        "당신은 '{cert}' 자격증 시험 출제위원입니다.\n"
        "다음 범위에서 기출문제 스타일의 문제를 20문항 만들어주세요:\n\n"
        "범위: {chapters}\n\n"
        "작성 지침:\n"
        "- 객관식 4지선다형으로 출제\n"
        "- 난이도는 쉬움 5문항, 보통 10문항, 어려움 5문항으로 구성\n"
        "- 실제 시험과 유사한 형식으로 작성\n"
        "- 마크다운 기호(*, #, ``` 등)를 사용하지 말고 일반 텍스트로만 작성\n\n"
        "형식:\n"
        "문제 1. [문제 내용]\n"
        "  (1) [보기1]\n"
        "  (2) [보기2]\n"
        "  (3) [보기3]\n"
        "  (4) [보기4]\n\n"
        "문제만 출력하고 정답은 포함하지 마세요."
    ),
    "answers": (
        "당신은 '{cert}' 자격증 시험 출제위원입니다.\n"
        "다음 문제들의 정답과 상세한 해설을 작성해주세요:\n\n"
        "{questions}\n\n"
        "작성 지침:\n"
        "- 각 문제의 정답 번호를 먼저 제시\n"
        "- 왜 해당 보기가 정답인지 상세히 설명\n"
        "- 오답인 보기들에 대해서도 간단히 왜 틀렸는지 설명\n"
        "- 관련 핵심 개념을 한 줄로 요약\n"
        "- 마크다운 기호(*, #, ``` 등)를 사용하지 말고 일반 텍스트로만 작성\n\n"
        "형식:\n"
        "문제 1. 정답: (번호)\n"
        "[해설]\n"
        "핵심 개념: [한줄 요약]\n"
    ),
}


def generate_outline(model, cert_name: str) -> str:
    """Generate table of contents for the certification prep book."""
    prompt = PROMPTS["outline"].format(cert=cert_name)
    return generate_content(model, prompt)


def generate_theory(model, cert_name: str, chapter: str) -> str:
    """Generate theory content for a specific chapter."""
    prompt = PROMPTS["theory"].format(cert=cert_name, chapter=chapter)
    return generate_content(model, prompt)


def generate_questions(model, cert_name: str, chapters: str) -> str:
    """Generate practice exam questions."""
    prompt = PROMPTS["questions"].format(cert=cert_name, chapters=chapters)
    return generate_content(model, prompt)


def generate_answers(model, cert_name: str, questions: str) -> str:
    """Generate answer key with explanations."""
    prompt = PROMPTS["answers"].format(cert=cert_name, questions=questions)
    return generate_content(model, prompt)


def parse_chapters(outline: str) -> list[str]:
    """Extract chapter titles from the outline text."""
    chapters = []
    for line in outline.strip().split("\n"):
        stripped = line.strip()
        if stripped and (stripped.startswith("제") and "장" in stripped[:5]):
            chapters.append(stripped)
    return chapters if chapters else [outline.strip().split("\n")[0]]
