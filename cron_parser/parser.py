import re

TITLE_COL_MAX = 14

class TimePeriod:
    def __init__(self, title, intervals, lower_bound, upper_bound):
        self.title = title
        self.times = set()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        for expr in intervals.split(","):
            self.parse(expr)

    def parse(self, expr):
        if "-" in expr:
            range_to_add = [int(r) for r in expr.split("-")]
            self.add_range_values(*range_to_add)
        elif "/" in expr:
            step = expr.split("/")[1]
            self.add_step_values(int(step))
        elif expr == "*":
            self.add_entire_period()
        else:
            self.add_predefined_value(int(expr))

    def add_step_values(self, step):
        current_step = self.lower_bound
        num_intervals = (self.upper_bound + 1) // step
        for _ in range(num_intervals):
            self.times.add(current_step)
            current_step += step

    def add_range_values(self, range_from, range_to):
        for value in range(range_from, range_to + 1):
            self.times.add(value)

    def add_entire_period(self):
        for value in range(self.lower_bound, self.upper_bound + 1):
            self.times.add(value)

    def add_predefined_value(self, value):
        self.times.add(value)

    def get_title(self):
        title = self.title
        if len(title) > TITLE_COL_MAX:
            return title[:TITLE_COL_MAX]
        else:
            i = 0
            for i in range(TITLE_COL_MAX - len(title)):
                title += " "
        return title

    def __str__(self):
        sorted_times = list(self.times)
        sorted_times.sort()
        title = self.get_title()
        return title + " ".join([str(element) for element in sorted_times])

def validate_command(command_str):
    """
    Validates a CRON entry (* * * * * /bin/command)
    and returns its parsed components
    """
    regex = r"^(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)\s(.+)$"
    m = re.match(regex, command_str)
    if m:
        minute  = TimePeriod(title='minute', intervals=m.group(1), lower_bound=0, upper_bound=59)
        hour    = TimePeriod(title='hour', intervals=m.group(2), lower_bound=0, upper_bound=23)
        day     = TimePeriod(title='day of month', intervals=m.group(3), lower_bound=1, upper_bound=31)
        month   = TimePeriod(title='month', intervals=m.group(4), lower_bound=1, upper_bound=12)
        weekday = TimePeriod(title='day of week', intervals=m.group(5), lower_bound=0, upper_bound=6)
        command = m.group(6)
        return minute, hour, day, month, weekday, command

def main(args):
    args_without_filename = args[1:]
    cron_command = args_without_filename[0]

    minute, hour, day, month, weekday, command = validate_command(cron_command)
    print(minute)
    print(hour)
    print(day)
    print(month)
    print(weekday)
    print(command)
