import curses

def addstr_mid(window, string, height=0, color_pair=0):
    win_height, win_width = window.getmaxyx()
    window.addstr(height, win_width//2 - len(string)//2, string, curses.color_pair(color_pair))

def color(string):
    string = string.lower()
    if string=="red":
        return 1
    elif string=="green":
        return 2
    elif string=="yellow":
        return 3
    elif string=="blue":
        return 4
    elif string=="magenta":
        return 5
    elif string=="cyan":
        return 6
    elif string=='white':
        return 0
    
def format_frequency(frequency):
    prefixes = ['', 'K', 'M', 'G'] 
    magnitude = 0
    while frequency >= 1000:
        frequency /= 1000
        magnitude += 1
    formatted_frequency = "{:.0f}{}".format(frequency, prefixes[magnitude] + 'Hz')
    return formatted_frequency

def parity(num):
    return num&0x01^num&0x02^num&0x04^num&0x08^num&0x10^num&0x20^num&0x40^num&0x80