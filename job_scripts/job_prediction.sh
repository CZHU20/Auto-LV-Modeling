#!/bin/bash
# Job name:
#SBATCH --job-name=2dunet
#
# Account:
#SBATCH --account=fc_biome
#
# Partition:
#SBATCH --partition=savio2_gpu
#
# QoS:
#SBATCH --qos=savio_normal
#
# Number of nodes:
#SBATCH --nodes=1
#
# Number of tasks (one for each GPU desired for use case) (example):
#SBATCH --ntasks=1
#
# Number of processors for single task needed for use case (example):
#SBATCH --cpus-per-task=4
#
#Number of GPUs, this can be in the format of "gpu:[1-4]", or "gpu:K80:[1-4] with the type included
#SBATCH --gres=gpu:1
#
# Wall clock limit:
#SBATCH --time=04:30:00
#
## Command(s) to run (example):
#module load gcc openmpi python
module load python
module load tensorflow/1.12.0-py36-pip-gpu
module load cuda
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_3 \
#    --output 2DUNet/Logs/MMWHS_3/mr_run7/test_axial \
#    --model 2DUNet/Logs/MMWHS_3/mr_run7 \
#    --view 0 \
#    --modality mr \
#    --mode validate

#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_3 \
#   --output 2DUNet/Logs/MMWHS_3/mr_run6/test_axial \
#    --model 2DUNet/Logs/MMWHS_3/mr_run6 \
#    --view 0 \
#    --modality mr \
#    --mode validate

#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS \
#    --output 2DUNet/Logs/MMWHS/total_run3/test_axial \
#    --model 2DUNet/Logs/MMWHS/total_run3 \
#    --view 0 \
#    --modality ct mr \
#    --mode validate
#
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_small \
#    --output 2DUNet/Logs/MMWHS_editted_aug/run0/test_axial \
#    --model 2DUNet/Logs/MMWHS_editted_aug/run0 \
#    --view 0 \
#    --modality ct mr \
#    --mode test
#
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_small \
#    --output 2DUNet/Logs/MMWHS_editted_aug/run0/test_coronal \
#    --model 2DUNet/Logs/MMWHS_editted_aug/run0 \
#    --view 1 \
#    --modality ct mr \
#    --mode test
#
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_small \
#    --output 2DUNet/Logs/MMWHS_editted_aug/run0/test_sagittal \
#    --model 2DUNet/Logs/MMWHS_editted_aug/run0 \
#    --view 2 \
#    --modality ct mr \
#    --mode test
#

#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_small \
#    --output 2DUNet/Logs/MMWHS_editted_aug/run0/val_axial \
#    --model 2DUNet/Logs/MMWHS_editted_aug/run0 \
#    --view 0 \
#    --modality ct mr \
#    --mode validate

#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS_small \
#    --output 2DUNet/Logs/MMWHS_aug2/run1-total_run_small_lr-total_run_small_lr_mean_dice_ensemble \
#    --model 2DUNet/Logs/MMWHS_aug2/total_run_small_lr_mean_dice 2DUNet/Logs/MMWHS_aug2/total_run_small_lr 2DUNet/Logs/MMWHS_aug2/run1\
#    --view 0 1 2 \
#    --modality ct mr \
#    --mode validate

python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
    --image ImageData/MMWHS \
    --output 2DUNet/Logs/MMWHS_aug2/run1/test_ensemble2 \
    --model 2DUNet/Logs/MMWHS_aug2/run1 \
    --view 0 1 2 \
    --modality ct mr \
    --mode test

#
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS \
#    --output 2DUNet/Logs/MMWHS/total_run3/test_coronal \
#    --model 2DUNet/Logs/MMWHS/total_run3 \
#    --view 1 \
#    --modality ct mr \
#    --mode test
#
#python /global/scratch/fanwei_kong/DeepLearning/2DUNet/prediction.py \
#    --image ImageData/MMWHS \
#    --output 2DUNet/Logs/MMWHS/total_run3/test_sagittal \
#    --model 2DUNet/Logs/MMWHS/total_run3 \
#    --view 2 \
#    --modality ct mr \
#    --mode test


