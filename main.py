from texlib import wrap


def add_closing_penalty (L, configs):
    "Add the standard penalty for the end of a paragraph"
    if configs['style'] == 'centered':
        L.append( wrap.Glue(0, 18, 0) ) 
    L.append( wrap.Penalty(0, -wrap.INFINITY, 0) )

def show_box_glue_penalty(L, normalForm=False):  
    i = 0 
    while i < len(L):
        obj = L[i]
        if obj.is_box():
            if normalForm:
                i = _addUpNearBoxes(i, L, obj.width)
            else:
                print i, ".", "B(", obj.width, ")" 
                i+=1
        elif obj.is_glue():
            print i, ".", "G(", obj.width, ",", obj.stretch, ",", obj.shrink, ")"
            i+=1
        elif obj.is_penalty():
            print i, ".", "P(", obj.width, ",", obj.penalty, ",", obj.flagged, ")" 
            i+=1

def _addUpNearBoxes(i, L, acc):
    while i < len(L):
        i += 1
        obj = L[i]
        if obj.is_box():
            return _addUpNearBoxes(i, L, acc+obj.width)
        else:
            print "B(", acc, ")" 
            return i


def isPunctuation(ch):
    return ch in {"!","\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\",
    "]", "^", "_", "\\", "|"}

def assemble_paragraph(text, configs):
        """Turn a paragraph of text into an ObjectList.

        '@' indicates a forced line break.
        '$' indicates a forced non line break.
        """
        # Normalize the text
        text = ' '.join(text.split())
        L = wrap.ObjectList()
        L.debug=1
        if configs['identation'] != None or configs['style'] == 'centered':
            if configs['identation']:
                b = wrap.Box(configs['identation'], ' ')
            else:
                b = wrap.Glue(0, 18, 0)
            L.append( b )
        for ch in text:
            if ch in ' \n': 
                # Append interword space
                if configs['style'] == "ragged_right":
                    L.append( wrap.Glue(0, 18, 0) )
                    L.append( wrap.Penalty(0, 0) ) 
                    L.append( wrap.Glue(6, -18, 0) )
                elif configs['style'] == "centered":
                    L.append( wrap.Glue(0, 18, 0) )
                    L.append( wrap.Penalty(0, 0) ) 
                    L.append( wrap.Glue(6, -36, 0) )
                    L.append( wrap.Box(0, ch) )
                    L.append( wrap.Penalty(0, wrap.INFINITY) ) 
                    L.append( wrap.Glue(0, 18, 0) )
                else:
                    L.append( wrap.Glue(configs['glueWidth'],configs['glueStrechability'],configs['glueShrinkability']) )
            elif ch == '@':
                # Append forced break
                L.append( wrap.Penalty(0, -wrap.INFINITY) )
            elif ch == '$':
                # Append forced break
                L.append( wrap.Penalty(0, wrap.INFINITY) )    
            else:
                # Append characters
                if ch == '-':
                    if configs['style'] == "ragged_right":
                        L.append( wrap.Penalty(0, wrap.INFINITY ) ) 
                        L.append( wrap.Glue(0, 18, 0) )
                        L.append( wrap.Penalty(6, 500, 1 ) ) 
                        L.append( wrap.Glue(0 , -18, 0) )
                    else:
                        b = wrap.Box(configs["punctuationChar"], ch)
                elif configs["punctuationChar"] != None and isPunctuation(ch):
                    b = wrap.Box(configs["punctuationChar"], ch)
                elif ch.isdigit():
                    b = wrap.Box(configs["digitChar"], ch)
                elif ch.islower():
                    b = wrap.Box(configs["lowerCaseChar"], ch)
                else:
                    b = wrap.Box(configs["upperCaseChar"], ch)
                L.append( b )

        # Append closing penalty and glue
        add_closing_penalty(L, configs)
        return L


if __name__ == '__main__':
    text = """Assume a table with 100$ 000 records where each record has 68 bytes."""
    configs={
        "lowerCaseChar": 4,
        "upperCaseChar": 5,
        "punctuationChar": 2,
        "digitChar": 4,
        "glueWidth": 3,
        "glueStrechability": 4,
        "glueShrinkability": 3,
        "identation": 10,
        "lineWidth": 95,
        "style": None #ragged_right, #centered
    }
    L = assemble_paragraph(text, configs)
    show_box_glue_penalty(L)
    line_lengths = [configs['lineWidth']]
    breaks = L.compute_breakpoints(line_lengths)
    feasible_breaks = L.get_feasible_breakpoints()
    print "Optimal breakpoints:", breaks
    print "Feasible breakpoints:", feasible_breaks
