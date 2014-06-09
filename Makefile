BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
DEPLOYDIR=$(BASEDIR)/deploy
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py


devhtml:
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

pubhtml:
	pelican $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF)

devs:
	$(BASEDIR)/develop_server.sh start

stops:
	$(BASEDIR)/develop_server.sh stop

publish:
	cp $(BASEDIR)/CNAME $(OUTPUTDIR)/
	git clone -b gitcafe-pages $(BASEDIR) $(DEPLOYDIR) --single-branch
	rm -rf $(DEPLOYDIR)/*
	cp -r $(OUTPUTDIR)/* $(DEPLOYDIR)/

clean:
	rm -rf $(OUTPUTDIR) $(DEPLOYDIR) *.pyc


.PHONY: devhtml pubhtml devs stops publish clean
