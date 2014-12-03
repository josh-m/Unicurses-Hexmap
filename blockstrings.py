

def convert(str):
    idx = 0
    str = str.upper()
    block = ['','','','','']
    
    for i in range(len(str)):
        ch = str[i]
        if (ch == ' '):
            block[0] += "    "
            block[1] += "    "
            block[2] += "    "
            block[3] += "    "
            block[4] += "    "
        elif (ch == 'A'):
            block[0] += " ___ "
            block[1] += "|   |"
            block[2] += "|___|"
            block[3] += "|   |"
            block[4] += "|   |"
        elif (ch == 'B'):
            block[0] += " ___ "
            block[1] += "|   \\"
            block[2] += "|___/"
            block[3] += "|   \\"
            block[4] += "|___/"
        elif (ch == 'C'):
            block[0] += " ____"
            block[1] += "|    "
            block[2] += "|    "
            block[3] += "|    "
            block[4] += "|____"
        elif (ch == 'D'):
            block[0] += " __  "
            block[1] += "|  \ "
            block[2] += "|   \\"
            block[3] += "|   /"
            block[4] += "|__/ "
        elif (ch == 'E'):
            block[0] += " ____"
            block[1] += "|    "
            block[2] += "|__  "
            block[3] += "|    "
            block[4] += "|____"
        elif (ch == 'F'):
            block[0] += " ____"
            block[1] += "|    "
            block[2] += "|__  "
            block[3] += "|    "
            block[4] += "|    "
        elif (ch == 'G'):
            block[0] += " ____"
            block[1] += "|    "
            block[2] += "|  __"
            block[3] += "|   |"
            block[4] += "|___|"
        elif (ch == 'H'):
            block[0] += "     "
            block[1] += "|   |"
            block[2] += "|___|"
            block[3] += "|   |"
            block[4] += "|   |"
        elif (ch == 'I'):
            block[0] += "_____"
            block[1] += "  |  "
            block[2] += "  |  "
            block[3] += "  |  "
            block[4] += "_____"
        elif (ch == 'J'):
            block[0] += " ____"
            block[1] += "   | "
            block[2] += "   | "
            block[3] += "   | "
            block[4] += "|__| "
        elif (ch == 'K'):
            block[0] += "     "
            block[1] += "|   /"
            block[2] += "|__/ "
            block[3] += "|  \ "
            block[4] += "|   \\"
        elif (ch == 'L'):
            block[0] += "     "
            block[1] += "|    "
            block[2] += "|    "
            block[3] += "|    "
            block[4] += "|____"
        elif (ch == 'M'):
            block[0] += "_   _"
            block[1] += "|\ /|"
            block[2] += "| V |"
            block[3] += "|   |"
            block[4] += "|   |"
        elif (ch == 'N'):
            block[0] += "     "
            block[1] += "|\  |"
            block[2] += "| \ |"
            block[3] += "|  \|"
            block[4] += "|   |"
        elif (ch == 'O'):
            block[0] += " ___ "
            block[1] += "|   |"
            block[2] += "|   |"
            block[3] += "|   |" 
            block[4] += "|___|"
        elif (ch == 'P'):
            block[0] += " ___ "
            block[1] += "|   |"
            block[2] += "|___|"
            block[3] += "|    "
            block[4] += "|    "
        elif (ch == 'Q'):
            block[0] += " ___ "
            block[1] += "|   |"
            block[2] += "|   |"
            block[3] += "|  \|"
            block[4] += "|___\\"
        elif (ch == 'R'):
            block[0] += " ___ "
            block[1] += "|   \\"
            block[2] += "|___/"
            block[3] += "|  \ "
            block[4] += "|   \\"
        elif (ch == 'S'):
            block[0] += " ____"
            block[1] += "|    "
            block[2] += "|___ "
            block[3] += "    |"
            block[4] += "____|"
        elif (ch == 'T'):
            block[0] += "_____"
            block[1] += "  |  "
            block[2] += "  |  "
            block[3] += "  |  "
            block[4] += "  |  "
        elif (ch == 'U'):
            block[0] += "_   _"
            block[1] += "|   |"
            block[2] += "|   |"
            block[3] += "|   |"
            block[4] += "|___|"
        elif (ch == 'V'):
            block[0] += "     "
            block[1] += "|   |"
            block[2] += "\   /"
            block[3] += " \ / "
            block[4] += "  V  "
        elif (ch == 'W'):
            block[0] += "     "
            block[1] += "|   |"
            block[2] += "|   |"
            block[3] += "| ^ |"
            block[4] += "|/ \|"
        elif (ch == 'X'):
            block[0] += "     "
            block[1] += "\  / "
            block[2] += " \/  "
            block[3] += " /\  "
            block[4] += "/  \ "
        elif (ch == 'Y'):
            block[0] += " "
            block[1] += "\   |"
            block[2] += " \__|"
            block[3] += "    |"
            block[4] += " ___|"
        elif (ch == 'Z'):
            block[0] += "____ "
            block[1] += "   / "
            block[2] += "  /  "
            block[3] += " /   "
            block[4] += "/___ "         
            
            
            #insert spacing between letters
        if (not i==len(str)-1):
            block[0] += " "
            block[1] += " "
            block[2] += " "
            block[3] += " "
            block[4] += " "    
    return block
    
def printBlock(b_ch):
    for line in b_ch:
        print line