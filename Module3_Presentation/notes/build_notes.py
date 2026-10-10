import re
from notes_data import NOTES

WPM = 135
def esc(t):
    t = t.replace('\\','\\textbackslash{}')
    for a,b in [('&','\\&'),('%','\\%'),('$','\\$'),('#','\\#'),('_','\\_')]:
        t = t.replace(a,b)
    t = re.sub(r'"([^"]*)"', r"``\1''", t)
    return t

total_words = sum(len(n.split()) for _,n in NOTES)
total_sec = sum(round(len(n.split())/WPM*60) for _,n in NOTES)

out = [r"""\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1.7cm,top=2.2cm,bottom=2cm]{geometry}
\usepackage{graphicx}
\usepackage[table]{xcolor}
\usepackage{tikz}
\usepackage{fancyhdr}
\usepackage[most]{tcolorbox}
\usepackage{microtype}
\definecolor{navy}{RGB}{21,45,99}
\definecolor{ocean}{RGB}{28,97,158}
\definecolor{aqua}{RGB}{0,142,150}
\definecolor{sky}{RGB}{235,243,252}
\definecolor{ink}{RGB}{40,40,50}
\renewcommand{\familydefault}{\sfdefault}
\color{ink}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fhead{}
\fancyhead[L]{\small\color{navy}\textbf{Module 3: Security Goals, Authorization and Access Control} \,\textbar\, Lecture Notes}
\fancyhead[R]{\includegraphics[height=0.75cm]{../au_logo.png}}
\fancyfoot[C]{\small\color{ocean}\thepage}
\setlength{\parindent}{0pt}
\newtcolorbox{slidebox}[3]{enhanced,breakable=false,colback=white,colframe=ocean,boxrule=0.6pt,arc=2mm,
  left=3mm,right=3mm,top=2mm,bottom=2mm,
  title={\textbf{Slide #1}\;\,|\;\,#2\quad\normalfont\small(about #3 seconds)},
  fonttitle=\sffamily\color{white},colbacktitle=navy,attach boxed title to top left={yshift=-2mm,xshift=3mm},
  boxed title style={arc=1.5mm,colback=navy},before skip=5mm,after skip=3mm}
\begin{document}
""".replace("\\fhead{}\n","")]

# cover
out.append(r"""\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[navy] (current page.north west) rectangle ([yshift=-9.5cm]current page.north east);
  \fill[aqua] ([yshift=-9.5cm]current page.north west) rectangle ([yshift=-9.7cm]current page.north east);
  \node[anchor=north east] at ([xshift=-1.5cm,yshift=-1.2cm]current page.north east) {\includegraphics[height=2.4cm]{../au_logo.png}};
  \node[anchor=west,white,font=\large] at ([xshift=1.8cm,yshift=-2.2cm]current page.north west) {NETWORK SECURITY \,\textbar\, MODULE 3};
  \node[anchor=west,white,font=\fontsize{30}{36}\selectfont\bfseries] at ([xshift=1.8cm,yshift=-4.2cm]current page.north west) {Lecture Notes};
  \node[anchor=west,white,font=\Large] at ([xshift=1.8cm,yshift=-5.6cm]current page.north west) {Security Goals, Authorization and Access Control};
  \node[anchor=west,white,font=\normalsize,align=left] at ([xshift=1.8cm,yshift=-7.2cm]current page.north west)
    {Lesson 4: Security and Authorization\\Lesson 7: Multi Level Model of Security};
\end{tikzpicture}
\vspace*{8.6cm}

\begin{tcolorbox}[colback=sky,colframe=ocean,arc=2mm,title=\textbf{How to use these notes},fonttitle=\sffamily]
\begin{itemize}\setlength{\itemsep}{3pt}
  \item There is \textbf{one note for each of the 49 slides}, in the same order as \texttt{module3.pdf}. A small picture of the slide sits beside each note.
  \item The notes are written \textbf{from teacher to students} in \textbf{simple language}: read them aloud as they are, or use them as a guide in your own words.
  \item Each note takes \textbf{at most 2 minutes} to speak (about 140--170 words, roughly 1--1\textonequarter{} minutes) at a steady classroom pace of about """+str(WPM)+r""" words per minute. The estimate for each slide is shown in its title bar.
  \item Phrases such as ``look at the diagram'' tell you when to point at the slide.
\end{itemize}
\end{tcolorbox}

\vspace{4mm}
\begin{center}
\renewcommand{\arraystretch}{1.5}
\begin{tabular}{>{\columncolor{navy}\color{white}\bfseries}l >{\columncolor{sky}}l}
Slides & 49 \\
Total words & """+f"{total_words:,}"+r""" \\
Estimated talking time & about """+str(round(total_sec/60))+r""" minutes (without pauses or questions) \\
Lesson 4 & slides 3--26 \\
Lesson 7 & slides 27--49 \\
\end{tabular}
\end{center}
\newpage
""")

for i,(title,text) in enumerate(NOTES,1):
    sec = round(len(text.split())/WPM*60)
    out.append(r"\begin{slidebox}{%d}{%s}{%d}" % (i, esc(title), sec) + "\n")
    out.append(r"\begin{minipage}[t]{0.40\linewidth}\vspace{0pt}\includegraphics[width=\linewidth,page=%d]{../module3.pdf}\end{minipage}\hfill" % i + "\n")
    out.append(r"\begin{minipage}[t]{0.57\linewidth}\vspace{0pt}\small\linespread{1.1}\selectfont " + esc(text) + r"\end{minipage}" + "\n")
    out.append(r"\end{slidebox}" + "\n")
out.append(r"\end{document}")
open('module3_lecture_notes.tex','w').write("".join(out))
print(total_words, total_sec/60)
