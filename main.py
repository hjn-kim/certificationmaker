"""
자격증 시험 대비서 생성기
========================
사용자가 입력한 자격증에 대한 대비서(표지, 목차, 이론, 기출문제, 답안)를
Gemini API로 생성하고 PDF로 출력합니다.

사용법:
    python main.py
"""

import sys
from src.gemini_client import get_client
from src.generator import (
    generate_outline,
    generate_theory,
    generate_questions,
    generate_answers,
    parse_chapters,
)
from src.pdf_builder import CertPDF


def main():
    print("=" * 50)
    print("  자격증 시험 대비서 생성기")
    print("  (Gemini AI 기반)")
    print("=" * 50)
    print()

    cert_name = input("응시할 자격증 이름을 입력하세요: ").strip()
    if not cert_name:
        print("자격증 이름이 입력되지 않았습니다.")
        sys.exit(1)

    print(f"\n'{cert_name}' 자격증 대비서를 생성합니다...\n")

    # Initialize Gemini client
    try:
        model = get_client()
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)

    # Step 1: Generate outline
    print("[1/4] 목차 생성 중...")
    outline = generate_outline(model, cert_name)
    chapters = parse_chapters(outline)
    print(f"  -> {len(chapters)}개 챕터 구성 완료")

    # Step 2: Generate theory for each chapter
    print("[2/4] 이론 내용 생성 중...")
    theories = []
    for i, chapter in enumerate(chapters, 1):
        print(f"  -> 챕터 {i}/{len(chapters)}: {chapter}")
        theory = generate_theory(model, cert_name, chapter)
        theories.append((chapter, theory))

    # Step 3: Generate practice questions
    print("[3/4] 기출문제 생성 중...")
    all_chapters_str = "\n".join(chapters)
    questions = generate_questions(model, cert_name, all_chapters_str)
    print("  -> 20문항 생성 완료")

    # Step 4: Generate answer key
    print("[4/4] 정답 및 해설 생성 중...")
    answers = generate_answers(model, cert_name, questions)
    print("  -> 해설 생성 완료")

    # Build PDF
    print("\nPDF 생성 중...")
    pdf = CertPDF(cert_name)

    # Cover page
    pdf.add_cover_page()

    # Table of contents
    pdf.add_toc_page(outline)

    # Theory sections
    for chapter_title, theory_content in theories:
        pdf.add_theory_section(chapter_title, theory_content)

    # Questions
    pdf.add_questions_section(questions)

    # Answers
    pdf.add_answers_section(answers)

    # Save
    filepath = pdf.save()
    print(f"\n대비서가 생성되었습니다!")
    print(f"파일 위치: {filepath}")
    print()


if __name__ == "__main__":
    main()
