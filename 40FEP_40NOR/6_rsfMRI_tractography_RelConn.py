import os 
import re
import sys
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import pandas as pd


def threshold(voxelsize, side, smoothing, IC):

    log = 'subjects.txt'
    #log = 'test_subj.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    for subject in subjects:
        
        dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
            
        dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
        for dataDir in dataDirs:
            dataFile = '{dataLoc}/{dataDir}/fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
            
            for thr in range(10,30,10):
                thresh_dataFile = '{dataLoc}/{dataDir}/{thr}_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir, thr=thr)
                if not os.path.isfile(thresh_dataFile):
                    command = 'fslmaths {dataFile} -thrP {thr} {thresh_dataFile}'.format(dataFile=dataFile, thr=thr, thresh_dataFile=thresh_dataFile)
                    os.popen(command).read



def extractRelConn(voxelsize, side, smoothing, IC):
    
    #IC_connectivity = 'RelativeConnectivity_{voxelsize}_{side}_{smoothing}_{IC}IC.csv'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    IC_connectivity = 're_RelativeConnectivity_{voxelsize}_{side}_{smoothing}_{IC}IC.csv'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
    
    if not os.path.isfile(IC_connectivity):
        
        allData = []
        
        log = 'subjects.txt'
        
        #log = 'test_subj.txt'
        with open(log, 'r') as f:
            subjects = f.read().split()

        imgInputs = []
        for subject in subjects:
            
            dataLoc = '{subject}/rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC)
            
            dataDirs = [ x for x in os.listdir(dataLoc) if '_demeaned_' in x]
            for dataDir in dataDirs:
                dataFile = '{dataLoc}/{dataDir}/fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir)
                imgInputs.append(dataFile)
                for thr in range(10,30,10):
                    thresh_dataFile = '{dataLoc}/{dataDir}/{thr}_fdt_paths.nii.gz'.format(dataLoc=dataLoc, dataDir=dataDir, thr=thr)
                    imgInputs.append(thresh_dataFile)

        for dataDir in dataDirs:
            ic = dataDir.split("_")[1]
            imgs = [x for x in imgInputs if '{ic}'.format(ic=ic) in x]
            for subject in subjects:
                subj_imgs = [x for x in imgs if '{subject}'.format(subject=subject) in x]
                img = [x for x in subj_imgs if not '0_fdt' in x]
                im = nb.load(''.join(img)).get_data()
                ic_connectivity = sum(im[im != 0])

                allData.append((subject, ic, 'None', ic_connectivity))
                
                for thr in range(10,30,10):
                    thr_img = [x for x in subj_imgs if '{thr}_fdt'.format(thr=thr) in x]
                    thr_im = nb.load(''.join(thr_img)).get_data()
                    thr_ic_connectivity = sum(thr_im[thr_im != 0])
                
                    allData.append((subject, ic, thr, thr_ic_connectivity))
            
        
        df = pd.DataFrame(allData)
        df.columns = ['subject', 'IC_number', 'Threshold', 'IC_connectivity']

        df.to_csv(IC_connectivity)

    df = pd.read_csv(IC_connectivity, index_col=0)
    df['side'] = '{side}'.format(side=side)
    df['voxel_size'] = '{voxelsize}'.format(voxelsize=voxelsize)
    df['spatial_smoothing'] = '{smoothing}'.format(smoothing=smoothing)
    total_connectivity_sum = df.groupby(['subject', 'Threshold']).sum().reset_index()
    total_connectivity_sum.columns = ['subject', 'Threshold', 'Total_connectivity']
    new_df = pd.merge(df, total_connectivity_sum, on=['subject', 'Threshold'], how='inner')
    new_df['Relative_connectivity'] = new_df.IC_connectivity / new_df.Total_connectivity
    new_df['group'] = new_df['subject'].str[:3]
    
    #new_df = new_df.sort_values(by=['IC_number', 'Threshold'])
    
    new_df.to_csv(IC_connectivity)
    
    
    

    demo = pd.read_csv('subjects_demo.csv')
    demo = demo.rename(columns = {'folderName': 'subject'})
    for_stats = pd.merge(new_df, demo, on=['subject'], how='inner')
    for_stats = for_stats.sort_values(by=['IC_number', 'Threshold'])

    for_stats.to_csv(IC_connectivity)








            
            
            

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
	parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
	parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
	parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
	args = parser.parse_args()

	threshold(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
	extractRelConn(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
