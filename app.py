from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time

app = Flask(__name__)

# Game constants
WIDTH, HEIGHT = 800, 400
PADDLE_W, PADDLE_H = 12, 80
BALL_R = 12
PADDLE_SPEED = 8
BALL_SPEED = 6

game_state = {
    "left_paddle": {"x": 16, "y": HEIGHT // 2 - PADDLE_H // 2, "w": PADDLE_W, "h": PADDLE_H},
    "right_paddle": {"x": WIDTH - 16 - PADDLE_W, "y": HEIGHT // 2 - PADDLE_H // 2, "w": PADDLE_W, "h": PADDLE_H},
    "ball": {"x": WIDTH // 2, "y": HEIGHT // 2, "vx": BALL_SPEED, "vy": BALL_SPEED, "r": BALL_R},
    "scores": {"left": 0, "right": 0},
    "player_mouse_y": HEIGHT // 2
}

lock = threading.Lock()

def reset_ball():
    import random
    game_state["ball"]["x"] = WIDTH // 2
    game_state["ball"]["y"] = HEIGHT // 2
    # Ball direction random
    game_state["ball"]["vx"] = BALL_SPEED * (1 if random.random() < 0.5 else -1)
    game_state["ball"]["vy"] = BALL_SPEED * (1 if random.random() < 0.5 else -1)

def update_game():
    while True:
        time.sleep(1/60)
        with lock:
            # Player paddle follows mouse
            py = game_state["player_mouse_y"] - PADDLE_H // 2
            py = max(0, min(HEIGHT - PADDLE_H, py))
            game_state["left_paddle"]["y"] = py

            # AI paddle tracks ball
            ball_y = game_state["ball"]["y"]
            ai_y = game_state["right_paddle"]["y"] + PADDLE_H // 2
            if ai_y < ball_y:
                game_state["right_paddle"]["y"] += PADDLE_SPEED
            elif ai_y > ball_y:
                game_state["right_paddle"]["y"] -= PADDLE_SPEED
            game_state["right_paddle"]["y"] = max(0, min(HEIGHT - PADDLE_H, game_state["right_paddle"]["y"]))

            # Ball movement
            ball = game_state["ball"]
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]

            # Wall collision
            if ball["y"] - BALL_R < 0 or ball["y"] + BALL_R > HEIGHT:
                ball["vy"] *= -1

            # Paddle collision: left
            lp = game_state["left_paddle"]
            if (lp["x"] < ball["x"] - BALL_R < lp["x"] + lp["w"] and
                lp["y"] < ball["y"] < lp["y"] + lp["h"]):
                ball["vx"] = abs(ball["vx"])

            # Paddle collision: right
            rp = game_state["right_paddle"]
            if (rp["x"] < ball["x"] + BALL_R < rp["x"] + rp["w"] and
                rp["y"] < ball["y"] < rp["y"] + rp["h"]):
                ball["vx"] = -abs(ball["vx"])

            # Score
            if ball["x"] < 0:
                game_state["scores"]["right"] += 1
                reset_ball()
            elif ball["x"] > WIDTH:
                game_state["scores"]["left"] += 1
                reset_ball()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_player", methods=["POST"])
def update_player():
    data = request.get_json()
    with lock:
        game_state["player_mouse_y"] = int(data["mouse_y"])
    return jsonify(success=True)

@app.route("/game_state")
def get_game_state():
    with lock:
        # Send only needed fields
        state = {
            "left_paddle": game_state["left_paddle"].copy(),
            "right_paddle": game_state["right_paddle"].copy(),
            "ball": game_state["ball"].copy(),
            "scores": game_state["scores"].copy()
        }
    return jsonify(state)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    threading.Thread(target=update_game, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)