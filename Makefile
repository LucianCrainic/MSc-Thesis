report: src/thesis.tex
	tectonic src/thesis.tex

slides: docs/slides.tex
	tectonic docs/slides.tex

clean:
	rm -f *.pdf *.toc *.out *.log *.aux *.synctex.gz *.auto.dot *.fls *.fdb_latexmk
