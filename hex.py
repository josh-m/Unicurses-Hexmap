
class StrHexMap():
    def __init__(self, ncols, nrows):
        self.map = self.strHexMap(nrows, ncols)

    def strHexMap(self,width, height):
        map_list = list()
        
        if height < 1 or width < 1:
            return map_list
            
        map_list.append( strTopLine(width) )
        
        for row in range(0, height/2):
            map_list += strEvenRow(width)
            map_list += strOddRow(width)
            
        if height % 2:
            map_list += strLastEvenRow(width)
            
        return map_list

       
#Private methods
def strTopLine(length):
    off = "  "
    line = " / \\"
    str = off + line*length

    return str
   
def strEvenRow(length):
    btm = " / \\"
    mid = "|   "
    off = "  "

    mid_str = off + mid*length + '|'
    btm_str = btm*(length+1)
    
    return (mid_str, btm_str)

def strLastEvenRow(length):
    btm = " \ /"
    mid = "|   "
    off = "  "
    
    mid_str = off + mid*length + '|'
    btm_str = off + btm*length
    
    return (mid_str, btm_str)
    
def strOddRow(length):
    mid = "|   "
    btm = " \ /"
    off = "  "
    
    mid_str = mid*(length+1) + '|'
    btm_str = btm*(length+1)
    return (mid_str, btm_str)
