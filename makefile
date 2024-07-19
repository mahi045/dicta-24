PAPERNAME=main
TEXFILES =  *.tex *.bib *.sty

all:
	pdflatex $(PAPERNAME)
	bibtex $(PAPERNAME)
	pdflatex $(PAPERNAME)
	pdflatex $(PAPERNAME)
	rm -f *.ps $(PAPERNAME).dvi *.aux *.log *.bbl *.blg  *~ *.ilg *.idx *.out *.in *.gz

clean:
	rm -f *.ps $(PAPERNAME).pdf *.dvi *.aux *.log *.bbl  *.blg  *~ *.ilg *.idx *.out *.in *.gz
