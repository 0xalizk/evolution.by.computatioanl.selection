# usage: both bib, 'bib' is optional, if included the bibliography will be built, make sure both.sh has a link in /usr/bin/both
python src/combine.py $PWD/tex && bash src/compile.sh tex/combined.tex $1
