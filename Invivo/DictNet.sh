#!/bin/sh
#SBATCH -p standard
#SBATCH -t 03:00:00
#SBATCH --mem=32GB
#SBATCH --job-name=DictNet

# Use for Single Shell protocols
# Usage: sbatch run_DictNet.sh <protocol_no>
# Abrar F. (abrarfaiyaz.iutcse@gmail.com)

module load keras/2.0.5 #cudnn/9.0-7
proto=$1 #P12
seed=$2 #47
baseLoc=`pwd`
OUTPUTDIR="$baseLoc/$proto/DictNet2_Out/"
protocol="$baseLoc/$proto/"
echo "$1"
mkdir $OUTPUTDIR

#Single Shell generated dti_FA and dti_S0
protocolDTI="$baseLoc/P1/"

python dictnet_train_invivo2.py $protocol/List1_train_norm_dwi.txt $protocol/List2_train_brain_mask.txt $protocolDTI/List10_train_T2.txt $protocolDTI/List20_train_FA.txt $protocol/List3_train_ficvf.txt $protocol/List4_train_fiso.txt $protocol/List5_train_odi.txt  $OUTPUTDIR $proto $seed

python dictnet_test_invivo2.py $protocol/List1_train_norm_dwi.txt $protocol/List6_test_norm_dwi.txt $protocol/List7_test_brain_mask.txt $protocolDTI/List11_test_T2.txt $protocolDTI/List21_test_FA.txt $OUTPUTDIR $proto $seed


#Training Components
#List1_train_norm_dwi.txt                       dwi train images (eddy corrected + normalized)
#List2_train_brain_mask.txt                     mask (nodif_brain_mask)
#List3_train_ficvf.txt                          NDI (NODDI generated)
#List4_train_fiso.txt 						    fISO  (NODDI generated)
#List5_train_odi.txt 							ODI (NODDI generated)
#List10_train_T2.txt							T2 / S0
#List20_train_FA.txt							FA


#Test Components
#List6_test_norm_dwi.txt                    	dwi test images (eddy corrected + normalized)
#List7_test_brain_mask.txt				        mask (nodif_brain_mask from fsl)
#List11_train_T2.txt							T2 / S0 
#List21_train_FA.txt							FA
