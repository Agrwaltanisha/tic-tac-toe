import streamlit as st
from database import init_db, save_game
from game_logic import check_winner

st.set_page_config(page_title="Tic Tac Toe", layout="centered")
init_db()

# Header
st.markdown("<h1 style='text-align: center; color: #4a4a4a;'>🎮 Tic Tac Toe</h1>", unsafe_allow_html=True)

# Style
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            height: 60px;
            font-size: 24px;
            border: 2px solid #ccc;
            border-radius: 8px;
            transition: 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #f0f0f0;
        }
        .reset-button > button {
            background-color: #f44336;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
        }
        .reset-button > button:hover {
            background-color: #e53935;
        }
    </style>
""", unsafe_allow_html=True)

# Session state
if "board" not in st.session_state:
    st.session_state.board = [[""] * 3 for _ in range(3)]
    st.session_state.current = "X"
    st.session_state.moves = []
    st.session_state.finished = False
    st.session_state.players = ["Player X", "Player O"]

col1, col2 = st.columns(2)
with col1:
    st.session_state.players[0] = st.text_input("Player X", st.session_state.players[0])
with col2:
    st.session_state.players[1] = st.text_input("Player O", st.session_state.players[1])

def reset():
    st.session_state.board = [[""] * 3 for _ in range(3)]
    st.session_state.current = "X"
    st.session_state.moves = []
    st.session_state.finished = False

st.markdown("<div class='reset-button' style='text-align: center;'>", unsafe_allow_html=True)
st.button("🔄 Reset Game", on_click=reset)
st.markdown("</div>", unsafe_allow_html=True)

# Turn display
if not st.session_state.finished:
    st.markdown(
        f"<h4 style='text-align: center; color: #555;'>{st.session_state.players[0 if st.session_state.current == 'X' else 1]}'s turn ({st.session_state.current})</h4>",
        unsafe_allow_html=True
    )

# Game board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        label = st.session_state.board[i][j] or " "
        if cols[j].button(label, key=f"{i}-{j}") and not st.session_state.finished:
            if st.session_state.board[i][j] == "":
                st.session_state.board[i][j] = st.session_state.current
                st.session_state.moves.append(f"{st.session_state.current}:{i},{j}")
                winner = check_winner(st.session_state.board)
                if winner:
                    st.balloons()
                    st.success(f"{st.session_state.players[0 if winner == 'X' else 1]} wins!")
                    save_game(
                        st.session_state.players[0],
                        st.session_state.players[1],
                        ";".join(st.session_state.moves),
                        st.session_state.players[0 if winner == 'X' else 1]
                    )
                    st.session_state.finished = True
                elif all(cell != "" for row in st.session_state.board for cell in row):
                    st.info("It's a draw!")
                    save_game(
                        st.session_state.players[0],
                        st.session_state.players[1],
                        ";".join(st.session_state.moves),
                        "Draw"
                    )
                    st.session_state.finished = True
                else:
                    st.session_state.current = "O" if st.session_state.current == "X" else "X"
