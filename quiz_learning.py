# quiz_learning.py - LABBAIK Interactive Quiz & Learning Gamification
# Version: 1.0.1 - FIXED HTML RENDERING
# Updated: 2025-12-06
# Author: MS Hadianto

"""
================================================================================
📚 LABBAIK QUIZ & LEARNING GAMIFICATION
================================================================================

Interactive learning features to increase engagement and knowledge:

1. 🧠 QUIZZES
   - Daily quiz challenges
   - Topic-based quizzes (Manasik, Doa, Sejarah)
   - Timed challenges
   - Multiplayer quiz

2. 📖 LEARNING PATHS
   - Beginner to Expert progression
   - Milestone rewards
   - Certificates

3. 🎯 MINI GAMES
   - Doa matching game
   - Timeline challenge
   - Geography quiz

================================================================================
"""

import streamlit as st
import random
from datetime import datetime

# ============================================
# BRAND COLORS
# ============================================
COLORS = {
    "gold": "#D4AF37",
    "dark": "#1A1A1A",
    "dark_light": "#2D2D2D",
    "green": "#4CAF50",
    "blue": "#2196F3",
    "purple": "#9C27B0",
    "orange": "#FF9800",
    "red": "#F44336",
    "sand": "#C9A86C",
}

# ============================================
# QUIZ DATABASE
# ============================================
QUIZZES = {
    "manasik": {
        "title": "Quiz Manasik Umrah",
        "icon": "🕋",
        "description": "Uji pengetahuan manasik umrah kamu",
        "difficulty": "medium",
        "time_limit": 300,  # 5 minutes
        "points_per_question": 10,
        "questions": [
            {
                "question": "Apa rukun umrah yang pertama?",
                "options": ["Ihram", "Tawaf", "Sa'i", "Tahallul"],
                "correct": 0,
                "explanation": "Ihram adalah rukun pertama umrah, yaitu niat memasuki ibadah umrah dengan memakai pakaian ihram."
            },
            {
                "question": "Berapa kali putaran tawaf yang harus dilakukan?",
                "options": ["5 kali", "6 kali", "7 kali", "8 kali"],
                "correct": 2,
                "explanation": "Tawaf dilakukan sebanyak 7 putaran mengelilingi Ka'bah, dimulai dari Hajar Aswad."
            },
            {
                "question": "Sa'i dilakukan antara bukit apa saja?",
                "options": ["Safa dan Marwa", "Arafah dan Muzdalifah", "Mina dan Arafah", "Jabal Nur dan Tsur"],
                "correct": 0,
                "explanation": "Sa'i adalah berjalan/berlari kecil antara bukit Safa dan Marwa sebanyak 7 kali."
            },
            {
                "question": "Apa yang dimaksud dengan Tahallul?",
                "options": ["Berdoa di Multazam", "Mencium Hajar Aswad", "Mencukur/memotong rambut", "Minum air zamzam"],
                "correct": 2,
                "explanation": "Tahallul adalah mencukur atau memotong rambut sebagai tanda selesainya ibadah umrah."
            },
            {
                "question": "Miqat untuk jamaah dari Indonesia yang naik pesawat adalah?",
                "options": ["Yalamlam", "Qarnul Manazil", "Juhfah", "Dzul Hulaifah"],
                "correct": 1,
                "explanation": "Qarnul Manazil (As-Sail Al-Kabir) adalah miqat untuk jamaah yang datang dari arah timur termasuk Indonesia."
            },
            {
                "question": "Apa hukum melakukan umrah?",
                "options": ["Wajib sekali seumur hidup", "Sunnah muakkadah", "Fardhu kifayah", "Mubah"],
                "correct": 1,
                "explanation": "Menurut mayoritas ulama, umrah hukumnya sunnah muakkadah (sangat dianjurkan)."
            },
            {
                "question": "Idhtiba' adalah?",
                "options": ["Berlari kecil saat tawaf", "Membuka bahu kanan saat tawaf", "Mencium Hajar Aswad", "Berdoa di Hijr Ismail"],
                "correct": 1,
                "explanation": "Idhtiba' adalah menyingkapkan/membuka bahu kanan dengan menaruh kain ihram di bawah ketiak kanan."
            },
            {
                "question": "Ramal dilakukan pada putaran tawaf ke berapa?",
                "options": ["Putaran 1-3", "Putaran 4-7", "Semua putaran", "Putaran terakhir saja"],
                "correct": 0,
                "explanation": "Ramal (berjalan cepat dengan langkah pendek) dilakukan pada 3 putaran pertama tawaf."
            },
            {
                "question": "Di mana lokasi Hajar Aswad?",
                "options": ["Pojok timur Ka'bah", "Pojok selatan Ka'bah", "Pojok barat Ka'bah", "Pojok utara Ka'bah"],
                "correct": 0,
                "explanation": "Hajar Aswad terletak di pojok timur Ka'bah, menjadi titik awal dan akhir tawaf."
            },
            {
                "question": "Sholat sunnah setelah tawaf dilakukan di?",
                "options": ["Hijr Ismail", "Belakang Maqam Ibrahim", "Multazam", "Di mana saja dalam Masjidil Haram"],
                "correct": 1,
                "explanation": "Sholat 2 rakaat setelah tawaf dianjurkan di belakang Maqam Ibrahim."
            },
        ]
    },
    "doa": {
        "title": "Quiz Doa-Doa Umrah",
        "icon": "🤲",
        "description": "Seberapa hapal kamu dengan doa-doa umrah?",
        "difficulty": "easy",
        "time_limit": 240,
        "points_per_question": 10,
        "questions": [
            {
                "question": "Doa apa yang dibaca saat memulai tawaf?",
                "options": [
                    "Bismillahi Allahu Akbar",
                    "Subhanallah walhamdulillah",
                    "Rabbana atina fiddunya",
                    "La ilaha illallah"
                ],
                "correct": 0,
                "explanation": "Saat memulai tawaf dan setiap melewati Hajar Aswad, kita membaca 'Bismillahi Allahu Akbar'."
            },
            {
                "question": "Doa yang dibaca di antara Rukun Yamani dan Hajar Aswad adalah?",
                "options": [
                    "Rabbana atina fiddunya hasanah...",
                    "Allahumma inni as'aluka...",
                    "Rabbi zidni ilma",
                    "Subhanallahi wa bihamdihi"
                ],
                "correct": 0,
                "explanation": "Di antara Rukun Yamani dan Hajar Aswad, dianjurkan membaca 'Rabbana atina fiddunya hasanah wa fil akhirati hasanah wa qina adzaban nar'."
            },
            {
                "question": "Bacaan talbiyah yang benar adalah?",
                "options": [
                    "Labbaik Allahumma labbaik, labbaika la syarika laka labbaik...",
                    "Subhanallah walhamdulillah wala ilaha illallah...",
                    "Allahu Akbar Allahu Akbar...",
                    "La hawla wala quwwata illa billah..."
                ],
                "correct": 0,
                "explanation": "Talbiyah: Labbaik Allahumma labbaik, labbaika la syarika laka labbaik, innal hamda wan ni'mata laka wal mulk, la syarika lak."
            },
            {
                "question": "Kapan talbiyah dihentikan?",
                "options": [
                    "Saat sampai di hotel",
                    "Saat mulai tawaf",
                    "Setelah selesai sa'i",
                    "Saat tahallul"
                ],
                "correct": 1,
                "explanation": "Talbiyah dihentikan saat mulai tawaf, yaitu saat menyentuh atau menghadap Hajar Aswad."
            },
            {
                "question": "Doa naik ke bukit Safa adalah?",
                "options": [
                    "Innassafa wal marwata min sya'airillah...",
                    "Rabbana taqabbal minna...",
                    "Allahumma anta rabbi...",
                    "Subhanaka Allahumma wa bihamdika"
                ],
                "correct": 0,
                "explanation": "Saat naik ke Safa, dibaca: Innassafa wal marwata min sya'airillah (QS. Al-Baqarah: 158)."
            },
        ]
    },
    "sejarah": {
        "title": "Quiz Sejarah Ka'bah & Mekkah",
        "icon": "📜",
        "description": "Pelajari sejarah tempat suci",
        "difficulty": "hard",
        "time_limit": 360,
        "points_per_question": 15,
        "questions": [
            {
                "question": "Siapa yang pertama kali membangun Ka'bah?",
                "options": ["Nabi Ibrahim AS", "Nabi Adam AS", "Nabi Ismail AS", "Nabi Muhammad SAW"],
                "correct": 1,
                "explanation": "Menurut riwayat, Ka'bah pertama kali dibangun oleh Nabi Adam AS, kemudian dibangun ulang oleh Nabi Ibrahim AS dan Ismail AS."
            },
            {
                "question": "Apa nama sumur yang airnya diminum oleh jamaah haji/umrah?",
                "options": ["Sumur Salsabil", "Sumur Zamzam", "Sumur Kautsar", "Sumur Barakah"],
                "correct": 1,
                "explanation": "Zamzam adalah sumur yang airnya memancar untuk Hajar dan Ismail AS, dan masih mengalir hingga kini."
            },
            {
                "question": "Kapan Nabi Muhammad SAW meletakkan kembali Hajar Aswad?",
                "options": ["Sebelum kenabian", "Saat hijrah", "Setelah Fathu Makkah", "Saat haji wada"],
                "correct": 0,
                "explanation": "Peristiwa peletakan Hajar Aswad terjadi 5 tahun sebelum kenabian saat renovasi Ka'bah oleh Quraisy."
            },
            {
                "question": "Berapa tinggi Ka'bah saat ini?",
                "options": ["10 meter", "13.1 meter", "15 meter", "20 meter"],
                "correct": 1,
                "explanation": "Ka'bah saat ini memiliki tinggi sekitar 13.1 meter (43 kaki)."
            },
            {
                "question": "Kiswah (kain penutup Ka'bah) diganti setiap?",
                "options": ["Setiap bulan", "Setiap Ramadhan", "Setiap tahun (9 Dzulhijjah)", "Setiap 5 tahun"],
                "correct": 2,
                "explanation": "Kiswah diganti setiap tahun pada tanggal 9 Dzulhijjah (hari Arafah)."
            },
        ]
    }
}

# ============================================
# LEARNING PATHS
# ============================================
LEARNING_PATHS = {
    "beginner": {
        "title": "Pemula - Mengenal Umrah",
        "icon": "🌱",
        "description": "Dasar-dasar umrah untuk jamaah pemula",
        "modules": [
            {"id": "intro", "title": "Apa itu Umrah?", "points": 20, "duration": 10},
            {"id": "rukun", "title": "5 Rukun Umrah", "points": 30, "duration": 15},
            {"id": "wajib", "title": "Wajib-Wajib Umrah", "points": 25, "duration": 12},
            {"id": "sunnah", "title": "Sunnah-Sunnah Umrah", "points": 25, "duration": 12},
            {"id": "larangan", "title": "Larangan Saat Ihram", "points": 30, "duration": 15},
        ],
        "completion_reward": 200,
        "badge": "beginner_complete"
    },
    "intermediate": {
        "title": "Menengah - Praktik Manasik",
        "icon": "🌿",
        "description": "Memperdalam praktik manasik umrah",
        "modules": [
            {"id": "ihram_detail", "title": "Ihram Lengkap", "points": 35, "duration": 20},
            {"id": "tawaf_detail", "title": "Tawaf Lengkap", "points": 40, "duration": 25},
            {"id": "sai_detail", "title": "Sa'i Lengkap", "points": 35, "duration": 20},
            {"id": "doa_complete", "title": "Doa-Doa Lengkap", "points": 50, "duration": 30},
            {"id": "ziarah", "title": "Ziarah di Mekkah & Madinah", "points": 40, "duration": 25},
        ],
        "completion_reward": 400,
        "badge": "intermediate_complete"
    },
    "advanced": {
        "title": "Mahir - Umrah Mandiri",
        "icon": "🌳",
        "description": "Persiapan umrah mandiri tanpa travel agent",
        "modules": [
            {"id": "visa", "title": "Proses Visa Umrah", "points": 50, "duration": 25},
            {"id": "tiket", "title": "Tips Tiket Pesawat", "points": 40, "duration": 20},
            {"id": "hotel", "title": "Booking Hotel", "points": 45, "duration": 22},
            {"id": "transport", "title": "Transportasi Lokal", "points": 35, "duration": 18},
            {"id": "emergency", "title": "Penanganan Darurat", "points": 55, "duration": 28},
        ],
        "completion_reward": 600,
        "badge": "advanced_complete"
    }
}


# ============================================
# QUIZ FUNCTIONS
# ============================================

def init_quiz_state():
    """Initialize quiz session state"""
    if "quiz" not in st.session_state:
        st.session_state.quiz = {
            "active": False,
            "current_quiz": None,
            "current_question": 0,
            "answers": [],
            "score": 0,
            "start_time": None,
            "completed_quizzes": [],
        }


def start_quiz(quiz_id):
    """Start a new quiz"""
    init_quiz_state()
    quiz = QUIZZES.get(quiz_id)
    if quiz:
        st.session_state.quiz["active"] = True
        st.session_state.quiz["current_quiz"] = quiz_id
        st.session_state.quiz["current_question"] = 0
        st.session_state.quiz["answers"] = []
        st.session_state.quiz["score"] = 0
        st.session_state.quiz["start_time"] = datetime.now()


def submit_answer(answer_index):
    """Submit an answer for current question"""
    quiz_id = st.session_state.quiz["current_quiz"]
    quiz = QUIZZES.get(quiz_id)
    current_q = st.session_state.quiz["current_question"]
    
    question = quiz["questions"][current_q]
    is_correct = answer_index == question["correct"]
    
    st.session_state.quiz["answers"].append({
        "question": current_q,
        "answer": answer_index,
        "correct": is_correct
    })
    
    if is_correct:
        st.session_state.quiz["score"] += quiz["points_per_question"]
    
    # Move to next question or finish
    if current_q + 1 < len(quiz["questions"]):
        st.session_state.quiz["current_question"] += 1
    else:
        finish_quiz()


def finish_quiz():
    """Finish the current quiz"""
    quiz_id = st.session_state.quiz["current_quiz"]
    st.session_state.quiz["active"] = False
    st.session_state.quiz["completed_quizzes"].append({
        "quiz_id": quiz_id,
        "score": st.session_state.quiz["score"],
        "completed_at": datetime.now().isoformat()
    })


# ============================================
# QUIZ UI COMPONENTS
# ============================================

def render_quiz_hub():
    """Render main quiz hub"""
    init_quiz_state()
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: {COLORS['gold']}; font-size: 2rem; margin-bottom: 5px;">
            🧠 Quiz & Learning Center
        </h1>
        <p style="color: {COLORS['sand']};">
            Uji dan tingkatkan pengetahuan umrah kamu!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily Challenge Banner
    render_daily_quiz_banner()
    
    st.markdown("### 📚 Pilih Kategori Quiz")
    
    cols = st.columns(3)
    for i, (quiz_id, quiz) in enumerate(QUIZZES.items()):
        with cols[i % 3]:
            completed = quiz_id in [q["quiz_id"] for q in st.session_state.quiz.get("completed_quizzes", [])]
            
            difficulty_colors = {"easy": COLORS["green"], "medium": COLORS["orange"], "hard": COLORS["red"]}
            diff_color = difficulty_colors.get(quiz["difficulty"], COLORS["gold"])
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['dark_light']} 100%);
                        border-radius: 15px; padding: 20px; margin-bottom: 15px;
                        border: 1px solid {COLORS['gold'] if completed else COLORS['dark_light']};">
                <div style="font-size: 2.5rem; text-align: center; margin-bottom: 10px;">{quiz['icon']}</div>
                <div style="color: white; font-weight: 700; text-align: center; margin-bottom: 5px;">
                    {quiz['title']} {'✅' if completed else ''}
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.8rem; text-align: center; margin-bottom: 10px;">
                    {quiz['description']}
                </div>
                <div style="display: flex; justify-content: center; gap: 10px;">
                    <span style="background: {diff_color}30; color: {diff_color}; padding: 3px 10px; 
                                border-radius: 10px; font-size: 0.7rem; font-weight: 600;">
                        {quiz['difficulty'].upper()}
                    </span>
                    <span style="background: {COLORS['gold']}30; color: {COLORS['gold']}; padding: 3px 10px;
                                border-radius: 10px; font-size: 0.7rem; font-weight: 600;">
                        {len(quiz['questions'])} soal
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Mulai Quiz", key=f"start_{quiz_id}", use_container_width=True):
                start_quiz(quiz_id)
                st.rerun()


def render_daily_quiz_banner():
    """Render daily quiz challenge banner"""
    
    # Random daily quiz
    daily_quiz = random.choice(list(QUIZZES.keys()))
    quiz = QUIZZES[daily_quiz]
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2D1F3D 0%, {COLORS['dark']} 100%);
                border: 2px solid {COLORS['purple']}; border-radius: 20px; padding: 20px;
                margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: {COLORS['purple']}; font-size: 0.8rem; font-weight: 600; margin-bottom: 5px;">
                    ⚡ TANTANGAN HARIAN
                </div>
                <div style="color: white; font-size: 1.2rem; font-weight: 700;">
                    {quiz['icon']} {quiz['title']}
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.85rem;">
                    Selesaikan untuk mendapat bonus poin!
                </div>
            </div>
            <div style="text-align: right;">
                <div style="background: {COLORS['gold']}; color: {COLORS['dark']}; padding: 10px 20px;
                            border-radius: 25px; font-weight: 700;">
                    +{len(quiz['questions']) * quiz['points_per_question'] * 2} LP
                </div>
                <div style="color: {COLORS['sand']}; font-size: 0.75rem; margin-top: 5px;">
                    2x poin hari ini!
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_active_quiz():
    """Render active quiz interface"""
    init_quiz_state()
    
    if not st.session_state.quiz["active"]:
        return False
    
    quiz_id = st.session_state.quiz["current_quiz"]
    quiz = QUIZZES.get(quiz_id)
    current_q = st.session_state.quiz["current_question"]
    question = quiz["questions"][current_q]
    
    # Progress header
    progress = (current_q / len(quiz["questions"])) * 100
    
    st.markdown(f"""
    <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="color: white; font-weight: 600;">
                {quiz['icon']} {quiz['title']}
            </div>
            <div style="color: {COLORS['gold']}; font-weight: 700;">
                Skor: {st.session_state.quiz['score']}
            </div>
        </div>
        <div style="background: {COLORS['dark_light']}; border-radius: 10px; height: 8px; margin-bottom: 10px; overflow: hidden;">
            <div style="background: {COLORS['gold']}; height: 100%; width: {progress}%;"></div>
        </div>
        <div style="text-align: center; color: {COLORS['sand']}; font-size: 0.85rem;">
            Pertanyaan {current_q + 1} dari {len(quiz['questions'])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #1E3D2F 100%);
                border-radius: 20px; padding: 30px; margin-bottom: 20px;
                border: 1px solid {COLORS['gold']}40;">
        <div style="color: white; font-size: 1.3rem; font-weight: 600; text-align: center; line-height: 1.6;">
            {question['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    for i, option in enumerate(question["options"]):
        if st.button(f"{chr(65+i)}. {option}", key=f"answer_{i}", use_container_width=True):
            submit_answer(i)
            
            # Show result
            if i == question["correct"]:
                st.success(f"✅ Benar! {question['explanation']}")
            else:
                st.error(f"❌ Salah. Jawaban yang benar: {question['options'][question['correct']]}")
                st.info(question['explanation'])
            
            st.rerun()
    
    return True


def render_quiz_results():
    """Render quiz results"""
    init_quiz_state()
    
    if st.session_state.quiz["active"]:
        return False
    
    if not st.session_state.quiz["completed_quizzes"]:
        return False
    
    last_quiz = st.session_state.quiz["completed_quizzes"][-1]
    quiz = QUIZZES.get(last_quiz["quiz_id"])
    score = last_quiz["score"]
    max_score = len(quiz["questions"]) * quiz["points_per_question"]
    percentage = (score / max_score) * 100
    
    # Determine grade
    if percentage >= 90:
        grade = {"letter": "A+", "text": "Luar Biasa!", "color": COLORS["gold"], "icon": "🏆"}
    elif percentage >= 80:
        grade = {"letter": "A", "text": "Sangat Bagus!", "color": COLORS["green"], "icon": "⭐"}
    elif percentage >= 70:
        grade = {"letter": "B", "text": "Bagus!", "color": COLORS["blue"], "icon": "👍"}
    elif percentage >= 60:
        grade = {"letter": "C", "text": "Cukup Baik", "color": COLORS["orange"], "icon": "📚"}
    else:
        grade = {"letter": "D", "text": "Perlu Belajar Lagi", "color": COLORS["red"], "icon": "💪"}
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['dark']} 0%, #2D1F3D 100%);
                border-radius: 25px; padding: 40px; text-align: center; margin: 20px 0;
                border: 2px solid {grade['color']};">
        <div style="font-size: 4rem; margin-bottom: 15px;">{grade['icon']}</div>
        <div style="color: {grade['color']}; font-size: 3rem; font-weight: 800; margin-bottom: 10px;">
            {grade['letter']}
        </div>
        <div style="color: white; font-size: 1.5rem; font-weight: 600; margin-bottom: 5px;">
            {grade['text']}
        </div>
        <div style="color: {COLORS['sand']}; font-size: 1.1rem; margin-bottom: 20px;">
            Skor: {score}/{max_score} ({percentage:.0f}%)
        </div>
        
        <div style="background: {COLORS['dark']}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
            <div style="color: {COLORS['gold']}; font-size: 1.8rem; font-weight: 700;">
                +{score} LP
            </div>
            <div style="color: {COLORS['sand']}; font-size: 0.85rem;">
                Poin ditambahkan ke akun kamu
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ulangi Quiz", use_container_width=True):
            start_quiz(last_quiz["quiz_id"])
            st.rerun()
    with col2:
        if st.button("📚 Quiz Lainnya", use_container_width=True):
            st.session_state.quiz["completed_quizzes"] = []
            st.rerun()
    
    return True


def render_learning_paths():
    """Render learning paths section"""
    
    st.markdown(f"""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <h3 style="color: {COLORS['gold']};">📖 Learning Paths</h3>
        <p style="color: {COLORS['sand']};">Ikuti jalur pembelajaran terstruktur</p>
    </div>
    """, unsafe_allow_html=True)
    
    for path_id, path in LEARNING_PATHS.items():
        # Calculate progress (placeholder)
        completed_modules = random.randint(0, len(path["modules"]))
        progress = (completed_modules / len(path["modules"])) * 100
        total_points = sum(m["points"] for m in path["modules"])
        
        with st.expander(f"{path['icon']} {path['title']}", expanded=False):
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="color: {COLORS['sand']}; margin-bottom: 10px;">{path['description']}</div>
                <div style="background: {COLORS['dark']}; border-radius: 10px; height: 10px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {COLORS['green']} 0%, {COLORS['gold']} 100%);
                                height: 100%; width: {progress}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                    <span style="color: {COLORS['sand']}; font-size: 0.8rem;">{completed_modules}/{len(path['modules'])} modul</span>
                    <span style="color: {COLORS['gold']}; font-size: 0.8rem;">Total: {total_points} LP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for module in path["modules"]:
                is_complete = random.choice([True, False])
                st.markdown(f"""
                <div style="background: {COLORS['dark']}; border-radius: 10px; padding: 12px; margin-bottom: 8px;
                            display: flex; justify-content: space-between; align-items: center;
                            border-left: 3px solid {COLORS['green'] if is_complete else COLORS['dark_light']};">
                    <div>
                        <div style="color: white; font-weight: 600;">{module['title']} {'✅' if is_complete else ''}</div>
                        <div style="color: {COLORS['sand']}; font-size: 0.75rem;">⏱️ {module['duration']} menit</div>
                    </div>
                    <div style="color: {COLORS['gold']}; font-weight: 600;">+{module['points']} LP</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: {COLORS['gold']}20; border-radius: 10px; padding: 12px; margin-top: 15px;
                        text-align: center;">
                <span style="color: {COLORS['gold']};">🎁 Selesaikan semua untuk bonus </span>
                <span style="color: white; font-weight: 700;">+{path['completion_reward']} LP + Badge!</span>
            </div>
            """, unsafe_allow_html=True)


# ============================================
# MAIN RENDER FUNCTION
# ============================================

def render_quiz_page():
    """Main quiz page render function"""
    init_quiz_state()
    
    # Check if quiz is active
    if render_active_quiz():
        return
    
    # Check if showing results
    if render_quiz_results():
        return
    
    # Show quiz hub
    render_quiz_hub()
    
    # Show learning paths
    render_learning_paths()


# ============================================
# EXPORT
# ============================================
__all__ = [
    "init_quiz_state",
    "start_quiz",
    "render_quiz_page",
    "render_quiz_hub",
    "render_active_quiz",
    "render_quiz_results",
    "render_learning_paths",
    "QUIZZES",
    "LEARNING_PATHS",
]
