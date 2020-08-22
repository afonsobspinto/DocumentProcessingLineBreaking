from texlib import wrap

def add_closing_penalty (L):
    "Add the standard penalty for the end of a paragraph"
    L.append( wrap.Penalty(0, -wrap.INFINITY, 1) )

def showBoxGluePenalty(objs):  
    i = 0 
    while i < len(objs):
        obj = objs[i]
        if obj.is_box():
            i = _addUpNearBoxes(i, objs, obj.width) 
        elif obj.is_glue():
            print "G(", obj.width, ",", obj.stretch, ",", obj.shrink, ")"
            i+=1
        elif obj.is_penalty():
            print "P(", obj.width, ",", obj.penalty, ",", obj.flagged, ")" 
            i+=1

def _addUpNearBoxes(i, objs, acc):
    while i < len(objs):
        i += 1
        obj = objs[i]
        if obj.is_box():
            return _addUpNearBoxes(i, objs, acc+obj.width)
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
        if configs['identation'] != None:
                b = wrap.Box(configs['identation'], ' ')
                L.append( b )
        for ch in text:
            if ch in ' \n':
                # Append interword space
                L.append( wrap.Glue(configs['glueWidth'],configs['glueStrechability'],configs['glueShrinkability']) )
            elif ch == '@':
                # Append forced break
                L.append( wrap.Penalty(0, -wrap.INFINITY) )
            elif ch == '$':
                # Append forced break
                L.append( wrap.Penalty(0, wrap.INFINITY) )    
            else:
                # Append characters
                if configs["punctuationChar"] != None and isPunctuation(ch):
                    b = wrap.Box(configs["punctuationChar"], ch)
                elif ch.isdigit():
                    b = wrap.Box(configs["digitChar"], ch)
                elif ch.islower():
                    b = wrap.Box(configs["lowerCaseChar"], ch)
                else:
                    b = wrap.Box(configs["upperCaseChar"], ch)
                L.append( b )

        # Append closing penalty and glue
        add_closing_penalty(L)
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
    }
    L = assemble_paragraph(text, configs)
    showBoxGluePenalty(L)
