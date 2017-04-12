#ifndef Utils_PlotUtils_h
#define Utils_PlotUtils_h

#include <iostream>
#include <vector>
#include <string>

#include "TH1F.h"
#include "TString.h"
#include "TCanvas.h"
#include "TIterator.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TLatex.h"
#include "TLine.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TROOT.h"

#include "RooPlot.h"
#include "RooHist.h"
#include "RooRealVar.h"
#include "RooFitResult.h"
#include "RooAbsPdf.h"
#include "RooAbsReal.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooPlot.h"

#include "Util.h"

void CMS_lumi( TPad* pad, int iPeriod=3, int iPosX=10, TString eet="" );


void GetDataPoissonInterval(const RooAbsData*, RooRealVar*, RooPlot*, const int & = 1); 

RooPlot* get_pull(RooRealVar*, RooPlot*, RooDataSet*, RooAbsPdf*, RooFitResult* , const std::string & = "data", const std::string & = "model_mc", const int & = 1, const int & = 1, std::vector<TObject*>* = NULL);

RooPlot* get_ratio(RooRealVar*, RooDataSet*, RooAbsPdf*, RooFitResult* , const int & = 1, const int & = 1, std::vector<TObject*>* = NULL);

RooPlot* get_pull_ws(RooRealVar*, RooPlot*, TGraphAsymmErrors* , const std::string & = "data", const std::string & = "model_mc", const int & = 1);

TLatex* banner4Plot(const std::string & = "mu", const float & = 19.5, const int & = 1, const int & = 0);

TLegend* legend4Plot(RooPlot*, const int & = 0, const double & = 0, const double & = 0,  const double & = 0, const double & = 0, const int & = 1, const std::string & = "mu" );

// draw canvas with plots with pull
void draw_canvas_with_pull(RooPlot*, RooPlot*, RooArgList*, const std::string & = "", const std::string & = "", const std::string & = "", const std::string & = "mu", const int & = 0, const int & = 0, const float & lumi = 19.5);

void draw_canvas(RooPlot*, const std::string & = "" ,  const TString & = "", const std::string & = "mu", const float & = 19.5, const int & = 0, const int & = 0, const int & = 0);

// set tdr style function
void setTDRStyle();

//
float GetLumi(const std::string & = "em");



#endif
