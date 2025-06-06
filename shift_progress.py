import tkinter as tk
from datetime import datetime, time, timedelta

START_HOUR = 9
END_HOUR = 17
NUM_OF_HOURS = END_HOUR - START_HOUR
# UI Scaling
BAR_LENGTH = 500
BAR_HEIGHT = 40
FONT_SIZE = 20

def update_progress():
    now = datetime.now().time()
    total_minutes = NUM_OF_HOURS * 60
    bar_canvas.delete("all")

    if shift_start <= now <= shift_end:
        elapsed = (datetime.combine(datetime.today(), now) -
                   datetime.combine(datetime.today(), shift_start)).seconds // 60
        percentage = (elapsed * 100) // total_minutes

        # Draw progress bar
        fill_length = (percentage / 100) * BAR_LENGTH
        bar_canvas.create_rectangle(0, 0, fill_length, BAR_HEIGHT, fill='green')

        # Time formatting
        hours = elapsed // 60
        minutes = elapsed % 60

        # Milestone calculation
        next_milestone_percent = ((percentage // 10) + 1) * 10
        next_milestone_minutes = (next_milestone_percent / 100) * total_minutes
        minutes_until_milestone = next_milestone_minutes - elapsed
        next_milestone_time = (
            datetime.combine(datetime.today(), shift_start) +
            timedelta(minutes=next_milestone_minutes)
        ).time()

        # Draw milestone marker
        milestone_x = (next_milestone_percent / 100) * BAR_LENGTH
        bar_canvas.create_line(milestone_x, 0, milestone_x, \
        BAR_HEIGHT, fill='black', width=2, dash=(5, 2))

        label.config(text=
            f"{percentage}% done, {100 - percentage}% to go\n"
            f"Next milestone: {next_milestone_percent}% "
            f"in {int(minutes_until_milestone)} minute(s)"
        )
    elif now < shift_start:
        label.config(text="0% done, 100% to go\nShift has not started yet")
    else:
        bar_canvas.create_rectangle(0, 0, BAR_LENGTH, BAR_HEIGHT, fill='green')
        label.config(text="100% done, 0% to go\nShift has ended")

    now_dt = datetime.now()
    next_minute = now_dt.replace(second=0, microsecond=0) + timedelta(minutes=1)
    delay_ms = int((next_minute - now_dt).total_seconds() * 1000) + 10
    root.after(delay_ms, update_progress)

shift_start = time(START_HOUR, 0)
shift_end = time(END_HOUR, 0)

root = tk.Tk()
root.title("Shift Progress")
label = tk.Label(root, font=('Arial', FONT_SIZE))
label.pack(pady=10)

bar_canvas = tk.Canvas(root, width=BAR_LENGTH, height=BAR_HEIGHT, bg='gray')
bar_canvas.pack()

update_progress()
root.mainloop()

