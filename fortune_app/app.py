from __future__ import annotations

from datetime import date, datetime
import hashlib
import random

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


FORTUNE_OPENINGS = [
    "오늘은 흐름을 억지로 바꾸기보다, 좋은 타이밍을 기다릴수록 유리한 날입니다.",
    "작은 선택 하나가 하루의 분위기를 크게 바꿉니다. 서두르지 않는 태도가 중요합니다.",
    "주변의 말보다 스스로 정한 기준을 믿을수록 안정적인 하루가 됩니다.",
    "평소보다 감각이 예민하게 작동하는 날입니다. 미묘한 신호를 잘 읽어보세요.",
    "운은 준비된 쪽으로 기울기 쉬운 날입니다. 미뤄둔 일을 먼저 손보면 좋습니다.",
]

MONEY_FORTUNES = [
    "지출을 줄이려는 의식이 실제로 도움이 됩니다. 충동구매만 피하면 만족도가 높습니다.",
    "큰 수익보다 새는 돈을 막는 쪽이 더 중요합니다. 정기결제를 점검해 보세요.",
    "가벼운 소비는 괜찮지만, 비교 없이 결제하는 일은 피하는 편이 좋습니다.",
    "금전운은 무난합니다. 필요한 곳에는 쓰되, 체면 때문에 쓰는 돈은 줄이는 게 좋습니다.",
    "예상 밖의 할인이나 작은 이득을 챙길 가능성이 있습니다.",
]

LOVE_FORTUNES = [
    "관계운은 대화의 온도에 달려 있습니다. 정답보다 진심이 더 잘 통합니다.",
    "상대의 반응을 너무 빨리 해석하지 않는 편이 좋습니다. 한 번 더 여유를 두세요.",
    "좋아하는 마음이 있다면 표현을 아끼지 말고, 없다면 애매한 신호는 줄이는 게 좋습니다.",
    "가까운 사람과 사소한 오해가 생길 수 있지만, 먼저 부드럽게 풀면 금방 회복됩니다.",
    "혼자만의 시간이 관계운에도 도움이 됩니다. 마음을 정리한 뒤 대화해 보세요.",
]

HEALTH_FORTUNES = [
    "몸은 버틸 수 있어도 컨디션은 솔직합니다. 수면 리듬을 먼저 챙기세요.",
    "오래 앉아 있었다면 가볍게 걷는 것만으로도 몸 상태가 꽤 달라질 수 있습니다.",
    "피로가 누적되기 쉬운 날이라, 카페인보다 휴식의 질이 더 중요합니다.",
    "소화와 목, 어깨 쪽을 가볍게 관리하면 하루가 훨씬 편안해질 수 있습니다.",
    "무리한 계획보다 꾸준한 회복이 더 잘 맞는 날입니다.",
]

LUCKY_ITEMS = [
    "밝은 색 메모장",
    "차분한 향의 음료",
    "작은 손거울",
    "파란색 소품",
    "이어폰",
    "따뜻한 차",
    "정리된 책상",
    "은색 액세서리",
]

LUCKY_COLORS = [
    "골드",
    "네이비",
    "화이트",
    "코랄",
    "올리브",
    "스카이 블루",
    "버건디",
    "민트",
]


def make_rng(birth_date: str, today: date) -> random.Random:
    seed = f"{birth_date}:{today.isoformat()}".encode("utf-8")
    digest = hashlib.sha256(seed).hexdigest()
    return random.Random(int(digest[:16], 16))


def build_fortune(birth_date: str) -> dict[str, str | int]:
    today = date.today()
    rng = make_rng(birth_date, today)

    total_score = rng.randint(68, 96)
    money_score = rng.randint(55, 95)
    love_score = rng.randint(58, 97)
    health_score = rng.randint(60, 94)

    return {
        "today": today.strftime("%Y년 %m월 %d일"),
        "birth_date": datetime.strptime(birth_date, "%Y-%m-%d").strftime("%Y년 %m월 %d일"),
        "total_score": total_score,
        "money_score": money_score,
        "love_score": love_score,
        "health_score": health_score,
        "opening": rng.choice(FORTUNE_OPENINGS),
        "money": rng.choice(MONEY_FORTUNES),
        "love": rng.choice(LOVE_FORTUNES),
        "health": rng.choice(HEALTH_FORTUNES),
        "lucky_color": rng.choice(LUCKY_COLORS),
        "lucky_item": rng.choice(LUCKY_ITEMS),
        "advice": "중요한 결정을 한 번에 끝내려 하지 말고, 오전과 오후의 판단을 나눠서 보세요.",
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fortune", methods=["POST"])
def fortune():
    birth_date = request.form.get("birth_date", "").strip()
    if not birth_date:
        return jsonify({"error": "생일을 입력해 주세요."}), 400

    try:
        parsed = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "생일 형식이 올바르지 않습니다."}), 400

    if parsed > date.today():
        return jsonify({"error": "미래 날짜는 입력할 수 없습니다."}), 400

    return jsonify(build_fortune(birth_date))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
