import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🧭 البوصلة المهنية للصم",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# CSS – تصميم احترافي متكامل
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');

:root {
  --bg:       #07080f;
  --bg2:      #0e0f1a;
  --card:     rgba(255,255,255,0.04);
  --border:   rgba(255,255,255,0.08);
  --purple:   #7c3aed;
  --purple-l: #a78bfa;
  --teal:     #10b981;
  --teal-l:   #34d399;
  --amber:    #f59e0b;
  --rose:     #f43f5e;
  --text:     #f0ece4;
  --muted:    #6b7280;
}

* { font-family: 'Tajawal', sans-serif !important; direction: rtl; box-sizing: border-box; }
html, body, [class*="css"] { background: var(--bg); color: var(--text); }

/* ── PARTICLES BG ── */
body::before {
  content:''; position:fixed; inset:0; z-index:-2; pointer-events:none;
  background:
    radial-gradient(ellipse 70% 50% at 15% 15%, rgba(124,58,237,.22) 0%, transparent 55%),
    radial-gradient(ellipse 55% 70% at 85% 85%, rgba(16,185,129,.16) 0%, transparent 55%),
    radial-gradient(ellipse 40% 40% at 50% 50%, rgba(245,158,11,.08) 0%, transparent 60%),
    var(--bg);
  animation: bg 14s ease-in-out infinite alternate;
}
@keyframes bg { to { filter: hue-rotate(25deg) brightness(1.05); } }

/* dots texture */
body::after {
  content:''; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background-image: radial-gradient(rgba(255,255,255,.04) 1px, transparent 1px);
  background-size: 32px 32px;
}

/* ── HERO ── */
.hero { text-align:center; padding:2.5rem 1rem 1.5rem; }
.hero-badge {
  display:inline-block; padding:.3rem 1rem; border-radius:50px;
  background:rgba(124,58,237,.15); border:1px solid rgba(124,58,237,.35);
  color:var(--purple-l); font-size:.8rem; font-weight:700;
  letter-spacing:.08em; margin-bottom:1rem;
  animation: fadeDown .6s ease both;
}
.hero-icon {
  font-size:5rem; display:block; margin:.4rem 0;
  filter: drop-shadow(0 0 32px rgba(124,58,237,.7));
  animation: floatY 3.5s ease-in-out infinite;
}
@keyframes floatY { 0%,100%{transform:translateY(0) rotate(-4deg)} 50%{transform:translateY(-14px) rotate(4deg)} }
.hero-title {
  font-size:clamp(2rem,5vw,3.4rem); font-weight:900; line-height:1.15;
  background:linear-gradient(135deg,var(--purple-l),var(--teal-l),var(--amber));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  animation: fadeUp .7s .1s ease both;
}
.hero-sub { font-size:1.15rem; color:var(--muted); margin:.5rem 0 1rem; font-weight:300; animation:fadeUp .7s .2s ease both; }
.hero-bar { width:100px; height:3px; margin:.8rem auto; border-radius:4px;
  background:linear-gradient(90deg,var(--purple),var(--teal),var(--amber));
  animation:expandW .8s .3s ease both; }
@keyframes expandW { from{width:0} }
@keyframes fadeUp  { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:none} }
@keyframes fadeDown{ from{opacity:0;transform:translateY(-10px)} to{opacity:1;transform:none} }

/* ── PROGRESS BAR ── */
.prog-wrap {
  max-width:700px; margin:0 auto 2.5rem;
  background:rgba(255,255,255,.05); border-radius:50px;
  padding:.6rem 1.2rem; border:1px solid var(--border);
}
.prog-track { display:flex; align-items:center; justify-content:space-between; gap:.3rem; }
.prog-step {
  display:flex; flex-direction:column; align-items:center; gap:.25rem;
  flex:1; cursor:default;
}
.prog-dot {
  width:34px; height:34px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:.85rem; font-weight:800; transition:all .3s;
  background:rgba(255,255,255,.05); border:2px solid rgba(255,255,255,.1); color:var(--muted);
}
.prog-dot.done  { background:rgba(16,185,129,.2);  border-color:var(--teal);   color:var(--teal-l); }
.prog-dot.active{ background:rgba(124,58,237,.25); border-color:var(--purple); color:var(--purple-l);
  box-shadow:0 0 18px rgba(124,58,237,.5); animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{box-shadow:0 0 18px rgba(124,58,237,.5)} 50%{box-shadow:0 0 30px rgba(124,58,237,.8)} }
.prog-label { font-size:.72rem; color:var(--muted); text-align:center; white-space:nowrap; }
.prog-label.active { color:var(--purple-l); font-weight:700; }
.prog-label.done   { color:var(--teal-l); }
.prog-line { flex:1; height:2px; background:rgba(255,255,255,.07); border-radius:2px; margin-bottom:1rem; transition:.4s; }
.prog-line.done { background:linear-gradient(90deg,var(--teal),var(--purple)); }

/* ── CARDS ── */
.card {
  background:var(--card); backdrop-filter:blur(24px);
  border:1px solid var(--border); border-radius:22px;
  padding:1.8rem 2rem; margin-bottom:1.4rem;
  position:relative; overflow:hidden;
  transition:box-shadow .3s;
}
.card::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(135deg,rgba(255,255,255,.035),transparent 60%);
}
.card-t { border-top:3px solid; }
.c-purple{ border-top-color:var(--purple) !important; }
.c-teal  { border-top-color:var(--teal)   !important; }
.c-amber { border-top-color:var(--amber)  !important; }
.c-rose  { border-top-color:var(--rose)   !important; }
.card-h  { font-size:1.25rem; font-weight:800; margin-bottom:.3rem; }
.card-s  { font-size:.88rem; color:var(--muted); margin-bottom:1rem; }

/* ── CHOICE BUTTONS (radio simulation) ── */
.stRadio [data-testid="stWidgetLabel"] { display:none; }
.stRadio > div { display:flex; flex-wrap:wrap; gap:.5rem; }
.stRadio label {
  background:rgba(255,255,255,.04) !important;
  border:1.5px solid rgba(255,255,255,.1) !important;
  border-radius:14px !important; padding:.55rem 1.1rem !important;
  cursor:pointer !important; transition:all .2s !important;
  font-weight:600 !important;
}
.stRadio label:hover { border-color:var(--purple) !important; background:rgba(124,58,237,.1) !important; }

/* ── MULTISELECT ── */
.stMultiSelect [data-testid="stWidgetLabel"] { display:none; }
span[data-baseweb="tag"] {
  background:linear-gradient(135deg,rgba(124,58,237,.3),rgba(16,185,129,.2)) !important;
  border:1px solid rgba(124,58,237,.4) !important; border-radius:50px !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div > div { background:linear-gradient(90deg,var(--purple),var(--teal)) !important; }
[data-testid="stSlider"] { padding:.3rem 0; }

/* ── TEXT AREA ── */
textarea {
  background:rgba(255,255,255,.05) !important;
  border:1px solid var(--border) !important;
  border-radius:14px !important; color:var(--text) !important;
}
textarea:focus { border-color:var(--purple) !important; box-shadow:0 0 0 2px rgba(124,58,237,.2) !important; }

/* ── BUTTONS ── */
.stButton > button {
  width:100%; padding:.9rem 2rem; border:none; border-radius:16px;
  background:linear-gradient(135deg,var(--purple),var(--teal));
  color:#fff; font-size:1.05rem; font-weight:800; cursor:pointer;
  box-shadow:0 6px 28px rgba(124,58,237,.35); transition:all .25s;
  letter-spacing:.02em;
}
.stButton > button:hover {
  transform:translateY(-3px); box-shadow:0 10px 36px rgba(124,58,237,.55);
}
.stButton > button:active { transform:translateY(0); }

/* ── VOTE ROWS ── */
.vote-row {
  display:flex; align-items:center; gap:1rem;
  padding:.85rem 1.1rem; margin-bottom:.8rem;
  background:rgba(255,255,255,.03); border-radius:14px;
  border:1px solid var(--border); transition:.2s;
}
.vote-row:hover { border-color:rgba(124,58,237,.3); }
.vote-label { font-weight:700; min-width:160px; }
.vote-track { flex:1; background:rgba(255,255,255,.07); border-radius:8px; height:10px; overflow:hidden; }
.vote-fill  { height:10px; border-radius:8px; transition:width .9s cubic-bezier(.4,0,.2,1); }
.vote-pct   { font-weight:800; font-size:1.05rem; color:var(--purple-l); min-width:42px; text-align:center; }
.vote-count { color:var(--muted); font-size:.85rem; min-width:32px; }

/* ── METRIC BOXES ── */
.m-box {
  background:var(--card); border:1px solid var(--border);
  border-radius:18px; padding:1.4rem 1rem; text-align:center;
}
.m-val {
  font-size:2.6rem; font-weight:900;
  background:linear-gradient(135deg,var(--purple-l),var(--teal-l));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.m-lbl { font-size:.82rem; color:var(--muted); margin-top:.2rem; }

/* ── TAG CLOUD ── */
.tag {
  display:inline-block; padding:.3rem .9rem; margin:.2rem;
  border-radius:50px; font-size:.8rem; font-weight:700;
  background:rgba(124,58,237,.18); border:1px solid rgba(124,58,237,.3);
  color:var(--purple-l); transition:.2s;
}
.tag:hover { background:rgba(124,58,237,.3); }
.tag.teal { background:rgba(16,185,129,.15); border-color:rgba(16,185,129,.3); color:var(--teal-l); }
.tag.amber{ background:rgba(245,158,11,.15); border-color:rgba(245,158,11,.3); color:#fcd34d; }

/* ── RESULT HERO ── */
.result-wrap {
  text-align:center; padding:2.8rem 2rem;
  background:linear-gradient(135deg,rgba(124,58,237,.14),rgba(16,185,129,.1));
  border:1px solid rgba(124,58,237,.3); border-radius:26px; margin-bottom:1.5rem;
  position:relative; overflow:hidden;
}
.result-wrap::before {
  content:''; position:absolute; inset:0;
  background:radial-gradient(ellipse 60% 60% at 50% 0%, rgba(124,58,237,.2), transparent);
  pointer-events:none;
}
.result-trophy { font-size:4rem; margin-bottom:.5rem; animation:floatY 3s ease-in-out infinite; }
.result-title  { font-size:2rem; font-weight:900; margin-bottom:.3rem; }
.result-badge  {
  display:inline-block; padding:.55rem 1.6rem; border-radius:50px; margin-top:.8rem;
  background:linear-gradient(135deg,var(--purple),var(--teal));
  font-weight:800; font-size:1.1rem; letter-spacing:.02em;
}

/* ── COMPETENCE WHEEL (SVG ring labels) ── */
.comp-ring-label { font-size:.9rem; font-weight:700; text-align:center; margin-top:.4rem; }

/* ── INSIGHT BOXES ── */
.insight {
  display:flex; align-items:flex-start; gap:1rem;
  padding:1rem 1.2rem; border-radius:14px; margin-bottom:.7rem;
  background:rgba(255,255,255,.03); border:1px solid var(--border);
}
.insight-icon { font-size:1.5rem; }
.insight-text { flex:1; }
.insight-head { font-weight:800; margin-bottom:.2rem; }
.insight-body { font-size:.88rem; color:var(--muted); }

/* ── PLAN CARDS ── */
.plan-card {
  background:var(--card); border:1px solid var(--border);
  border-radius:18px; padding:1.2rem 1.4rem; margin-bottom:.8rem;
  border-right:4px solid;
}

/* ── DIVIDER ── */
.div-fancy { text-align:center; color:rgba(255,255,255,.12); padding:.6rem; letter-spacing:.6em; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu,footer,header,[data-testid="stToolbar"] { visibility:hidden; height:0; }
.block-container { padding:0 2rem 5rem !important; max-width:1140px; }
[data-testid="stSidebar"] { display:none; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════
def init_state():
    defs = {
        "step": 0,
        "pre": {},
        "loves": [],
        "my_skills": [],
        "my_values": [],
        "love_txt": "",
        "skill_txt": "",
        "market": "",
        "votes": {"أنا في المسار الصحيح ✅": 0,
                  "أحتاج إلى توجيه 🧭": 0,
                  "لست متأكداً بعد 🤔": 0},
        "compass": {},
        "plan": ["", "", ""],
        "post": {},
        "show_result": False,
        "pre_score": 0,
        "post_score": 0,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
s = st.session_state

STEPS = [
    ("📋", "التقييم القبلي"),
    ("🗳️", "التصويت الجماهيري"),
    ("🔍", "من أنا؟"),
    ("🧭", "البوصلة"),
    ("📅", "خطة 30 يوم"),
    ("🏆", "نتيجتي"),
]

# ══════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ ورشة تفاعلية مباشرة</div>
  <span class="hero-icon">🧭</span>
  <div class="hero-title">البوصلة المهنية للصم</div>
  <div class="hero-sub">أرى إمكانياتي … أحدد مساري</div>
  <div class="hero-bar"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PROGRESS BAR
# ══════════════════════════════════════════════════════════════
prog_html = '<div class="prog-wrap"><div class="prog-track">'
for i, (icon, label) in enumerate(STEPS):
    dot_cls  = "done" if i < s.step else ("active" if i == s.step else "")
    lbl_cls  = dot_cls
    dot_cont = "✓" if i < s.step else icon
    prog_html += f'<div class="prog-step"><div class="prog-dot {dot_cls}">{dot_cont}</div><div class="prog-label {lbl_cls}">{label}</div></div>'
    if i < len(STEPS)-1:
        line_cls = "done" if i < s.step else ""
        prog_html += f'<div class="prog-line {line_cls}"></div>'
prog_html += '</div></div>'
st.markdown(prog_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def next_btn(label, next_step):
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button(label, key=f"next_{next_step}"):
            s.step = next_step
            st.rerun()

def card(title, sub="", color="purple", content_fn=None):
    col_map = {"purple":"c-purple","teal":"c-teal","amber":"c-amber","rose":"c-rose"}
    st.markdown(f'<div class="card card-t {col_map.get(color,"c-purple")}">'
                f'<div class="card-h">{title}</div>'
                + (f'<div class="card-s">{sub}</div>' if sub else "")
                + '</div>', unsafe_allow_html=True)

def insight_box(icon, head, body):
    st.markdown(f"""
    <div class="insight">
      <div class="insight-icon">{icon}</div>
      <div class="insight-text">
        <div class="insight-head">{head}</div>
        <div class="insight-body">{body}</div>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# STEP 0 – تقييم قبلي
# ══════════════════════════════════════════════════════════════
if s.step == 0:
    card("📋 التقييم القبلي",
         "أجب بصدق — لا توجد إجابة خاطئة، هذا ليس اختباراً", "purple")

    questions = [
        ("q1", "🎯 هل لديك وضوح حول مسارك المهني؟",
         ["نعم بشكل كامل ✅","إلى حد ما 🙂","لا أعرف بعد 😕","لا على الإطلاق ❌"], [4,3,2,1]),
        ("q2", "💪 هل تعرف نقاط قوتك المهنية؟",
         ["نعم أعرفها جيداً ✅","بعضها فقط 🙂","أبحث عنها 😕","لا أعرفها ❌"], [4,3,2,1]),
        ("q3", "🏢 هل تعرف ما يحتاجه سوق العمل في مجالك؟",
         ["نعم بشكل واضح ✅","لدي فكرة عامة 🙂","ليس لدي فكرة 😕","لا يهمني الآن ❌"], [4,3,2,1]),
    ]

    total_pre = 0
    for key, label, opts, scores_map in questions:
        st.markdown(f'<div class="card"><div class="card-h" style="font-size:1rem">{label}</div></div>',
                    unsafe_allow_html=True)
        ans = st.radio("", opts, key=f"pre_{key}", horizontal=True, label_visibility="collapsed")
        s.pre[key] = ans
        idx = opts.index(ans) if ans in opts else 0
        total_pre += scores_map[idx]

    s.pre_score = total_pre

    # Mini gauge
    pct_pre = int((total_pre / 12) * 100)
    color_pre = "#10b981" if pct_pre >= 70 else ("#f59e0b" if pct_pre >= 45 else "#f43f5e")
    st.markdown(f"""
    <div class="card" style="text-align:center; margin-top:1rem;">
      <div class="card-h">مستوى وضوحك الآن</div>
      <div style="font-size:3rem; font-weight:900; color:{color_pre}; margin:.5rem 0">{pct_pre}%</div>
      <div style="background:rgba(255,255,255,.07); border-radius:50px; height:10px; overflow:hidden; max-width:400px; margin:0 auto">
        <div style="height:10px; width:{pct_pre}%; background:{color_pre}; border-radius:50px; transition:width 1s ease"></div>
      </div>
      <div style="color:var(--muted); font-size:.85rem; margin-top:.5rem">
        {"🟢 وضوح ممتاز" if pct_pre>=70 else ("🟡 وضوح جزئي" if pct_pre>=45 else "🔴 تحتاج توجيهاً")}
      </div>
    </div>
    """, unsafe_allow_html=True)

    next_btn("التالي ← التصويت الجماهيري 🗳️", 1)


# ══════════════════════════════════════════════════════════════
# STEP 1 – تصويت جماهيري
# ══════════════════════════════════════════════════════════════
elif s.step == 1:
    card("🗳️ التصويت الجماهيري المباشر",
         "صوّت الآن — نتائج الجمهور تظهر فورياً على الشاشة الكبيرة", "teal")

    total_votes = sum(s.votes.values()) or 1
    col_vote, col_result = st.columns([1, 1], gap="large")

    with col_vote:
        st.markdown("### 📢 اضغط لتصويت!")
        colors_v = ["#7c3aed", "#10b981", "#f59e0b"]
        emojis_v = ["🙌","🧭","🤔"]
        for (opt, cnt), clr, em in zip(s.votes.items(), colors_v, emojis_v):
            if st.button(f"  {opt}  ", key=f"v_{opt}"):
                s.votes[opt] += 1
                st.rerun()

        st.markdown(f"""
        <div class="m-box" style="margin-top:1.2rem;">
          <div class="m-val">{total_votes}</div>
          <div class="m-lbl">إجمالي الأصوات</div>
        </div>
        """, unsafe_allow_html=True)

    with col_result:
        st.markdown("### 📊 النتائج اللحظية")
        for (opt, cnt), clr in zip(s.votes.items(), colors_v):
            pct = int(cnt / total_votes * 100)
            st.markdown(f"""
            <div class="vote-row">
              <span class="vote-label">{opt}</span>
              <div class="vote-track">
                <div class="vote-fill" style="width:{pct}%; background:{clr};
                  box-shadow:0 0 10px {clr}88;"></div>
              </div>
              <span class="vote-pct">{pct}%</span>
              <span class="vote-count">({cnt})</span>
            </div>
            """, unsafe_allow_html=True)

        # Donut chart
        if total_votes > 1:
            labels = list(s.votes.keys())
            values = list(s.votes.values())
            winner = labels[values.index(max(values))]

            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=.65,
                marker_colors=colors_v,
                textinfo="none",
                hovertemplate="%{label}<br>%{percent}<extra></extra>"
            ))
            fig.add_annotation(
                text=f"<b>{max(values)}</b><br><span style='font-size:11px'>أعلى صوت</span>",
                x=.5, y=.5, showarrow=False,
                font=dict(size=16, color="#f0ece4", family="Tajawal")
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=10),
                height=240, showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    next_btn("التالي ← من أنا؟ 🔍", 2)


# ══════════════════════════════════════════════════════════════
# STEP 2 – من أنا؟
# ══════════════════════════════════════════════════════════════
elif s.step == 2:
    card("🔍 من أنا؟ — اكتشف ذاتك المهنية",
         "ما تحب · ما تجيد · ما يهمك — هذه مكونات بوصلتك", "amber")

    col1, col2, col3 = st.columns(3, gap="medium")

    loves_opts  = ["التصميم الإبداعي","البرمجة والتقنية","التعليم والتدريب","الإدارة والتنظيم",
                   "الفن والرسم","التواصل مع الناس","البحث العلمي","المحاسبة والأرقام",
                   "الصحة والرياضة","الكتابة الإبداعية","التسويق الرقمي","الهندسة"]
    skills_opts = ["التحليل والتفكير","القيادة والتأثير","الإقناع والتفاوض","الدقة والتفاصيل",
                   "العمل الجماعي","الابتكار والإبداع","التخطيط الاستراتيجي","المهارات التقنية",
                   "الاستماع الفعّال","حل المشكلات","إدارة الوقت","التصميم البصري"]
    values_opts = ["الاستقلالية في العمل","الأمان الوظيفي","التأثير الاجتماعي","التطور المستمر",
                   "الإبداع والحرية","الدخل المرتفع","التوازن الحياتي","المكانة المهنية",
                   "العدالة والمساواة","الخدمة الإنسانية","العمل مع الصم","الابتكار"]

    with col1:
        st.markdown('<div class="card card-t c-purple"><div class="card-h">❤️ ما الذي أحبه؟</div>'
                    '<div class="card-s">اختر كل ما يشعل حماسك</div></div>', unsafe_allow_html=True)
        s.loves = st.multiselect("", loves_opts, default=s.loves,
                                  key="loves_ms", label_visibility="collapsed")
        s.love_txt = st.text_area("أضف شيئاً آخر:", value=s.love_txt,
                                   placeholder="أحب أيضاً...", height=75,
                                   key="love_txt_i", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="card card-t c-teal"><div class="card-h">⚡ ما الذي أجيده؟</div>'
                    '<div class="card-s">مهاراتك الحقيقية والموهوبة</div></div>', unsafe_allow_html=True)
        s.my_skills = st.multiselect("", skills_opts, default=s.my_skills,
                                      key="skills_ms", label_visibility="collapsed")
        s.skill_txt = st.text_area("أضف مهارة:", value=s.skill_txt,
                                    placeholder="أجيد أيضاً...", height=75,
                                    key="skill_txt_i", label_visibility="collapsed")

    with col3:
        st.markdown('<div class="card card-t c-amber"><div class="card-h">🌟 ما الذي يهمني؟</div>'
                    '<div class="card-s">قيمك ومبادئك في العمل</div></div>', unsafe_allow_html=True)
        s.my_values = st.multiselect("", values_opts, default=s.my_values,
                                      key="values_ms", label_visibility="collapsed")

    # Market needs
    st.markdown('<div class="card card-t c-rose"><div class="card-h">🏢 ما يحتاجه سوق العمل</div>'
                '<div class="card-s">اختر المجال الأقرب إليك</div></div>', unsafe_allow_html=True)
    market_opts = ["💻 تقنية المعلومات","📚 التعليم والتدريب","🏥 الصحة والطب",
                   "💰 المحاسبة والمال","📢 الإعلام والتسويق","🎨 التصميم الجرافيكي",
                   "⚙️ الهندسة","🤝 الخدمات الاجتماعية","🌐 ريادة الأعمال"]
    s.market = st.radio("", market_opts, key="market_r",
                         horizontal=True, label_visibility="collapsed")

    # Live tag cloud preview
    all_sel = s.loves + s.my_skills + s.my_values
    if all_sel:
        colors_tag = ([""] * len(s.loves) +
                      ["teal"] * len(s.my_skills) +
                      ["amber"] * len(s.my_values))
        tags_html = "".join(
            f'<span class="tag {c}">{t}</span>'
            for t, c in zip(all_sel, colors_tag)
        )
        st.markdown(f'<div class="card" style="margin-top:.5rem">'
                    f'<div class="card-h">🎨 صورتك المهنية الآن</div>'
                    f'<div style="margin-top:.8rem">{tags_html}</div>'
                    f'</div>', unsafe_allow_html=True)

    next_btn("التالي ← البوصلة المهنية 🧭", 3)


# ══════════════════════════════════════════════════════════════
# STEP 3 – البوصلة المهنية (Radar + Bars)
# ══════════════════════════════════════════════════════════════
elif s.step == 3:
    card("🧭 بوصلتك المهنية الشخصية",
         "قيّم نفسك في كل محور من 0 إلى 10 — كن صادقاً مع نفسك", "purple")

    axes = {
        "❤️ الميول والشغف":         "مدى حبك لما تفعله",
        "⚡ القدرات والمهارات":      "مستوى كفاءتك الحقيقية",
        "🌟 القيم والمبادئ":        "توافق عملك مع قيمك",
        "🏢 فرص السوق":              "توفر فرص حقيقية في مجالك",
        "📚 التحضير والتأهيل":       "مدى استعدادك ومؤهلاتك",
    }

    col_sl, col_chart = st.columns([1, 1], gap="large")
    scores = {}

    with col_sl:
        st.markdown("#### 🎚️ اضبط مستواك في كل محور")
        for ax, desc in axes.items():
            st.markdown(f'<div style="font-weight:700; margin-top:.9rem">{ax}</div>'
                        f'<div style="font-size:.8rem; color:var(--muted); margin-bottom:.2rem">{desc}</div>',
                        unsafe_allow_html=True)
            val = st.slider("", 0, 10, 5, key=f"ax_{ax}", label_visibility="collapsed")
            scores[ax] = val

            # Mini progress bar
            bar_color = "#10b981" if val >= 7 else ("#f59e0b" if val >= 4 else "#f43f5e")
            st.markdown(f"""
            <div style="background:rgba(255,255,255,.07); border-radius:6px; height:6px; margin-bottom:.3rem">
              <div style="width:{val*10}%; height:6px; background:{bar_color};
                border-radius:6px; transition:width .4s"></div>
            </div>""", unsafe_allow_html=True)

    with col_chart:
        cats = list(scores.keys())
        vals = list(scores.values())
        cats_c = cats + [cats[0]]
        vals_c = vals + [vals[0]]

        # Radar
        fig = go.Figure()
        # Reference line (ideal = 8)
        fig.add_trace(go.Scatterpolar(
            r=[8]*len(cats)+[8], theta=cats_c,
            fill='toself', fillcolor='rgba(255,255,255,0.03)',
            line=dict(color='rgba(255,255,255,0.12)', width=1, dash='dot'),
            name="المستوى المرجعي", showlegend=True
        ))
        fig.add_trace(go.Scatterpolar(
            r=vals_c, theta=cats_c,
            fill='toself', fillcolor='rgba(124,58,237,0.28)',
            line=dict(color='#a78bfa', width=3),
            marker=dict(size=10, color='#34d399',
                        line=dict(color='#07080f', width=2.5),
                        symbol='circle'),
            name="بوصلتك", showlegend=True
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0,10],
                                tickfont=dict(color='#4b5563', size=9),
                                gridcolor='rgba(255,255,255,0.06)',
                                linecolor='rgba(255,255,255,0.08)'),
                angularaxis=dict(tickfont=dict(color='#c4b5fd', size=11, family='Tajawal'),
                                 gridcolor='rgba(255,255,255,0.06)',
                                 linecolor='rgba(255,255,255,0.08)'),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#9ca3af', family='Tajawal'),
                        bgcolor='rgba(0,0,0,0)', x=.5, xanchor='center', y=-.08, orientation='h'),
            margin=dict(t=20,b=40,l=60,r=60), height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Overall score
        total = sum(vals)
        max_t  = len(axes)*10
        pct    = int(total/max_t*100)
        if pct >= 70: lbl, clr = "🟢 مسار واضح وقوي", "#10b981"
        elif pct >= 45: lbl, clr = "🟡 مسار يحتاج تعزيزاً", "#f59e0b"
        else: lbl, clr = "🔴 يحتاج إعادة توجيه", "#f43f5e"

        st.markdown(f"""
        <div class="m-box">
          <div class="m-val">{pct}%</div>
          <div class="m-lbl" style="color:{clr}; font-weight:700">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    # Insights based on lowest scores
    min_ax  = min(scores, key=scores.get)
    max_ax  = max(scores, key=scores.get)
    st.markdown('<div class="div-fancy">· · ·</div>', unsafe_allow_html=True)
    st.markdown("#### 💡 رسائل بوصلتك")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        insight_box("🏆", f"نقطة قوتك: {max_ax}",
                    f"هذا هو أعلى محور لديك ({scores[max_ax]}/10) — ابنِ عليه مسارك")
    with col_i2:
        insight_box("🎯", f"محور التطوير: {min_ax}",
                    f"هذا يحتاج انتباهك ({scores[min_ax]}/10) — ضعه في خطتك")

    s.compass = scores
    next_btn("التالي ← خطة 30 يوم 📅", 4)


# ══════════════════════════════════════════════════════════════
# STEP 4 – خطة 30 يوم
# ══════════════════════════════════════════════════════════════
elif s.step == 4:
    card("📅 خطتي لـ 30 يوماً",
         "ضع 3 أهداف حقيقية قابلة للتنفيذ — ستراها في تقريرك النهائي", "teal")

    weeks = [
        ("الأسبوع الأول", "1–7", "🟣", "#7c3aed", "ابدأ بخطوة واحدة واضحة"),
        ("الأسبوع الثاني", "8–14", "🔵", "#3b82f6", "بنِ العادة وداوم عليها"),
        ("الأسبوع 3 والرابع", "15–30", "🟢", "#10b981", "قيّم تقدمك واحتفل بإنجازاتك"),
    ]

    placeholders = [
        "مثال: سأسجّل في دورة تدريبية في مجال التصميم",
        "مثال: سأتواصل مع 3 محترفين في مجالي",
        "مثال: سأقدّم على 5 فرص عمل أو تطوع",
    ]

    for i, (week, days, em, clr, hint) in enumerate(weeks):
        st.markdown(f"""
        <div class="plan-card" style="border-right-color:{clr}">
          <div style="display:flex; align-items:center; gap:.7rem; margin-bottom:.4rem">
            <span style="font-size:1.4rem">{em}</span>
            <div>
              <div style="font-weight:800; font-size:1.05rem">{week} (اليوم {days})</div>
              <div style="font-size:.82rem; color:var(--muted)">💡 {hint}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        s.plan[i] = st.text_area(
            f"هدفي:", value=s.plan[i],
            placeholder=placeholders[i],
            height=80, key=f"plan_{i}", label_visibility="collapsed"
        )

    # Gantt timeline
    filled = [(i, g) for i, g in enumerate(s.plan) if g.strip()]
    if filled:
        st.markdown('<div class="div-fancy">· · ·</div>', unsafe_allow_html=True)
        st.markdown("#### 🗓️ خط زمني بصري لخطتك")
        today = datetime.today()
        starts_d = [today, today+timedelta(days=7), today+timedelta(days=14)]
        ends_d   = [today+timedelta(days=6), today+timedelta(days=13), today+timedelta(days=29)]
        clrs_g   = ["#7c3aed","#3b82f6","#10b981"]

        df_rows = []
        for i, g in filled:
            df_rows.append(dict(
                Semaine=g[:40]+"…" if len(g)>40 else g,
                Debut=starts_d[i].strftime("%Y-%m-%d"),
                Fin=ends_d[i].strftime("%Y-%m-%d"),
                Couleur=weeks[i][0]
            ))
        df = pd.DataFrame(df_rows)
        fig2 = px.timeline(df, x_start="Debut", x_end="Fin", y="Semaine",
                           color="Semaine",
                           color_discrete_sequence=[clrs_g[i] for i,_ in filled])
        fig2.update_yaxes(autorange="reversed")
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f0ece4', family='Tajawal'),
            height=max(160, len(filled)*70),
            showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
            xaxis=dict(gridcolor='rgba(255,255,255,.05)',
                       tickfont=dict(color='#6b7280')),
            yaxis=dict(gridcolor='rgba(255,255,255,.05)')
        )
        st.plotly_chart(fig2, use_container_width=True)

    next_btn("التالي ← تقييمي البعدي ✅", 5)


# ══════════════════════════════════════════════════════════════
# STEP 5 – تقييم بعدي + نتيجة كاملة
# ══════════════════════════════════════════════════════════════
elif s.step == 5:
    card("✅ التقييم البعدي — كيف تشعر الآن؟",
         "قارن إجاباتك مع بداية الورشة وشاهد تحوّلك", "rose")

    post_qs = [
        ("p1", "🌟 هل اكتسبت وضوحاً أكبر حول مسارك المهني؟",
         ["نعم بشكل كبير ✅","إلى حد ما 🙂","قليلاً 😕","لم يتغير شيء ❌"], [4,3,2,1]),
        ("p2", "💪 هل تعرفت على نقاط قوة لم تكن تعرفها؟",
         ["نعم اكتشفت الكثير ✅","بعض الأشياء 🙂","شيء بسيط 😕","لا ❌"], [4,3,2,1]),
        ("p3", "🚀 هل أنت مستعد للبدء بخطتك اليوم؟",
         ["نعم سأبدأ اليوم ✅","سأبدأ هذا الأسبوع 🙂","أحتاج وقتاً 😕","لا أزال متردداً ❌"], [4,3,2,1]),
    ]

    total_post = 0
    for key, label, opts, sc in post_qs:
        st.markdown(f'<div class="card"><div class="card-h" style="font-size:1rem">{label}</div></div>',
                    unsafe_allow_html=True)
        ans = st.radio("", opts, key=f"post_{key}", horizontal=True, label_visibility="collapsed")
        s.post[key] = ans
        idx = opts.index(ans) if ans in opts else 0
        total_post += sc[idx]
    s.post_score = total_post

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🏆 عرض تقريري المهني الكامل", key="show_res"):
            s.show_result = True
            st.rerun()

    # ── النتيجة الكاملة ──────────────────────────────────────
    if s.show_result:
        st.markdown('<div class="div-fancy">✦ ✦ ✦</div>', unsafe_allow_html=True)

        # ── حساب المسار المقترح ──
        loves_all  = s.loves  + ([s.love_txt]  if s.love_txt.strip()  else [])
        skills_all = s.my_skills + ([s.skill_txt] if s.skill_txt.strip() else [])
        values_all = s.my_values

        recs = {
            "🎨 مصمم جرافيك / UX": {"التصميم الإبداعي","الفن والرسم","الابتكار والإبداع","التصميم البصري"},
            "💻 مطور برمجيات":      {"البرمجة والتقنية","المهارات التقنية","التحليل والتفكير"},
            "📚 مدرب / معلم":       {"التعليم والتدريب","التواصل مع الناس","الاستماع الفعّال","الخدمة الإنسانية"},
            "💰 محاسب / مالي":      {"المحاسبة والأرقام","الدقة والتفاصيل","التحليل والتفكير"},
            "📋 مدير مشاريع":       {"الإدارة والتنظيم","القيادة والتأثير","التخطيط الاستراتيجي"},
            "✍️ كاتب / إعلامي":    {"الكتابة الإبداعية","التسويق الرقمي","الإقناع والتفاوض"},
            "🌐 رائد أعمال":        {"الابتكار والإبداع","القيادة والتأثير","حل المشكلات"},
        }
        best, best_score = "🌟 خبير متعدد المجالات", 0
        all_chosen = set(loves_all) | set(skills_all)
        for title, kws in recs.items():
            sc = len(kws & all_chosen)
            if sc > best_score:
                best, best_score = title, sc

        # ── قبل/بعد comparison ──
        pct_pre  = int((s.pre_score  / 12) * 100)
        pct_post = int((s.post_score / 12) * 100)
        growth   = pct_post - pct_pre

        st.markdown(f"""
        <div class="result-wrap">
          <div class="result-trophy">🏆</div>
          <div class="result-title">تقريرك المهني الشخصي</div>
          <p style="color:var(--muted)">استناداً لإجاباتك الكاملة في البوصلة المهنية</p>
          <div class="result-badge">{best}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Metrics row ──
        c_a, c_b, c_c, c_d = st.columns(4)
        with c_a:
            st.markdown(f'<div class="m-box"><div class="m-val">{len(loves_all)}</div>'
                        '<div class="m-lbl">💖 اهتمام مكتشف</div></div>', unsafe_allow_html=True)
        with c_b:
            st.markdown(f'<div class="m-box"><div class="m-val">{len(skills_all)}</div>'
                        '<div class="m-lbl">⚡ مهارة موثّقة</div></div>', unsafe_allow_html=True)
        with c_c:
            goals_done = sum(1 for g in s.plan if g.strip())
            st.markdown(f'<div class="m-box"><div class="m-val">{goals_done}/3</div>'
                        '<div class="m-lbl">📅 أهداف مخطّطة</div></div>', unsafe_allow_html=True)
        with c_d:
            clr_g = "#10b981" if growth >= 0 else "#f43f5e"
            st.markdown(f'<div class="m-box"><div class="m-val" style="color:{clr_g}">+{growth}%</div>'
                        '<div class="m-lbl">📈 نمو الوضوح</div></div>', unsafe_allow_html=True)

        # ── Before/After Bar Chart ──
        st.markdown('<div class="div-fancy">· · ·</div>', unsafe_allow_html=True)
        st.markdown("#### 📊 تحوّلك قبل وبعد الورشة")

        fig_ba = go.Figure()
        fig_ba.add_trace(go.Bar(
            name="قبل الورشة", x=["مستوى الوضوح المهني"],
            y=[pct_pre], marker_color="#4b5563",
            text=[f"{pct_pre}%"], textposition="outside",
            textfont=dict(color="#9ca3af", family="Tajawal", size=14)
        ))
        fig_ba.add_trace(go.Bar(
            name="بعد الورشة", x=["مستوى الوضوح المهني"],
            y=[pct_post], marker_color="#7c3aed",
            text=[f"{pct_post}%"], textposition="outside",
            textfont=dict(color="#a78bfa", family="Tajawal", size=14)
        ))
        fig_ba.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0ece4", family="Tajawal"),
            barmode="group", height=280,
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#9ca3af")),
            margin=dict(t=30,b=10,l=10,r=10),
            yaxis=dict(range=[0,120], gridcolor="rgba(255,255,255,.05)",
                       tickfont=dict(color="#6b7280"), ticksuffix="%"),
            xaxis=dict(tickfont=dict(color="#9ca3af"))
        )
        st.plotly_chart(fig_ba, use_container_width=True)

        # ── Compass Radar final ──
        if s.compass:
            st.markdown("#### 🧭 بوصلتك المهنية")
            cats = list(s.compass.keys())
            vals_r = list(s.compass.values())
            fig_r = go.Figure(go.Scatterpolar(
                r=vals_r+[vals_r[0]], theta=cats+[cats[0]],
                fill='toself', fillcolor='rgba(124,58,237,0.22)',
                line=dict(color='#a78bfa', width=2.5),
                marker=dict(size=9, color='#34d399', line=dict(color='#07080f',width=2))
            ))
            fig_r.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0,10],
                                    tickfont=dict(color='#4b5563',size=9),
                                    gridcolor='rgba(255,255,255,.06)'),
                    angularaxis=dict(tickfont=dict(color='#c4b5fd',size=11,family='Tajawal'),
                                     gridcolor='rgba(255,255,255,.06)'),
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20,b=20,l=60,r=60), height=320, showlegend=False
            )
            st.plotly_chart(fig_r, use_container_width=True)

        # ── Tags ──
        all_tags = loves_all + skills_all + values_all
        if all_tags:
            st.markdown("#### 🎨 مخزونك المهني الكامل")
            tag_colors = ([""] * len(loves_all) +
                          ["teal"] * len(skills_all) +
                          ["amber"] * len(values_all))
            tags_html = "".join(f'<span class="tag {c}">{t}</span>'
                                for t, c in zip(all_tags, tag_colors))
            st.markdown(f'<div class="card">{tags_html}</div>', unsafe_allow_html=True)

        # ── Plan summary ──
        filled_plan = [(i+1, g) for i, g in enumerate(s.plan) if g.strip()]
        if filled_plan:
            st.markdown("#### 📌 التزاماتك للـ 30 يوم القادمة")
            week_clrs = ["#7c3aed","#3b82f6","#10b981"]
            week_names = ["الأسبوع الأول","الأسبوع الثاني","الأسبوع 3 و4"]
            for num, g in filled_plan:
                clr = week_clrs[num-1]
                wn  = week_names[num-1]
                st.markdown(f"""
                <div class="plan-card" style="border-right-color:{clr}">
                  <span style="color:{clr}; font-weight:800">{wn}:</span> {g}
                </div>""", unsafe_allow_html=True)

        # ── Motivational close ──
        st.markdown(f"""
        <div class="card" style="text-align:center; margin-top:1.5rem;
          background:linear-gradient(135deg,rgba(124,58,237,.12),rgba(16,185,129,.08));">
          <div style="font-size:2rem; margin-bottom:.5rem">🌟</div>
          <div style="font-size:1.2rem; font-weight:800; margin-bottom:.5rem">
            أنت الآن تملك بوصلتك!
          </div>
          <div style="color:var(--muted); max-width:500px; margin:0 auto">
            لا تنتظر الفرصة المثالية — ابدأ بخطوة واحدة صغيرة اليوم
            وستتضح الطريق أمامك تدريجياً.
          </div>
          <div style="margin-top:1rem; color:var(--purple-l); font-weight:700">
            مسارك المقترح: {best}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="text-align:center; padding:1.5rem 0; color:#374151; font-size:.85rem">'
                    '🧭 البوصلة المهنية للصم · صُمِّم بصرياً بكل احترام وتقدير للمجتمع الصامت'
                    '</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🔄 إعادة الورشة من البداية", key="restart"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()