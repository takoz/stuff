# coding: utf-8
import sys, os, subprocess, re, signal
from time import sleep


BAR_CHAR = '|'
YELLOW_LIMIT = 70
RED_LIMIT = 80
SCALE = 0.4
SHOW_BAR = True
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


clear = lambda: os.system('clear')


def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        return False


has_colours = has_colours(sys.stdout)


def colorise(text, colour=WHITE):
    result = text
    if has_colours:
        result = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    return result


def get_temp():
    temp = 0.0
    sensors_info = subprocess.check_output('sensors')
    searched = re.search('Physical id 0:[ ]*\+(.{4})?', sensors_info)
    if searched:
        temp = float(searched.groups(1)[0])
    return temp


def get_bar(value, max_value):
    percent = (100 * value) / max_value
    green_bar = ''; green_multiplier = 0
    yelow_bar = ''; yellow_multiplier = 0
    red_bar = ''; red_multiplier = 0

    if percent <= YELLOW_LIMIT:
        green_multiplier = percent
    elif percent <= RED_LIMIT:
        green_multiplier = YELLOW_LIMIT
        yellow_multiplier = percent - YELLOW_LIMIT
    else:
        green_multiplier = YELLOW_LIMIT
        yellow_multiplier = RED_LIMIT - YELLOW_LIMIT
        red_multiplier = percent - RED_LIMIT

    green_bar = colorise(BAR_CHAR * int(green_multiplier * SCALE), GREEN)
    yelow_bar = colorise(BAR_CHAR * int(yellow_multiplier * SCALE), YELLOW)
    red_bar = colorise(BAR_CHAR * int(red_multiplier * SCALE), RED)
    return ''.join([green_bar, yelow_bar, red_bar])


def signal_handler(signal, frame):
    clear()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        clear()
        temp = get_temp()
        if float(temp) >= RED_LIMIT:
            colored_temp = colorise('Temperature: {0} °C'.format(temp), RED)
        elif float(temp) >= YELLOW_LIMIT:
            colored_temp = colorise('Temperature: {0} °C'.format(temp), YELLOW)
        else:
            colored_temp = colorise('Temperature: {0} °C'.format(temp), GREEN)
        if SHOW_BAR:
            out_str = '\r{0} {1}'.format(colored_temp, get_bar(temp, 100))
        else:
            out_str = '\r{0}'.format(colored_temp)
        sys.stdout.write(out_str)
        sys.stdout.flush()
        sleep(0.5)

