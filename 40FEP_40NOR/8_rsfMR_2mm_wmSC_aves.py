import sys, os
from os.path import join, basename, isfile, isdir
import argparse
import nibabel as nb
import numpy as np
import nilearn
from nilearn import image


def GroupAvePerIC(voxelsize, side, smoothing, IC):
    
    ave_dir = '2mm_Ave_wmSCfromrsFC'
    if not os.path.exists(ave_dir):
        os.mkdir(ave_dir)

    
    out_dir=join(ave_dir, '{voxelsize}_{side}_{smoothing}_{IC}ICs'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC))
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    componentNum = int('{IC}'.format(IC=IC))
    ICs=["%02d" % x for x in range(0,componentNum)]

    log = 'subjects.txt'
    with open(log, 'r') as f:
        subjects = f.read().split()

    thrs = [ '95', '90', '20', '10' ]
    
    for ic in ICs:
        for thr in thrs:
            imgInputs = []
            zero_imgInputs = []
            for subject in subjects:
                dataLoc = '{subject}/2mm_rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs/2mm_brain_{smoothing}_IC{ic}_demeaned_tfce_corrp_tstat1'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, ic=ic)
                dataFile = '/{thr}thrP_fdt_paths.nii.gz'.format(thr=thr)
                imgInputs.append(dataLoc+dataFile)
        
                zero_dataFile = '/fdt_paths.nii.gz'
                zero_imgInputs.append(dataLoc+zero_dataFile)

            averaged_perIC = join(out_dir, '{thr}thrP_all_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(thr=thr, voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if  not os.path.isfile(averaged_perIC):
                perSubj_perIC = [x for x in imgInputs if '{ic}'.format(ic=ic) and '{thr}thrP'.format(thr=thr) in x]
                ave_perIC = nilearn.image.mean_img(perSubj_perIC)
                ave_perIC.to_filename(averaged_perIC)
        
            zero_averaged_perIC = join(out_dir, 'all_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if  not os.path.isfile(zero_averaged_perIC):
                zero_perSubj_perIC = [x for x in zero_imgInputs if '{ic}'.format(ic=ic) in x]
                zero_ave_perIC = nilearn.image.mean_img(zero_perSubj_perIC)
                zero_ave_perIC.to_filename(zero_averaged_perIC)

	

    for ic in ICs:
        for thr in thrs:
            FEPimgInputs = [] 
            zero_FEPimgInputs = [] 
            for subject in subjects:
                if subject.startswith('FEP'):
                    FEP_dataLoc = '{subject}/2mm_rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs/2mm_brain_{smoothing}_IC{ic}_demeaned_tfce_corrp_tstat1'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, ic=ic)
                    FEP_dataFile = '/{thr}thrP_fdt_paths.nii.gz'.format(thr=thr)
                    FEPimgInputs.append(FEP_dataLoc+FEP_dataFile)

                    zero_FEP_dataFile = '/fdt_paths.nii.gz'
                    zero_FEPimgInputs.append(FEP_dataLoc+zero_FEP_dataFile)

            FEP_averaged_perIC = join(out_dir, '{thr}thrP_FEP_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(thr=thr, voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            FEP_merged_perIC = join(out_dir, '{thr}thrP_FEP_merged_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(thr=thr, voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(FEP_averaged_perIC):
                FEP_perSubj_perIC = [x for x in FEPimgInputs if '{ic}'.format(ic=ic) and '{thr}thrP'.format(thr=thr) in x]
                #FEP_concat_perIC = nilearn.image.concat_imgs(FEP_perSubj_perIC)
                #FEP_concat_perIC.to_filename(FEP_merged_perIC)
                FEP_ave_perIC = nilearn.image.mean_img(FEP_perSubj_perIC)
                FEP_ave_perIC.to_filename(FEP_averaged_perIC)




            zero_FEP_averaged_perIC = join(out_dir, 'FEP_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(zero_FEP_averaged_perIC):
                zero_FEP_perSubj_perIC = [x for x in zero_FEPimgInputs if '{ic}'.format(ic=ic) in x]
                zero_FEP_ave_perIC = nilearn.image.mean_img(zero_FEP_perSubj_perIC)
                zero_FEP_ave_perIC.to_filename(zero_FEP_averaged_perIC)





    for ic in ICs:
        for thr in thrs:
            NORimgInputs = [] 
            zero_NORimgInputs = [] 
            for subject in subjects:
                if subject.startswith('NOR'):
                    NOR_dataLoc = '{subject}/2mm_rsFC_seed_tractography/{voxelsize}_{side}_{smoothing}_{IC}ICs/2mm_brain_{smoothing}_IC{ic}_demeaned_tfce_corrp_tstat1'.format(subject=subject, voxelsize=voxelsize, side=side, smoothing=smoothing, IC=IC, ic=ic)
                    NOR_dataFile = '/{thr}thrP_fdt_paths.nii.gz'.format(thr=thr)
                    NORimgInputs.append(NOR_dataLoc+NOR_dataFile)

                    zero_NOR_dataFile = '/fdt_paths.nii.gz'
                    zero_NORimgInputs.append(NOR_dataLoc+zero_NOR_dataFile)


            NOR_averaged_perIC = join(out_dir, '{thr}thrP_NOR_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(thr=thr, voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(NOR_averaged_perIC):
                NOR_perSubj_perIC = [x for x in NORimgInputs if '{ic}'.format(ic=ic) and '{thr}thrP'.format(thr=thr) in x]
                NOR_ave_perIC = nilearn.image.mean_img(NOR_perSubj_perIC)
                NOR_ave_perIC.to_filename(NOR_averaged_perIC)



            zero_NOR_averaged_perIC = join(out_dir, 'NOR_ave_{voxelsize}_{side}_{smoothing}_IC{ic}.nii.gz'.format(voxelsize=voxelsize, side=side, smoothing=smoothing, ic=ic))
            if not os.path.isfile(zero_NOR_averaged_perIC):
                zero_NOR_perSubj_perIC = [x for x in zero_NORimgInputs if '{ic}'.format(ic=ic) in x]
                zero_NOR_ave_perIC = nilearn.image.mean_img(zero_NOR_perSubj_perIC)
                zero_NOR_ave_perIC.to_filename(zero_NOR_averaged_perIC)







if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--voxelsize', '-vox', nargs=1, type=str)
    parser.add_argument('--side', '-side', nargs=1, help = 'left or right', type=str)
    parser.add_argument('--smoothing', '-smooth', nargs=1,  help = 'e.g., nosmooth, fwhm6, fwhm6preproc', type=str)
    parser.add_argument('--IC', '-IC', nargs=1, help = 'e.g., 10 or 20', type=str)
    args = parser.parse_args()

    GroupAvePerIC(args.voxelsize[0], args.side[0], args.smoothing[0], args.IC[0])
