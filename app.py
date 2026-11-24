import streamlit as st
from questions import QUESTIONS
from results import RESULT_TYPES, calculate_result

st.set_page_config(
    page_title="ANIMAL PATH — Find Your Way",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ANIMALS = {
    "토끼": {"emoji": "🐇", "english": "THE RABBIT", "tagline": "조용한 호기심으로 숲을 살피는 친구"},
    "강아지": {"emoji": "🐕", "english": "THE DOG", "tagline": "따뜻한 마음으로 곁을 지키는 친구"},
    "고양이": {"emoji": "🐈", "english": "THE CAT", "tagline": "자신만의 리듬으로 걷는 친구"},
    "악어": {"emoji": "🐊", "english": "THE CROCODILE", "tagline": "낯선 길도 씩씩하게 건너는 친구"},
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

def reset():
    st.session_state.page = "home"
    st.session_state.animal = None
    st.session_state.answers = []
    st.rerun()

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
    :root {
      --ink:#25352d; --muted:#77847a; --forest:#29483a; --moss:#718b69;
      --sage:#dce6d7; --cream:#f6f4eb; --paper:#fffef9; --line:#e4e7dc;
      --gold:#d9b978; --coral:#d58e78;
    }
    html, body, [class*="css"] { font-family:'DM Sans','Noto Sans KR',sans-serif; }
    .stApp {
      background:
        radial-gradient(ellipse at 8% 5%, rgba(218,231,211,.65), transparent 30%),
        radial-gradient(ellipse at 94% 20%, rgba(238,224,195,.42), transparent 28%),
        linear-gradient(180deg,#f7f6ef 0%,#f1f2e9 100%);
      color:var(--ink);
    }
    [data-testid="stHeader"] {background:transparent;}
    [data-testid="stToolbar"] {right:1rem;}
    .block-container {max-width:900px;padding-top:2.1rem;padding-bottom:4rem;}
    #MainMenu, footer {visibility:hidden;}
    h1,h2,h3,p {color:var(--ink);}
    .topbar {display:flex;align-items:center;justify-content:space-between;margin-bottom:2.2rem;}
    .wordmark {font-size:.82rem;font-weight:800;letter-spacing:.22em;color:var(--forest);}
    .wordmark span {color:var(--moss);}
    .topnote {font-size:.68rem;letter-spacing:.15em;color:#9aa397;text-transform:uppercase;}
    .hero {
      position:relative; overflow:hidden; text-align:center;
      padding:3.3rem 2rem 2.6rem; border:1px solid rgba(220,226,213,.9);
      border-radius:30px; background:rgba(255,254,249,.82);
      box-shadow:0 24px 70px rgba(49,68,51,.08);
      animation:rise .8s cubic-bezier(.2,.7,.2,1) both;
    }
    .hero:before,.hero:after {content:"";position:absolute;border-radius:50%;pointer-events:none;}
    .hero:before {width:240px;height:240px;left:-125px;top:-130px;background:#e8eedf;}
    .hero:after {width:180px;height:180px;right:-90px;bottom:-100px;background:#f1e8d5;}
    .kicker {font-size:.68rem;font-weight:700;letter-spacing:.24em;color:#879482;text-transform:uppercase;}
    .brand {font-size:clamp(3.2rem,9vw,6.4rem);line-height:.98;font-weight:800;letter-spacing:-.075em;color:var(--forest);margin:.7rem 0 .5rem;}
    .brand em {font-style:normal;color:#91a486;}
    .tagline {font-size:1rem;letter-spacing:.06em;color:#788477;margin:.8rem 0 1.1rem;}
    .introcopy {font-size:.94rem;line-height:1.95;color:#68766b;max-width:560px;margin:0 auto;}
    .scene {
      position:relative;height:260px;overflow:hidden;border-radius:24px;margin:1.3rem 0 1.5rem;
      border:1px solid rgba(203,215,197,.8);
      background:linear-gradient(180deg,#dfe9df 0%,#e9eddf 48%,#c5d2b6 49%,#aabd9e 100%);
      box-shadow:inset 0 0 55px rgba(255,255,255,.25);
    }
    .scene:before {content:"";position:absolute;left:-8%;right:-8%;bottom:-68px;height:170px;background:#8fa987;border-radius:50% 50% 0 0;transform:rotate(-3deg);}
    .scene:after {content:"";position:absolute;left:24%;bottom:-115px;width:52%;height:240px;background:#e7d9bd;border-radius:50% 50% 0 0;transform:rotate(2deg);box-shadow:0 -7px 0 rgba(255,255,255,.12);}
    .sun {position:absolute;right:14%;top:28px;width:58px;height:58px;border-radius:50%;background:#f3dca4;box-shadow:0 0 38px rgba(243,220,164,.7);animation:sunpulse 5s ease-in-out infinite;}
    .hill {position:absolute;bottom:48px;width:55%;height:115px;border-radius:50%;background:#afc2a3;opacity:.75;}
    .hill.left {left:-15%;}.hill.right {right:-16%;background:#9db596;}
    .tree {position:absolute;z-index:2;bottom:57px;font-size:4.5rem;filter:drop-shadow(0 8px 4px rgba(48,68,49,.12));}
    .tree.left {left:7%;}.tree.right {right:8%;font-size:4rem;}
    .firefly {position:absolute;z-index:4;width:6px;height:6px;border-radius:50%;background:#fff4bd;box-shadow:0 0 13px #fff4bd;animation:firefly 4s ease-in-out infinite;}
    .f1{left:24%;top:35%;}.f2{right:27%;top:56%;animation-delay:1.2s}.f3{left:70%;top:22%;animation-delay:2.1s}
    .companion {position:absolute;z-index:5;left:50%;bottom:39px;transform:translateX(-50%);font-size:4.5rem;filter:drop-shadow(0 10px 5px rgba(42,62,45,.18));animation:companion 2.2s ease-in-out infinite;}
    .scene-label {position:absolute;z-index:6;left:0;right:0;top:17px;text-align:center;font-size:.65rem;letter-spacing:.22em;color:#6f826f;font-weight:700;}
    .sectionhead {margin:.4rem 0 1.2rem;}
    .step {font-size:.68rem;letter-spacing:.2em;font-weight:800;color:#91a08d;text-transform:uppercase;}
    .headline {font-size:clamp(1.65rem,4vw,2.25rem);font-weight:800;letter-spacing:-.055em;line-height:1.35;margin:.35rem 0;color:var(--forest);}
    .subhead {font-size:.9rem;line-height:1.75;color:#7c897e;}
    .panel {background:rgba(255,254,249,.82);border:1px solid var(--line);border-radius:24px;padding:1.4rem;box-shadow:0 14px 38px rgba(49,68,51,.045);}
    .animal-card {height:100%;min-height:170px;text-align:center;padding:1.2rem .8rem;border-radius:20px;background:#fffef9;border:1px solid #e6e9df;box-shadow:0 8px 24px rgba(49,68,51,.035);transition:transform .25s,box-shadow .25s;}
    .animal-card:hover {transform:translateY(-5px);box-shadow:0 15px 30px rgba(49,68,51,.1);}
    .animal-emoji {font-size:3.3rem;display:block;margin:.2rem 0 .7rem;animation:idle 3s ease-in-out infinite;}
    .animal-name {font-weight:800;color:var(--forest);font-size:1rem;}
    .animal-desc {font-size:.74rem;color:#8b958a;line-height:1.5;margin-top:.35rem;}
    .question-number {display:flex;justify-content:space-between;align-items:center;color:#8a978a;font-size:.72rem;letter-spacing:.14em;font-weight:700;margin:.2rem 0 .7rem;}
    .question-title {font-size:clamp(1.45rem,4vw,2rem);font-weight:800;letter-spacing:-.045em;line-height:1.45;color:var(--forest);margin:.2rem 0 .7rem;}
    .fork-scene {
      height:280px;position:relative;overflow:hidden;border-radius:24px;margin:1rem 0 1.35rem;
      border:1px solid #d4dfd1;background:#dfe9df;
      box-shadow:inset 0 0 50px rgba(255,255,255,.25);
    }
    .fork-art {position:absolute;inset:0;width:100%;height:100%;display:block;}
    .fork-label {
      position:absolute;z-index:4;top:17px;padding:.43rem .72rem;border-radius:99px;
      background:rgba(255,254,249,.88);border:1px solid rgba(255,255,255,.75);
      color:#506b55;font-size:.65rem;font-weight:800;letter-spacing:.16em;
      box-shadow:0 4px 14px rgba(45,67,48,.08);
    }
    .fork-label.left {left:7%;}.fork-label.right {right:7%;}
    .fork-hint {position:absolute;z-index:4;bottom:14px;left:0;right:0;text-align:center;
      color:#758574;font-size:.62rem;letter-spacing:.18em;font-weight:800;text-shadow:0 1px 5px rgba(255,255,255,.8);}
    .choice-wrap {background:rgba(255,254,249,.9);border:1px solid #e4e8df;border-radius:20px;padding:1.1rem 1.1rem .8rem;min-height:145px;transition:all .25s;}
    .choice-wrap:hover {border-color:#b8c9b0;transform:translateY(-3px);box-shadow:0 12px 28px rgba(49,68,51,.07);}
    .choice-symbol {font-size:1.7rem;margin-bottom:.4rem;}
    .choice-title {font-weight:800;color:#3c5544;font-size:.98rem;line-height:1.55;}
    .choice-sub {font-size:.78rem;color:#8b958a;margin-top:.3rem;line-height:1.55;}
    .walkstage {position:relative;overflow:hidden;text-align:center;border-radius:24px;padding:2rem 1rem;background:linear-gradient(180deg,#e1eadf,#c2d2b8);border:1px solid #d3dfce;}
    .walkanimal {display:inline-block;font-size:5rem;animation:travel 2.2s ease-in-out infinite;}
    .walkpath {height:14px;width:65%;margin:1.4rem auto .5rem;background:#e8d9bd;border-radius:100%;position:relative;overflow:hidden;}
    .walkpath:after {content:"";position:absolute;left:-20%;top:0;height:100%;width:25%;background:rgba(255,255,255,.65);animation:pathmove 1.5s linear infinite;}
    .result-shell {position:relative;overflow:hidden;border-radius:30px;background:#fffef9;border:1px solid #e1e6db;box-shadow:0 24px 70px rgba(49,68,51,.09);padding:2rem;}
    .result-top {text-align:center;padding:1rem .5rem 1.5rem;border-bottom:1px solid #edf0e8;}
    .result-medal {font-size:4.7rem;display:inline-block;animation:celebrate 1.4s ease-in-out infinite;}
    .result-name {font-size:clamp(2rem,6vw,3rem);font-weight:800;letter-spacing:-.06em;color:var(--forest);margin:.2rem 0;}
    .result-en {font-size:.7rem;letter-spacing:.25em;color:#9aa596;font-weight:700;}
    .result-desc {font-size:.93rem;line-height:1.95;color:#68766b;max-width:590px;margin:1rem auto 0;}
    .keyword {display:inline-block;padding:.5rem .85rem;margin:.2rem;border-radius:100px;background:#edf2e9;color:#5d755d;font-size:.76rem;font-weight:700;}
    .quote {background:#f5f2e8;border-left:3px solid #c8b17d;border-radius:0 14px 14px 0;padding:1rem 1.1rem;color:#66715f;font-size:.95rem;line-height:1.7;margin:1.2rem 0;}
    .journey-meta {display:flex;justify-content:space-between;gap:.5rem;flex-wrap:wrap;margin-top:1.2rem;color:#929d90;font-size:.72rem;letter-spacing:.04em;}
    div.stButton > button {
      border-radius:14px;border:1px solid #d8e0d4;background:#fffef9;color:#385342;
      min-height:3.05rem;font-weight:700;letter-spacing:.01em;transition:all .2s;
      box-shadow:0 4px 12px rgba(44,67,48,.035);
    }
    div.stButton > button:hover {border-color:#8da685;background:#edf3e9;color:#29483a;transform:translateY(-2px);box-shadow:0 9px 20px rgba(44,67,48,.09);}
    div.stButton > button[kind="primary"] {background:#315642;border-color:#315642;color:#fff;}
    div.stButton > button[kind="primary"]:hover {background:#244532;border-color:#244532;color:#fff;}
    .stProgress > div > div > div > div {background:linear-gradient(90deg,#7e9b76,#c1b17c);}
    [data-testid="stProgress"] {margin:.2rem 0 1rem;}
    [data-testid="stCaptionContainer"] p {color:#9aa397;font-size:.75rem;}
    .footnote {text-align:center;color:#a0a99d;font-size:.7rem;letter-spacing:.05em;margin-top:2rem;}
    @keyframes rise {from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
    @keyframes idle {0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-7px) rotate(2deg)}}
    @keyframes companion {0%,100%{transform:translateX(-50%) translateY(0) rotate(-3deg)}50%{transform:translateX(-50%) translateY(-10px) rotate(3deg)}}
    @keyframes celebrate {0%,100%{transform:translateY(0) rotate(-8deg) scale(1)}50%{transform:translateY(-12px) rotate(8deg) scale(1.08)}}
    @keyframes travel {0%,100%{transform:translateX(-28px) rotate(-7deg)}50%{transform:translateX(28px) rotate(7deg)}}
    @keyframes pathmove {to{left:110%}}
    @keyframes firefly {0%,100%{opacity:.25;transform:translateY(0)}50%{opacity:1;transform:translateY(-13px)}}
    @keyframes sunpulse {0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
    @keyframes twinkle {0%,100%{opacity:.45;transform:translateX(-50%) scale(.9)}50%{opacity:1;transform:translateX(-50%) scale(1.15)}}
    @media (max-width:640px) {
      .block-container{padding:1.1rem 1rem 3rem;}
      .hero{padding:2.4rem 1.1rem 1.8rem;border-radius:24px;}
      .scene{height:215px;}
      .result-shell{padding:1.25rem;}
      .topbar{margin-bottom:1.4rem;}
    }
    @media (prefers-reduced-motion:reduce) {
      *,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition:none!important;}
    }
    </style>
    """, unsafe_allow_html=True)

def topbar(note="A STORYBOOK PERSONALITY JOURNEY"):
    st.markdown(f"""
      <div class="topbar">
        <div class="wordmark">ANIMAL <span>PATH</span></div>
        <div class="topnote">{note}</div>
      </div>
    """, unsafe_allow_html=True)

def forest_scene(animal=None, fork=False):
    if fork:
        st.markdown("""
        <div class="fork-scene">
          <span class="fork-label left">A · LEFT PATH</span>
          <span class="fork-label right">B · RIGHT PATH</span>
          <svg class="fork-art" viewBox="0 0 860 280" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <defs>
              <linearGradient id="forkSky" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#dce9e2"/>
                <stop offset="100%" stop-color="#f0eedf"/>
              </linearGradient>
              <linearGradient id="forkMeadow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#b8cbae"/>
                <stop offset="100%" stop-color="#91aa8d"/>
              </linearGradient>
              <linearGradient id="forkDirt" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#f0e3ca"/>
                <stop offset="100%" stop-color="#d8c5a5"/>
              </linearGradient>
              <filter id="pathShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feGaussianBlur stdDeviation="5"/>
              </filter>
            </defs>
            <rect width="860" height="280" fill="url(#forkSky)"/>
            <circle cx="690" cy="58" r="31" fill="#f2dfaa" opacity=".85"/>
            <path d="M0 145 Q145 95 275 143 T560 130 T860 132 V280 H0Z" fill="#c4d4bd"/>
            <path d="M0 175 Q160 126 300 172 T600 162 T860 170 V280 H0Z" fill="url(#forkMeadow)"/>
            <g opacity=".85">
              <path d="M0 190 Q80 142 165 184 T340 186 V280 H0Z" fill="#9eb99b"/>
              <path d="M530 184 Q650 135 760 180 T860 178 V280 H530Z" fill="#a4bd9d"/>
            </g>
            <!-- distant forest -->
            <g fill="#789778" opacity=".72">
              <path d="M0 160 L35 72 L70 160Z M48 164 L92 58 L136 164Z M112 165 L153 84 L194 165Z"/>
              <path d="M666 162 L705 70 L744 162Z M718 165 L765 48 L812 165Z M790 165 L827 82 L864 165Z"/>
            </g>
            <g fill="#54775d" opacity=".85">
              <path d="M22 210 L63 104 L104 210Z M73 214 L119 91 L165 214Z"/>
              <path d="M700 212 L746 91 L792 212Z M760 214 L808 104 L856 214Z"/>
            </g>
            <!-- forked trail: shadow, earth edge, then sunlit center -->
            <g fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M430 302 C426 245 420 208 419 181 C414 153 350 119 238 92" stroke="#75896f" stroke-width="112" opacity=".22" filter="url(#pathShadow)"/>
              <path d="M430 302 C434 245 440 208 441 181 C449 151 522 119 635 91" stroke="#75896f" stroke-width="112" opacity=".22" filter="url(#pathShadow)"/>
              <path d="M430 302 C426 245 420 208 419 181 C414 153 350 119 238 92" stroke="#c7b18f" stroke-width="91"/>
              <path d="M430 302 C434 245 440 208 441 181 C449 151 522 119 635 91" stroke="#c7b18f" stroke-width="91"/>
              <path d="M430 302 C426 245 420 208 419 181 C414 153 350 119 238 92" stroke="url(#forkDirt)" stroke-width="79"/>
              <path d="M430 302 C434 245 440 208 441 181 C449 151 522 119 635 91" stroke="url(#forkDirt)" stroke-width="79"/>
              <path d="M430 302 C430 250 430 214 430 181" stroke="#e9ddc6" stroke-width="72"/>
            </g>
            <!-- small stepping stones and flowers -->
            <g fill="#c8b797" opacity=".55">
              <ellipse cx="430" cy="246" rx="13" ry="4"/><ellipse cx="428" cy="222" rx="9" ry="3"/>
              <ellipse cx="426" cy="202" rx="6" ry="2.5"/>
            </g>
            <g fill="#f5e8bd">
              <circle cx="172" cy="208" r="3"/><circle cx="184" cy="218" r="2.5"/>
              <circle cx="674" cy="210" r="3"/><circle cx="686" cy="220" r="2.5"/>
            </g>
            <g fill="#fff3c8" opacity=".9">
              <circle cx="286" cy="72" r="2.5"/><circle cx="570" cy="54" r="2.5"/><circle cx="615" cy="146" r="2"/>
            </g>
          </svg>
          <span class="fork-hint">TAKE A MOMENT · FOLLOW YOUR INSTINCT</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        companion = f'<div class="companion">{animal}</div>' if animal else ""
        st.markdown(f"""
        <div class="scene">
          <div class="scene-label">THE ENCHANTED WOOD</div>
          <div class="sun"></div><div class="hill left"></div><div class="hill right"></div>
          <div class="tree left">🌳</div><div class="tree right">🌲</div>
          <div class="firefly f1"></div><div class="firefly f2"></div><div class="firefly f3"></div>
          {companion}
        </div>
        """, unsafe_allow_html=True)

inject_css()
topbar()

if st.session_state.page == "home":
    st.markdown("""
      <div class="hero">
        <div class="kicker">A LITTLE JOURNEY TO FIND YOURSELF</div>
        <div class="brand">ANIMAL <em>PATH</em></div>
        <div class="tagline">작은 선택들이 모여, 나만의 길이 되다</div>
        <div class="introcopy">
          신비로운 숲속, 다섯 번의 갈림길이 당신을 기다리고 있어요.<br>
          마음이 이끄는 방향을 따라 천천히 걸으며<br>
          지금의 나를 닮은 성향을 발견해 보세요.
        </div>
      </div>
    """, unsafe_allow_html=True)
    forest_scene("🐇")
    _, center, _ = st.columns([1, 1.25, 1])
    with center:
        if st.button("나의 숲속 여행 시작하기  →", type="primary", use_container_width=True):
            go("animal")
    st.markdown('<div class="footnote">5 CHOICES · 1 COMPANION · YOUR OWN STORY</div>', unsafe_allow_html=True)

elif st.session_state.page == "animal":
    st.markdown("""
      <div class="sectionhead">
        <div class="step">01 / YOUR COMPANION</div>
        <div class="headline">여행을 함께할 친구를 골라주세요.</div>
        <div class="subhead">숲길을 걷는 동안 당신의 곁을 지켜줄 동행자예요.</div>
      </div>
    """, unsafe_allow_html=True)
    cols = st.columns(4)
    for col, (name, data) in zip(cols, ANIMALS.items()):
        with col:
            st.markdown(f"""
              <div class="animal-card">
                <span class="animal-emoji">{data['emoji']}</span>
                <div class="animal-name">{name}</div>
                <div class="animal-desc">{data['tagline']}</div>
              </div>
            """, unsafe_allow_html=True)
            if st.button(f"{name}와 함께하기", key=f"animal_{name}", use_container_width=True):
                st.session_state.animal = name
                go("intro")
    st.caption("선택한 동물은 여행의 동행자이며, 성격 유형 결과에는 영향을 주지 않습니다.")

elif st.session_state.page == "intro":
    animal = st.session_state.animal
    st.markdown("""
      <div class="sectionhead">
        <div class="step">02 / THE JOURNEY BEGINS</div>
        <div class="headline">준비되셨나요?</div>
        <div class="subhead">서두를 필요는 없어요. 다섯 번의 선택이 당신만의 이야기를 만들어 줄 거예요.</div>
      </div>
    """, unsafe_allow_html=True)
    forest_scene(ANIMALS[animal]["emoji"])
    st.markdown(f"""
      <div class="panel" style="text-align:center">
        <div style="font-size:2rem">{ANIMALS[animal]['emoji']}</div>
        <div style="font-weight:800;color:#315642;margin:.4rem 0">{animal}가 당신을 기다리고 있어요</div>
        <div style="font-size:.83rem;color:#879286">{ANIMALS[animal]['tagline']}</div>
      </div>
    """, unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1.2, 1])
    with c:
        if st.button("숲속으로 들어가기  →", type="primary", use_container_width=True):
            go("quiz")

elif st.session_state.page == "quiz":
    idx = len(st.session_state.answers)
    if idx >= len(QUESTIONS):
        go("result")
    else:
        q = QUESTIONS[idx]
        st.markdown(f"""
          <div class="question-number"><span>THE FOREST PATH</span><span>0{idx+1} — 05</span></div>
          <div class="question-title">{q['question']}</div>
        """, unsafe_allow_html=True)
        st.progress((idx + 1) / len(QUESTIONS))
        forest_scene(fork=True)
        st.markdown('<div class="subhead" style="text-align:center;margin:-.1rem 0 1rem">어느 쪽으로 걸어가고 싶나요?</div>', unsafe_allow_html=True)
        left, right = st.columns(2, gap="medium")
        for col, option, letter, side in [(left, q["A"], "A", "LEFT PATH"), (right, q["B"], "B", "RIGHT PATH")]:
            with col:
                st.markdown(f"""
                  <div class="choice-wrap">
                    <div class="step">{side}</div>
                    <div class="choice-symbol">{option['emoji']}</div>
                    <div class="choice-title">{option['text']}</div>
                    <div class="choice-sub">{option.get('sub','')}</div>
                  </div>
                """, unsafe_allow_html=True)
                if st.button(f"{letter} · 이 길을 선택하기", key=f"answer_{idx}_{letter}", use_container_width=True):
                    st.session_state.answers.append(letter)
                    if len(st.session_state.answers) == len(QUESTIONS):
                        go("result")
                    else:
                        go("walk")
        st.caption("정답은 없어요. 가장 먼저 마음이 끌린 쪽을 선택해 주세요.")

elif st.session_state.page == "walk":
    animal = st.session_state.animal
    next_num = len(st.session_state.answers) + 1
    st.markdown(f"""
      <div class="sectionhead">
        <div class="step">A QUIET MOMENT ON THE WAY</div>
        <div class="headline">선택한 길을 따라 걸어가요.</div>
        <div class="subhead">당신의 작은 선택이 숲속 풍경을 바꾸고 있어요.</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
      <div class="walkstage">
        <div style="font-size:.66rem;letter-spacing:.2em;color:#6f826f;font-weight:800">WALKING TO THE NEXT FORK</div>
        <div class="walkanimal">{ANIMALS[animal]['emoji']}</div>
        <div class="walkpath"></div>
        <div style="font-size:.82rem;color:#627765;margin-top:.8rem">{animal}와 함께 숲길을 걷는 중</div>
      </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="footnote">NEXT STOP · FORK {next_num} / 5</div>', unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1.2, 1])
    with c:
        if st.button("다음 갈림길로  →", type="primary", use_container_width=True):
            go("quiz")

elif st.session_state.page == "result":
    animal = st.session_state.animal
    result = calculate_result(st.session_state.answers)
    keywords = "".join([f'<span class="keyword">{word}</span>' for word in result["keywords"]])
    answer_marks = "".join([f'<span style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:#e9efe5;color:#567052;font-size:.72rem;font-weight:800;margin:0 3px">{a}</span>' for a in st.session_state.answers])
    st.markdown(f"""
      <div class="result-shell">
        <div class="result-top">
          <div class="step">YOUR PATH, YOUR STORY</div>
          <div style="font-size:.7rem;letter-spacing:.22em;color:#9aa596;font-weight:700;margin-top:.7rem">YOUR PERSONALITY TYPE</div>
          <div class="result-medal">{ANIMALS[animal]['emoji']}</div>
          <div class="result-name">{result['name']}</div>
          <div class="result-en">{result['english']}</div>
          <div class="result-desc">{result['description']}</div>
          <div style="margin-top:1rem">{keywords}</div>
        </div>
        <div style="padding:1.35rem .2rem .2rem">
          <div class="step" style="text-align:center">A NOTE FROM THE FOREST</div>
          <div class="quote">“{result['quote']}”</div>
          <div style="text-align:center;font-size:.78rem;color:#849083">당신의 여행을 함께한 친구는 <b style="color:#526d54">{animal} {ANIMALS[animal]['emoji']}</b>입니다.</div>
          <div class="journey-meta"><span>YOUR FIVE CHOICES</span><span>{answer_marks}</span></div>
        </div>
      </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("처음부터 다시 여행하기", use_container_width=True):
            reset()
    with c2:
        if st.button("다른 동물과 여행하기", use_container_width=True):
            st.session_state.animal = None
            st.session_state.answers = []
            go("animal")
    st.markdown('<div class="footnote">ANIMAL PATH IS A LIGHTHEARTED PERSONALITY EXPERIENCE, NOT A CLINICAL TEST.</div>', unsafe_allow_html=True)
