all:
	+$(MAKE) -C BiasStudy/
	+$(MAKE) -C FitUtils/
	+$(MAKE) -C PDFs/
	+$(MAKE) -C PlotStyle/

clean:
	+$(MAKE) clean -C BiasStudy/
	+$(MAKE) clean -C FitUtils/
	+$(MAKE) clean -C PDFs/
	+$(MAKE) clean -C PlotStyle/
