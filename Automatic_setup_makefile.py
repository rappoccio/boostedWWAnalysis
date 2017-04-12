import os
import glob
import math
import array
import ROOT
import ntpath
import sys
import subprocess

from optparse import OptionParser
from subprocess import Popen
from ROOT import gROOT, gStyle, gSystem, TLatex

parser = OptionParser()
parser.add_option('--vclean', help='clean all the so files', type=int, default=0.)

(options, args) = parser.parse_args()

if __name__ == "__main__":
  ROOT.gSystem.AddIncludePath("-I$ROOTSYS/include/root");
  ROOT.gSystem.Load("$ROOTSYS/lib/root/libRooFitCore.so")
  ROOT.gSystem.Load("PlotStyle/Util.so");
  ROOT.gSystem.Load("PlotStyle/PlotUtils.so");
  ROOT.gSystem.Load("PDFs/PdfDiagonalizer.so");
  ROOT.gSystem.Load("PDFs/HWWLVJRooPdfs.so");
  ROOT.gSystem.Load("PDFs/MakePdf.so");
  ROOT.gSystem.Load("BiasStudy/BiasUtils.so");
  ROOT.gSystem.Load("FitUtils/FitUtils.so");
  
  
  
