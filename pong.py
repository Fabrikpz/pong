import py5
import time

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
game_started = False
countdown = 3
countdown_start_time = None
ball_trail = []  # Lista para almacenar las posiciones de la pelota

# Estado de las teclas presionadas
keys = set()

def setup():
    py5.size(800, 400)
    global paddle_width, paddle_height, paddle_speed, ball_size
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle1_y, paddle2_y, player1_score, player2_score
    paddle_width = 20
    paddle_height = 100
    paddle_speed = 7
    ball_size = 20
    reset_game()

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y, player1_score, player2_score, game_started, countdown, countdown_start_time, ball_trail
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0
    countdown = 3
    game_started = False
    countdown_start_time = time.time()
    ball_trail = []  # Reiniciar la estela

def draw():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score, game_started, countdown, countdown_start_time

    py5.background(0)
    
    # Mostrar el contador antes de iniciar la partida
    if not game_started:
        if countdown_start_time:
            elapsed = time.time() - countdown_start_time
            if elapsed >= 1:
                countdown -= 1
                countdown_start_time = time.time()
        
        if countdown > 0:
            py5.text_size(64)
            py5.fill(255)
            py5.text_align(py5.CENTER, py5.CENTER)
            py5.text(str(countdown), py5.width / 2, py5.height / 2)
        else:
            game_started = True
    
    # Si el juego no ha empezado, salir del draw
    if not game_started:
        return
    
    # Dibujar los paddles
    py5.rect(30, paddle1_y, paddle_width, paddle_height)  # Pala izquierda
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)  # Pala derecha
    
    # Actualizar la posición de la pelota y agregar a la estela
    ball_trail.append((ball_x, ball_y))  # Guardar posición actual
    ball_x += ball_dx
    ball_y += ball_dy

    # Dibujar la estela
    for i in range(len(ball_trail) - 1):
        # Gradiente de opacidad en la estela
        alpha = 255 - (i * (255 // len(ball_trail)))
        py5.stroke(255, alpha)
        py5.line(ball_trail[i][0], ball_trail[i][1], ball_trail[i + 1][0], ball_trail[i + 1][1])
    
    # Limitar la longitud de la estela
    if len(ball_trail) > 20:  # Mantener las últimas 20 posiciones
        ball_trail.pop(0)

    # Dibujar la pelota
    py5.fill(255)
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)
    
    # Dibujar el marcador
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)
    
    # Dibujar ayuda de teclas
    py5.text_size(16)
    py5.text_align(py5.LEFT)
    py5.fill(255)
    py5.text("Jugador 1: W (Arriba), S (Abajo)", 10, 30)
    py5.text_align(py5.RIGHT)
    py5.text("Jugador 2: O (Arriba), L (Abajo)", py5.width - 10, 30)

    # Rebote de la pelota en la parte superior e inferior
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1
    
    # Verificar colisiones con los paddles
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            ball_x = 30 + paddle_width + ball_size / 2
    
    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ball_x = py5.width - 30 - paddle_width - ball_size / 2
    
    # Si la pelota sale por la izquierda
    if ball_x < 0:
        player2_score += 1
        start_new_round()
    
    # Si la pelota sale por la derecha
    if ball_x > py5.width:
        player1_score += 1
        start_new_round()

    # Limitar el movimiento de los paddles
    if 'w' in keys and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if 's' in keys and paddle1_y < py5.height - paddle_height:
        paddle1_y += paddle_speed
    if 'o' in keys and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if 'l' in keys and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed

def key_pressed():
    global keys
    keys.add(py5.key)

def key_released():
    global keys
    keys.discard(py5.key)

def start_new_round():
    global ball_x, ball_y, ball_dx, ball_dy, countdown, game_started, countdown_start_time, ball_trail
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5 * (1 + (player1_score + player2_score) * 0.1)  # Incremento de velocidad con cada punto
    ball_dy = py5.random(-3, 3)
    countdown = 3
    game_started = False
    countdown_start_time = time.time()
    ball_trail = []  # Reiniciar la estela

if __name__ == "__main__":
    py5.run_sketch()