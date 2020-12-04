%% Tested on Matlab 2019a

%% Getting started NODDI toolbox with DLpN
pathToExternal='/gpfs/fs2/scratch/mdoyley_lab/afaiyaz/DLpriorNODDI/DLpriorNODDI/SyntheticData_Exp/Simulation/'; % add path to 'external' directory
addpath(genpath([pathToExternal '/external'])); % To make sure NODDI toolbox is in path
nCore=2; % 24

%% DLpN routine using NODDI toolbox
dataName="101915"; % comment if running from bash script
Protocol="P2"; % comment if running from bash script

dataloc=[ pwd '/Data/' char(dataName) '/T1w/Diffusion/protocolwise_tmp/' char(Protocol) '/'];
maskloc=[pwd '/Data/' char(dataName) '/T1w/Diffusion/'];
priorloc=[ pathToExternal '/DictNet/Invivo/input/' char(Protocol) '/DictNet2_Out/' ];

cd(dataloc);

noddi_roi=['DLpN_roi_' char(dataName) '.mat'];
fittedParams=['DLpN_FittedParams_' char(dataName) '.mat'];
kappa_iso_save=true;

% Change the Prior Names here.
CreateROI_forDLpriorNODDI_P1S0([ char(dataloc) 'NODDI_DWI.nii'],[priorloc char(dataName) '_DictNet_fISO.nii.gz'],[char(maskloc) 'brain_mask.nii'],noddi_roi); 
protocol = FSL2Protocol([ char(Protocol) '.bval'],[ char(Protocol) '.bvec'],10);
noddi = MakeModel('WatsonSHStickTortIsoV_B0');
batch_fitting_DLpN(noddi_roi, protocol, noddi,fittedParams , nCore); 
SaveParamsAsNIfTI(fittedParams, noddi_roi, [char(maskloc) 'brain_mask.nii'], ['DLpN_' char(Protocol)],kappa_iso_save)



