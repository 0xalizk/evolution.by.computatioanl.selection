#!/bin/bash

# usage: bash compile.sh tex/xxxx.tex bib , the 'bib' is optional, include it if you want bibliography to be rebuilt

rm -rf $(biber --cache)
rm .build/*
cp $1 .build/
cp tex/*.bib  .build/
cd .build
echo 'pdflatex 1'
pdflatex *.tex
echo ''
echo ''
if [ $2 = "bib" ] ;
    then
       #echo 'biber:'
       #biber *.bcf
       echo 'bibtex'
       bibtex *aux
       echo ''
       echo 'pdflatex 2: > .build/pdflatex2.log'
       pdflatex *.tex > pdflatex2.log
       echo 'pdflatex 3: > .build/pdflatex3.log'
       pdflatex *.tex > pdflatex3.log
fi

mv *.pdf ../pdf/compiled.pdf
cd ..
echo "Done: auxilaries in .build/ .. launching pdf/compiled.pdf"
open pdf/compiled.pdf
