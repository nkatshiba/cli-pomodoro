import time
import curses
from datetime import timedelta
from pyfiglet import Figlet

DEFAULT_TIME = 35

def display_centered_text(win, text):
    win.clear()
    height, width = win.getmaxyx()
    fig = Figlet(font='big')
    ascii_art_text = fig.renderText(text)
    lines = ascii_art_text.split('\n')
    start_y = (height - len(lines)) // 2
    for i, line in enumerate(lines):
        start_x = (width - len(line)) // 2
        win.addstr(start_y + i, start_x, line)
    win.refresh()

def countdown(pomodoro_length, win):
    end_time = time.time() + pomodoro_length * 60
    try:
        while True:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break
            formatted_time = str(timedelta(seconds=int(remaining_time)))
            display_centered_text(win, formatted_time)
            time.sleep(0.1)
    except KeyboardInterrupt:
        display_centered_text(win, "Pomodoro cancelled.")
        time.sleep(2)
        return
    display_centered_text(win, "Pomodoro complete!")
    time.sleep(2)

def main(stdscr):
    # Turn off cursor visibility
    curses.curs_set(0)
    # Clear the screen
    stdscr.clear()
    # Ask the user for the duration of the Pomodoro session
    stdscr.addstr(f"Enter the duration of the Pomodoro session in minutes (default {DEFAULT_TIME}): ")
    stdscr.refresh()
    # Use curses echo to show input
    curses.echo()
    try:
        pomodoro_duration = int(stdscr.getstr().decode())
    except ValueError:
        pomodoro_duration = DEFAULT_TIME
    # Turn off echo
    curses.noecho()
    countdown(pomodoro_duration, stdscr)

curses.wrapper(main)
