# Nice functions for good looking debug printouts
def centredTextPrintout(Text, width = 75):
    padding = (width - len(Text)) // 2
    line = "-" * padding + Text + "-" * padding
    print(line)

def dashedSeperator(width = 75, LineEnd = False):
    if LineEnd: print("-" * width + "\n")
    else: print("-" * width)