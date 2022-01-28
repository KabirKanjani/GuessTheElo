import mysql.connector
import io
import data as d
import datetime
import streamlit as st
import chess.pgn
import chess.svg
import base64
import mysql.connector
import random

st.set_page_config(layout="wide")
new_title = '<meta name="viewport" content="width=device-width, initial-scale=1" /><div class="header"><center><p style="font-family:sans-serif; color:White; font-size: 4vh;">Guess The ' \
            'Elo(Lichess Ratings)</p></div> '
st.markdown(new_title, unsafe_allow_html=True)
hide_menu_style = """
        <style>
        html
        {
        margin:0;
        padding:0;
        border:0;
        }
        img
        {
        width:100%;
        height:100%;
        }
        div.stButton > button:first-child 
        {
        background-color:#769456;color:white;font-size:2vh;
        }
        .header
        {
        height:10%;                
        }
         MainMenu {visibility: hidden;
        footer {visibility: hidden;}


        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
first, sec, last = st.columns([2, 1, 2])
one, two, three = st.columns([1, 1, 1])
Ne = sec.button("Next Game")
if Ne:
    st.session_state.count1 += \
        1
    for key in st.session_state.keys():
        if key == 'score' or key == 'count1' or key == 'count':
            print()
        else:
            del st.session_state[key]


def getgame():
    myd = mysql.connector.connect(host=d.host, port=d.port, user=d.user,
                                  password=d.pwd, database=d.db)
    c = myd.cursor()
    # c.execute("select count(*) from chess")
    # r = int(list(c)[0][0])
    ra = random.randint(1, 8656)
    print(ra)
    c.execute("select * from chess where pid=%d" % ra)
    game = ""
    result = ""
    whiteelo = ""
    blackelo = ""
    white = ""
    black = ""
    for i in c:
        game = i[1]
        whiteelo = i[2]
        blackelo = i[3]
        white = i[4]
        black = i[5]
        result = i[6]
        link = i[7]
    if 'link' not in st.session_state:
        st.session_state.link = link
    if 'whiteleo' not in st.session_state:
        st.session_state.whiteelo = whiteelo
    if 'blackeleo' not in st.session_state:
        st.session_state.blackelo = blackelo
    if 'white' not in st.session_state:
        st.session_state.white = white
    if 'black' not in st.session_state:
        st.session_state.black = black
    if 'result' not in st.session_state:
        st.session_state.result = result
    return game


if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game' not in st.session_state:
    st.session_state.game = getgame()
else:
    dat = ""
pgn = io.StringIO(st.session_state.game)
first_game = chess.pgn.read_game(pgn)


def render_svg(svg):
    svg = svg.replace("#cdd16a", "#b9ca44")
    svg = svg.replace("d18b47", "769557")
    svg = svg.replace("ffce9e", "fff")
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    first.write(html, unsafe_allow_html=True)


bt = two.button("Next Move")

if 'data' not in st.session_state:
    j = 0
    board = first_game.board()
    squares = board.attacks(chess.E4)
    st.session_state.data = []
    st.session_state.clockw = []
    st.session_state.clockb = []
    for move in first_game.mainline_moves():
        st.session_state.data.append(move)
        board.push(move)
    for move1 in first_game.mainline():
        if j % 2 == 0:
            st.session_state.clockw.append(move1.clock())
        else:
            st.session_state.clockb.append(move1.clock())
        j += 1
    # print(st.session_state.clockb)
    # print(st.session_state.clockw)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'count1' not in st.session_state:
    st.session_state.count1 = 1
if 'clw' not in st.session_state:
    st.session_state.clw = 0
if 'clb' not in st.session_state:
    st.session_state.clb = 0

if 'board1' not in st.session_state:
    st.session_state.board1 = first_game.board()
if 'squares1' not in st.session_state:
    st.session_state.squares1 = st.session_state.board1.attacks(chess.E4)
if 'i' not in st.session_state:
    st.session_state.i = 0
    render_svg(chess.svg.board(st.session_state.board1, squares=st.session_state.squares1, coordinates=False))
if st.session_state.i > 0:
    bs = one.button("Prev")

    if bs:
        st.session_state.i -= 1
        st.session_state.board1.pop()
        render_svg(
            chess.svg.board(st.session_state.board1, squares=st.session_state.squares1, coordinates=False))
        if st.session_state.i % 2 == 0:
            st.session_state.clw -= 1
        else:
            st.session_state.clb -= 1
        if st.session_state.clb < len(st.session_state.clockb) and st.session_state.clw < len(st.session_state.clockw):
            sec.header(datetime.timedelta(seconds=st.session_state.clockb[st.session_state.clb]))
            sec.header(datetime.timedelta(seconds=st.session_state.clockw[st.session_state.clw]))
        else:
            sec.header(datetime.timedelta(seconds=st.session_state.clockb[len(st.session_state.clockb) - 1]))
            sec.header(datetime.timedelta(seconds=st.session_state.clockw[len(st.session_state.clockw) - 1]))
try:
    if bt:
        # print(st.session_state.board1)
        st.session_state.board1.push(chess.Move.from_uci(str(st.session_state.data[st.session_state.i])))
        render_svg(
            chess.svg.board(st.session_state.board1, squares=st.session_state.squares1, coordinates=False,
                            lastmove=st.session_state.data[st.session_state.i]))

        if st.session_state.clb < len(st.session_state.clockb) and st.session_state.clw < len(st.session_state.clockw):
            sec.header(datetime.timedelta(seconds=st.session_state.clockb[st.session_state.clb]))
            sec.header(datetime.timedelta(seconds=st.session_state.clockw[st.session_state.clw]))
        else:
            sec.header(datetime.timedelta(seconds=st.session_state.clockb[len(st.session_state.clockb) - 1]))
            sec.header(datetime.timedelta(seconds=st.session_state.clockw[len(st.session_state.clockw) - 1]))
        if st.session_state.i % 2 == 0:
            st.session_state.clw += 1
        else:
            st.session_state.clb += 1
        st.session_state.i += 1

except (IndexError, AssertionError):

    render_svg(
        chess.svg.board(st.session_state.board1, squares=st.session_state.squares1, coordinates=False))
    sec.header(datetime.timedelta(seconds=st.session_state.clockb[len(st.session_state.clockb) - 1]))
    sec.header(datetime.timedelta(seconds=st.session_state.clockw[len(st.session_state.clockw) - 1]))
    sec.header(f"Result:{st.session_state.result}")
# print(st.session_state.i, len(st.session_state.data), st.session_state.data[st.session_state.i])
# print(st.session_state.clb, len(st.session_state.clockb), st.session_state.clockb[st.session_state.clb])
# print(st.session_state.clw, len(st.session_state.clockw), st.session_state.clockw[st.session_state.clw])
with last.form(key="form1"):
    number_input = st.number_input("Enter Your Guess:", min_value=100, max_value=2900, value=1700, step=1)
    submit = st.form_submit_button(label="Submit")

if submit:
    st.session_state.count += 1
    render_svg(
        chess.svg.board(st.session_state.board1, squares=st.session_state.squares1, coordinates=False))
    st.session_state.avg = (st.session_state.whiteelo + st.session_state.blackelo) / 2
    if abs(st.session_state.avg - number_input) > 100:
        last.header(st.session_state.result)
        last.write(f'White Player:{st.session_state.white}({st.session_state.whiteelo})')
        last.write(f'Black Player:{st.session_state.black}({st.session_state.blackelo})')
        last.header(f'Average Rating:{int(st.session_state.avg)}')
        last.header("You got 0 Points")
        # last.header(f"Total Points:{st.session_state.score}")
        last.header(f"Average Score:{int(st.session_state.score / st.session_state.count)}")
        last.header(f"Link:{st.session_state.link}")
        last.header(f"Game Count:{st.session_state.count1}")
    else:
        last.header(st.session_state.result)
        last.write(f'White Player:{st.session_state.white}({st.session_state.whiteelo})')
        last.write(f'Black Player:{st.session_state.black}({st.session_state.blackelo})')
        last.header(f'Average Rating:{int(st.session_state.avg)}')
        last.header(f'You got {int(100 - abs(st.session_state.avg - number_input))} Points')
        st.session_state.score = st.session_state.score + int(100 - abs(st.session_state.avg - number_input))
        # last.header(f"Total Points:{st.session_state.score}")
        last.header(f"Average Score:{int(st.session_state.score / st.session_state.count)}")
        last.header(f"Link:{st.session_state.link}")
        last.header(f"Game Count:{st.session_state.count1}")
