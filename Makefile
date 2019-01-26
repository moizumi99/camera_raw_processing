SRCS=camera_raw_toc.ipynb camera_raw_chapter_1.ipynb camera_raw_chapter_2.ipynb camera_raw_chapter_3_1.ipynb camera_raw_chapter_3_2.ipynb
MDS=$(SRCS:.ipynb=.md)

camera_raw.pdf: $(MDS)
	pandoc $(MDS) -s -o camera_raw.pdf --latex-engine=xelatex -V CJKmainfont=IPAexMincho --listings -H listings-setup.tex

%.md: %.ipynb
	jupyter nbconvert --to markdown $<
	sed -i 's/https:\/\/github.com\/moizumi99\/camera_raw_processing\/raw\/master\///g' $@

.PHONY: clean
clean:
	rm -f *.pdf
	rm -f $(MDS)
