import re

TITLE_COL_MAX = 14


class Printable:
    def __init__(self, title, contents=""):
        self.title = title
        self.contents = contents

    def get_title(self):
        title = self.title
        if len(title) > TITLE_COL_MAX:
            return title[:TITLE_COL_MAX]
        else:
            i = 0
            for i in range(TITLE_COL_MAX - len(title)):
                title += " "
        return title

    def get_contents(self):
        return self.contents

    def __str__(self):
        return self.get_title() + self.contents


class TimePeriod(Printable):
    def __init__(self, title, intervals, lower_bound, upper_bound):
        super().__init__(title)
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
        if step <= 0:
            raise ValueError(f"Invalid step value: {step}. Minimum possible value is: 1")
        current_step = self.lower_bound
        num_intervals = (self.upper_bound + 1) // step
        for _ in range(num_intervals):
            self.times.add(current_step)
            current_step += step

    def add_range_values(self, range_from, range_to):
        if range_from < self.lower_bound:
            raise ValueError(f"Invalid lower bound value: {range_from}. Minimum possible value is: {self.lower_bound}")
        if range_to > self.upper_bound:
            raise ValueError(f"Invalid upper bound value: {range_to}. Maximum possible value is: {self.upper_bound}")
        for value in range(range_from, range_to + 1):
            self.times.add(value)

    def add_entire_period(self):
        for value in range(self.lower_bound, self.upper_bound + 1):
            self.times.add(value)

    def add_predefined_value(self, value):
        if value < self.lower_bound or value > self.upper_bound:
            raise ValueError(f"Value out of range: {value}. Allowed range: [{self.lower_bound}, {self.upper_bound}]")
        self.times.add(value)

    def get_contents(self):
        sorted_times = list(self.times)
        sorted_times.sort()
        return sorted_times

    def __str__(self):
        sorted_times = list(self.times)
        sorted_times.sort()
        title = self.get_title()
        return title + " ".join([str(element) for element in sorted_times])


def validate_command(command_str):
    """
    Validates a CRON entry (* * * * * /bin/command)
    and returns its components TimePeriod and Printable objects
    """
    regex = r"^\s*(\S+?)\s+(\S+?)\s+(\S+?)\s+(\S+?)\s+(\S+?)\s+(?=\S)(.+)$"
    m = re.match(regex, command_str)
    if m:
        minute  = TimePeriod(title='minute', intervals=m.group(1), lower_bound=0, upper_bound=59)
        hour    = TimePeriod(title='hour', intervals=m.group(2), lower_bound=0, upper_bound=23)
        day     = TimePeriod(title='day of month', intervals=m.group(3), lower_bound=1, upper_bound=31)
        month   = TimePeriod(title='month', intervals=m.group(4), lower_bound=1, upper_bound=12)
        weekday = TimePeriod(title='day of week', intervals=m.group(5), lower_bound=0, upper_bound=6)
        command = Printable(title='command', contents=m.group(6))
        return minute, hour, day, month, weekday, command
    else:
        raise ValueError("Invalid crontab entry")


def print_usage():
    print('Usage: cron_parser "minutes hours days months weekdays /command/to/run"')
    print('Example: cron_parser "*/5 0 1,15 * 1-6 /bin/bash /path/to/script.sh"')


def main(args):
    args_without_filename = args[1:]
    if not args_without_filename:
        print_usage()
        exit(1)
    cron_command = args_without_filename[0]

    try:
        minute, hour, day, month, weekday, command = validate_command(cron_command)
        print(minute)
        print(hour)
        print(day)
        print(month)
        print(weekday)
        print(command)
    except ValueError as e:
        print(e)
        print_usage()
        exit(1)
