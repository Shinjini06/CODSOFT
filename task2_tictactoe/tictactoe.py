import streamlit as st
import random

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="🎮", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
body { background-color: #f5f0e8 !important; min-height: 100vh; }
.stApp { background-color: #f5f0e8 !important; }
.main { background: transparent !important; }
.header { text-align: center; color: #4a3f6b; margin-bottom: 1.5rem; }
.header h1 { font-size: 2.5rem; font-weight: 800; margin: 0; color: #4a3f6b; text-shadow: 0 2px 8px rgba(102, 126, 234, 0.15); }
.header p { font-size: 0.9rem; opacity: 0.75; margin-top: 0.3rem; color: #6b5ea8; }
.scoreboard { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0; }
.score-card { background: rgba(255,255,255,0.95); padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1); transition: transform 0.3s; }
.score-card:hover { transform: translateY(-3px); }
.score-label { color: #667eea; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.score-value { font-size: 2rem; font-weight: 800; margin-top: 0.3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.status-box { background: rgba(255,255,255,0.95); padding: 1.2rem; border-radius: 12px; text-align: center; font-size: 1.1rem; font-weight: 700; color: #667eea; margin: 1rem 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
.stButton > button { border-radius: 10px !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

def is_full(board):
    return all(c != "" for c in board)

def minimax(board, depth, is_max, alpha, beta):
    winner = check_winner(board)
    if winner == "O": return 10 - depth
    if winner == "X": return depth - 10
    if is_full(board): return 0
    if is_max:
        best = -1000
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, depth+1, False, alpha, beta))
                board[i] = ""
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, depth+1, True, alpha, beta))
                board[i] = ""
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def best_move(board):
    best_val, move = -1000, -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            val = minimax(board, 0, False, -1000, 1000)
            board[i] = ""
            if val > best_val:
                best_val, move = val, i
    return move

def easy_move(board):
    empty = [i for i in range(9) if board[i] == ""]
    return random.choice(empty) if empty else -1

def medium_move(board):
    if random.random() < 0.6:
        return best_move(board)
    empty = [i for i in range(9) if board[i] == ""]
    return random.choice(empty) if empty else -1

if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "status" not in st.session_state:
    st.session_state.status = "Your Turn!"
if "scores" not in st.session_state:
    st.session_state.scores = {"You": 0, "AI": 0, "Draw": 0}
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

def play(i):
    if st.session_state.game_over or st.session_state.board[i] != "":
        return
    board = st.session_state.board
    board[i] = "X"
    if check_winner(board) == "X":
        st.session_state.game_over = True
        st.session_state.status = "🎉 You Won!"
        st.session_state.scores["You"] += 1
        return
    if is_full(board):
        st.session_state.game_over = True
        st.session_state.status = "🤝 Draw!"
        st.session_state.scores["Draw"] += 1
        return
    if st.session_state.difficulty == "Easy":
        ai_idx = easy_move(board)
    elif st.session_state.difficulty == "Medium":
        ai_idx = medium_move(board)
    else:
        ai_idx = best_move(board)
    board[ai_idx] = "O"
    if check_winner(board) == "O":
        st.session_state.game_over = True
        st.session_state.status = "🤖 AI Wins!"
        st.session_state.scores["AI"] += 1
        return
    if is_full(board):
        st.session_state.game_over = True
        st.session_state.status = "🤝 Draw!"
        st.session_state.scores["Draw"] += 1
        return
    st.session_state.status = "Your Turn!"

st.markdown("""
<div class="header">
    <h1>🎮 Tic-Tac-Toe</h1>
    <p>CodSoft Internship • Task 2</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 Easy", use_container_width=True):
        st.session_state.difficulty = "Easy"
        st.session_state.board = [""] * 9
        st.session_state.game_over = False
        st.session_state.status = "Your Turn!"
        st.rerun()
with col2:
    if st.button("🟡 Medium", use_container_width=True):
        st.session_state.difficulty = "Medium"
        st.session_state.board = [""] * 9
        st.session_state.game_over = False
        st.session_state.status = "Your Turn!"
        st.rerun()
with col3:
    if st.button("🔴 Hard", use_container_width=True):
        st.session_state.difficulty = "Hard"
        st.session_state.board = [""] * 9
        st.session_state.game_over = False
        st.session_state.status = "Your Turn!"
        st.rerun()

st.caption(f"Current Difficulty: **{st.session_state.difficulty}**")

sc = st.session_state.scores
st.markdown(f"""
<div class="scoreboard">
    <div class="score-card"><div class="score-label">You (X)</div><div class="score-value">{sc['You']}</div></div>
    <div class="score-card"><div class="score-label">Draw</div><div class="score-value">{sc['Draw']}</div></div>
    <div class="score-card"><div class="score-label">AI (O)</div><div class="score-value">{sc['AI']}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="status-box">{st.session_state.status}</div>', unsafe_allow_html=True)

board = st.session_state.board
for row in range(3):
    cols = st.columns(3, gap="small")
    for col_idx, col in enumerate(cols):
        cell_idx = row * 3 + col_idx
        val = board[cell_idx]
        btn_text = val if val else "•"
        with col:
            if st.button(btn_text, key=f"cell_{cell_idx}", disabled=st.session_state.game_over, use_container_width=True):
                play(cell_idx)
                st.rerun()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.board = [""] * 9
        st.session_state.game_over = False
        st.session_state.status = "Your Turn!"
        st.rerun()
