.PHONY: etc

COMPONENT := core


include ../Makefile.common


run:
	nameko run --config config.yaml articles.services.$(COMPONENT).service:ArticleService
