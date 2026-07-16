from collections import Counter
import html
import os

import gradio as gr


# =========================================================
# 1. 質問文と選択肢
# =========================================================
QUESTIONS = [
    {
        "number": "Q1",
        "label": "どんな「人の役に立ち方」に、一番ワクワクする？",
        "class_name": "question-a",
        "choices": [
            "A｜目の前の人の話をじっくり聴いて、その人が自分らしく一歩を踏み出せるまで心に寄り添う。",
            "B｜生活の中の困りごとを一緒に解決するために、医療や福祉、地域のサポートを上手に組み合わせて暮らしを支える。",
            "C｜「人間って、なんでこういう行動をしちゃうんだろう？」という心の仕組みを、企業や行政の仕事、新しいサービス作りに活かす。",
            "D｜普段の街づくりや災害時の現場に飛び込んで、人と人をつなぎながら、みんなが安心して暮らせる社会の土台をつくる。",
        ],
    },
    {
        "number": "Q2",
        "label": "学校のグループワークや行事で、あなたが「ついやってしまう役割」は？",
        "class_name": "question-b",
        "choices": [
            "A｜落ち込んでいる友達や、悩んでいそうなメンバーの隣にいって、そっと話を聴く。",
            "B｜困っている人に「先生に聞いてみようか？」「あの資料に書いてあったよ」と、解決できる人や情報をつなぐ。",
            "C｜「みんなはどうしたいんだろう？」とアンケートをとってアイデアを整理したり、みんなが納得する企画を考えたりする。",
            "D｜「みんなでやろうよ！」と声をかけたり、他のグループや地域の人と交渉したりして、チームを外へと広げていく。",
        ],
    },
    {
        "number": "Q3",
        "label": "大学の授業を受けるとしたら、どんなテーマが一番おもしろそう？",
        "class_name": "question-c",
        "choices": [
            "A｜心の病気や悩みのメカニズム、専門的なカウンセリングの技術について。",
            "B｜福祉や医療の仕組み、困っている人が社会のサポートを受けられるようにする方法について。",
            "C｜記憶、感情、人間関係など、私たちの「普段の心の動き」をデータから読み解き、社会に役立てる方法について。",
            "D｜地域でのボランティア活動、防災、多様な人がお互いに助け合える社会の作り方について。",
        ],
    },
    {
        "number": "Q4",
        "label": "将来、仕事の現場でどんな言葉をかけられたら、一番ガッツポーズしたくなる？",
        "class_name": "question-d",
        "choices": [
            "A｜「あなたに話を聴いてもらえて、本当に心が軽くなりました」",
            "B｜「いろいろな手続きやサポートを紹介してくれたおかげで、安心して生活できるようになりました」",
            "C｜「あなたの分析や企画のおかげで、みんなが毎日を楽しく、便利に過ごせる新しい仕組みができました！」",
            "D｜「あなたたちがこの街にいてくれるから、毎日を安心して過ごせます」",
        ],
    },
]


# =========================================================
# 2. コース情報
# =========================================================
COURSES = {
    "A": {
        "course": "心理学コース",
        "headline": "公認心理師のたまご",
        "type": "人の心に深く向き合う専門家タイプ",
        "icon": "🫶",
        "description": (
            "学校や病院などで、悩みを抱える一人ひとりの話をじっくり聴き、"
            "その人が自分らしく前を向けるように専門的な心理カウンセリングで寄り添うことに関心があるタイプです。"
            "心のアドバイザーとして、目の前の人を丁寧に支える学びに向いています。"
        ),
        "career": (
            "スクールカウンセラー、病院・クリニック、児童相談所・福祉施設、"
            "裁判所・少年鑑別所など。公認心理師を目指す学びにつながります。"
        ),
    },
    "B": {
        "course": "精神保健福祉コース",
        "headline": "精神保健福祉士のたまご",
        "type": "暮らしと社会をつなぐコーディネータータイプ",
        "icon": "🤝",
        "description": (
            "医療や福祉の専門知識を活かし、生活に困りごとを抱える人が安心して暮らせるように、"
            "福祉制度や地域の力をつなぐことに関心があるタイプです。"
            "誰もが孤立せず、その人らしい生活を送れる環境をチームで整える学びに向いています。"
        ),
        "career": (
            "精神科病院・メンタルクリニック、障がい者福祉施設、就労支援施設、"
            "保健所・市役所、企業の相談窓口など。精神保健福祉士を目指す学びにつながります。"
        ),
    },
    "C": {
        "course": "人間科学コース（心理学）",
        "headline": "企業・行政の心理学活用のたまご",
        "type": "日常を楽しく快適にするヒットメーカータイプ",
        "icon": "💡",
        "description": (
            "人がつい惹かれるデザインや快適な仕組みなど、人間の心や行動の特徴をデータから科学的に読み解き、"
            "多くの人の毎日をより楽しく便利にすることに関心があるタイプです。"
            "心理学とデータ分析を社会で活かす学びに向いています。"
        ),
        "career": (
            "企業のマーケティング・商品開発・企画・人事、広告代理店、"
            "行政機関の企画・広報など。心理学とデータ分析を活かす幅広い進路につながります。"
        ),
    },
    "D": {
        "course": "人間科学コース（ソーシャルワーク）",
        "headline": "地域支援・災害支援のリーダーのたまご",
        "type": "社会を動かすアクティブタイプ",
        "icon": "🌏",
        "description": (
            "普段の街づくりから災害時の支援まで、現場に飛び込み、人と人をつなぎながら、"
            "安心して暮らせるコミュニティをつくることに関心があるタイプです。"
            "防災、ボランティア、地域イベントなどを通した実践的な学びに向いています。"
        ),
        "career": (
            "行政の街づくり・防災・危機管理部門、地域団体、NPO、"
            "企業のCSR・企画、イベント運営など。人と地域をつなぐ力を活かす進路につながります。"
        ),
    },
}


# =========================================================
# 3. HTML生成
# =========================================================
def course_overview_html():
    cards = []
    for code in "ABCD":
        info = COURSES[code]
        cards.append(
            f"""
            <div class="mini-course mini-{code.lower()}">
                <div class="mini-icon">{info["icon"]}</div>
                <div class="mini-code">{code}</div>
                <div class="mini-title">{html.escape(info["course"])}</div>
            </div>
            """
        )
    return f'<div class="course-overview">{"".join(cards)}</div>'


def score_badges_html(scores):
    badges = []
    for code in "ABCD":
        info = COURSES[code]
        badges.append(
            f"""
            <div class="score-badge score-{code.lower()}">
                <span class="score-letter">{code}</span>
                <span class="score-number">{scores[code]}</span>
                <span class="score-course">{html.escape(info["course"])}</span>
            </div>
            """
        )
    return f'<div class="score-grid">{"".join(badges)}</div>'


def result_card_html(code, score):
    info = COURSES[code]
    return f"""
    <article class="result-card result-{code.lower()}">
        <div class="result-ribbon">あなたへのおすすめ</div>
        <div class="result-main">
            <div class="result-icon">{info["icon"]}</div>
            <div>
                <div class="result-code">TYPE {code}</div>
                <h2>{html.escape(info["course"])}</h2>
                <p class="result-headline">{html.escape(info["headline"])}</p>
            </div>
        </div>
        <div class="result-type">✨ {html.escape(info["type"])}</div>
        <p>{html.escape(info["description"])}</p>
        <div class="career-box">
            <strong>将来の活躍例</strong><br>
            {html.escape(info["career"])}
        </div>
        <div class="result-score">今回の得点：4問中 <strong>{score}点</strong></div>
    </article>
    """


# =========================================================
# 4. 診断処理
# =========================================================
def diagnose(q1, q2, q3, q4):
    """4つの回答を集計し、最多コースを表示する。同点なら複数候補を表示する。"""
    answers = [q1, q2, q3, q4]

    if any(answer is None for answer in answers):
        return """
        <div class="notice notice-warning">
            <div class="notice-icon">⚠️</div>
            <div>
                <h3>未回答の質問があります</h3>
                <p>4つすべてに答えてから「診断する」を押してください。</p>
            </div>
        </div>
        """

    selected_codes = [answer.split("｜", 1)[0] for answer in answers]
    counter = Counter(selected_codes)
    scores = {code: counter.get(code, 0) for code in "ABCD"}

    max_score = max(scores.values())
    winners = [code for code in "ABCD" if scores[code] == max_score]

    if len(winners) == 1:
        heading = """
        <div class="result-heading">
            <span>🎉</span>
            <div>
                <p>DIAGNOSIS RESULT</p>
                <h1>あなたにおすすめのコース</h1>
            </div>
        </div>
        """
    else:
        heading = """
        <div class="result-heading">
            <span>🌈</span>
            <div>
                <p>DIAGNOSIS RESULT</p>
                <h1>あなたにおすすめのコース候補</h1>
                <div class="tie-message">
                    最多数が同点だったため、複数のコースが候補になりました。
                    それぞれの授業内容や資格も比べてみましょう。
                </div>
            </div>
        </div>
        """

    result_cards = "".join(result_card_html(code, scores[code]) for code in winners)

    return f"""
    <section class="result-section">
        {heading}
        <div class="result-cards">{result_cards}</div>

        <div class="score-section">
            <h3>あなたの回答バランス</h3>
            {score_badges_html(scores)}
        </div>

        <div class="disclaimer">
            ※この診断は、興味や関心を考えるための簡易的な目安です。
            最終的なコース選択は、授業内容、取得可能な資格、入学後のガイダンスなども確認して検討してください。
        </div>
    </section>
    """


def reset_answers():
    return None, None, None, None, ""


# =========================================================
# 5. 画面デザイン
# =========================================================
CSS = r"""
:root {
    --ink: #27304a;
    --muted: #65708d;
    --pink: #ff6f91;
    --orange: #ff9f43;
    --purple: #7667f2;
    --blue: #3d9ee8;
    --green: #23b7a4;
}

body {
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 158, 189, .28), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(118, 103, 242, .22), transparent 30%),
        radial-gradient(circle at 75% 85%, rgba(61, 158, 232, .18), transparent 28%),
        linear-gradient(135deg, #fff8fb 0%, #f7f5ff 48%, #f4fbff 100%);
}

.gradio-container {
    max-width: 1080px !important;
    margin: 0 auto !important;
    padding-bottom: 60px !important;
    color: var(--ink);
    font-size: 17px !important;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 38px 28px 34px;
    border-radius: 28px;
    margin: 18px 0 20px;
    color: white;
    text-align: center;
    background: linear-gradient(135deg, #ff7196 0%, #a36ff4 48%, #508de8 100%);
    box-shadow: 0 18px 45px rgba(100, 87, 188, .28);
}

.hero::before,
.hero::after {
    content: "";
    position: absolute;
    border-radius: 999px;
    background: rgba(255,255,255,.16);
}

.hero::before {
    width: 220px;
    height: 220px;
    top: -110px;
    left: -70px;
}

.hero::after {
    width: 170px;
    height: 170px;
    right: -55px;
    bottom: -85px;
}

.hero-kicker {
    position: relative;
    z-index: 1;
    display: inline-block;
    padding: 7px 16px;
    border: 1px solid rgba(255,255,255,.5);
    border-radius: 999px;
    background: rgba(255,255,255,.14);
    font-size: .84rem;
    font-weight: 800;
    letter-spacing: .12em;
}

.hero h1 {
    position: relative;
    z-index: 1;
    margin: 14px 0 9px;
    font-size: clamp(1.75rem, 4vw, 2.65rem);
    line-height: 1.3;
}

.hero p {
    position: relative;
    z-index: 1;
    max-width: 760px;
    margin: 0 auto;
    font-size: 1.04rem;
    line-height: 1.9;
    color: rgba(255,255,255,.95);
}

.course-overview {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 0 0 24px;
}

.mini-course {
    min-height: 138px;
    padding: 18px 14px;
    border-radius: 20px;
    text-align: center;
    background: #ffffff;
    border: 2px solid #dfe3ef;
    box-shadow: 0 10px 28px rgba(67, 70, 120, .12);
}

.mini-a {
    background: #fff1f5;
    border-color: #ff8ba7;
    border-top: 7px solid #e83e68;
}
.mini-b {
    background: #eafbf7;
    border-color: #62cdbf;
    border-top: 7px solid #078579;
}
.mini-c {
    background: #fff7e8;
    border-color: #ffc46e;
    border-top: 7px solid #c96800;
}
.mini-d {
    background: #f0f1ff;
    border-color: #9fa9ff;
    border-top: 7px solid #4f5fd5;
}

.mini-icon {
    font-size: 1.8rem;
    margin-bottom: 2px;
}

.mini-code {
    display: inline-block;
    min-width: 34px;
    padding: 4px 11px;
    margin-bottom: 7px;
    border-radius: 999px;
    background: #ffffff;
    border: 2px solid currentColor;
    font-size: 1rem;
    font-weight: 950;
    color: #4c3fb7;
}

.mini-title {
    font-size: 1.08rem;
    font-weight: 950;
    line-height: 1.45;
    letter-spacing: .01em;
}

.mini-a .mini-code,
.mini-a .mini-title { color: #9f1239; }

.mini-b .mini-code,
.mini-b .mini-title { color: #05685f; }

.mini-c .mini-code,
.mini-c .mini-title { color: #9a4b00; }

.mini-d .mini-code,
.mini-d .mini-title { color: #303fa8; }

.section-lead {
    margin: 22px 0 12px;
    text-align: center;
}

.section-lead h2 {
    margin: 0 0 7px;
    font-size: 1.62rem;
    color: #27304a;
}

.section-lead p {
    margin: 0;
    color: #4f5b78;
    font-size: 1.02rem;
    font-weight: 650;
}

.question-card {
    padding: 18px 20px 13px !important;
    margin: 13px 0 !important;
    border-radius: 22px !important;
    background: rgba(255,255,255,.92) !important;
    border: 1px solid rgba(232, 230, 245, .95) !important;
    box-shadow: 0 11px 30px rgba(52, 56, 103, .09) !important;
    transition: transform .18s ease, box-shadow .18s ease;
}

.question-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 36px rgba(52, 56, 103, .13) !important;
}

.question-a { border-left: 7px solid #ff7899 !important; }
.question-b { border-left: 7px solid #28b7a5 !important; }
.question-c { border-left: 7px solid #ffad45 !important; }
.question-d { border-left: 7px solid #6b7bf3 !important; }

.question-title {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 9px;
}

.question-number {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 48px;
    height: 34px;
    padding: 0 10px;
    border-radius: 999px;
    color: white;
    font-weight: 900;
    background: linear-gradient(135deg, #ff7196, #786ef2);
    box-shadow: 0 6px 14px rgba(119, 101, 231, .22);
}

.question-text {
    padding-top: 2px;
    font-size: 1.18rem;
    font-weight: 900;
    line-height: 1.6;
    color: #202942;
}

.question-card label {
    border-radius: 13px !important;
    color: #202942 !important;
    font-size: 1.06rem !important;
    font-weight: 650 !important;
    line-height: 1.65 !important;
    padding-top: 9px !important;
    padding-bottom: 9px !important;
}

.question-card label span,
.question-card label p {
    color: #202942 !important;
    font-size: 1.06rem !important;
    line-height: 1.65 !important;
}

.question-card label:hover {
    background: #f0edff !important;
}

.action-row {
    margin-top: 22px;
}

#diagnose-btn {
    min-height: 60px;
    border: none !important;
    border-radius: 16px !important;
    font-size: 1.18rem !important;
    font-weight: 950 !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #e74270 0%, #7254d6 56%, #2674c9 100%) !important;
    box-shadow: 0 12px 25px rgba(113, 91, 214, .30) !important;
    transition: transform .18s ease, box-shadow .18s ease;
}

#diagnose-btn * {
    color: #ffffff !important;
    font-size: 1.18rem !important;
    font-weight: 950 !important;
}

#diagnose-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 30px rgba(113, 91, 214, .36) !important;
}

#reset-btn {
    min-height: 60px;
    border: 3px solid #334155 !important;
    border-radius: 16px !important;
    color: #172033 !important;
    background: #ffffff !important;
    font-size: 1.18rem !important;
    font-weight: 950 !important;
    box-shadow: 0 8px 20px rgba(35, 48, 73, .16) !important;
    transition: transform .18s ease, background .18s ease, box-shadow .18s ease;
}

#reset-btn * {
    color: #172033 !important;
    font-size: 1.18rem !important;
    font-weight: 950 !important;
}

#reset-btn:hover {
    transform: translateY(-2px);
    background: #e9ecf5 !important;
    border-color: #172033 !important;
    box-shadow: 0 12px 24px rgba(35, 48, 73, .22) !important;
}

#reset-btn:hover * {
    color: #111827 !important;
}

.notice {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    margin-top: 24px;
    border-radius: 19px;
}

.notice-warning {
    color: #70431e;
    border: 1px solid #ffd59a;
    background: linear-gradient(135deg, #fff8e9, #fff0dd);
}

.notice-icon {
    font-size: 2rem;
}

.notice h3,
.notice p {
    margin: 0;
}

.result-section {
    margin-top: 30px;
}

.result-heading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 18px;
    text-align: left;
}

.result-heading > span {
    font-size: 2.5rem;
}

.result-heading p {
    margin: 0 0 2px;
    color: #7a6ed0;
    font-size: .78rem;
    font-weight: 900;
    letter-spacing: .16em;
}

.result-heading h1 {
    margin: 0;
    font-size: clamp(1.55rem, 4vw, 2.2rem);
}

.tie-message {
    margin-top: 8px;
    color: var(--muted);
    font-size: .94rem;
    line-height: 1.65;
}

.result-cards {
    display: grid;
    gap: 18px;
}

.result-card {
    position: relative;
    overflow: hidden;
    padding: 28px;
    border-radius: 25px;
    background: rgba(255,255,255,.95);
    border: 1px solid rgba(255,255,255,.95);
    box-shadow: 0 16px 42px rgba(54, 57, 110, .14);
}

.result-card::after {
    content: "";
    position: absolute;
    width: 170px;
    height: 170px;
    right: -70px;
    bottom: -75px;
    border-radius: 999px;
    opacity: .12;
}

.result-a { border-top: 8px solid #ff7899; }
.result-a::after { background: #ff7899; }
.result-b { border-top: 8px solid #28b7a5; }
.result-b::after { background: #28b7a5; }
.result-c { border-top: 8px solid #ffad45; }
.result-c::after { background: #ffad45; }
.result-d { border-top: 8px solid #6b7bf3; }
.result-d::after { background: #6b7bf3; }

.result-ribbon {
    display: inline-block;
    padding: 6px 13px;
    margin-bottom: 17px;
    border-radius: 999px;
    color: #6f5fc8;
    background: #f2efff;
    font-size: .82rem;
    font-weight: 900;
}

.result-main {
    display: flex;
    align-items: center;
    gap: 16px;
}

.result-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 68px;
    height: 68px;
    border-radius: 20px;
    font-size: 2.15rem;
    background: linear-gradient(135deg, #fff4f8, #f0efff);
}

.result-code {
    color: #8376d4;
    font-size: .77rem;
    font-weight: 900;
    letter-spacing: .13em;
}

.result-card h2 {
    margin: 4px 0 4px;
    font-size: clamp(1.7rem, 4.5vw, 2.35rem);
    font-weight: 950;
    line-height: 1.35;
}

.result-a h2 { color: #9f1239; }
.result-b h2 { color: #05685f; }
.result-c h2 { color: #9a4b00; }
.result-d h2 { color: #303fa8; }

.result-headline {
    margin: 0;
    color: #4b5671;
    font-size: 1.08rem;
    font-weight: 850;
}

.result-type {
    display: inline-block;
    margin: 20px 0 10px;
    padding: 10px 15px;
    border-radius: 13px;
    color: #3f376d;
    background: #eeeafd;
    font-size: 1.05rem;
    font-weight: 900;
}

.result-card p {
    color: #27304a;
    font-size: 1.05rem;
    line-height: 1.9;
}

.career-box {
    position: relative;
    z-index: 1;
    padding: 17px 19px;
    border-radius: 15px;
    color: #26324c;
    font-size: 1.03rem;
    line-height: 1.8;
    background: #f4f7ff;
    border: 2px solid #dce3f5;
}

.result-score {
    margin-top: 15px;
    color: #27304a;
    font-size: 1.12rem;
    font-weight: 750;
}

.score-section {
    margin-top: 22px;
    padding: 22px;
    border-radius: 22px;
    background: rgba(255,255,255,.78);
    box-shadow: 0 10px 30px rgba(62, 65, 116, .08);
}

.score-section h3 {
    margin: 0 0 15px;
    text-align: center;
}

.score-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

.score-badge {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 5px 9px;
    padding: 13px;
    border-radius: 16px;
    background: white;
    border: 1px solid #eceaf5;
}

.score-letter {
    grid-row: 1 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    color: white;
    font-weight: 900;
}

.score-a .score-letter { background: #ff7899; }
.score-b .score-letter { background: #28b7a5; }
.score-c .score-letter { background: #ffad45; }
.score-d .score-letter { background: #6b7bf3; }

.score-number {
    font-size: 1.38rem;
    font-weight: 950;
    color: #202942;
}

.score-course {
    font-size: .9rem;
    font-weight: 900;
    line-height: 1.35;
}

.score-a .score-course { color: #9f1239; }
.score-b .score-course { color: #05685f; }
.score-c .score-course { color: #9a4b00; }
.score-d .score-course { color: #303fa8; }

.disclaimer {
    margin: 18px 4px 0;
    color: #4f5b78;
    font-size: .94rem;
    font-weight: 600;
    line-height: 1.75;
    text-align: center;
}

.footer-note {
    margin-top: 28px;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    color: #4f5b78;
    background: rgba(255,255,255,.72);
    font-size: .98rem;
    font-weight: 650;
}

@media (max-width: 760px) {
    .course-overview {
        grid-template-columns: repeat(2, 1fr);
    }

    .score-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero {
        padding: 30px 18px;
        border-radius: 22px;
    }

    .question-card,
    .result-card {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    .result-main {
        align-items: flex-start;
    }
}

@media (max-width: 480px) {
    .course-overview,
    .score-grid {
        grid-template-columns: 1fr;
    }

    .result-heading {
        align-items: flex-start;
    }

    .result-icon {
        width: 56px;
        height: 56px;
        font-size: 1.8rem;
    }
}
"""


# =========================================================
# 6. Gradio画面
# =========================================================
APP_THEME = gr.themes.Soft(
    primary_hue="violet",
    secondary_hue="pink",
    neutral_hue="slate",
)

with gr.Blocks(
    title="心理臨床学科 コース適性診断テスト",
) as demo:
    gr.HTML(
        """
        <header class="hero">
            <div class="hero-kicker">4 QUESTIONS · COURSE FINDER</div>
            <h1>🧭 心理臨床学科<br>コース適性診断テスト</h1>
            <p>
                「誰かの力になりたい」「心や社会の仕組みを知りたい」――
                4つの質問に直感で答えて、あなたらしい学びの方向を見つけてみましょう。
            </p>
        </header>
        """
    )

    gr.HTML(course_overview_html())

    gr.HTML(
        """
        <div class="section-lead">
            <h2>あなたの直感に近いものを選んでください</h2>
            <p>正解・不正解はありません。考えすぎず、最もワクワクする答えを選びましょう。</p>
        </div>
        """
    )

    radios = []
    for question in QUESTIONS:
        with gr.Group(elem_classes=["question-card", question["class_name"]]):
            gr.HTML(
                f"""
                <div class="question-title">
                    <span class="question-number">{question["number"]}</span>
                    <span class="question-text">{html.escape(question["label"])}</span>
                </div>
                """
            )
            radio = gr.Radio(
                choices=question["choices"],
                show_label=False,
                type="value",
            )
            radios.append(radio)

    with gr.Row(elem_classes="action-row"):
        diagnose_button = gr.Button(
            "✨ 診断結果を見る",
            variant="primary",
            elem_id="diagnose-btn",
        )
        reset_button = gr.Button(
            "↻ 回答をリセット",
            elem_id="reset-btn",
        )

    result_output = gr.HTML()

    diagnose_button.click(
        fn=diagnose,
        inputs=radios,
        outputs=result_output,
    )

    reset_button.click(
        fn=reset_answers,
        inputs=None,
        outputs=[*radios, result_output],
    )

    gr.HTML(
        """
        <div class="footer-note">
            心理臨床学科での学びを考えるための簡易診断です。
            オープンキャンパスや進学相談でも、ぜひ各コースの詳しい内容をご確認ください。
        </div>
        """
    )


# =========================================================
# 7. 起動
# =========================================================
if __name__ == "__main__":
    running_in_colab = "COLAB_RELEASE_TAG" in os.environ

    if running_in_colab:
        demo.launch(
            share=True,
            debug=True,
            theme=APP_THEME,
            css=CSS,
        )
    else:
        demo.launch(
            server_name="0.0.0.0",
            server_port=int(os.getenv("PORT", "7860")),
            theme=APP_THEME,
            css=CSS,
        )
