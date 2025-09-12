import sys
import os
import subprocess
import time

from PyQt6.QtGui import QIcon


# optional dependency checks
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

# PYGAME GAME IMPLEMENTATIONS (kept inline for subprocess mode)
def ensure_pygame():
    try:
        import pygame
        return pygame
    except Exception:
        raise RuntimeError("pygame is required for this game. Install with: pip install pygame")

def run_snake():
    pygame = ensure_pygame()
    import random
    pygame.init()
    W, H = 640, 480
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    CELL = 20
    dirs = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}

    def game_over(scr, score):
        txt = font.render(f"Game Over! Score: {score}  Press ESC to quit", True, (255, 255, 255))
        scr.fill((0, 0, 0)); scr.blit(txt, (20, H//2-20)); pygame.display.flip()
        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

    head = [W//2//CELL, H//2//CELL]
    snake = [tuple(head)]
    direction = 'RIGHT'
    food = (random.randint(0, (W//CELL)-1), random.randint(0, (H//CELL)-1))
    score = 0
    speed = 8
    while True:
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

def run_pong():
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
    while True:
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

def run_breakout():
    pygame = ensure_pygame()
    pygame.init()
    import random
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
    while True:
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
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
        screen.fill((10,10,20))
        pygame.draw.rect(screen, (200,200,200), paddle)
        pygame.draw.ellipse(screen, (255,100,100), ball)
        for b in bricks:
            pygame.draw.rect(screen, (50,150,250), b)
        txt = font.render(f"Score: {score}", True, (240,240,240))
        screen.blit(txt, (6,6))
        pygame.display.flip()
        clock.tick(60)

# Dispatcher
def run_game_by_name(name: str):
    name = (name or "").strip().lower()
    if name == 'snake': run_snake()
    elif name == 'pong': run_pong()
    elif name == 'breakout': run_breakout()
    else:
        print("Available games: snake, pong, breakout, runner, ball")
        print("Usage: python games_all.py <game>")

# Reusable PyQt6 launcher widget
def _safe_import_pyqt():
    try:
        from PyQt6.QtWidgets import (
            QWidget, QListWidget, QPushButton, QLabel, QTextEdit,
            QHBoxLayout, QVBoxLayout, QMessageBox
        )
        from PyQt6.QtCore import Qt
        return {
            'QWidget': QWidget, 'QListWidget': QListWidget,
            'QPushButton': QPushButton, 'QLabel': QLabel,
            'QTextEdit': QTextEdit, 'QHBoxLayout': QHBoxLayout,
            'QVBoxLayout': QVBoxLayout, 'QMessageBox': QMessageBox,
            'Qt': Qt
        }
    except Exception:
        return None

class GameLauncherWidget:
    def __init__(self):
        self._pyqt = _safe_import_pyqt()
        if self._pyqt is None:
            raise RuntimeError("PyQt6 not available")
        # games list: (Title, key, desc)
        self.games = [
            ("Snake", "snake", "Classic snake in a grid (Pygame)."),
            ("Pong", "pong", "Two-player pong (keyboard)."),
            ("Breakout", "breakout", "Break bricks with a paddle (mouse)."),
        ]
        # process handle
        self.proc = None
        self.current_game = None
        self._widget = None

    def create_widget(self):
        # lazily create the QWidget for embedding
        if self._widget is not None:
            return self._widget

        QWidget = self._pyqt['QWidget']; QListWidget = self._pyqt['QListWidget']
        QPushButton = self._pyqt['QPushButton']; QLabel = self._pyqt['QLabel']
        QTextEdit = self._pyqt['QTextEdit']; QHBoxLayout = self._pyqt['QHBoxLayout']
        QVBoxLayout = self._pyqt['QVBoxLayout']; QMessageBox = self._pyqt['QMessageBox']
        Qt = self._pyqt['Qt']

        w = QWidget()
        layout = QHBoxLayout(w)

        left = QWidget(); left_l = QVBoxLayout(left)
        self.listw = QListWidget()
        for title, key, desc in self.games:
            self.listw.addItem(f"{title} ({key})")
        left_l.addWidget(self.listw)

        btns = QWidget(); btns_l = QHBoxLayout(btns)
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        btns_l.addWidget(self.start_btn); btns_l.addWidget(self.stop_btn)
        left_l.addWidget(btns)

        right = QWidget(); right_l = QVBoxLayout(right)
        self.preview_title = QLabel("Select a game")
        self.preview_desc = QTextEdit(); self.preview_desc.setReadOnly(True)
        right_l.addWidget(self.preview_title); right_l.addWidget(self.preview_desc)

        layout.addWidget(left, 1); layout.addWidget(right, 2)

        # connect signals
        self.listw.currentRowChanged.connect(self.on_select)
        self.start_btn.clicked.connect(self.on_start)
        self.stop_btn.clicked.connect(self.on_stop)
        self.listw.setCurrentRow(0)

        # Save them
        self._widget = w

        # Immediately mark missing deps in list
        for i, (_, key, _) in enumerate(self.games):
            item = self.listw.item(i)
            ok = True
            if key in ('snake', 'pong', 'breakout'):
                ok = has_pygame()
            elif key in ('runner', 'ball'):
                ok = has_ursina()
            if not ok:
                item.setText(item.text() + " — missing dependency")

        return self._widget

    def on_select(self, idx):
        if idx < 0: return
        title, key, desc = self.games[idx]
        self.preview_title.setText(title)
        self.preview_desc.setPlainText(desc)

    def _start_process_for_key(self, key):
        # spawn new python process that runs this file and game key
        python = sys.executable
        args = [python, os.path.abspath(__file__), key]
        try:
            proc = subprocess.Popen(args, cwd=os.path.dirname(os.path.abspath(__file__)))
            return proc
        except Exception as e:
            raise

    def on_start(self):
        idx = self.listw.currentRow()
        if idx < 0: return
        _, key, _ = self.games[idx]
        # dependency checks
        if key in ('snake', 'pong', 'breakout') and not has_pygame():
            self._pyqt['QMessageBox'].warning(self._widget, "Missing dependency", "pygame is not installed.")
            return
        if key in ('runner', 'ball') and not has_ursina():
            self._pyqt['QMessageBox'].warning(self._widget, "Missing dependency", "ursina is not installed.")
            return
        # start subprocess
        try:
            self.proc = self._start_process_for_key(key)
            self.current_game = key
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        except Exception as e:
            self._pyqt['QMessageBox'].critical(self._widget, "Failed to start", f"Could not start {key}: {e}")

    def on_stop(self):
        if self.proc:
            try:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=1.0)
                except Exception:
                    self.proc.kill()
                self.proc = None
                self.current_game = None
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
            except Exception as e:
                self._pyqt['QMessageBox'].warning(self._widget, "Stop failed", f"Failed to stop process: {e}")

    def close(self):
        # ensure termination if embedded and removed
        if getattr(self, 'proc', None):
            try:
                self.proc.terminate()
                time.sleep(0.05)
                if self.proc.poll() is None:
                    self.proc.kill()
            except Exception:
                pass

# GamesApp wrapper for embedding in Luxxer_OS

from PyQt6.QtWidgets import QWidget as _QWidget
class GamesApp(_QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.ico'))
        try:
            launcher = GameLauncherWidget()
            widget = launcher.create_widget()
            # simple layout to host it
            from PyQt6.QtWidgets import QVBoxLayout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0,0,0,0)
            layout.addWidget(widget)
            self._launcher = launcher
        except Exception as e:
            # if PyQt missing, show a message label
            from PyQt6.QtWidgets import QLabel, QVBoxLayout
            layout = QVBoxLayout(self)
            lbl = QLabel("Games launcher unavailable: PyQt6 required.")
            layout.addWidget(lbl)
            self._launcher = None

    def closeEvent(self, ev):
        if getattr(self, "_launcher", None):
            try:
                self._launcher.close()
            except Exception:
                pass
        super().closeEvent(ev)

# Standalone launcher entrypoint
def launcher_main():
    pyqt = _safe_import_pyqt()
    if pyqt is None:
        print("PyQt6 not installed. Install with: pip install PyQt6")
        return
    from PyQt6.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    w = QMainWindow()
    w.setWindowTitle("Games Launcher")
    launcher = GameLauncherWidget()
    widget = launcher.create_widget()
    w.setCentralWidget(widget)
    w.resize(700, 420)
    w.show()
    sys.exit(app.exec())