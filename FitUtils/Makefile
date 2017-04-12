CXX = $(shell root-config --cxx)
CXXFLAGS = $(shell root-config --cflags)
LDFLAGS:= $(shell root-config --ldflags)
LDLIBS:= $(shell root-config --libs)
ROOTLIBS:=-lRooFit -lHtml -lMinuit -lRooFitCore -lRooStats -lHistFactory
GLIBS   = $(shell root-config --glibs)
MACFLAGS = -bundle -undefined dynamic_lookup
ARCH = $(shell root-config --arch)



SOURCESRAW = $(wildcard *.cxx)
SOURCES = $(filter-out %_dict.cxx, $(SOURCESRAW))
HEADERS = $(wildcard *.h)
SHOBJECTS = $(patsubst %.cxx,%.so,$(SOURCES))
OBJECTS = $(patsubst %.cxx,%.o,$(SOURCES))
DICTS = $(patsubst %.cxx,%_dict.cxx,$(SOURCES))



all: $(DICTS) $(SHOBJECTS)

%_dict.cxx: %.h
	rootcint -f $@ $(CXXFLAGS) -p $^

%.so : %.cxx %_dict.cxx
ifeq ($(ARCH),macosx64)
	$(CXX) $(MACFLAGS) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS) $(GLIBS) $(ROOTLIBS) $^ -o $@
else
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS) $(GLIBS) $(ROOTLIBS) $^ -o $@
endif



clean:
	rm -f *.so *.d *.pcm *_dict.cxx
