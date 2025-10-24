import sys
import os
import json
import time
import signal
import traceback
import subprocess
from pathlib import Path

# Config / Helpers

ROOT = Path(os.path.abspath(os.path.dirname(__file__)))
STATUS_DIR = ROOT / ".games_status"
STATUS_DIR.mkdir(exist_ok=True)

def write_status(path: Path, data: dict):
    try:
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        tmp.replace(path)
    except Exception:
        # fallback: best-effort, don't crash the game because of status write
        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(json.dumps({"error": "status write failed"}))
        except Exception:
            pass

def default_status_path(key: str) -> Path:
    return STATUS_DIR / f"{key}.status"

# Dependency helpers

def has_pygame():
    try:
        import pygame  # noqa: F401
        return True
    except Exception:
        return False

def has_ursina():
    try:
        import ursina  # noqa: F401
        return True
    except Exception:
        return False

def ensure_pygame():
    try:
        import pygame
        return pygame
    except Exception as e:
        raise RuntimeError("pygame is required. Install: pip install pygame") from e

def ensure_ursina():
    try:
        import ursina
        return ursina
    except Exception as e:
        raise RuntimeError("ursina is required. Install: pip install ursina") from e

# Generic game runner helpers (used by each game function)

def _game_entry_wrapper(key: str, status_path: Path, title: str, run_fn):
    pid = os.getpid()
    started_at = time.time()
    status_path = Path(status_path) if status_path else default_status_path(key)
    write_status(status_path, {"key": key, "title": title or key, "pid": pid, "status": "starting", "started_at": started_at})

    # signal handling: set a flag to request exit
    _exit_requested = {"flag": False}
    def _on_exit(signum, frame):
        _exit_requested["flag"] = True
    signal.signal(signal.SIGINT, _on_exit)
    try:
        # Periodic ticker thread not used to avoid extra threads; games themselves should return on exit.
        write_status(status_path, {"key": key, "title": title or key, "pid": pid, "status": "running", "started_at": started_at})
        run_fn(_exit_requested)
        # normal exit
        write_status(status_path, {"key": key, "title": title or key, "pid": pid, "status": "exited", "started_at": started_at, "exited_at": time.time()})
    except SystemExit:
        write_status(status_path, {"key": key, "title": title or key, "pid": pid, "status": "exited", "started_at": started_at, "exited_at": time.time()})
        raise
    except Exception as e:
        tb = traceback.format_exc()
        write_status(status_path, {"key": key, "title": title or key, "pid": pid, "status": "error", "error": str(e), "traceback": tb, "started_at": started_at, "errored_at": time.time()})
        # print for user's console
        print("Game crashed:", e)
        print(tb)
        # exit non-zero so launcher can detect failure
        sys.exit(1)

# PYGAME GAMES (2D)
# Each run_* accepts a single parameter 'exit_requested' dict with .flag True/False

def run_snake_game(exit_requested):
    pygame = ensure_pygame()
    import random
    pygame.init()
    W, H = 640, 480
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    CELL = 20
    dirs = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}

    def game_over(scr, score):
        txt = font.render(f"Game Over! Score: {score}  Press ESC to quit", True, (255, 255, 255))
        scr.fill((0, 0, 0)); scr.blit(txt, (20, H//2-20)); pygame.display.flip()
        waiting = True
        while waiting and not exit_requested["flag"]:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            pygame.time.wait(50)

    head = [W//2//CELL, H//2//CELL]
    snake = [tuple(head)]
    direction = 'RIGHT'
    food = (random.randint(0, (W//CELL)-1), random.randint(0, (H//CELL)-1))
    score = 0
    speed = 8
    while not exit_requested["flag"]:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if ev.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
                if ev.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
                if ev.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
                if ev.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

        dx, dy = dirs[direction]
        head[0] += dx
        head[1] += dy
        head_pos = (head[0] % (W//CELL), head[1] % (H//CELL))

        if head_pos in snake:
            game_over(screen, score)
            break

        snake.insert(0, head_pos)
        if head_pos == food:
            score += 1
            food = (random.randint(0, (W//CELL)-1), random.randint(0, (H//CELL)-1))
            if score % 5 == 0: speed += 1
        else:
            snake.pop()

        screen.fill((10, 10, 10))
        for s in snake:
            pygame.draw.rect(screen, (0, 200, 0), (s[0]*CELL, s[1]*CELL, CELL-1, CELL-1))
        pygame.draw.rect(screen, (200, 50, 50), (food[0]*CELL, food[1]*CELL, CELL-1, CELL-1))
        txt = font.render(f"Score: {score}", True, (200, 200, 200))
        screen.blit(txt, (6, 6))
        pygame.display.flip()
        clock.tick(speed)
    pygame.quit()

def run_pong_game(exit_requested):
    pygame = ensure_pygame()
    pygame.init()
    W, H = 800, 500
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    p1 = pygame.Rect(20, H//2-50, 10, 100)
    p2 = pygame.Rect(W-30, H//2-50, 10, 100)
    ball = pygame.Rect(W//2-10, H//2-10, 20, 20)
    vel = [5, 4]
    score1 = score2 = 0
    speed = 60
    while not exit_requested["flag"]:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: p1.y -= 6
        if keys[pygame.K_s]: p1.y += 6
        if keys[pygame.K_UP]: p2.y -= 6
        if keys[pygame.K_DOWN]: p2.y += 6
        p1.y = max(0, min(H-p1.height, p1.y))
        p2.y = max(0, min(H-p2.height, p2.y))
        ball.x += vel[0]; ball.y += vel[1]
        if ball.top <= 0 or ball.bottom >= H: vel[1] = -vel[1]
        if ball.colliderect(p1) or ball.colliderect(p2): vel[0] = -vel[0]
        if ball.left < 0:
            score2 += 1; ball.center = (W//2, H//2); vel[0] = 5
        if ball.right > W:
            score1 += 1; ball.center = (W//2, H//2); vel[0] = -5
        screen.fill((8, 8, 8))
        pygame.draw.rect(screen, (200, 200, 200), p1); pygame.draw.rect(screen, (200, 200, 200), p2)
        pygame.draw.ellipse(screen, (220, 50, 50), ball)
        txt = font.render(f"{score1}  -  {score2}", True, (200, 200, 200))
        screen.blit(txt, (W//2-40, 10))
        pygame.display.flip()
        clock.tick(speed)
    pygame.quit()

def run_breakout_game(exit_requested):
    pygame = ensure_pygame()
    import random
    pygame.init()
    W, H = 640, 480
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    paddle = pygame.Rect(W//2-40, H-30, 80, 12)
    ball = pygame.Rect(W//2-8, H//2, 16, 16)
    vel = [4, -4]
    bricks = []
    rows = 5; cols = 10
    brick_w = W//cols; brick_h = 20
    for r in range(rows):
        for c in range(cols):
            bricks.append(pygame.Rect(c*brick_w+2, 40+r*brick_h+2, brick_w-4, brick_h-4))
    score = 0
    while not exit_requested["flag"]:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        mx = pygame.mouse.get_pos()[0]
        paddle.centerx = mx
        ball.x += vel[0]; ball.y += vel[1]
        if ball.left<=0 or ball.right>=W: vel[0] = -vel[0]
        if ball.top<=0: vel[1] = -vel[1]
        if ball.colliderect(paddle): vel[1] = -abs(vel[1])
        for b in bricks[:]:
            if ball.colliderect(b):
                bricks.remove(b)
                vel[1] *= -1
                score += 10
        if ball.bottom > H:
            txt = font.render(f"Game Over! Score: {score}  Press ESC to quit", True, (255,255,255))
            screen.fill((0,0,0)); screen.blit(txt, (20, H//2-20)); pygame.display.flip()
            waiting = True
            while waiting and not exit_requested["flag"]:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                pygame.time.wait(50)
            break
        screen.fill((10,10,20))
        pygame.draw.rect(screen, (200,200,200), paddle)
        pygame.draw.ellipse(screen, (255,100,100), ball)
        for b in bricks:
            pygame.draw.rect(screen, (50,150,250), b)
        txt = font.render(f"Score: {score}", True, (240,240,240))
        screen.blit(txt, (6,6))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def run_runner2d_game(exit_requested):
    pygame = ensure_pygame()
    pygame.init()
    W,H = 700,300
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption("Runner 2D")
    clock = pygame.time.Clock()
    player = pygame.Rect(80, H-60, 40, 40)
    obstacles = []
    speed = 6; spawn_timer=0; score=0
    font = pygame.font.SysFont(None, 28)
    player_vel_y = 0
    gravity = 0.6
    jump_strength = -12
    while not exit_requested["flag"]:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player.y >= H-60:
            player_vel_y = jump_strength
        player_vel_y += gravity
        player.y += player_vel_y
        if player.y > H-60:
            player.y = H-60
            player_vel_y = 0
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_timer = 0
            obstacles.append(pygame.Rect(W, H-60, 30, 40))
        for ob in obstacles[:]:
            ob.x -= speed
            if ob.colliderect(player):
                txt = font.render(f"Game Over! Score: {score}  Press ESC", True, (255,255,255))
                screen.fill((0,0,0)); screen.blit(txt,(20,H//2)); pygame.display.flip()
                waiting=True
                while waiting and not exit_requested["flag"]:
                    for ev in pygame.event.get():
                        if ev.type==pygame.QUIT:
                            pygame.quit(); sys.exit()
                        if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE:
                            pygame.quit(); sys.exit()
                    pygame.time.wait(50)
                return
            if ob.right < 0:
                obstacles.remove(ob); score+=1
        screen.fill((120,180,250))
        pygame.draw.rect(screen,(100,200,100),(0,H-20,W,20))
        pygame.draw.rect(screen,(200,50,50),player)
        for ob in obstacles:
            pygame.draw.rect(screen,(60,60,60),ob)
        txt = font.render(f"Score: {score}", True, (10,10,10))
        screen.blit(txt,(10,10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def run_ball2d_game(exit_requested):
    pygame = ensure_pygame()
    pygame.init()
    W,H = 640,480
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption("Ball2D")
    clock = pygame.time.Clock()
    ball = pygame.Rect(W//2-12, H//2-12, 24,24)
    vel = [4,3]
    while not exit_requested["flag"]:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        ball.x += vel[0]; ball.y += vel[1]
        if ball.left<=0 or ball.right>=W: vel[0] = -vel[0]
        if ball.top<=0 or ball.bottom>=H: vel[1] = -vel[1]
        screen.fill((30,30,30))
        pygame.draw.ellipse(screen,(200,200,100),ball)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

# URSINA GAMES (3D)
# Ursina scenes: each function uses the wrapper and passes an exit_requested flag

def ursina_minecraft_game(exit_requested):
    ursina = ensure_ursina()
    from ursina import Ursina, Entity, color, window, Sky
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    window.title = "Minecraft-ish (Ursina)"
    Sky()
    for x in range(-10, 11):
        for z in range(-10, 11):
            Entity(model='cube', texture='white_cube',
                   color=color.rgb(60, 180, 60) if (x+z) % 2 == 0 else color.rgb(80, 160, 50),
                   position=(x, -1, z), scale=(1,1,1))
    for i in range(6):
        Entity(model='cube', texture='white_cube', color=color.rgb(120,120,120), position=(i*3-6, 0, 4), scale=(1,1,1))
    player = FirstPersonController()
    player.gravity = 2
    # Ursina has its own loop: we cannot poll exit_requested easily. Use on_destroy to handle external kill.
    app.run()

def ursina_parkour_game(exit_requested):
    ursina = ensure_ursina()
    from ursina import Ursina, Entity, color, window, Sky
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    window.title = "Parkour 3D"
    Sky()
    for i in range(16):
        Entity(model='cube', color=color.azure, scale=(2,0.4,2), position=(i*3, i*0.9, 0))
    pc = FirstPersonController()
    pc.gravity = 2.5
    pc.jump_height = 1.4
    app.run()

def ursina_flycam_game(exit_requested):
    ursina = ensure_ursina()
    from ursina import Ursina, Entity, color, Sky
    from ursina.prefabs.editor_camera import EditorCamera
    app = Ursina()
    app.title = "FlyCam - Free Camera"
    Sky()
    for x in range(-6, 7, 2):
        for z in range(-6, 7, 2):
            Entity(model='cube', scale=(1,1,1), position=(x, -1, z), color=color.rgb(50,200,100))
    for i in range(-3,4):
        Entity(model='cube', scale=(0.8,6,0.8), position=(i*3, 2.5, 6), color=color.rgb(200,180,140))
    EditorCamera()
    app.run()

def ursina_runner3d_game(exit_requested):
    ursina = ensure_ursina()
    from ursina import Ursina, Entity, color, Sky
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    app.title = "Runner 3D"
    Sky()
    player = FirstPersonController()
    player.gravity = 2.5
    player.jump_height = 1.2
    for i in range(40):
        Entity(model='cube', scale=(4,0.2,8), position=(i*6, -1, 0), color=color.rgb(100,100,100))
    for n in range(8, 200, 12):
        Entity(model='cube', scale=(1.5,1.5,1.5), position=(n, 0, 0), color=color.red)
    app.run()

def ursina_platformer_game(exit_requested):
    ursina = ensure_ursina()
    from ursina import Ursina, Entity, color, Sky
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    app.title = "Platformer 3D"
    Sky()
    positions = [
        (0,0,0), (4,1.2,2), (8,2.4,-1), (12,3.6,3),
        (16,2.0,0), (20,3.0,-2)
    ]
    for p in positions:
        Entity(model='cube', scale=(3,0.4,3), position=p, color=color.rgb(180,200,255))
    Entity(model='cube', scale=(1,1,1), position=(22,4.0,0), color=color.gold)
    player = FirstPersonController()
    player.gravity = 2.8
    player.jump_height = 1.5
    app.run()

# Dispatcher mapping: map keys to wrapper calls
GAMES = {
    'snake': ('pygame', lambda key, s, t: _game_entry_wrapper(key, s, t, run_snake_game)),
    'pong': ('pygame', lambda key, s, t: _game_entry_wrapper(key, s, t, run_pong_game)),
    'breakout': ('pygame', lambda key, s, t: _game_entry_wrapper(key, s, t, run_breakout_game)),
    'runner2d': ('pygame', lambda key, s, t: _game_entry_wrapper(key, s, t, run_runner2d_game)),
    'ball2d': ('pygame', lambda key, s, t: _game_entry_wrapper(key, s, t, run_ball2d_game)),
    'ursina_minecraft': ('ursina', lambda key, s, t: _game_entry_wrapper(key, s, t, ursina_minecraft_game)),
    'ursina_parkour': ('ursina', lambda key, s, t: _game_entry_wrapper(key, s, t, ursina_parkour_game)),
    'ursina_flycam': ('ursina', lambda key, s, t: _game_entry_wrapper(key, s, t, ursina_flycam_game)),
    'ursina_runner3d': ('ursina', lambda key, s, t: _game_entry_wrapper(key, s, t, ursina_runner3d_game)),
    'ursina_platformer': ('ursina', lambda key, s, t: _game_entry_wrapper(key, s, t, ursina_platformer_game)),
}

def print_available():
    print("Available games:")
    for key, (kind, fn) in GAMES.items():
        print(f"  {key:20s} ({kind})")
    print("\nUsage examples:")
    print("  python games_all.py --gui")
    print("  python games_all.py snake --title \"Snake\" --status-file ./.games_status/snake.status")

def run_game_cli(key: str, status_file: str = None, title: str = None):
    key = key.strip().lower()
    if key not in GAMES:
        print(f"Unknown game: {key}")
        print_available()
        sys.exit(2)
    kind, wrapper = GAMES[key]
    if kind == 'pygame' and not has_pygame():
        print("Missing dependency: pygame. Install with: pip install pygame")
        sys.exit(3)
    if kind == 'ursina' and not has_ursina():
        print("Missing dependency: ursina. Install with: pip install ursina")
        sys.exit(4)
    status_path = Path(status_file) if status_file else default_status_path(key)
    # call wrapper which runs the game (blocks)
    wrapper(key, status_path, title)

# GUI Launcher (PyQt6, QMdiArea)

def run_gui_launcher():
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QWidget,
            QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QToolBar, QAction,
            QMessageBox, QFileDialog
        )
        from PyQt6.QtCore import Qt, QTimer
    except Exception as e:
        print("PyQt6 is required for GUI launcher: pip install PyQt6")
        print("Or run games directly via CLI.")
        sys.exit(1)

    class GameSubWindow(QMdiSubWindow):
        def __init__(self, title: str, key: str, parent=None):
            super().__init__(parent)
            self.key = key
            self.setWindowTitle(title or key)
            self.proc = None
            self.status_path = default_status_path(key)
            # widget contents
            w = QWidget()
            lay = QVBoxLayout(w)
            self.lbl_title = QLabel(f"<b>{title or key}</b>")
            self.lbl_status = QLabel("Status: stopped")
            self.lbl_pid = QLabel("PID: —")
            btn_row = QHBoxLayout()
            self.btn_start = QPushButton("Start")
            self.btn_stop = QPushButton("Stop")
            self.btn_restart = QPushButton("Restart")
            self.btn_open_log = QPushButton("Open Status")
            btn_row.addWidget(self.btn_start); btn_row.addWidget(self.btn_stop); btn_row.addWidget(self.btn_restart); btn_row.addWidget(self.btn_open_log)
            lay.addWidget(self.lbl_title)
            lay.addWidget(self.lbl_status)
            lay.addWidget(self.lbl_pid)
            lay.addLayout(btn_row)
            self.setWidget(w)

            self.btn_start.clicked.connect(self.start_proc)
            self.btn_stop.clicked.connect(self.stop_proc)
            self.btn_restart.clicked.connect(self.restart_proc)
            self.btn_open_log.clicked.connect(self.open_status_file)

            self.poll_timer = QTimer(self)
            self.poll_timer.setInterval(500)
            self.poll_timer.timeout.connect(self._poll_status)
            self.poll_timer.start()

            self.update_ui_for_stopped()

        def _status_from_file(self):
            try:
                if self.status_path.exists():
                    raw = self.status_path.read_text(encoding="utf-8")
                    return json.loads(raw)
            except Exception:
                return None
            return None

        def _poll_status(self):
            # update UI from status file / proc
            s = self._status_from_file()
            if s:
                st = s.get("status", "unknown")
                pid = s.get("pid", "—")
                self.lbl_status.setText(f"Status: {st}")
                self.lbl_pid.setText(f"PID: {pid}")
                # update buttons
                if st in ("running", "starting"):
                    self.update_ui_for_running()
                elif st in ("exited", "error"):
                    self.update_ui_for_stopped()
            else:
                # if no status file but subprocess handle exists, use that
                if self.proc and self.proc.poll() is None:
                    self.lbl_status.setText("Status: running (no status file)")
                    self.lbl_pid.setText(f"PID: {getattr(self.proc, 'pid', '—')}")
                    self.update_ui_for_running()
                else:
                    self.lbl_status.setText("Status: stopped")
                    self.lbl_pid.setText("PID: —")
                    self.update_ui_for_stopped()

        def update_ui_for_running(self):
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_restart.setEnabled(True)

        def update_ui_for_stopped(self):
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.btn_restart.setEnabled(True)

        def start_proc(self):
            if self.proc and self.proc.poll() is None:
                QMessageBox.information(self, "Info", "Process already running.")
                return
            python = sys.executable
            # Launch this same file as a subprocess with the game key and status-file
            args = [python, str(__file__), self.key, "--title", self.windowTitle(), "--status-file", str(self.status_path)]
            try:
                self.proc = subprocess.Popen(args, cwd=str(ROOT))
                # write initial status immediately
                write_status(self.status_path, {"key": self.key, "title": self.windowTitle(), "pid": self.proc.pid, "status": "launched", "launched_at": time.time()})
                self.lbl_pid.setText(f"PID: {self.proc.pid}")
                self.lbl_status.setText("Status: launched")
                self.update_ui_for_running()
            except Exception as e:
                QMessageBox.critical(self, "Failed to start", f"Could not start {self.key}: {e}")

        def stop_proc(self):
            if not self.proc or self.proc.poll() is not None:
                # attempt to update status file
                write_status(self.status_path, {"key": self.key, "status": "stopped_by_user", "stopped_at": time.time()})
                self.update_ui_for_stopped()
                return
            try:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=1.0)
                except Exception:
                    self.proc.kill()
                write_status(self.status_path, {"key": self.key, "status": "stopped_by_user", "stopped_at": time.time()})
                self.lbl_status.setText("Status: stopped")
                self.update_ui_for_stopped()
            except Exception as e:
                QMessageBox.warning(self, "Stop failed", f"Failed to stop process: {e}")

        def restart_proc(self):
            self.stop_proc()
            # small delay
            time.sleep(0.08)
            self.start_proc()

        def open_status_file(self):
            if self.status_path.exists():
                # open with default text editor dialog to pick file; here we show a simple message box with contents
                try:
                    raw = self.status_path.read_text(encoding="utf-8")
                    QMessageBox.information(self, f"Status: {self.key}", raw)
                except Exception as e:
                    QMessageBox.warning(self, "Open failed", f"Could not read status file: {e}")
            else:
                QMessageBox.information(self, "No status", "No status file available yet.")

        def closeEvent(self, ev):
            # do not auto-kill process on subwindow close; let user control stop
            super().closeEvent(ev)

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Games Launcher (QMdiArea)")
            self.mdi = QMdiArea()
            self.setCentralWidget(self.mdi)
            self.resize(1100, 700)
            self._create_toolbar()

        def _create_toolbar(self):
            tb = QToolBar("Games")
            self.addToolBar(tb)
            # add actions for each game
            for key, (kind, fn) in GAMES.items():
                act = QAction(f"{key} ({kind})", self)
                act.triggered.connect(lambda checked=False, k=key: self.add_game_subwindow(k))
                tb.addAction(act)
            tb.addSeparator()
            refresh_act = QAction("Refresh status dir", self)
            refresh_act.triggered.connect(self.refresh_all)
            tb.addAction(refresh_act)
            btn_open_dir = QAction("Open .games_status folder", self)
            btn_open_dir.triggered.connect(self.open_status_dir)
            tb.addAction(btn_open_dir)

        def add_game_subwindow(self, key):
            # create subwindow and add
            sw = GameSubWindow(key.replace("_", " ").title(), key, parent=self)
            self.mdi.addSubWindow(sw)
            sw.show()

        def refresh_all(self):
            for w in self.mdi.subWindowList():
                try:
                    w._poll_status()
                except Exception:
                    pass

        def open_status_dir(self):
            # open folder in file dialog so user can inspect
            dlg = QFileDialog(self, "Open status directory", str(STATUS_DIR))
            dlg.setFileMode(QFileDialog.FileMode.Directory)
            dlg.exec()

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

# CLI Argument Parsing

def _parse_cli(argv):
    # minimal parser: support --gui, <game_key>, --title, --status-file
    args = {
        "gui": False,
        "key": None,
        "title": None,
        "status_file": None
    }
    it = iter(argv[1:])
    for tok in it:
        if tok in ("--gui", "-g"):
            args["gui"] = True
        elif tok in ("--title",):
            try:
                args["title"] = next(it)
            except StopIteration:
                pass
        elif tok in ("--status-file",):
            try:
                args["status_file"] = next(it)
            except StopIteration:
                pass
        elif tok.startswith("--"):
            # ignore unknown flags
            pass
        else:
            # first non-flag token is the game key (if not gui)
            if args["key"] is None:
                args["key"] = tok
    return args

# Entrypoint

if __name__ == "__main__":
    parsed = _parse_cli(sys.argv)
    if parsed["gui"]:
        run_gui_launcher()
        sys.exit(0)
    if parsed["key"] is None:
        print_available()
        sys.exit(0)

    # invoked as game subprocess: provide status-file and title if present
    # Note: when launcher spawns a game, it will pass --status-file path and --title.
    # Find them in argv too (defensive)
    key = parsed["key"]
    # find explicit --status-file and --title in sys.argv if present
    title = parsed["title"]
    status_file = parsed["status_file"]
    # fallback scanning
    if status_file is None:
        for i, t in enumerate(sys.argv):
            if t == "--status-file" and i+1 < len(sys.argv):
                status_file = sys.argv[i+1]
    if title is None:
        for i, t in enumerate(sys.argv):
            if t == "--title" and i+1 < len(sys.argv):
                title = sys.argv[i+1]

    # launch chosen game
    run_game_cli(key, status_file, title)
