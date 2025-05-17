from random import randint

from cmu_graphics import *

# setup
app.background = rgb(220, 220, 240)
app.stepsPerSecond = 400
app.deadly_ovals_top = []
app.deadly_ovals_bottom = []
app.little_ovals_top = []
app.little_ovals_bottom = []
app.all_ovals = []
app.cursor = Circle(400, 400, 1, visible=False)
app.on = False
app.gameOver = False

app.score = 0
app.time = 0
app.difficulty = 1


class Deadly_oval:
    def __init__(self, radius, centerX, centerY, width):
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        self.width = width
        self.fill = get_color()
        self.shape = Oval(self.centerX, self.centerY, self.width, self.radius, fill=self.fill)

    def delete_oval(self):
        self.shape.visible = False
        if self in app.all_ovals:
            app.all_ovals.remove(self)
        if self in app.deadly_ovals_top:
            app.deadly_ovals_top.remove(self)
        if self in app.deadly_ovals_bottom:
            app.deadly_ovals_bottom.remove(self)
        if self in app.little_ovals_top:
            app.little_ovals_top.remove(self)
        if self in app.little_ovals_bottom:
            app.little_ovals_bottom.remove(self)

    def update(self):
        self.shape.centerX += 1 + app.difficulty if app.difficulty < 5 else 5
        if self.shape.left > 400:
            self.delete_oval()


def distance_between(pos1, pos2):
    return abs(abs(pos1) - abs(pos2))


def get_color():
    return rgb(randint(0, 255), randint(0, 255), randint(0, 255))


def onStep():
    if not app.on:
        return

    app.time += 1
    if app.time % 400 == 0:
        app.score += 1

    if app.time % 8000 == 0:
        app.difficulty += 1

    gap = max(15, 30 - app.difficulty)
    START_X = -250
    top_radius = randint(15, 215)
    bottom_radius = 400 - top_radius - gap

    if app.deadly_ovals_top:
        if distance_between(app.deadly_ovals_top[-1].shape.centerX, START_X) > 100:
            top = Deadly_oval(top_radius * 2, START_X, 0, 50)
            app.deadly_ovals_top.append(top)
    else:
        top = Deadly_oval(top_radius * 2, START_X, 0, 50)
        app.deadly_ovals_top.append(top)

    if app.deadly_ovals_bottom:
        if distance_between(app.deadly_ovals_bottom[-1].shape.centerX, START_X) > 100:
            bottom = Deadly_oval(bottom_radius * 2, START_X, 400, 50)
            app.deadly_ovals_bottom.append(bottom)
    else:
        bottom = Deadly_oval(bottom_radius * 2, START_X, 400, 50)
        app.deadly_ovals_bottom.append(bottom)

    if app.time % 5 == 0:
        for ovals in (app.deadly_ovals_top, app.deadly_ovals_bottom,
                      app.little_ovals_top, app.little_ovals_bottom):
            for oval in ovals:
                oval.update()

    if not app.little_ovals_top or app.little_ovals_top[-1].shape.centerX > 0:
        little_top = Deadly_oval(30, -30, 0, 30)
        app.little_ovals_top.append(little_top)

    if not app.little_ovals_bottom or app.little_ovals_bottom[-1].shape.centerX > 0:
        little_bottom = Deadly_oval(30, -30, 400, 30)
        app.little_ovals_bottom.append(little_bottom)

    app.all_ovals = (
            app.deadly_ovals_top + app.deadly_ovals_bottom +
            app.little_ovals_top + app.little_ovals_bottom
    )

    for oval in app.all_ovals:
        if oval.shape.hitsShape(app.cursor):
            gameOver()


def gameOver():
    hide_game()
    app.background = rgb(119, 242, 135)
    app.game_over_text = Label('Game Over!', 200, 175, size=20, bold=True)
    app.score_text = Label(f'Score: {app.score}', 200, 225, size=20, bold=True)
    app.on = False
    app.gameOver = True


def hide_game():
    for oval in app.all_ovals:
        oval.shape.fill = None

def onMouseLeave():
    gameOver()

def onMouseMove(mouseX, mouseY):
    app.cursor.centerX = mouseX
    app.cursor.centerY = mouseY

def onKeyPress(key):
    if app.on:
        return
    if app.gameOver:
        # revert variable values
        app.deadly_ovals_top.clear()
        app.deadly_ovals_bottom.clear()
        app.little_ovals_top.clear()
        app.little_ovals_bottom.clear()
        app.all_ovals.clear()
        app.score = 0
        app.time = 0
        app.difficulty = 1
        app.background = rgb(220, 220, 240)
        app.game_over_text.visible = False
        app.score_text.visible = False
        app.gameOver = False

    app.on = True
    app.title_text.visible = False
    app.info_text.visible = False


app.title_text = Label('DEADLY OVALS', 200, 175, size=20, bold=True)
app.info_text = Label('PRESS ANY KEY TO BEGIN...', 200, 200, size=20, bold=True)

cmu_graphics.run()