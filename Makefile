.PHONY: thesis slides notes analysis analysis-overview clean

thesis:
	tectonic thesis/thesis.tex

slides:
	tectonic slides/slides.tex

notes:
	cd docs/notes && tectonic --keep-logs --keep-intermediates --reruns 1 notes.tex

analysis:
	cd analysis && tectonic --keep-logs --keep-intermediates --reruns 1 analysis.tex

analysis-overview:
	cd analysis/overview && tectonic --keep-logs --keep-intermediates --reruns 1 overview.tex

clean:
	rm -f */*.pdf */*.toc */*.out */*.log */*.aux */*.synctex.gz */*.auto.dot */*.fls */*.fdb_latexmk
