import os
from flask import Flask, render_template, request, Response, stream_with_context
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAJ34fwRuHpKTP1QbmqmJlqwlTGe-l1V6k")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "당신은 한국의 전통 사주(四柱)와 현대 점성술을 결합한 운세 전문가입니다. "
        "사용자의 생년월일을 바탕으로 오늘의 운세를 친근하고 따뜻한 한국어로 알려주세요. "
        "운세는 다음 항목을 포함해주세요: "
        "1) 전체 총운, 2) 금전/재물운, 3) 연애/인간관계운, 4) 건강운, 5) 오늘의 조언. "
        "각 항목은 명확한 제목과 함께 자세히 설명해주세요."
        "재연 테스트1"
        "jyko test1"
        "고재연  test1"


    ),
)

goonghap_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "당신은 한국의 전통 사주(四柱)와 음양오행을 기반으로 두 사람의 궁합을 봐주는 전문가입니다. "
        "두 사람의 생년월일을 바탕으로 궁합을 친근하고 따뜻한 한국어로 분석해주세요. "
        "궁합 분석은 다음 항목을 포함해주세요: "
        "1) 종합 궁합 점수 (100점 만점), 2) 두 사람의 기본 기운과 성격 분석, "
        "3) 사랑/연애 궁합, 4) 우정/인간관계 궁합, 5) 함께하면 좋은 점, "
        "6) 주의해야 할 점, 7) 궁합을 높이는 조언. "
        "각 항목은 명확한 제목과 함께 자세히 설명해주세요. "
        "재미있고 희망적인 톤으로 작성해주세요."
        "재연 테스트2"
    ),
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fortune", methods=["POST"])
def fortune():
    birth_date = request.form.get("birth_date", "")
    if not birth_date:
        return "생년월일을 입력해주세요.", 400

    def generate():
        try:
            response = model.generate_content(
                f"제 생년월일은 {birth_date}입니다. 오늘의 운세를 알려주세요.",
                stream=True,
            )
            for chunk in response:
                if chunk.text:
                    yield f"data: {chunk.text}\n\n"
        except Exception as e:
            yield f"data: ❌ 오류가 발생했습니다: {e}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "재연 테스트3"
        },
    )


@app.route("/goonghap", methods=["POST"])
def goonghap():
    birth_date1 = request.form.get("birth_date1", "")
    birth_date2 = request.form.get("birth_date2", "")
    if not birth_date1 or not birth_date2:
        return "두 사람의 생년월일을 모두 입력해주세요.", 400

    def generate():
        try:
            response = goonghap_model.generate_content(
                f"첫 번째 사람의 생년월일은 {birth_date1}이고, 두 번째 사람의 생년월일은 {birth_date2}입니다. 두 사람의 궁합을 분석해주세요.",
                stream=True,
            )
            for chunk in response:
                if chunk.text:
                    yield f"data: {chunk.text}\n\n"
        except Exception as e:
            yield f"data: ❌ 오류가 발생했습니다: {e}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
