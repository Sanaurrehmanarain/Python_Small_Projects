"""
Minesweeper (Tkinter)
---------------------
A classic Minesweeper implementation with:
- Beginner/Intermediate/Expert/Custom difficulties
- First-click safety (no mine on first click and its neighbors)
- Left-click reveal, Right-click flag, Double-left-click to chord
- Timer, mine counter, reset (smiley) button
- Auto-expansion (flood fill) for zero-adjacent cells

Run:
    python minesweeper_tk.py

Tested with Python 3.10+ and the built-in tkinter module.
"""

import random
import time
import tkinter as tk
from tkinter import messagebox

NUMBER_COLORS = {
    1: '#1976D2',  # blue
    2: '#388E3C',  # green
    3: '#D32F2F',  # red
    4: '#512DA8',  # deep purple
    5: '#7B1FA2',  # purple
    6: '#00838F',  # teal
    7: '#212121',  # nearly black
    8: '#616161',  # gray
}

DIFFICULTIES = {
    'Beginner': (9, 9, 10),
    'Intermediate': (16, 16, 40),
    'Expert': (16, 30, 99),
}

class Cell:
    __slots__ = ('row','col','is_mine','is_revealed','is_flagged','adjacent','btn')
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent = 0
        self.btn: tk.Button | None = None

class MinesweeperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Minesweeper (Tkinter)')
        self.resizable(False, False)

        # Game state
        self.rows = 9
        self.cols = 9
        self.mines = 10
        self.grid: list[list[Cell]] = []
        self.first_click_done = False
        self.flags_placed = 0
        self.cells_revealed = 0
        self.game_over = False

        # Timer state
        self.start_time: float | None = None
        self.timer_running = False
        self.timer_job = None

        # UI setup
        self._build_menu()
        self._build_topbar()
        self._build_board()
        self.new_game(self.rows, self.cols, self.mines)

    # ---------------------- UI ----------------------
    def _build_menu(self):
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)
        for name in DIFFICULTIES:
            game_menu.add_command(label=name, command=lambda n=name: self.set_difficulty(n))
        game_menu.add_separator()
        game_menu.add_command(label='Custom…', command=self.custom_dialog)
        game_menu.add_separator()
        game_menu.add_command(label='New Game', command=lambda: self.new_game(self.rows, self.cols, self.mines))
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label='Game', menu=game_menu)
        self.config(menu=menubar)

    def _build_topbar(self):
        self.top = tk.Frame(self, padx=8, pady=6)
        self.top.grid(row=0, column=0, sticky='ew')

        self.mine_var = tk.StringVar(value='Mines: 010')
        self.timer_var = tk.StringVar(value='Time: 000')

        self.mine_lbl = tk.Label(self.top, textvariable=self.mine_var, width=10, anchor='w', font=('Segoe UI', 11, 'bold'))
        self.mine_lbl.pack(side='left')

        self.reset_btn = tk.Button(self.top, text='🙂', width=3, command=lambda: self.new_game(self.rows, self.cols, self.mines), font=('Segoe UI Emoji', 12))
        self.reset_btn.pack(side='left', padx=10)

        self.timer_lbl = tk.Label(self.top, textvariable=self.timer_var, width=10, anchor='e', font=('Segoe UI', 11, 'bold'))
        self.timer_lbl.pack(side='right')

    def _build_board(self):
        self.board_frame = tk.Frame(self, padx=6, pady=6, bg='#BDBDBD')
        self.board_frame.grid(row=1, column=0)

    # ---------------------- Game Logic ----------------------
    def set_difficulty(self, name: str):
        r, c, m = DIFFICULTIES[name]
        self.new_game(r, c, m)

    def custom_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('Custom Game')
        dlg.transient(self)
        dlg.resizable(False, False)
        tk.Label(dlg, text='Rows (max 30):').grid(row=0, column=0, sticky='e', padx=6, pady=4)
        tk.Label(dlg, text='Columns (max 40):').grid(row=1, column=0, sticky='e', padx=6, pady=4)
        tk.Label(dlg, text='Mines:').grid(row=2, column=0, sticky='e', padx=6, pady=4)
        er = tk.Entry(dlg, width=8)
        ec = tk.Entry(dlg, width=8)
        em = tk.Entry(dlg, width=8)
        er.grid(row=0, column=1, padx=6, pady=4)
        ec.grid(row=1, column=1, padx=6, pady=4)
        em.grid(row=2, column=1, padx=6, pady=4)
        er.insert(0, str(self.rows))
        ec.insert(0, str(self.cols))
        em.insert(0, str(self.mines))

        def ok():
            try:
                r = max(2, min(30, int(er.get())))
                c = max(2, min(40, int(ec.get())))
                max_m = r * c - 9  # leave space for first-click safety area
                m = int(em.get())
                if m < 1:
                    m = 1
                if m > max_m:
                    m = max_m
            except ValueError:
                messagebox.showerror('Invalid input', 'Please enter integers for rows, columns, and mines.')
                return
            self.new_game(r, c, m)
            dlg.destroy()

        btnf = tk.Frame(dlg)
        btnf.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btnf, text='OK', width=8, command=ok).pack(side='left', padx=6)
        tk.Button(btnf, text='Cancel', width=8, command=dlg.destroy).pack(side='left', padx=6)
        dlg.grab_set()
        dlg.wait_window()

    def new_game(self, rows: int, cols: int, mines: int):
        # Reset timer
        self._stop_timer()
        self.timer_var.set('Time: 000')
        self.reset_btn.config(text='🙂')

        # Save size and mines
        self.rows, self.cols, self.mines = rows, cols, mines
        self.first_click_done = False
        self.flags_placed = 0
        self.cells_revealed = 0
        self.game_over = False

        # Clear old board widgets
        for w in self.board_frame.winfo_children():
            w.destroy()

        # Model grid
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

        # Build buttons
        for r in range(rows):
            for c in range(cols):
                cell = self.grid[r][c]
                btn = tk.Button(self.board_frame, width=2, height=1, text=' ', relief='raised',
                                font=('Segoe UI', 11, 'bold'), bg='#E0E0E0',
                                command=lambda rr=r, cc=c: self.on_left_click(rr, cc))
                btn.grid(row=r, column=c, sticky='nsew')
                btn.bind('<Button-3>', lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                btn.bind('<Double-Button-1>', lambda e, rr=r, cc=c: self.on_chord(rr, cc))
                cell.btn = btn

        # Update mine counter
        self._update_mine_counter()

        # Resize window to fit content
        self.update_idletasks()
        total_w = self.board_frame.winfo_reqwidth() + 20
        total_h = self.board_frame.winfo_reqheight() + self.top.winfo_reqheight() + 40
        self.geometry(f'{total_w}x{total_h}')

    # ---------------------- Helpers ----------------------
    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def place_mines(self, safe_r, safe_c):
        # Avoid placing mines on first-click cell and its neighbors
        forbidden = {(safe_r, safe_c)} | set(self.neighbors(safe_r, safe_c))
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in forbidden]
        mine_cells = set(random.sample(all_cells, k=self.mines))
        for (r, c) in mine_cells:
            self.grid[r][c].is_mine = True
        # Compute adjacency counts
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.adjacent = -1
                else:
                    cell.adjacent = sum(1 for nr, nc in self.neighbors(r, c) if self.grid[nr][nc].is_mine)

    def _start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self._tick()

    def _stop_timer(self):
        self.timer_running = False
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def _tick(self):
        if not self.timer_running or self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_var.set(f'Time: {elapsed:03d}')
        self.timer_job = self.after(1000, self._tick)

    def _update_mine_counter(self):
        remaining = max(0, self.mines - self.flags_placed)
        self.mine_var.set(f'Mines: {remaining:03d}')

    def _reveal_button_style(self, cell: Cell):
        btn = cell.btn
        btn.config(relief='sunken', bg='#CFCFCF')
        if cell.is_mine:
            btn.config(text='💣', disabledforeground='#D32F2F', fg='#D32F2F')
        else:
            n = cell.adjacent
            if n > 0:
                color = NUMBER_COLORS.get(n, '#000000')
                btn.config(text=str(n), fg=color)
            else:
                btn.config(text='')

    # ---------------------- Interaction ----------------------
    def on_left_click(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.is_flagged or cell.is_revealed:
            return

        if not self.first_click_done:
            self.place_mines(r, c)
            self.first_click_done = True
            self._start_timer()
            self.reset_btn.config(text='😮')

        self.reveal_cell(r, c)

    def on_right_click(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged
        if cell.is_flagged:
            cell.btn.config(text='🚩', fg='#D32F2F')
            self.flags_placed += 1
        else:
            cell.btn.config(text=' ')
            self.flags_placed -= 1
        self._update_mine_counter()

    def on_chord(self, r, c):
        if self.game_over or not self.first_click_done:
            return
        cell = self.grid[r][c]
        if not cell.is_revealed:
            return
        # If number cell and flagged neighbors == number, reveal others
        if cell.adjacent > 0:
            flags = sum(1 for nr, nc in self.neighbors(r, c) if self.grid[nr][nc].is_flagged)
            if flags == cell.adjacent:
                to_reveal = [(nr, nc) for nr, nc in self.neighbors(r, c) if not self.grid[nr][nc].is_flagged and not self.grid[nr][nc].is_revealed]
                for (nr, nc) in to_reveal:
                    self.reveal_cell(nr, nc)

    def reveal_cell(self, r, c):
        cell = self.grid[r][c]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        self._reveal_button_style(cell)
        self.cells_revealed += 1

        if cell.is_mine:
            self.game_lost(r, c)
            return

        # Auto-expand zeros via flood fill
        if cell.adjacent == 0:
            self._flood_reveal(r, c)

        self.check_win()

    def _flood_reveal(self, r, c):
        stack = [(r, c)]
        visited = set()
        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            for nr, nc in self.neighbors(cr, cc):
                ncell = self.grid[nr][nc]
                if ncell.is_revealed or ncell.is_flagged:
                    continue
                ncell.is_revealed = True
                self._reveal_button_style(ncell)
                self.cells_revealed += 1
                if not ncell.is_mine and ncell.adjacent == 0:
                    stack.append((nr, nc))

    def game_lost(self, hit_r, hit_c):
        self.game_over = True
        self._stop_timer()
        self.reset_btn.config(text='😵')
        # Reveal all mines
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.btn.config(text='💣', fg='#D32F2F')
                cell.btn.config(state='disabled')
        # Mark the mine that was hit
        self.grid[hit_r][hit_c].btn.config(bg='#FFCDD2')

    def check_win(self):
        total_cells = self.rows * self.cols
        non_mine_cells = total_cells - self.mines
        if self.cells_revealed >= non_mine_cells and not self.game_over:
            self.game_over = True
            self._stop_timer()
            self.reset_btn.config(text='😎')
            # Disable all buttons and show flags on remaining mines (optional)
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell.is_mine and not cell.is_flagged:
                        cell.btn.config(text='🚩', fg='#388E3C')
                    cell.btn.config(state='disabled')


def main():
    app = MinesweeperApp()
    app.mainloop()


if __name__ == '__main__':
    main()
