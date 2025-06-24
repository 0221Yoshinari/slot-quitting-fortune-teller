import streamlit as st
import random

# --- 定義データ ---
# 質問項目と選択肢、および内部的なスコア付け
# スコアは例であり、表示パターンに影響します
QUESTIONS_DATA = [
    {
        "question": "今日の台とのつながり具合は？",
        "options": {"運命共同体": 5, "ソウルメイト": 3, "微妙な距離感": 0, "赤の他人": -5},
        "key": "q1_tsunagari"
    },
    {
        "question": "あなた自身のエスパー度合いは？",
        "options": {"裏モノ感知": 5, "ゾーンが見える": 3, "なんとなく分かる": 1, "全然分からない": -2},
        "key": "q2_esper"
    },
    {
        "question": "現在の台の調子はどう感じますか？",
        "options": {"絶好調！GOGOが止まらない": 5, "まあまあ、これから": 2, "波が荒い": -1, "どん底、地獄の業火": -5},
        "key": "q3_cond"
    },
    {
        "question": "過去に「やめて大失敗（後任者が大噴き）」の経験はありますか？",
        "options": {"はい、吐きそうです": -3, "はい、たまに": -1, "いいえ、常に完璧": 2, "いいえ、打たない": 0},
        "key": "q4_failure_exp"
    },
    {
        "question": "今まさに「やめ時」だと感じますか？",
        "options": {"はい、脳がそう指令する": -5, "いや、まだイケる": 2, "迷い中、助けてAI！": 0, "ヤメるという選択肢はない": 5},
        "key": "q5_feeling"
    },
    {
        "question": "隣の台は出玉爆発中ですか？",
        "options": {"はい、眩しい": -2, "はい、でも私の方が": 1, "いいえ、ドンマイ": 0, "いいえ、私も瀕死": -3},
        "key": "q6_neighbor"
    },
    {
        "question": "今日のパチ屋のトイレは綺麗でしたか？",
        "options": {"ピカピカ": 1, "普通": 0, "ちょっと…": -1, "行ってない": 0},
        "key": "q7_toilet"
    },
    {
        "question": "今日の運勢は？（来店前に占ったとして）",
        "options": {"大吉": 3, "吉": 2, "中吉": 1, "小吉": 0, "末吉": -1, "凶": -2, "大凶": -3},
        "key": "q8_fortune"
    },
    {
        "question": "GOGOランプに何かが宿っているのを感じますか？",
        "options": {"確信した": 4, "何となく": 2, "気のせい": 0, "見えない": -2},
        "key": "q9_gogo_aura"
    },
    {
        "question": "今日、店員さんが何回あなたの台に注目しましたか？",
        "options": {"3回以上": 3, "1,2回": 1, "0回": 0, "私を避けている": -2},
        "type": "radio_custom_value_map", # 数値入力からラジオボタンに変更するが、スコアは変わらない
        "key": "q10_staff_attention"
    },
    {
        "question": "あなたの後ろで、誰か台を待っていますか？",
        "options": {"はい、殺気を感じる": -3, "はい、チラ見": -1, "いいえ、快適": 1, "いいえ、私だけ": 0},
        "key": "q11_waiting"
    },
    {
        "question": "今日の最終目標出玉は何枚でしたか？",
        "options": {"目標達成済み": 3, "もう少し": 1, "絶望的": -2, "目標設定なし": 0}, # 数値入力から選択肢に変更
        "key": "q12_target_achieved"
    },
    {
        "question": "今の台、愛せますか？",
        "options": {"愛してる！": 5, "まあまあ好き": 2, "嫌いになりそう": -2, "無理": -5},
        "key": "q13_love_machine"
    },
    {
        "question": "お昼ご飯、美味しかったですか？",
        "options": {"最高！": 1, "普通": 0, "まずかった": -1, "食べてない": -1},
        "key": "q14_lunch"
    },
    {
        "question": "家で待つ家族（ペット含む）の顔がちらつきますか？",
        "options": {"はい、天使の笑顔": -4, "はい、そろそろ": -2, "いいえ、まだ闘う": 2, "家族？何それ": 5},
        "key": "q15_family_face"
    },
    {
        "question": "最終ボーナスから100G以内で当たっていますか？",
        "options": {"はい、連荘中": 3, "はい、すぐに": 2, "いいえ、ハマり中": -2},
        "key": "q16_within_100g"
    },
    {
        "question": "今日のレバーオン、脳汁が出ましたか？",
        "options": {"毎日出る": 3, "たまに": 1, "今日はまだ": -1, "出ない": -3},
        "key": "q17_noujiru"
    },
    {
        "question": "このツールにどこまで従いますか？",
        "options": {"全面的に信頼！": 2, "参考程度": 1, "半信半疑": 0, "自分の感性が全て": -2},
        "key": "q18_trust_tool"
    },
    {
        "question": "現在、あなたの背後でジャグラーのBGMが聞こえますか？",
        "options": {"はい、ファンキー！": 2, "はい、クラシック！": 1, "いいえ、別の台": 0, "無音": -1},
        "key": "q19_bgm"
    },
    {
        "question": "今日のあなたのラッキーカラーは何色でしたか？",
        "options": {"GOGOグリーン": 3, "ボーナスピンク": 2, "チェリーレッド": 1, "設定1ブラック": -2},
        "key": "q20_lucky_color"
    },
]

# --- 結果メッセージのパターン（30個） ---
# スコア帯に応じて表示されるメッセージを変える
# スコア範囲は仮で調整。質問の数やスコア付けで変わる。
# 各メッセージに「ユーモラス」な要素を加える。
RESULT_MESSAGES = {
    "score_very_low": [ # 超ヤメ時！危険信号！
        "🚨 **緊急速報！台があなたを嫌っています！** 今すぐ席を立ち、美味しいご飯を食べに行きましょう。後悔する前に！",
        "💀 **強制終了推奨！** このまま続行すると、明日の朝食はパンの耳だけになる未来が見えます。逃げて！",
        "🏃‍♂️ **高速退避！GOGO！ダッシュ！** あなたの背後に、やめ時の妖精が立っています。ダッシュで逃げましょう！",
        "🚫 **台からのレッドカード！** あなたの負けです。潔く席を立ち、遠くの景色でも眺めて心を落ち着かせましょう。",
        "💸 **財布が悲鳴を上げています。** 今すぐ席を立ち、銀行口座の残高を確認してください。手遅れになる前に！",
        "🌪️ **破滅の嵐が来ています！** 逃げてください、台があなたに牙を剥いています！",
        "👹 **魔界への扉が開いています！** その扉の向こうは、地獄です。絶対に入らないでください。",
        "👻 **幽霊があなたの肩を叩いています。** 『もう…ヤメロ…』と囁いていますよ？"
    ],
    "score_low": [ # ヤメ推奨！勇気ある撤退！
        "👋 **お疲れ様でした！** この台はもう、あなたに微笑みかけることはないでしょう。次の台との出会いに期待しましょう。",
        "🚶‍♀️ **冷静な判断こそ勝利への道。** 今日のところはこれくらいで勘弁してやりましょう。パチプロは引き際も肝心！",
        "🍵 **休憩タイムならぬ、退散タイム。** 一度ホールを出て、リフレッシュするのもアリですよ。リセットされてるかも？",
        "🔄 **心のリセットボタン、ポチッとな！** 次の機会に賭けて、今日は撤退しましょう。英断です。",
        "😈 **隣の台があなたを嘲笑っています。** 今すぐヤメて、心の平穏を取り戻しましょう。ヤメれば勝てる日もある！",
        "📉 **台が『もう無理…』と囁いています。** その声を無視してはいけません。きっと神の声です。",
        "💤 **体力の限界！** あなたの集中力はもう限界です。眠気と戦うのは、別の戦場で。",
        "✉️ **謎のメッセージ『ヤメ』。** あなたの第六感が、そう告げている気がしませんか？"
    ],
    "score_neutral": [ # 迷い中…熟考を！
        "🤔 **思考は深い沼。** この台はあなたを試しています。もう一度、己の感性とデータを見つめ直しましょう。",
        "⚖️ **天秤は揺れています。** 続行かヤメか…あなたの選んだ道が、今日の運命を決めます。後悔なき選択を！",
        "🎲 **運命のサイコロを振ってみますか？** 続けるも地獄、ヤメるも地獄…いや、そうでもないかも？",
        "🧘‍♀️ **無の心でレバーを叩け。** 邪念を捨てて打てば、GOGOランプが光る…かもしれません。",
        "🔮 **おみくじ結果は「吉」。** どちらに転ぶか分かりませんが、あなたの行動次第で未来は変わる！コンビニで甘いものでも買って考え直せ！",
        "🌈 **GOGOランプが、まだ見ぬ未来を暗示している…かも？** あと100Gだけ、試してみては？きっと何かが見える！",
        "🍀 **運命は五分五分。** 己の感性を信じるか、それとも現実を見るか…全てはあなた次第です。",
        "☕ **一度冷静になりましょう。** ホール内のカフェで一息入れてから、最終決断を。意外な閃きがあるかも？"
    ],
    "score_high": [ # 続行推奨！チャンス到来！
        "💪 **まだ戦える！** その台はあなたに「まだイケる！」と語りかけています。粘り勝ちを狙いましょう。",
        "📈 **上昇気流に乗れ！** 今日のあなたは、パチスロの神に愛されているかもしれません。この波を逃すな！",
        "💰 **諭吉があなたを呼んでいる！** このまま続行すれば、きっと財布がパンパンになるでしょう。夢を掴め！",
        "✨ **GOGOランプがあなたの心に輝きを放つ。** 勝利の予感がしますね！このチャンスを逃す手はありません！",
        "🦸‍♂️ **あなたのエスパー能力が目覚める時！** 今こそ、その超能力を解放し、設定6を掴み取りましょう！",
        "🏆 **勝利の女神があなたに微笑んでいる！** このまま続行して、伝説を作ってください！",
        "🚀 **ロケットスタートの予感！** ここからが本当の勝負です。目指せ万枚！"
    ],
    "score_very_high": [ # 超続行！神がかり！
        "🔥 **止め打ち厳禁！** その台はあなたを裏切らないでしょう。勝利の雄叫びを上げましょう！閉店まで全ツッパ！",
        "👑 **KING OF JUGGLER！** 今日のあなたは無敵です。設定6を掴んだかもしれません！最高の瞬間を味わい尽くせ！",
        "🤩 **脳汁大放出警報発令中！** その台はあなたのモノです。閉店まで全ツッパしましょう！隣の視線も気にせず！",
        "💫 **神の領域へようこそ。** あなたのパチスロ人生で最高の瞬間が訪れています。この奇跡を思う存分味わいましょう！"
    ]
}

# --- Streamlit UI 部分 ---

st.set_page_config(
    page_title="やめ時おみくじツッパ！",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🔮"
)

st.title("🎰 パチスロやめ時おみくじツッパ！ 🎰")
st.markdown("### あなたの第六感と、今日の運命を占います！")

st.markdown(
    """
    このツールは、あなたの『第六感』と『台との絆』を試す、全く新しいやめ時おみくじツールです！
    数値や解析は一切関係ありません。あなたの直感と、クスッと笑える質問に答えて、今日の運勢を占ってみましょう！
    ---
    """
)

st.header("▼質問に答えて、あなたの『やめ時』を占おう！▼")
st.markdown("正直に、直感で答えるのがポイントです！")

user_answers = {}
total_score = 0

with st.container(border=True):
    for i, q_data in enumerate(QUESTIONS_DATA):
        st.markdown(f"##### Q{i+1}. {q_data['question']}")
        
        # 質問タイプに応じてウィジェットを生成
        if q_data['key'] in ["q6_wallet_money", "q7_closing_hours", "q10_staff_attention", "q14_target_medals"]: # 数値入力
            if q_data['key'] == "q6_wallet_money":
                answer = st.number_input("残りいくら？(円)", min_value=0, value=0, step=1000, key=q_data['key'])
                if answer >= 50000: score = q_data['options'].get("目標達成済み", 0) # 仮のスコアロジック
                elif answer >= 10000: score = q_data['options'].get("もう少し", 0)
                elif answer > 0: score = q_data['options'].get("絶望的", 0)
                else: score = q_data['options'].get("目標設定なし", 0)
            elif q_data['key'] == "q7_closing_hours":
                answer = st.number_input("残り時間？(時間)", min_value=0, max_value=10, value=0, key=q_data['key'])
                if answer >= 5: score = 2
                elif answer >= 3: score = 1
                elif answer > 0: score = 0
                else: score = -2
            elif q_data['key'] == "q10_staff_attention":
                answer = st.number_input("何回？(回)", min_value=0, value=0, key=q_data['key'])
                if answer >= 3: score = 3
                elif answer >= 1: score = 1
                else: score = 0
            elif q_data['key'] == "q14_target_medals":
                answer = st.number_input("目標出玉は何枚？", min_value=0, value=0, step=1000, key=q_data['key'])
                if answer == 0: score = 0
                elif answer >= 50000: score = 5
                elif answer >= 10000: score = 3
                else: score = 1
            user_answers[q_data['key']] = answer
            total_score += score
        else: # 選択肢
            options_list = list(q_data['options'].keys())
            answer = st.selectbox("選択肢を選んでください", options_list, key=q_data['key'])
            score = q_data['options'].get(answer, 0)
            user_answers[q_data['key']] = answer
            total_score += score
        
        st.markdown("---") # 区切り線

st.markdown("### さあ、あなたのやめ時は！？")
predict_button = st.button("🔮 やめ時を占う！", type="primary")

if predict_button:
    # スコアに基づいたメッセージ選択
    if total_score >= 30:
        result_category = "score_very_high"
    elif total_score >= 10:
        result_category = "score_high"
    elif total_score >= -9: # ニュートラルの範囲を調整
        result_category = "score_neutral"
    elif total_score >= -29:
        result_category = "score_low"
    else:
        result_category = "score_very_low"
    
    selected_message = random.choice(RESULT_MESSAGES[result_category])
    
    st.subheader("▼おみくじ結果▼")
    st.markdown(f"## {selected_message}")
    st.markdown(f"（合計スコア: {total_score}点）")
    st.info("※この結果はあくまでおふざけです。遊技は自己責任でお願いします！")