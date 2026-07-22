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
            "B｜悩み事の背景にある複雑な出来事を一緒に考え、解決できるように支援していく。",
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
            "B｜困っている人の話をしっかり聴き、寄り添い（伴走）ながら、力になってくれる人へつないでいく。",
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
            "B｜「生きづらさ」を抱えている人が社会で生きていくための支援やサポート。",
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
            "B｜「いろんなことがあったけど、今充実した生活を送っています。」",
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
        "type": "人の心に深く向き合う専門家",
        "icon": "🫶",
        "description": (
            "学校や病院などで、悩みを抱える一人ひとりの話をじっくり聴き、"
            "その人が自分らしく前を向けるように専門的な心理カウンセリングで寄り添います。"
            "心のアドバイザーとして、目の前の人の笑顔を取り戻すサポートをじっくり学びたい人に向いています。"
        ),
        "career": (
            "スクールカウンセラー（教育分野）、病院やクリニック（医療・保健分野）、"
            "児童相談所や福祉施設（福祉分野）、裁判所や少年鑑別所（司法分野）など、"
            "国家資格「公認心理師」を武器に、心の専門職として幅広い現場で活躍が期待されます。"
        ),
    },
    "B": {
        "course": "精神保健福祉コース",
        "headline": "精神保健福祉士のたまご",
        "type": "その人らしい生き方と生活を支えるコーディネーター",
        "icon": "🤝",
        "description": (
            "様々な困難を抱えている人の思いを大事にしながら、医療や福祉の専門知識を活かして、"
            "安心してその人らしく生きていけるよう支援します。"
            "誰もが孤立せず、その人らしく生きていけるようにチームで支える人に向いています。"
        ),
        "career": (
            "精神科病院やメンタルクリニック（医療機関）、障がい者福祉施設や就労支援施設（福祉分野）、"
            "行政機関（保健所・市役所など）のほか、学校現場のスクールソーシャルワーカー、"
            "一般企業の相談窓口など、国家資格「精神保健福祉士」を活かして、"
            "こころの健康と生活を支える専門職として活躍できます。"
        ),
    },
    "C": {
        "course": "人間科学コース（心理学）",
        "headline": "快適づくりのたまご",
        "type": "人の行動を分析し、よりよい環境をつくるプランナー",
        "icon": "💡",
        "description": (
            "悩んでいる人を支える仕事よりも、「毎日をもっと快適にする」仕事にワクワクするタイプです。"
            "人間の心のクセをデータ分析で科学的に捉え、多くの人の意見を取り入れながら、"
            "より利用しやすい仕組みや商品づくり、働きやすい環境づくりにつなげることにやりがいを感じます。"
        ),
        "career": (
            "一般企業（マーケティング、商品開発、企画、人事・採用）、広告代理店、"
            "行政機関（企画課、広報課など）、警察官・警察行政職員などが舞台です。"
            "心理学で培った傾聴力とデータ分析のスキルは、業界や職種を問わず、多様な課題に対応できる強みになります。"
        ),
    },
    "D": {
        "course": "人間科学コース（ソーシャルワーク）",
        "headline": "コミュニティづくりのたまご",
        "type": "人と人をつなぎ、安心の輪を広げるプランナー",
        "icon": "🌏",
        "description": (
            "普段の街づくりから、もしもの災害時の現場までフットワーク軽く飛び込み、"
            "人と人をつなぎながら、みんなが安心して暮らせるコミュニティを作ります。"
            "防災、ボランティア、地域のイベント企画などを通して、人と地域を笑顔にする「つながりの場」を創り出すのが得意なタイプです。"
            "前に立って引っ張る人はもちろん、痒いところに手が届くような気配りで周囲を支える「縁の下の力持ち」にも向いています。"
        ),
        "career": (
            "公務員（行政の街づくり・防災・危機管理部門）、地域の生活を支える各種団体、NPO法人、"
            "警察官・警察行政職員、消防士、一般企業の社会貢献部門や企画職、イベント運営会社など。"
            "リーダーとしても、チームを支えるコーディネーターとしても、「人と人をつなぐ力」を生かして社会に貢献できます。"
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
        <div class="result-ribbon">{code}が多かったあなた</div>
        <div class="result-main">
            <div class="result-icon">{info["icon"]}</div>
            <div>
                <div class="result-code">TYPE {code}</div>
                <h2>{html.escape(info["course"])}</h2>
                <p class="result-headline">{html.escape(info["headline"])}</p>
            </div>
        </div>
        <div class="result-type"><strong>どんなタイプ？</strong> {html.escape(info["type"])}</div>
        <p>{html.escape(info["description"])}</p>
        <div class="career-box">
            <strong>将来の活躍の舞台は？</strong><br>
            {html.escape(info["career"])}
        </div>
        <div class="result-score">今回の得点：4問中 <strong>{score}点</strong></div>
    </article>
    """


# =========================================================
# 4. 診断処理
# =========================================================
def diagnose(q1, q2, q3, q4):
    """4つの回答を集計し、最多コースを表示する。同点なら迷っている複数候補を表示する。"""
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

    tie_guidance = ""

    if len(winners) == 1:
        heading = """
        <div class="result-heading">
            <span>🎉</span>
            <div>
                <p>DIAGNOSIS RESULT</p>
                <h1>診断結果</h1>
            </div>
        </div>
        """
    else:
        winner_course_names = [
            html.escape(COURSES[code]["course"]) for code in winners
        ]

        if len(winner_course_names) == 2:
            course_text = "と".join(winner_course_names)
        else:
            course_text = "・".join(winner_course_names)

        heading = f"""
        <div class="result-heading">
            <span>🌈</span>
            <div>
                <p>DIAGNOSIS RESULT</p>
                <h1>診断結果：{course_text}の間で迷っているようです</h1>
                <div class="tie-message">
                    選択数が同点だったため、これらの複数コースに同じくらい関心があることが結果に表れています。
                    それぞれの授業内容や資格も比べてみましょう。
                </div>
            </div>
        </div>
        """

        tie_guidance = """
        <section class="tie-guidance">
            <div class="tie-guidance-icon">🌱</div>
            <div class="tie-guidance-body">
                <h2>迷っている今も、大切な進路選びの途中です</h2>

                <div class="tie-guidance-point">
                    <span>😊</span>
                    <p>
                        <strong>今、迷っていても全然大丈夫です。</strong>
                        進路について迷うことは、自分の興味や将来を丁寧に考えている証拠でもあります。
                    </p>
                </div>

                <div class="tie-guidance-point">
                    <span>🎓</span>
                    <p>
                        <strong>入学後に学びながら、自分に合うコースを選択しても大丈夫です。</strong>
                        授業やさまざまな体験を通して、関心がよりはっきりしてくることがあります。
                    </p>
                </div>

                <div class="tie-guidance-point">
                    <span>🧠</span>
                    <p>
                        人を直接支援するかどうか、人の役に立つ仕事を目指すかどうかにかかわらず、
                        <strong>人間の心や社会・環境に関心がある人には、心理臨床学科への入学をおすすめします。</strong>
                    </p>
                </div>
            </div>
        </section>
        """

    result_cards = "".join(result_card_html(code, scores[code]) for code in winners)

    return f"""
    <section class="result-section">
        {heading}
        {tie_guidance}
        <div class="result-cards">{result_cards}</div>

        <div class="score-section">
            <h3>あなたの回答バランス</h3>
            {score_badges_html(scores)}
        </div>

        <div class="disclaimer">
            ※選んだA・B・C・Dのうち、一番多かった文字があなたの未来のヒントです。
            この診断は興味や関心を考えるための簡易的な目安です。最終的なコース選択は、授業内容、取得可能な資格、入学後のガイダンスなども確認して検討してください。
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
    max-width: 820px;
    margin: 0 auto;
    font-size: 1.08rem;
    line-height: 1.95;
    color: rgba(255,255,255,.98);
}

.hero p strong {
    display: inline-block;
    margin-top: 6px;
    padding: 4px 12px;
    border-radius: 999px;
    color: #ffffff;
    background: rgba(35, 25, 96, .28);
    font-size: 1.14rem;
    font-weight: 950;
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

.section-lead .diagnosis-guide {
    display: inline-block;
    margin-top: 12px;
    padding: 10px 16px;
    border-radius: 14px;
    color: #3f2f7f;
    background: #f0ecff;
    border: 2px solid #c8bdf8;
    font-size: 1.03rem;
    font-weight: 850;
    line-height: 1.6;
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

/* =========================================================
   高校生向け・明るい高コントラストデザイン
   文章や診断ロジックは変更せず、表示デザインのみ上書き
   ========================================================= */

:root {
    --bright-ink: #17213d;
    --bright-navy: #172554;
    --bright-muted: #43506d;
    --bright-pink: #d91f5d;
    --bright-green: #087f6f;
    --bright-orange: #bd5b00;
    --bright-blue: #3548b8;
    --bright-purple: #6941c6;
    --bright-yellow: #ffd84d;
    --bright-white: #ffffff;
}

html {
    font-size: 18px;
}

body {
    min-height: 100vh;
    background:
        radial-gradient(circle at 7% 7%, rgba(255, 215, 75, .48), transparent 24%),
        radial-gradient(circle at 93% 11%, rgba(255, 105, 150, .30), transparent 27%),
        radial-gradient(circle at 87% 85%, rgba(70, 174, 255, .24), transparent 29%),
        radial-gradient(circle at 10% 90%, rgba(63, 211, 170, .23), transparent 26%),
        linear-gradient(135deg, #fffdf1 0%, #fff4fa 34%, #f6f4ff 67%, #eefaff 100%) !important;
}

.gradio-container {
    max-width: 1140px !important;
    padding: 0 18px 76px !important;
    color: var(--bright-ink) !important;
    font-size: 1.08rem !important;
    line-height: 1.78 !important;
}

/* タイトル */
.hero {
    position: relative;
    overflow: hidden;
    padding: 48px 32px 43px !important;
    border: 4px solid rgba(255,255,255,.94) !important;
    border-radius: 32px !important;
    color: #ffffff !important;
    background:
        linear-gradient(130deg, rgba(255,255,255,.14), transparent 42%),
        linear-gradient(135deg, #f2386e 0%, #e74d9a 31%, #8756da 63%, #247bd7 100%) !important;
    box-shadow:
        0 23px 50px rgba(103, 68, 179, .31),
        inset 0 1px 0 rgba(255,255,255,.38) !important;
}

.hero::before {
    content: "🧠" !important;
    position: absolute !important;
    top: 18px !important;
    left: 25px !important;
    width: auto !important;
    height: auto !important;
    border-radius: 0 !important;
    background: none !important;
    font-size: clamp(2.8rem, 6vw, 4.6rem) !important;
    opacity: .25 !important;
    transform: rotate(-12deg);
}

.hero::after {
    content: "🚀" !important;
    position: absolute !important;
    right: 25px !important;
    bottom: 15px !important;
    width: auto !important;
    height: auto !important;
    border-radius: 0 !important;
    background: none !important;
    font-size: clamp(2.8rem, 6vw, 4.5rem) !important;
    opacity: .30 !important;
    transform: rotate(10deg);
}

.hero-kicker {
    padding: 9px 19px !important;
    border: 2px solid rgba(255,255,255,.88) !important;
    color: #ffffff !important;
    background: rgba(49, 27, 107, .34) !important;
    font-size: 1rem !important;
    font-weight: 950 !important;
}

.hero-kicker::before {
    content: "✨ ";
}

.hero-kicker::after {
    content: " ✨";
}

.hero h1 {
    margin: 17px 0 13px !important;
    color: #ffffff !important;
    font-size: clamp(2.25rem, 5.5vw, 3.45rem) !important;
    font-weight: 950 !important;
    line-height: 1.27 !important;
    text-shadow: 0 3px 9px rgba(37, 19, 83, .38);
}

.hero p {
    max-width: 860px !important;
    color: #ffffff !important;
    font-size: clamp(1.17rem, 2.5vw, 1.36rem) !important;
    font-weight: 760 !important;
    line-height: 1.93 !important;
    text-shadow: 0 2px 6px rgba(37, 19, 83, .30);
}

.hero p strong {
    margin-top: 9px !important;
    padding: 7px 15px !important;
    border: 2px solid rgba(255,255,255,.72);
    color: #ffffff !important;
    background: rgba(41, 24, 92, .36) !important;
    font-size: 1.22rem !important;
    font-weight: 950 !important;
}

/* 上部のコースカード */
.course-overview {
    gap: 16px !important;
    margin-bottom: 30px !important;
}

.mini-course {
    position: relative;
    overflow: hidden;
    min-height: 176px !important;
    padding: 22px 16px 19px !important;
    border: 3px solid !important;
    border-radius: 25px !important;
    box-shadow: 0 15px 32px rgba(57, 57, 111, .15) !important;
    transition: transform .18s ease, box-shadow .18s ease !important;
}

.mini-course:hover {
    transform: translateY(-5px) rotate(-.4deg);
    box-shadow: 0 21px 40px rgba(57, 57, 111, .21) !important;
}

.mini-course::after {
    content: "★";
    position: absolute;
    top: 10px;
    right: 12px;
    font-size: 1.35rem;
    opacity: .44;
}

.mini-a {
    color: #8e123b !important;
    background: linear-gradient(145deg, #fffafd, #ffdeea) !important;
    border-color: #e95682 !important;
}

.mini-b {
    color: #05675d !important;
    background: linear-gradient(145deg, #f7fffc, #ccefe6) !important;
    border-color: #19a58f !important;
}

.mini-c {
    color: #7a3c00 !important;
    background: linear-gradient(145deg, #fffdf4, #ffe29a) !important;
    border-color: #e99218 !important;
}

.mini-d {
    color: #2b3a9b !important;
    background: linear-gradient(145deg, #fbfbff, #dce2ff) !important;
    border-color: #6676df !important;
}

.mini-icon {
    font-size: 2.65rem !important;
    line-height: 1 !important;
    margin-bottom: 8px !important;
    filter: drop-shadow(0 4px 4px rgba(37, 40, 78, .13));
}

.mini-code {
    min-width: 44px !important;
    padding: 4px 14px !important;
    border: 3px solid currentColor !important;
    color: inherit !important;
    background: rgba(255,255,255,.94) !important;
    font-size: 1.17rem !important;
    font-weight: 950 !important;
}

.mini-title {
    color: inherit !important;
    font-size: 1.22rem !important;
    font-weight: 950 !important;
    line-height: 1.5 !important;
}

/* 教示カード */
.section-lead {
    position: relative;
    overflow: hidden;
    margin: 30px 0 20px !important;
    padding: 25px 26px !important;
    border: 3px solid #725bd1 !important;
    border-radius: 25px !important;
    color: var(--bright-navy) !important;
    background:
        linear-gradient(90deg, rgba(255, 218, 72, .25), transparent 34%),
        linear-gradient(135deg, #ffffff 0%, #fbf6ff 59%, #edf7ff 100%) !important;
    box-shadow: 0 15px 33px rgba(63, 55, 123, .15) !important;
}

.section-lead::before {
    content: "🎯";
    position: absolute;
    left: 25px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2.65rem;
}

.section-lead::after {
    content: "✨";
    position: absolute;
    right: 25px;
    top: 15px;
    font-size: 1.9rem;
}

.section-lead h2 {
    margin: 0 62px 9px !important;
    color: #1a2550 !important;
    font-size: clamp(1.65rem, 3.5vw, 2.08rem) !important;
    font-weight: 950 !important;
    line-height: 1.45 !important;
}

.section-lead p {
    margin-left: 62px !important;
    margin-right: 62px !important;
    color: #344165 !important;
    font-size: clamp(1.15rem, 2.5vw, 1.3rem) !important;
    font-weight: 800 !important;
    line-height: 1.78 !important;
}

.section-lead .diagnosis-guide {
    padding: 12px 18px !important;
    border: 3px solid #ad94eb !important;
    color: #382579 !important;
    background: #f2edff !important;
    font-size: 1.15rem !important;
    font-weight: 950 !important;
}

/* 質問カード */
.question-card {
    position: relative;
    overflow: hidden;
    padding: 23px 25px 19px !important;
    margin: 18px 0 !important;
    border: 3px solid !important;
    border-radius: 26px !important;
    background: #ffffff !important;
    box-shadow: 0 15px 34px rgba(46, 52, 101, .14) !important;
}

.question-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 21px 42px rgba(46, 52, 101, .19) !important;
}

.question-card::before {
    position: absolute;
    right: 20px;
    top: 11px;
    font-size: 2.35rem;
    opacity: .20;
    pointer-events: none;
}

.question-a {
    border-color: #e75c86 !important;
    background: linear-gradient(150deg, #ffffff 56%, #ffedf4 100%) !important;
}

.question-b {
    border-color: #20a790 !important;
    background: linear-gradient(150deg, #ffffff 56%, #e7faf4 100%) !important;
}

.question-c {
    border-color: #eb9824 !important;
    background: linear-gradient(150deg, #ffffff 56%, #fff5d9 100%) !important;
}

.question-d {
    border-color: #6574dc !important;
    background: linear-gradient(150deg, #ffffff 56%, #ecefff 100%) !important;
}

.question-a::before { content: "🫶"; }
.question-b::before { content: "🤝"; }
.question-c::before { content: "💡"; }
.question-d::before { content: "🌏"; }

.question-title {
    gap: 15px !important;
    margin-bottom: 16px !important;
    padding-right: 48px;
}

.question-number {
    min-width: 74px !important;
    height: auto !important;
    min-height: 49px !important;
    padding: 3px 16px !important;
    border: 3px solid rgba(255,255,255,.87) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-size: 1.4rem !important;
    font-weight: 950 !important;
    box-shadow: 0 8px 18px rgba(45, 43, 95, .23) !important;
}

.question-a .question-number {
    background: #c92558 !important;
}

.question-b .question-number {
    background: #087f6f !important;
}

.question-c .question-number {
    background: #bf5d00 !important;
}

.question-d .question-number {
    background: #3e50b9 !important;
}

.question-text {
    padding-top: 3px !important;
    color: #14203d !important;
    font-size: clamp(1.31rem, 2.8vw, 1.54rem) !important;
    font-weight: 950 !important;
    line-height: 1.58 !important;
}

/* 回答選択肢 */
.question-card label {
    min-height: 59px !important;
    margin: 8px 0 !important;
    padding: 12px 15px !important;
    border: 2px solid #d4dceb !important;
    border-radius: 16px !important;
    color: #17213d !important;
    background: #ffffff !important;
    box-shadow: 0 4px 10px rgba(48, 56, 100, .07) !important;
    font-size: 1.19rem !important;
    font-weight: 740 !important;
    line-height: 1.78 !important;
    transition: transform .14s ease, background .14s ease, border-color .14s ease !important;
}

.question-card label span,
.question-card label p {
    color: #17213d !important;
    font-size: 1.19rem !important;
    font-weight: 740 !important;
    line-height: 1.78 !important;
}

.question-card label:hover {
    transform: translateX(4px);
    border-color: #8069d2 !important;
    background: #f6f2ff !important;
}

.question-card label:has(input:checked) {
    border: 3px solid #a95f00 !important;
    color: #352300 !important;
    background: linear-gradient(135deg, #fff9c8, #ffe785) !important;
    box-shadow: 0 8px 18px rgba(190, 128, 0, .18) !important;
}

.question-card label:has(input:checked) span,
.question-card label:has(input:checked) p {
    color: #352300 !important;
    font-weight: 950 !important;
}

/* 操作ボタン */
.action-row {
    gap: 16px !important;
    margin-top: 28px !important;
}

#diagnose-btn {
    min-height: 70px !important;
    border: 3px solid #ffffff !important;
    border-radius: 20px !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #e82c62 0%, #a43bc0 48%, #2670cf 100%) !important;
    box-shadow: 0 16px 30px rgba(105, 62, 179, .32) !important;
    font-size: 1.38rem !important;
    font-weight: 950 !important;
}

#diagnose-btn * {
    color: #ffffff !important;
    font-size: 1.38rem !important;
    font-weight: 950 !important;
}

#diagnose-btn:hover {
    transform: translateY(-3px) scale(1.01) !important;
    filter: saturate(1.12);
    box-shadow: 0 21px 38px rgba(105, 62, 179, .40) !important;
}

#reset-btn {
    min-height: 70px !important;
    border: 3px solid #25365f !important;
    border-radius: 20px !important;
    color: #17213d !important;
    background: linear-gradient(135deg, #ffffff 0%, #eaf1ff 100%) !important;
    box-shadow: 0 11px 24px rgba(35, 48, 73, .18) !important;
    font-size: 1.34rem !important;
    font-weight: 950 !important;
}

#reset-btn * {
    color: #17213d !important;
    font-size: 1.34rem !important;
    font-weight: 950 !important;
}

#reset-btn:hover {
    transform: translateY(-3px) !important;
    border-color: #25365f !important;
    color: #ffffff !important;
    background: #334978 !important;
    box-shadow: 0 16px 29px rgba(35, 48, 73, .28) !important;
}

#reset-btn:hover * {
    color: #ffffff !important;
}

/* 未回答表示 */
.notice {
    gap: 19px !important;
    padding: 24px !important;
    margin-top: 28px !important;
    border-radius: 22px !important;
}

.notice-warning {
    color: #5e3000 !important;
    border: 3px solid #eb9723 !important;
    background: linear-gradient(135deg, #fffaf0, #ffe5ad) !important;
    box-shadow: 0 14px 30px rgba(120, 83, 14, .14);
}

.notice-icon {
    font-size: 2.75rem !important;
}

.notice h3 {
    color: #5e3000 !important;
    font-size: 1.43rem !important;
    font-weight: 950 !important;
}

.notice p {
    color: #5e3000 !important;
    font-size: 1.15rem !important;
    font-weight: 760 !important;
}

/* 診断結果 */
.result-section {
    margin-top: 37px !important;
}

.result-heading {
    gap: 18px !important;
    margin-bottom: 24px !important;
    padding: 20px 23px !important;
    border: 3px solid #735fd0;
    border-radius: 24px;
    background: linear-gradient(135deg, #ffffff, #f2edff);
    box-shadow: 0 15px 32px rgba(62, 51, 119, .14);
}

.result-heading > span {
    font-size: 3.3rem !important;
}

.result-heading p {
    color: #5639aa !important;
    font-size: .98rem !important;
    font-weight: 950 !important;
}

.result-heading h1 {
    color: #1a2550 !important;
    font-size: clamp(1.9rem, 4.4vw, 2.65rem) !important;
    font-weight: 950 !important;
    line-height: 1.36 !important;
}

.tie-message {
    color: #344165 !important;
    font-size: 1.12rem !important;
    font-weight: 730 !important;
    line-height: 1.75 !important;
}

.result-cards {
    gap: 22px !important;
}

.result-card {
    padding: 33px !important;
    border: 4px solid !important;
    border-radius: 29px !important;
    background: #ffffff !important;
    box-shadow: 0 19px 44px rgba(51, 55, 105, .18) !important;
}

.result-card::before {
    content: "✨";
    position: absolute;
    top: 18px;
    right: 21px;
    font-size: 2.05rem;
    opacity: .43;
}

.result-a {
    border-color: #e45780 !important;
    background: linear-gradient(145deg, #ffffff 64%, #ffedf4) !important;
}

.result-b {
    border-color: #1fa58e !important;
    background: linear-gradient(145deg, #ffffff 64%, #e7faf4) !important;
}

.result-c {
    border-color: #e99420 !important;
    background: linear-gradient(145deg, #ffffff 64%, #fff3d1) !important;
}

.result-d {
    border-color: #6473d9 !important;
    background: linear-gradient(145deg, #ffffff 64%, #ebeeff) !important;
}

.result-ribbon {
    padding: 8px 17px !important;
    border: 2px solid #8b72da;
    color: #493092 !important;
    background: #f2edff !important;
    font-size: 1.03rem !important;
    font-weight: 950 !important;
}

.result-main {
    gap: 19px !important;
}

.result-icon {
    width: 84px !important;
    height: 84px !important;
    border: 3px solid rgba(91, 71, 170, .20);
    border-radius: 24px !important;
    font-size: 2.85rem !important;
    box-shadow: 0 8px 19px rgba(64, 50, 120, .13);
}

.result-code {
    color: #533ba7 !important;
    font-size: .98rem !important;
    font-weight: 950 !important;
}

.result-card h2 {
    font-size: clamp(2.05rem, 4.9vw, 2.82rem) !important;
    font-weight: 950 !important;
}

.result-headline {
    color: #35415f !important;
    font-size: 1.27rem !important;
    font-weight: 900 !important;
    line-height: 1.52 !important;
}

.result-type {
    margin: 23px 0 13px !important;
    padding: 12px 17px !important;
    border: 2px solid #b29de8;
    color: #30215f !important;
    background: #f2edff !important;
    font-size: 1.22rem !important;
    font-weight: 950 !important;
}

.result-card p {
    color: #1d2945 !important;
    font-size: 1.2rem !important;
    font-weight: 630 !important;
    line-height: 1.98 !important;
}

.career-box {
    padding: 21px 22px !important;
    border: 3px solid #c6d3ec !important;
    border-radius: 18px !important;
    color: #1d2945 !important;
    background: #f6f9ff !important;
    font-size: 1.18rem !important;
    font-weight: 660 !important;
    line-height: 1.92 !important;
}

.career-box strong {
    color: #17275a !important;
    font-size: 1.22rem !important;
    font-weight: 950 !important;
}

.result-score {
    margin-top: 18px !important;
    color: #17213d !important;
    font-size: 1.3rem !important;
    font-weight: 880 !important;
}

/* 回答バランス */
.score-section {
    margin-top: 27px !important;
    padding: 26px !important;
    border: 3px solid #7480d5;
    border-radius: 26px !important;
    background: linear-gradient(135deg, #ffffff, #f3f6ff) !important;
    box-shadow: 0 14px 31px rgba(57, 62, 116, .13) !important;
}

.score-section h3 {
    color: #1a2550 !important;
    font-size: 1.64rem !important;
    font-weight: 950 !important;
}

.score-grid {
    gap: 14px !important;
}

.score-badge {
    min-height: 88px;
    padding: 16px !important;
    border: 3px solid !important;
    border-radius: 19px !important;
    box-shadow: 0 8px 17px rgba(51, 58, 108, .10);
}

.score-a {
    border-color: #e45780 !important;
    background: #fff5f8 !important;
}

.score-b {
    border-color: #1fa58e !important;
    background: #effbf7 !important;
}

.score-c {
    border-color: #e99420 !important;
    background: #fff9ed !important;
}

.score-d {
    border-color: #6473d9 !important;
    background: #f4f5ff !important;
}

.score-letter {
    width: 49px !important;
    height: 49px !important;
    border-radius: 15px !important;
    color: #ffffff !important;
    font-size: 1.31rem !important;
    font-weight: 950 !important;
}

.score-a .score-letter { background: #c62558 !important; }
.score-b .score-letter { background: #087f6f !important; }
.score-c .score-letter { background: #bf5d00 !important; }
.score-d .score-letter { background: #3e50b9 !important; }

.score-number {
    color: #17213d !important;
    font-size: 1.68rem !important;
    font-weight: 950 !important;
}

.score-course {
    font-size: 1.04rem !important;
    font-weight: 950 !important;
    line-height: 1.42 !important;
}

.disclaimer {
    margin-top: 22px !important;
    padding: 17px 19px;
    border: 2px dashed #858eb1;
    border-radius: 16px;
    color: #344165 !important;
    background: rgba(255,255,255,.86);
    font-size: 1.08rem !important;
    font-weight: 710 !important;
    line-height: 1.82 !important;
}

/* フッター */
.footer-note {
    position: relative;
    margin-top: 33px !important;
    padding: 21px 25px !important;
    border: 3px solid #d99a26;
    border-radius: 21px !important;
    color: #4b3300 !important;
    background: linear-gradient(135deg, #fffdf3, #ffebb1) !important;
    box-shadow: 0 12px 27px rgba(119, 87, 17, .13);
    font-size: 1.14rem !important;
    font-weight: 820 !important;
    line-height: 1.8 !important;
}

.footer-note::before {
    content: "🎓 ";
    font-size: 1.45rem;
}

.footer-note::after {
    content: " 🌟";
    font-size: 1.45rem;
}

/* タブレット */
@media (max-width: 820px) {
    html {
        font-size: 17px;
    }

    .course-overview,
    .score-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }

    .hero {
        padding: 39px 21px 37px !important;
    }

    .section-lead::before {
        left: 14px;
        font-size: 2.05rem;
    }

    .section-lead::after {
        right: 14px;
        font-size: 1.45rem;
    }

    .section-lead h2,
    .section-lead p {
        margin-left: 44px !important;
        margin-right: 38px !important;
    }

    .question-card,
    .result-card {
        padding-left: 19px !important;
        padding-right: 19px !important;
    }
}

/* スマートフォン */
@media (max-width: 520px) {
    html {
        font-size: 16px;
    }

    .gradio-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .course-overview,
    .score-grid {
        grid-template-columns: 1fr !important;
    }

    .hero::before,
    .hero::after {
        opacity: .15 !important;
    }

    .section-lead {
        padding: 22px 15px !important;
    }

    .section-lead::before,
    .section-lead::after {
        display: none;
    }

    .section-lead h2,
    .section-lead p {
        margin-left: 0 !important;
        margin-right: 0 !important;
    }

    .question-title {
        gap: 11px !important;
        padding-right: 0;
    }

    .question-card::before {
        display: none;
    }

    .question-number {
        min-width: 63px !important;
        min-height: 45px !important;
        font-size: 1.24rem !important;
    }

    .question-card label,
    .question-card label span,
    .question-card label p {
        font-size: 1.1rem !important;
    }

    .action-row {
        flex-direction: column;
    }

    .result-heading {
        align-items: flex-start !important;
        padding: 18px !important;
    }

    .result-heading > span {
        font-size: 2.6rem !important;
    }

    .result-main {
        align-items: flex-start !important;
        gap: 14px !important;
    }

    .result-icon {
        width: 67px !important;
        height: 67px !important;
        font-size: 2.2rem !important;
    }

    .result-card {
        padding: 25px 19px !important;
    }
}


/* =========================================================
   タイトル・見出し・教示文・質問文の文字サイズ調整
   ========================================================= */

/* 英字の小見出し */
.hero-kicker {
    font-size: 0.9rem !important;
}

/* Webアプリのメインタイトル */
.hero h1 {
    font-size: clamp(1.95rem, 4.8vw, 3rem) !important;
    line-height: 1.3 !important;
}

/* タイトル下の導入・教示文 */
.hero p {
    font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
    line-height: 1.85 !important;
}

/* 「あなたにぴったりのコースが見つかります」 */
.hero p strong {
    font-size: 1.1rem !important;
}

/* 質問前の見出し */
.section-lead h2 {
    font-size: clamp(1.42rem, 3vw, 1.8rem) !important;
    line-height: 1.45 !important;
}

/* 質問前の教示文 */
.section-lead p {
    font-size: clamp(1.03rem, 2.1vw, 1.18rem) !important;
    line-height: 1.72 !important;
}

/* 診断方法の教示文 */
.section-lead .diagnosis-guide {
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
}

/* Q1～Q4 */
.question-number {
    min-width: 68px !important;
    min-height: 45px !important;
    padding: 2px 14px !important;
    font-size: 1.22rem !important;
}

/* 各質問文 */
.question-text {
    font-size: clamp(1.17rem, 2.45vw, 1.35rem) !important;
    line-height: 1.55 !important;
}

/* スマートフォン表示 */
@media (max-width: 520px) {
    .hero h1 {
        font-size: clamp(1.8rem, 8.3vw, 2.35rem) !important;
    }

    .hero p {
        font-size: 1.02rem !important;
    }

    .hero p strong {
        font-size: 1.05rem !important;
    }

    .section-lead h2 {
        font-size: 1.38rem !important;
    }

    .section-lead p,
    .section-lead .diagnosis-guide {
        font-size: 1rem !important;
    }

    .question-number {
        min-width: 59px !important;
        min-height: 41px !important;
        font-size: 1.1rem !important;
    }

    .question-text {
        font-size: 1.14rem !important;
    }
}


/* =========================================================
   タイトル・見出し・教示文・質問文をさらに一段階縮小
   ========================================================= */

/* 英字の小見出し */
.hero-kicker {
    font-size: 0.82rem !important;
    padding: 7px 16px !important;
}

/* Webアプリのメインタイトル */
.hero h1 {
    font-size: clamp(1.72rem, 4.2vw, 2.62rem) !important;
    line-height: 1.3 !important;
}

/* タイトル下の導入・教示文 */
.hero p {
    font-size: clamp(0.98rem, 1.95vw, 1.12rem) !important;
    line-height: 1.8 !important;
}

/* 「あなたにぴったりのコースが見つかります」 */
.hero p strong {
    font-size: 1rem !important;
    padding: 5px 13px !important;
}

/* 質問前の見出し */
.section-lead h2 {
    font-size: clamp(1.25rem, 2.6vw, 1.58rem) !important;
    line-height: 1.42 !important;
}

/* 質問前の教示文 */
.section-lead p {
    font-size: clamp(0.96rem, 1.85vw, 1.08rem) !important;
    line-height: 1.68 !important;
}

/* 診断方法の教示文 */
.section-lead .diagnosis-guide {
    font-size: 0.97rem !important;
    line-height: 1.6 !important;
    padding: 9px 15px !important;
}

/* Q1～Q4 */
.question-number {
    min-width: 62px !important;
    min-height: 41px !important;
    padding: 2px 12px !important;
    font-size: 1.08rem !important;
}

/* 各質問文 */
.question-text {
    font-size: clamp(1.07rem, 2.15vw, 1.22rem) !important;
    line-height: 1.52 !important;
}

/* タイトル・教示部分の余白も少し圧縮 */
.hero {
    padding-top: 40px !important;
    padding-bottom: 36px !important;
}

.section-lead {
    padding-top: 21px !important;
    padding-bottom: 21px !important;
}

/* スマートフォン表示 */
@media (max-width: 520px) {
    .hero-kicker {
        font-size: 0.76rem !important;
    }

    .hero h1 {
        font-size: clamp(1.58rem, 7.4vw, 2.05rem) !important;
    }

    .hero p {
        font-size: 0.94rem !important;
        line-height: 1.72 !important;
    }

    .hero p strong {
        font-size: 0.96rem !important;
    }

    .section-lead h2 {
        font-size: 1.23rem !important;
    }

    .section-lead p {
        font-size: 0.94rem !important;
    }

    .section-lead .diagnosis-guide {
        font-size: 0.92rem !important;
    }

    .question-number {
        min-width: 55px !important;
        min-height: 38px !important;
        padding: 1px 10px !important;
        font-size: 1rem !important;
    }

    .question-text {
        font-size: 1.04rem !important;
        line-height: 1.48 !important;
    }
}


/* =========================================================
   問題選択肢以外の文字サイズを全体的に縮小
   ※回答選択肢（.question-card label 内）は変更しない
   ========================================================= */

/* アプリ全体の基準文字サイズ */
html {
    font-size: 16px !important;
}

.gradio-container {
    font-size: 0.98rem !important;
    line-height: 1.68 !important;
}

/* タイトル領域 */
.hero-kicker {
    font-size: 0.72rem !important;
    padding: 6px 14px !important;
}

.hero h1 {
    font-size: clamp(1.48rem, 3.7vw, 2.25rem) !important;
    line-height: 1.28 !important;
}

.hero p {
    font-size: clamp(0.88rem, 1.7vw, 1rem) !important;
    line-height: 1.72 !important;
}

.hero p strong {
    font-size: 0.9rem !important;
    padding: 4px 11px !important;
}

/* 上部コースカード */
.mini-icon {
    font-size: 2.15rem !important;
}

.mini-code {
    min-width: 38px !important;
    padding: 3px 11px !important;
    font-size: 0.94rem !important;
}

.mini-title {
    font-size: 1rem !important;
    line-height: 1.42 !important;
}

/* 教示・見出し */
.section-lead h2 {
    font-size: clamp(1.1rem, 2.2vw, 1.4rem) !important;
    line-height: 1.4 !important;
}

.section-lead p {
    font-size: clamp(0.87rem, 1.55vw, 0.98rem) !important;
    line-height: 1.62 !important;
}

.section-lead .diagnosis-guide {
    font-size: 0.88rem !important;
    line-height: 1.55 !important;
    padding: 8px 13px !important;
}

/* Q番号・質問文 */
.question-number {
    min-width: 56px !important;
    min-height: 37px !important;
    padding: 1px 10px !important;
    font-size: 0.96rem !important;
}

.question-text {
    font-size: clamp(0.98rem, 1.9vw, 1.1rem) !important;
    line-height: 1.48 !important;
}

/*
問題選択肢の文字サイズはここで明示的に維持する。
既存の最終設定値をそのまま適用。
*/
.question-card label,
.question-card label span,
.question-card label p {
    font-size: 1.19rem !important;
    line-height: 1.78 !important;
}

/* 操作ボタン */
#diagnose-btn,
#diagnose-btn * {
    font-size: 1.08rem !important;
}

#reset-btn,
#reset-btn * {
    font-size: 1.04rem !important;
}

/* 未回答メッセージ */
.notice-icon {
    font-size: 2.1rem !important;
}

.notice h3 {
    font-size: 1.12rem !important;
}

.notice p {
    font-size: 0.94rem !important;
}

/* 診断結果見出し */
.result-heading > span {
    font-size: 2.45rem !important;
}

.result-heading p {
    font-size: 0.78rem !important;
}

.result-heading h1 {
    font-size: clamp(1.45rem, 3.4vw, 2rem) !important;
    line-height: 1.3 !important;
}

.tie-message {
    font-size: 0.94rem !important;
    line-height: 1.62 !important;
}

/* 診断結果カード */
.result-ribbon {
    font-size: 0.88rem !important;
    padding: 6px 13px !important;
}

.result-icon {
    width: 68px !important;
    height: 68px !important;
    font-size: 2.25rem !important;
}

.result-code {
    font-size: 0.8rem !important;
}

.result-card h2 {
    font-size: clamp(1.55rem, 3.7vw, 2.2rem) !important;
    line-height: 1.28 !important;
}

.result-headline {
    font-size: 1.02rem !important;
    line-height: 1.45 !important;
}

.result-type {
    font-size: 1rem !important;
    padding: 9px 14px !important;
}

.result-card p {
    font-size: 0.98rem !important;
    line-height: 1.78 !important;
}

.career-box {
    font-size: 0.96rem !important;
    line-height: 1.72 !important;
}

.career-box strong {
    font-size: 1rem !important;
}

.result-score {
    font-size: 1.02rem !important;
}

/* 回答バランス */
.score-section h3 {
    font-size: 1.28rem !important;
}

.score-letter {
    width: 42px !important;
    height: 42px !important;
    font-size: 1.08rem !important;
}

.score-number {
    font-size: 1.38rem !important;
}

.score-course {
    font-size: 0.88rem !important;
    line-height: 1.32 !important;
}

/* 注意書き・フッター */
.disclaimer {
    font-size: 0.88rem !important;
    line-height: 1.62 !important;
}

.footer-note {
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
}

/* 装飾絵文字も少し縮小 */
.hero::before,
.hero::after {
    font-size: clamp(2.2rem, 5vw, 3.6rem) !important;
}

.section-lead::before {
    font-size: 2.1rem !important;
}

.section-lead::after {
    font-size: 1.5rem !important;
}

.question-card::before {
    font-size: 1.9rem !important;
}

.result-card::before {
    font-size: 1.65rem !important;
}

/* スマートフォン表示 */
@media (max-width: 520px) {
    html {
        font-size: 15px !important;
    }

    .hero-kicker {
        font-size: 0.68rem !important;
    }

    .hero h1 {
        font-size: clamp(1.38rem, 6.6vw, 1.82rem) !important;
    }

    .hero p {
        font-size: 0.84rem !important;
    }

    .hero p strong {
        font-size: 0.87rem !important;
    }

    .mini-title {
        font-size: 0.94rem !important;
    }

    .section-lead h2 {
        font-size: 1.08rem !important;
    }

    .section-lead p,
    .section-lead .diagnosis-guide {
        font-size: 0.84rem !important;
    }

    .question-number {
        min-width: 50px !important;
        min-height: 34px !important;
        font-size: 0.9rem !important;
    }

    .question-text {
        font-size: 0.96rem !important;
    }

    /* 問題選択肢はスマートフォンでも維持 */
    .question-card label,
    .question-card label span,
    .question-card label p {
        font-size: 1.19rem !important;
        line-height: 1.72 !important;
    }

    #diagnose-btn,
    #diagnose-btn *,
    #reset-btn,
    #reset-btn * {
        font-size: 1rem !important;
    }

    .result-heading h1 {
        font-size: 1.38rem !important;
    }

    .result-card h2 {
        font-size: 1.55rem !important;
    }

    .result-headline,
    .result-type,
    .result-card p,
    .career-box,
    .result-score {
        font-size: 0.92rem !important;
    }

    .score-section h3 {
        font-size: 1.16rem !important;
    }

    .score-course,
    .disclaimer,
    .footer-note {
        font-size: 0.82rem !important;
    }
}


/* =========================================================
   同率時の「迷っている」診断コメント
   ========================================================= */

.tie-guidance {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin: 0 0 22px;
    padding: 21px 22px;
    border: 3px solid #46a88f;
    border-radius: 22px;
    color: #173f39;
    background:
        linear-gradient(135deg, rgba(255,255,255,.92), rgba(232,255,247,.95)),
        linear-gradient(90deg, #fff8ce, #e6fff6);
    box-shadow: 0 13px 29px rgba(39, 117, 97, .14);
}

.tie-guidance-icon {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    justify-content: center;
    width: 54px;
    height: 54px;
    border: 2px solid #69bba7;
    border-radius: 17px;
    background: #ffffff;
    font-size: 1.8rem;
    box-shadow: 0 6px 14px rgba(39, 117, 97, .12);
}

.tie-guidance-body {
    min-width: 0;
}

.tie-guidance h2 {
    margin: 1px 0 12px;
    color: #155e54 !important;
    font-size: 1.13rem !important;
    font-weight: 950 !important;
    line-height: 1.45 !important;
}

.tie-guidance-point {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    margin: 9px 0;
    padding: 10px 12px;
    border: 1px solid #b9e3d8;
    border-radius: 13px;
    background: rgba(255,255,255,.78);
}

.tie-guidance-point > span {
    flex: 0 0 auto;
    padding-top: 1px;
    font-size: 1.08rem;
}

.tie-guidance-point p {
    margin: 0 !important;
    color: #23453f !important;
    font-size: 0.94rem !important;
    font-weight: 650 !important;
    line-height: 1.7 !important;
}

.tie-guidance-point strong {
    color: #124f47 !important;
    font-weight: 950 !important;
}

@media (max-width: 520px) {
    .tie-guidance {
        gap: 11px;
        padding: 17px 15px;
    }

    .tie-guidance-icon {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        font-size: 1.45rem;
    }

    .tie-guidance h2 {
        font-size: 1rem !important;
    }

    .tie-guidance-point {
        gap: 7px;
        padding: 9px 10px;
    }

    .tie-guidance-point p {
        font-size: 0.88rem !important;
        line-height: 1.62 !important;
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
    title="心理臨床学科 学びのコンパス",
) as demo:
    gr.HTML(
        """
        <header class="hero">
            <div class="hero-kicker">4 QUESTIONS · COURSE FINDER</div>
            <h1>🧭 心理臨床学科<br>学びのコンパス</h1>
            <p>
                「誰かの力になりたい」「心や社会の仕組みを知りたい」<br>
                ……そんなあなたの未来の姿をのぞいてみませんか？<br>
                4つの質問に、直感で答えてみてね！<br>
                <strong>あなたにぴったりのコースが見つかります</strong>
            </p>
        </header>
        """
    )

    gr.HTML(course_overview_html())

    gr.HTML(
        """
        <div class="section-lead">
            <h2>4つの質問に、直感で答えてみてね！</h2>
            <p>各質問で、あなたの気持ちに一番近い答えを1つ選んでください。正解・不正解はありません。</p>
            <p class="diagnosis-guide">選んだA・B・C・Dのうち、一番多かった文字が、あなたの未来のヒントです！</p>
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
