import streamlit as st
import streamlit.components.v1 as components
from questions import QUESTIONS
from results import RESULT_TYPES, calculate_result

st.set_page_config(page_title="ANIMAL PATH", page_icon="🌿", layout="wide")

ANIMALS = {
    "토끼": {"emoji": "🐰", "line": "작은 발걸음으로 함께 떠나볼까요?"},
    "강아지": {"emoji": "🐶", "line": "오늘은 어떤 친구들을 만나게 될까요?"},
    "고양이": {"emoji": "🐱", "line": "서두르지 말고 천천히 둘러봐요."},
    "악어": {"emoji": "🐊", "line": "새로운 길도 씩씩하게 가보자고요!"},
}

if "page" not in st.session_state:
    st.session_state.page = "home"
if "animal" not in st.session_state:
    st.session_state.animal = None
if "answers" not in st.session_state:
    st.session_state.answers = []

def go(page):
    st.session_state.page = page
    st.rerun()

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');
    :root { --cream:#fbf6eb; --ink:#4f5146; --green:#9ebc91; --deep:#627c5a; --pink:#e9bcb4; --lav:#d9d2e8; }
    .stApp { background: radial-gradient(circle at 15% 10%, #fffdf7 0, transparent 35%), linear-gradient(145deg,#fbf6eb,#f1f0e4); color:var(--ink); }
    html, body, [class*="css"] { font-family:'Gowun Dodum',sans-serif; }
    h1,h2,h3,.brand { font-family:'Jua',sans-serif !important; color:#596b51; }
    .block-container { max-width: 980px; padding-top: 2.2rem; padding-bottom: 3rem; }
    .hero { text-align:center; padding:2.5rem 1.2rem 2rem; border:1px solid #e9e2d3; border-radius:28px; background:rgba(255,253,247,.76); box-shadow:0 12px 35px rgba(92,105,75,.08); }
    .brand { font-size: clamp(2.6rem,7vw,4.8rem); letter-spacing:.08em; margin:0; }
    .subtitle { color:#8b907c; font-size:1rem; letter-spacing:.12em; margin-top:.25rem; }
    .story { color:#6d725f; font-size:1.12rem; line-height:1.8; margin:1rem auto; max-width:620px; }
    .forest { position:relative; overflow:hidden; min-height:190px; border-radius:24px; margin:1.2rem 0; background:linear-gradient(#e7eee0 0 58%,#cbd9b9 58% 100%); border:1px solid #d7dfcb; }
    .forest:before,.forest:after { content:""; position:absolute; bottom:34px; width:180px; height:180px; border-radius:50%; background:#b6c9a7; opacity:.55; }
    .forest:before {left:-35px}.forest:after{right:-25px;background:#a8c09b}
    .path { position:absolute; bottom:-42px; left:28%; width:48%; height:125px; background:#e8d8bd; border-radius:50% 50% 0 0; transform:rotate(-3deg); }
    .sun { position:absolute; right:14%; top:20px; width:55px; height:55px; border-radius:50%; background:#f7df9f; box-shadow:0 0 35px #f7df9f; }
    .floating { position:absolute; z-index:2; font-size:2.5rem; animation:float 3s ease-in-out infinite; }
    .float1{left:18%;top:24px}.float2{right:25%;top:75px;animation-delay:1s}
    @keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
    .walker { display:inline-block; font-size:4.5rem; animation:walk 1s ease-in-out infinite alternate; filter:drop-shadow(0 8px 4px #78836a33); }
    @keyframes walk {from{transform:translateX(-5px) translateY(0) rotate(-3deg)}to{transform:translateX(8px) translateY(-5px) rotate(3deg)}}
    .dancer { display:inline-block; font-size:6rem; animation:dance .65s ease-in-out infinite alternate; }
    @keyframes dance {from{transform:rotate(-12deg) translateY(0)}to{transform:rotate(12deg) translateY(-13px)}}
    .choice-card { background:#fffdf7; border:1px solid #e9e2d3; border-radius:20px; padding:1.1rem; text-align:center; min-height:130px; }
    .choice-emoji {font-size:2.5rem}
    .eyebrow {color:#929780;font-size:.82rem;letter-spacing:.12em;font-weight:bold}
    .question {font-family:'Jua',sans-serif;color:#586b50;font-size:1.8rem;line-height:1.4;margin:.45rem 0 1rem}
    .progress-label {color:#89917e;font-size:.9rem}
    .result-card {background:rgba(255,253,247,.9);border:1px solid #e7dfcf;border-radius:26px;padding:1.6rem;text-align:center}
    div.stButton > button {border-radius:16px;border:1px solid #d8dfcf;background:#fffdf7;color:#586b50;font-weight:600;min-height:3rem;transition:all .2s}
    div.stButton > button:hover {border-color:#9ebc91;background:#eef3e8;color:#455c40;transform:translateY(-2px)}
    .stProgress > div > div > div > div {background:#91ad83}
    [data-testid="stMarkdownContainer"] p {line-height:1.7}
    </style>
    """, unsafe_allow_html=True)

def forest_scene(character="🌿", first_person=False):
    if first_person:
        st.markdown("""
        <div class="forest" style="min-height:220px">
          <div class="sun"></div><div class="path" style="left:20%;width:60%;transform:rotate(0)"></div>
          <span class="floating float1">🌼</span><span class="floating float2">🍄</span>
          <div style="position:absolute;z-index:3;left:8%;top:35%;font-size:2rem">🌳</div>
          <div style="position:absolute;z-index:3;right:8%;top:30%;font-size:2.2rem">🌲</div>
          <div style="position:absolute;z-index:4;left:43%;top:45%;font-size:1.5rem">↙　↘</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="forest">
          <div class="sun"></div><div class="path"></div>
          <span class="floating float1">🌼</span><span class="floating float2">🦋</span>
          <div style="position:absolute;z-index:3;left:45%;bottom:32px"><span class="walker">{character}</span></div>
          <div style="position:absolute;z-index:3;left:8%;top:25%;font-size:2.3rem">🌳</div>
          <div style="position:absolute;z-index:3;right:8%;top:28%;font-size:2.2rem">🌲</div>
        </div>
        """, unsafe_allow_html=True)

def reset():
    st.session_state.page = "home"
    st.session_state.animal = None
    st.session_state.answers = []
    st.rerun()

inject_css()

if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">A LITTLE JOURNEY TO FIND YOURSELF</div>
      <h1 class="brand">ANIMAL PATH</h1>
      <div class="subtitle">작은 선택들이 모여, 나만의 길이 되다</div>
      <div class="story">신비로운 숲속에는 다섯 번의 갈림길이 있어요.<br>마음이 이끄는 방향을 따라 걸으며 나만의 성향을 발견해 보세요.</div>
      <div style="font-size:3.2rem;margin:1rem">🌿　🌼　🦋</div>
    </div>
    """, unsafe_allow_html=True)
    forest_scene("🐰")
    _, center, _ = st.columns([1,1.3,1])
    with center:
        if st.button("여행 시작하기  →", use_container_width=True):
            go("animal")

elif st.session_state.page == "animal":
    st.markdown('<div class="eyebrow">STEP 01 · YOUR COMPANION</div><h1>여행을 함께할 친구를 골라주세요</h1><p>마음에 드는 동물을 선택하면 여행이 시작됩니다.</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (name, data) in zip(cols, ANIMALS.items()):
        with col:
            st.markdown(f'<div class="choice-card"><div class="choice-emoji">{data["emoji"]}</div><b>{name}</b><p style="font-size:.82rem;color:#8b907c">{data["line"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"{name} 선택", key=f"animal_{name}", use_container_width=True):
                st.session_state.animal = name
                go("intro")
    st.caption("동물은 여행의 동행자이며, 최종 성격 유형에는 영향을 주지 않아요.")

elif st.session_state.page == "intro":
    animal = st.session_state.animal
    st.markdown('<div class="eyebrow">YOUR JOURNEY BEGINS</div><h1>좋아요! 이제 출발해 볼까요?</h1>', unsafe_allow_html=True)
    forest_scene(ANIMALS[animal]["emoji"])
    st.markdown(f'<p style="text-align:center;font-size:1.1rem;color:#6d725f">{ANIMALS[animal]["emoji"]} {animal}: “{ANIMALS[animal]["line"]}”</p>', unsafe_allow_html=True)
    _, c, _ = st.columns([1,1.2,1])
    with c:
        if st.button("숲속으로 들어가기  →", use_container_width=True):
            go("quiz")

elif st.session_state.page == "quiz":
    idx = len(st.session_state.answers)
    if idx >= len(QUESTIONS):
        go("result")
    else:
        q = QUESTIONS[idx]
        st.markdown(f'<div class="eyebrow">THE FOREST PATH · QUESTION {idx+1} / 5</div>', unsafe_allow_html=True)
        st.progress((idx)/len(QUESTIONS))
        st.markdown(f'<div class="progress-label">갈림길 {idx+1} · 5</div>', unsafe_allow_html=True)
        forest_scene(first_person=True)
        st.markdown(f'<div class="question">{q["question"]}</div>', unsafe_allow_html=True)
        st.write("어느 쪽으로 걸어가고 싶나요?")
        left, right = st.columns(2)
        for col, option, letter in [(left,q["A"],"A"),(right,q["B"],"B")]:
            with col:
                st.markdown(f'<div class="choice-card"><div class="choice-emoji">{option["emoji"]}</div><b>{option["text"]}</b><p style="font-size:.82rem;color:#8b907c">{option.get("sub","")}</p></div>', unsafe_allow_html=True)
                if st.button(f"{letter} 선택하기", key=f"answer_{idx}_{letter}", use_container_width=True):
                    st.session_state.answers.append(letter)
                    if len(st.session_state.answers) == len(QUESTIONS):
                        go("result")
                    else:
                        go("walk")
        st.caption("정답은 없어요. 지금 마음이 끌리는 쪽을 선택해 주세요.")

elif st.session_state.page == "walk":
    animal = st.session_state.animal
    st.markdown('<div class="eyebrow">ON THE WAY</div><h1>선택한 길을 따라 걸어가요</h1>', unsafe_allow_html=True)
    forest_scene(ANIMALS[animal]["emoji"])
    st.markdown(f'<p style="text-align:center;color:#75816b">{ANIMALS[animal]["emoji"]} {animal}와 함께 다음 갈림길로 향하는 중...</p>', unsafe_allow_html=True)
    _, c, _ = st.columns([1,1.2,1])
    with c:
        if st.button("다음 갈림길로  →", use_container_width=True):
            go("quiz")

elif st.session_state.page == "result":
    animal = st.session_state.animal
    result = calculate_result(st.session_state.answers)
    st.markdown('<div class="eyebrow" style="text-align:center">YOUR PATH, YOUR STORY</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card">
      <div style="font-size:.9rem;color:#929780;letter-spacing:.15em">YOUR PERSONALITY TYPE</div>
      <div class="dancer">{ANIMALS[animal]["emoji"]}</div>
      <h1 style="font-size:2.5rem;margin:.2rem 0">{result["name"]}</h1>
      <div style="color:#89917e;letter-spacing:.12em">{result["english"]}</div>
      <p style="max-width:620px;margin:1rem auto;color:#6d725f">{result["description"]}</p>
      <div style="font-size:1.5rem;margin:.8rem">{"　".join(result["keywords"])}</div>
      <div style="margin-top:1rem;padding:1rem;background:#f4f1e7;border-radius:18px;color:#69745e">“{result["quote"]}”</div>
      <p style="color:#9a9b8b;font-size:.85rem;margin-top:1rem">당신의 여행에 함께한 친구: {animal}</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("처음부터 다시 여행하기", use_container_width=True):
            reset()
    with c2:
        if st.button("다른 동물과 여행하기", use_container_width=True):
            st.session_state.animal = None
            st.session_state.answers = []
            go("animal")
    st.caption("이 테스트는 재미를 위한 성향 콘텐츠이며 전문적인 심리검사가 아닙니다.")
