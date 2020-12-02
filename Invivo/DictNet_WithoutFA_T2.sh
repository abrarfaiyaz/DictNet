#!/bin/sh
#SBATCH -p standard
#SBATCH -t 07:00:00
#SBATCH -c 8
#SBATCH --mem=128GB
#SBATCH --job-name=DictNet


#### BATCH -t 02:00:00
#### BATCH -c 8


# Usage: sbatch run_DictNet.sh <protocol_no>

module load keras/2.0.5 #cudnn/9.0-7
proto=$1 #P12
seed=$2 #47
baseLoc="/scratch/mdoyley_lab/afaiyaz/HCP/DataPrep/DLpriorNODDI/"
OUTPUTDIR="$baseLoc/$proto/DictNet_Out/"
protocol="$baseLoc/$proto/"
echo "$1"
mkdir $OUTPUTDIR

#Single Shell generated dti_FA and dti_S0
protocolDTI="$baseLoc/P1/"

python dictnet_train_invivo.py $protocol/List1_train_norm_dwi.txt $protocol/List2_train_brain_mask.txt $protocolDTI/List10_train_T2.txt $protocolDTI/List20_train_FA.txt $protocol/List3_train_ficvf.txt $protocol/List4_train_fiso.txt $protocol/List5_train_odi.txt  $OUTPUTDIR $proto $seed

python dictnet_test_invivo.py $protocol/List1_train_norm_dwi.txt $protocol/List6_test_norm_dwi.txt $protocol/List7_test_brain_mask.txt $protocolDTI/List11_test_T2.txt $protocolDTI/List21_test_FA.txt $OUTPUTDIR $proto $seed



#List1_train_norm_dwi.txt                       b0 (eddy corrected + normalized)
#List2_train_brain_mask.txt                     mask (nodif_brain_mask)
#List3_train_ficvf.txt                          ICVF (NODDI generated)
#List4_train_fiso.txt 						    ISO  (NODDI generated)
#List5_train_odi.txt 							OD (NODDI generated)
#List6_test_norm_dwi.txt                    	b0 test images (eddy corrected + normalized)
#List7_test_brain_mask.txt				        mask (nodif_brain_mask from fsl)
