# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile livehtml doctest

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	sphinx-autobuild . -b html $(ALLSPHINXOPTS) \
		--delay=3 \
		--watch=. \
		--watch=../easycli \
		--ignore='*~' \
		--ignore='_build' \
        --ignore "*.sw*" \
        --ignore "4913" \
        --ignore "*.pdf" \
        --ignore "*.log" \
        --ignore "*.out" \
        --ignore "*.toc" \
        --ignore "*.aux" \
        --ignore "*.idx" \
        --ignore "*.ind" \
        --ignore "*.ilg" \
        --ignore "*.tex" \
		--port 8082 \
		$(BUILDDIR)/html 

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
