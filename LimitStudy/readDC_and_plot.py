#!/usr/bin/python

import os
import sys
import subprocess
import operator
from ROOT import TFile, TH1F, TCanvas, gStyle, TLine
from commands import getstatusoutput
from operator import itemgetter


# maximum number of systematics to consider and to plot
MAXSYST     = 300
MAXSYSTPLOT = 30


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

def getLimitFromFile (filename) :
    filenameResult = filename+".limit.txt"
    print "  >> file: "+filenameResult
    f = open (filenameResult, 'r')
    calcLimit = f.read()

    isThereTheLimit = False
    for line in calcLimit.split ('\n') :
      if line.find ('Expected 50.0') != -1 :
        isThereTheLimit = True

    if isThereTheLimit :
     thisLimit = [line for line in calcLimit.split ('\n') if line.find ('Expected 50.0') != -1][0].split ()[4]
    else :
      thisLimit = -1.

    print "thisLimit = "+str(thisLimit)
    return thisLimit


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


def clean (basename) :
    getstatusoutput('rm ./' + basename + '*')


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


def lookAtSystematics (datacardname) :

    # open the datacard file
    # ---- ---- ---- ---- ---- ---- ---- ----
    
    print 'Opening original input datacard: ', datacardname
    lines = open (datacardname, 'r').read().split ('\n')
    nametag = datacardname.split ('/')[-1].replace ('.txt', '')
    thepath = datacardname.replace (nametag + '.txt', '')

    # separate header and systematics
    # ---- ---- ---- ---- ---- ---- ---- ----
    
    gStyle.SetGridStyle (1)
    gStyle.SetGridColor (15)
#    gStyle.SetGridWidth (float (0.5))
    systime = 0
    header = []
    systematics = []
    systematics_fixed = []
    for linea in lines:
        if '---' in linea : continue
        if systime == 0 :
            header.append (linea)
            if linea.split (' ')[0] == 'rate' :
                systime = 1
        elif 'Deco' in linea:
            systematics_fixed.append(linea)
                        
        else:
            systematics.append (linea)

    systematics = [elem for elem in systematics if len (elem.split ()) > 0]

    # get the actual result with the original datacard
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    
    nominalLimit = getLimitFromFile (datacardname)
    
    # remove, one at a time, one systematic 
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

    removingLimits = {}
    removingLimits['NOMINAL'] = nominalLimit
    syslist = []
#    syslist.append ('NOMINAL')
#    syslist.append ('SHAPE SYST')
    
    for it in range (min(len (systematics),MAXSYST)) :
        elements = systematics[it].split ()
        syslist.append (systematics[it].split ()[0])
        if len (elements) == 0 : continue
        
        filename = thepath + 'tempo.remove.' + str (it) + '.' + systematics[it].split ()[0] + '.' + nametag
        #f = open(filename, 'w')
        #for linea in header: f.write (linea + '\n')
        #for it1 in range (min(len (systematics),MAXSYST)) :
            #if (it1 == it) : continue
            #if len (systematics[it1].split ()) == 0 : continue
            #f.write (systematics[it1] + '\n')
        #f.close ()

        thisLimit = getLimitFromFile (filename)
        removingLimits[systematics[it].split ()[0]] = thisLimit

    syslist.append ('NOMINAL')
    
    # get the result with no systematics
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    
    filename = thepath + 'tempo.stats.' + str (0.) + nametag + '.txt'
    #f = open(filename, 'w')
    #for linea in header: f.write (linea + '\n')
    #f.close ()
    statsLimit = getLimitFromFile (filename)

    addingLimits = {}
    addingLimits['NOMINAL'] = statsLimit


    # get the result with only shape systematics
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    
    filename2 = thepath + 'tempo.shape.' + str (0.) + nametag + '.txt'
    #f = open(filename, 'w')
    #for linea in header: f.write (linea + '\n')
    #f.close ()
    shapeLimit = getLimitFromFile (filename2)

#    addingLimits = {}
    addingLimits['SHAPE SYST'] = shapeLimit

    

    # add, one at a time, only one systematic source
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

    for it in range (min(len (systematics),MAXSYST)) :
        elements = systematics[it].split ()
        if len (elements) == 0 : continue
        
        filename = thepath + 'tempo.add.' + str (it) + '.' + systematics[it].split ()[0] +  '.' +  nametag
        #f = open(filename, 'w')
        #for linea in header: f.write (linea + '\n')
        #f.write (systematics[it] + '\n')
        #f.close ()
        
        thisLimit = getLimitFromFile (filename)
        addingLimits[systematics[it].split ()[0]] = thisLimit


    # filling histograms
    # ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
    
    #TGaxis::SetMaxDigits(3)
    gStyle.SetPadBottomMargin(0.50)
    gStyle.SetPadLeftMargin  (0.20)
    gStyle.SetPadRightMargin (0.01)
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat       (   0)
    gStyle.SetStatBorderSize(   0)
    gStyle.SetStatColor     (  10)
    gStyle.SetStatFont      (  42)
    gStyle.SetStatX         (0.94)
    gStyle.SetStatY         (0.91)
    gStyle . cd()

    h_removing = TH1F ('removing', 'removing', min(len (systematics)+1,MAXSYSTPLOT+1), 0, min(len (systematics)+1,MAXSYSTPLOT+1))
    h_removing.SetMarkerStyle (20)
    h_removing.SetMarkerColor (9)
    h_removing.SetMarkerSize (0.8)
    h_removing.GetYaxis().SetLabelFont(42)
    h_removing.GetXaxis().SetLabelFont(42)
    h_removing.GetXaxis().SetLabelSize(0.045)

    h_adding = TH1F ('adding', 'adding', min(len (systematics)+1,MAXSYSTPLOT+1), 0, min(len (systematics)+1,MAXSYSTPLOT+1))
    h_adding.SetMarkerStyle (4)
    h_adding.SetMarkerColor (9)
    h_adding.SetMarkerSize (0.8)
    h_adding.GetYaxis().SetLabelFont(42)
    h_adding.GetXaxis().SetLabelFont(42)
    h_adding.GetXaxis().SetLabelSize(0.045)

    binId = 1
    for syst in syslist:
        if binId <= min(len (systematics),MAXSYSTPLOT+1) :
           if syst != "SHAPE SYST":
               h_removing.GetXaxis ().SetBinLabel (binId, syst)
               h_removing.SetBinContent (binId, float (removingLimits[syst]))
           h_adding.GetXaxis ().SetBinLabel (binId, syst)
           h_adding.SetBinContent (binId, float (addingLimits[syst]))
#           print "binId = "+str(binId)
        binId += 1 

    h_sorted_adding = TH1F ('sorted_adding', 'sorted_adding', min(len (systematics)+1,MAXSYSTPLOT+1), 0, min(len (systematics)+1,MAXSYSTPLOT+1))
    h_sorted_adding.SetMarkerStyle (4)
    h_sorted_adding.SetMarkerColor (9)
    h_sorted_adding.SetMarkerSize (0.8)
 
    h_sorted_removing = TH1F ('sorted_removing', 'sorted_removing', min(len (systematics)+1,MAXSYSTPLOT+1), 0, min(len (systematics)+1,MAXSYSTPLOT+1))
    h_sorted_removing.SetMarkerStyle (20)
    h_sorted_removing.SetMarkerColor (9)
    h_sorted_removing.SetMarkerSize (0.8)

    #adding_dummy = sorted ([(k, v) for k, v in addingLimits.iteritems ()], key=itemgetter (1))
    adding_dummy = sorted ([(k, v) for k, v in addingLimits.iteritems ()], key=itemgetter (1), reverse=True)
    sorted_syslist = [k[0] for k in adding_dummy]

    binId = 1
    for syst in sorted_syslist:
        if binId <= min(len (systematics),MAXSYSTPLOT+1) :
           if syst != "SHAPE SYST":
               h_sorted_removing.GetXaxis ().SetBinLabel (binId, syst)
               h_sorted_removing.SetBinContent (binId, float (removingLimits[syst]))        
           h_sorted_adding.GetXaxis ().SetBinLabel (binId, syst)
           h_sorted_adding.SetBinContent (binId, float (addingLimits[syst]))        
        binId += 1 

    # final plotting and saving
    # ---- ---- ---- ---- ---- ---- ---- ----

    can = TCanvas ('can', 'can', 20 * min(len (systematics),MAXSYSTPLOT+1), 400)
    frac = float (600) / 20. * float (min(len (systematics),MAXSYSTPLOT+1))
    can.SetMargin (0.1 * float (frac), 0.025 * float (frac), 0.5, 0.1) #LRBT
    can.SetGridx ()

    l_nominal = TLine (0.,  float (nominalLimit), float (min(len (systematics),MAXSYSTPLOT+1)), float (nominalLimit))
    l_nominal.SetLineColor (1)
#    l_nominal.SetLineWidth (float (1))
    l_stats = TLine (0.,  float (statsLimit), float (min(len (systematics),MAXSYSTPLOT+1)), float (statsLimit))
    l_stats.SetLineColor (2)
#    l_stats.SetLineWidth (float (1))
    l_shape = TLine (0.,  float (shapeLimit), float (min(len (systematics),MAXSYSTPLOT+1)), float (shapeLimit))
    l_shape.SetLineColor (4)
    
    bkg = can.DrawFrame (0, float(statsLimit) * 0.9, min(len (systematics),MAXSYSTPLOT+1), float(nominalLimit) * 1.1)
    bkg.GetXaxis ().Set (min(len (systematics),MAXSYSTPLOT+1), 0, min(len (systematics),MAXSYSTPLOT+1))
    for i in range (0, min(len (systematics),MAXSYSTPLOT+1)) :
        bkg.GetXaxis ().SetBinLabel (i+1, syslist[i])
    bkg.GetYaxis().SetLabelFont(42);
    bkg.GetXaxis().SetLabelFont(42);
    bkg.GetXaxis().SetLabelSize(0.05);
    bkg.GetXaxis().LabelsOption ("v")

    bkg.SetTitle (nametag)
    bkg.GetYaxis ().SetTitle ('exp limit')
    bkg.Draw ()



    h_adding.GetYaxis().SetLabelFont(42)
    h_adding.GetXaxis().SetLabelFont(42)
    h_adding.GetXaxis().SetLabelSize(0.045)
    h_adding.GetXaxis().LabelsOption ("v")


    h_removing.GetYaxis().SetLabelFont(42)
    h_removing.GetXaxis().SetLabelFont(42)
    h_removing.GetXaxis().SetLabelSize(0.045)
    h_removing.GetXaxis().LabelsOption ("v")


    h_sorted_adding.GetYaxis().SetLabelFont(42)
    h_sorted_adding.GetXaxis().SetLabelFont(42)
    h_sorted_adding.GetXaxis().SetLabelSize(0.045)
    h_sorted_adding.GetXaxis().LabelsOption ("v")


    h_sorted_removing.GetYaxis().SetLabelFont(42)
    h_sorted_removing.GetXaxis().SetLabelFont(42)
    h_sorted_removing.GetXaxis().SetLabelSize(0.045)
    h_sorted_removing.GetXaxis().LabelsOption ("v")


    can.SetGrid()
    #h_adding.Draw ('P')
    l_nominal.Draw ('same')
    l_stats.Draw ('same')
    l_shape.Draw ('same')    
    h_adding.Draw ('Psame')
    h_removing.Draw ('Psame')    
    #can.Print ('result.' + nametag + '.pdf', 'pdf')
    #can.Print ('result.' + nametag + '.png', 'png')
    can.SaveAs ('result.' + nametag + '.pdf')
    can.SaveAs ('result.' + nametag + '.png')

    bkg_sorted = bkg.Clone ('bkg_sorted')
    for i in range (0, min(len (systematics),MAXSYSTPLOT+1)) :
        bkg_sorted.GetXaxis ().SetBinLabel (i+1, sorted_syslist[i])
    bkg_sorted.GetYaxis().SetLabelFont(42);
    bkg_sorted.GetXaxis().SetLabelFont(42);
    bkg_sorted.GetXaxis().SetLabelSize(0.035);
    bkg_sorted.GetXaxis().LabelsOption ("v")
    bkg_sorted.Draw ()
    #h_sorted_adding.Draw ('P')
    l_nominal.Draw ('same')
    l_stats.Draw ('same')
    l_shape.Draw ('same')
    h_sorted_adding.Draw ('Psame')
    h_sorted_removing.Draw ('Psame')
    #can.Print ('result.sorted.' + nametag + '.pdf', 'pdf')
    #can.Print ('result.sorted.' + nametag + '.png', 'png')
    can.SaveAs ('result.sorted.' + nametag + '.pdf')
    can.SaveAs ('result.sorted.' + nametag + '.png')


    outFile = TFile ('outfile.' + nametag + '.root', 'recreate')
    outFile.cd () 
    h_removing.Write ()
    h_adding.Write ()
    h_sorted_removing.Write ()
    h_sorted_adding.Write ()
    outFile.Close ()
    
    #clean (thepath + 'tempo') 
    #clean ('roostats') 


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


if __name__ == '__main__':


    if len (sys.argv) < 2 : 
        print 'input datacard folder missing\n'
        exit (1)
        
    folderName = sys.argv[1].split ('/')[-1] + '_copy'
    #result = getstatusoutput ('rm -rf ' + folderName)
    #if result[0] == 0 : print 'NB folder ' + folderName + ' cleaned, being replaced'

    currentFolder = getstatusoutput ('pwd')[1]
    #getstatusoutput ('cp -r ' + sys.argv[1] + ' ./' + folderName)
   
    listOfDatacards = []
    for elem in getstatusoutput ('ls ' + str (folderName) + ' | grep -v tempo | grep -v limit | grep -v submit | grep txt')[1].split ('\n'):
        listOfDatacards.append (currentFolder + '/' + folderName + '/' + str (elem))
    
    for datacard in listOfDatacards :
        lookAtSystematics (datacard)   
    


    
    
