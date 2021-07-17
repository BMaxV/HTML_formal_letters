import jinja2
import textwrap
import datetime

def DINA(s):
    x,y=841 , 1189
    c=0
    while c < s:
        x,y=y.__floordiv__(2),x
        c+=1
    return round(x,0),round(y,0)

def page(template_filename,x,y,keys,var_dict):
    with open(template_filename,"r") as f:
        t=f.read()
    T=jinja2.Template(t)
    x=str(x)+"mm"
    y=str(y)+"mm"
    html=T.render(x=x,y=y,keys=keys,var_dict=var_dict)
    
    return html
    
def svg(x,y,content=""):
    offset=5
    
    s="""<?xml version="1.0" standalone="no"?> \n"""
    s+="""<?xml-stylesheet href="test.css" type="text/css"?> \n"""
    
    s+="\n"
    s+="""<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n"""
    s+="\n"
    
    s+="""<svg viewBox="0 0 """+str(x)+"""mm +"""+str(y)+"""mm" version="1.1" width='"""+str(x)+"""mm' height='"""+str(y)+"""mm' xmlns="http://www.w3.org/2000/svg">\n"""
    
    s+="<rect x='"+str(offset)
    s+="mm' y='"+str(offset)
    s+="mm' width='"
    s+=str(x-offset*2)+"mm' height='"
    s+=str(y-offset*2)+"mm'  fill='white' stroke='black'/> \n"
    
    s+="\n"
    s+="</svg>\n"
    return s

def test_svg():
    x,y=DINA(4)
    s=svg(x,y,"hello there")
    with open("test_svg.svg","w") as f:
        f.write(s)
        
def make_formal_letter():
    with open("formal_letter_temp_svg.html","r") as f:
        t=f.read()
    T=jinja2.Template(t)
    
    
    lines_from=["Max Mustermann","Musterstraße","12345 Berlin","tel:NNNN NNN NN NN","mmmmm@ddddd.de"]
    lines_from_n=[]
    y=10
    c=0
    for x in lines_from:
        lines_from_n.append((str(y+c*5)+"mm",x))
        c+=1
    lines_from=lines_from_n
    
    lines_to=["Donal Duck","Disneyland","Big Castle"]
    lines_to_n=[]
    y=55
    c=0
    for x in lines_to:
        lines_to_n.append((str(y+c*5)+"mm",x))
        c+=1
    lines_to=lines_to_n
    
    t=["blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb",
        "blubb blubb blubb blubb blubb blubb blubb blubb blubb",
        "blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb",
        "blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb blubb",]
        
    pars=t
    #textwrap it, limit is 19*4 per line
    new_pars=[]
    base_p=130
    for par in pars:
        this=textwrap.wrap(par,19*4)
        thisn=[]
        c=0
        for x in this:
            thisn.append((str(base_p+c*5)+"mm",x))
            c+=1
        new_pars.append(thisn)
        base_p+=c*5+5
    pars=new_pars
    var_dict={
        "lines_from":lines_from,
        "lines_to":lines_to,
        "date":datetime.date.today().isoformat(),
        "Betreff":"Subject",
        "Anrede":"Dear Sirs",
        "pars":pars,
        "Formel":"regards",
        "Name":"Max Mustermann"}
    final=T.render(var_dict=var_dict)
    with open("formal_letter_demo.html","w") as f:
        f.write(final)
    

def make_CV(c=4):
    x,y=DINA(c)
    x=str(x)
    y=str(y)
    var_dict={
                "Education":[
                    "School 1066",
                    "Uni College 1966-1967",
                    "Internship 1999",],
                "Skill1":[
                    "detail1",
                    "detail2",
                    "detail3",
                    "detail4",],
                "Skill2":[
                    "detail1",
                    "detail2",
                    "detail3",
                    "detail4",],
                "Skill3":[
                    "detail1",
                    "detail2",
                    "detail3",
                    "detail4",],
                "email":
                    "email again,",
                "html_title":"title goes here",
                "picture":"./Mona_Lisa_Portrait.jpg",
            }
    
    keys=["Education","Skill1","Skill2","Skill3"]
    
    
    s=page("CV_template.html",x,y,keys,var_dict)
    
    with open("CV_demo.html","w") as f:
        f.write(s)


def tag_wrap(fn):
    with open(fn,"r") as f:
        text=f.read()
    text=text.split("\n")
    new_text=[]
    for el in text:
        new_text.append(el.strip())
    text=new_text
    while "" in text:
        text.remove("")
    
    text="</p>\n<p>".join(text)
    with open("tagged"+fn,"w") as f:
        f.write(text)
    
if __name__=="__main__":
    make_formal_letter()
    make_CV()
    test_svg()
