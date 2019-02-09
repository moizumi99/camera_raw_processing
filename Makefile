SRCS=camera_raw_toc.ipynb camera_raw_chapter_1.ipynb camera_raw_chapter_2.ipynb camera_raw_chapter_3_1.ipynb camera_raw_chapter_3_2.ipynb camera_raw_chapter_3_3.ipynb camera_raw_chapter_3_4.ipynb camera_raw_chapter_3_5.ipynb camera_raw_chapter_4.ipynb camera_raw_chapter_4_2.ipynb camera_raw_chapter_4_3.ipynb camera_raw_chapter_4_4.ipynb camera_raw_chapter_4_5.ipynb camera_raw_chapter_5.ipynb camera_raw_chapter_5_2.ipynb camera_raw_chapter_5_3.ipynb camera_raw_chapter_5_4.ipynb
MDS=$(SRCS:.ipynb=.md)

camera_raw.pdf: camera_raw.md
	pandoc $< -s -o camera_raw.pdf --latex-engine=xelatex -V CJKmainfont=IPAexMincho --listings -H listings-setup.tex

camera_raw.md: $(MDS)
	cat $(MDS) > $@
	sed -i 's/https:\/\/github.com\/moizumi99\/camera_raw_processing\/raw\/master\///g' $@

%.md: %.ipynb
	jupyter nbconvert --to markdown $<

.PHONY: clean
clean:
	rm -f *.pdf
	rm -f $(MDS)
