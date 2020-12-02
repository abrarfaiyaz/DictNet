seedvalue=47

import sys
import os
import nibabel as nib
import numpy as np
from keras.models import Sequential, Model
from keras.layers.core import Lambda
from keras.optimizers import Adam
from keras.layers.advanced_activations import ThresholdedReLU
from keras.layers import merge, Dense, Input, Activation, add, multiply
from keras.constraints import nonneg
from keras.layers.merge import add
from keras.callbacks import EarlyStopping
import time

    
dwinames = None
directory = None
testdwinames = None
testt2names=None
testFAnames=None
testmasknames = None
protocol=None
seedvalue=None

    

if len(sys.argv) == 9:
    dwinames = sys.argv[1]
    testdwinames = sys.argv[2]
    testmasknames = sys.argv[3]
    testt2names=sys.argv[4]
    testFAnames=sys.argv[5]
    directory = sys.argv[6]
    protocol= sys.argv[7]
    seedvalue= int(sys.argv[8])
else:
    print("Check Input Arguments")
if os.path.exists(directory) == False:
    os.mkdir(directory)
start = time.time()
 

#### Determine input shape
print("Determine Input Shape...")    

with open(dwinames) as f:
    allDwiNames = f.readlines()


allDwiNames = [x.strip('\n') for x in allDwiNames]

neighbor_size = 27        
dwi = nib.load(allDwiNames[0]).get_data()  
comps = dwi.shape[3]  



### DictNet Architecture (Abrar Faiyaz)                  
print "Setup DictNet..."

nDict1 = 200
nDict2 = 50

ReLUThres = 0.01


inputs = Input(shape=(dwi.shape[3]*neighbor_size,))
t2in=Input(shape=(neighbor_size,))
FAin=Input(shape=(neighbor_size,))
I = Sequential()
I.add(Dense(comps, activation='relu', bias = True, input_shape=(comps*neighbor_size,))) #I is a network to address 3x3x3 neighbouring voxels --> *neighbor_size
smooth_inputs = I(inputs)

L= Dense(nDict1, activation='sigmoid', use_bias = True)(smooth_inputs)

# Define Stochastic Input layer
d=Input(shape=(comps,))
D = Sequential() 
D.add(Dense(nDict1, activation='sigmoid', use_bias = True, input_shape=(comps,)))


r_din = ThresholdedReLU(theta = ReLUThres)(d)

# Skipping IHT iterations
LD=add([L,D(d)])
r_din = ThresholdedReLU(theta = ReLUThres)(LD)

# Defining Subnetworks
L_NDI = Sequential()
L_NDI.add(Dense(nDict2, input_dim = nDict1, activation='relu'))
L_NDI.add(Dense(1, activation='relu'))

L_OD= Sequential()
L_OD.add(Dense(nDict2, input_dim = nDict1, activation='relu'))
L_OD.add(Dense(1, activation='relu'))


nL=4;

L_T2 = Sequential() 
L_T2.add(Dense(nDict2, activation='sigmoid', use_bias = True,input_shape=(neighbor_size,)))
L_T2.add(Dense(nL, activation='relu'))

o_T2=L_T2(t2in)

L_FA = Sequential() 
L_FA.add(Dense(nDict2, activation='sigmoid', use_bias = True,input_shape=(neighbor_size,)))
L_FA.add(Dense(nL, activation='relu'))

o_FA=L_FA(FAin)

L_aISO= Sequential()
L_aISO.add(Dense(nDict2, input_dim = nDict1, activation='relu'))
L_aISO.add(Dense(nL, activation='relu'))

LT2_fISO=add([L_aISO(r_din),o_T2,o_FA])

r2_din = ThresholdedReLU(theta = ReLUThres)(LT2_fISO)

L_fISO= Sequential()
L_fISO.add(Dense(4, input_dim = nL, activation='relu'))
L_fISO.add(Dense(1, activation='relu'))



#o_NDI=L_NDI(r_din)
#o_ODI=L_OD(r_din)
o_fISO=L_fISO(r2_din)


weight = [1.0]
print "nDict1, nDict2: ", \
nDict1, nDict2
### fitting the model ###                    
print("Fitting")

clf = Model(input=[inputs,t2in,FAin,d],output=[o_fISO]) #clf = Model(input=[inputs,t2in,FAin,d],output=[o_fISO,o_NDI,o_ODI])

# Load WeightVector (Always)
load=1
if load==1:
    clf.load_weights("DictNet2_" + protocol +"_"+ str(seedvalue)+ ".h5")


clf.compile(optimizer=Adam(lr=0.001), loss='mse', loss_weights = weight)
end = time.time()
print("Loading time %f" % (end-start))



###### Test #######
print("Test Phase")    

start = time.time()
with open(testdwinames) as f:
    allTestDwiNames = f.readlines()
with open(testmasknames) as f:
    allTestMaskNames = f.readlines()
with open(testt2names) as f:
    allTestT2Names = f.readlines()
with open(testFAnames) as f:
    allTestFANames = f.readlines()

allTestDwiNames = [x.strip('\n') for x in allTestDwiNames]
allTestMaskNames = [x.strip('\n') for x in allTestMaskNames]
allTestT2Names = [x.strip('\n') for x in allTestT2Names]
allTestFANames = [x.strip('\n') for x in allTestFANames]
#save_model
'''
save=0
if save==1:
    name_af=allTestDwiNames[0]
    a,b=name_af.split('protocolwise_tmp/')
    name_af,c=b.split('/nNODDI_DWI')
    clf.save_weights("AFnet_"+ name_af +".h5")
'''

for iMask in range(len(allTestDwiNames)):
    name_af=allTestDwiNames[iMask]
    #a,b=name_af.split('DataPrep/')
    #name_af,c=b.split('//protocolwise_tmp')
    ##name_af = name_af.strip('/scratch/mdoyley_lab/afaiyaz/HCP/DataPrep/*/T1w/Diffusion/protocolwise_tmp/*/nNODDI_DWI.nii\n')
    print("Processing Subject: %d" % iMask)
    #### load images
    print(str(iMask) +" "+ str(name_af))
    dwi_nii = nib.load(allTestDwiNames[iMask])
    dwi = dwi_nii.get_data()
    mask = nib.load(allTestMaskNames[iMask]).get_data()
    t2= nib.load(allTestT2Names[iMask]).get_data()
    FA= nib.load(allTestFANames[iMask]).get_data()
    print("Counting Voxels")
    nVox = 0
    for i in range(dwi.shape[0]):
        for j in range(dwi.shape[1]):
            for k in range(dwi.shape[2]):
                if mask[i,j,k] > 0:
                    nVox = nVox + 1
                    
    voxelList = np.zeros([nVox, 3], int)
    dwiTest = np.zeros([nVox, dwi.shape[3]*neighbor_size])
    t2Test=np.zeros([nVox, neighbor_size])
    FATest=np.zeros([nVox, neighbor_size])
    constant_input_d=np.zeros([nVox, dwi.shape[3]])
    np.random.seed(seedvalue)
    np_var = np.random.uniform(0, 1, size=(1,comps))
    print("Setting Voxels")
    nVox = 0
    for i in range(dwi.shape[0]):
        for j in range(dwi.shape[1]):
            for k in range(dwi.shape[2]):
                if mask[i,j,k] > 0:
                    constant_input_d[nVox,:]=np_var;
                    tcount=0
                    for ii in [-1,0,1]:
                        for jj in [-1,0,1]:
                            for kk in [-1,0,1]:
                                if i + ii >= 0 and i + ii < dwi.shape[0] and j + jj >= 0 and j + jj < dwi.shape[1] \
                                    and k + kk >= 0 and k + kk < dwi.shape[2] and mask[i + ii, j + jj, k + kk] > 0:  
                                    dwiTest[nVox, ((ii+1)*9 + (jj+1)*3 + (kk+1))*dwi.shape[3]:((ii+1)*9 + (jj+1)*3 + (kk+1) + 1)*dwi.shape[3]] = dwi[i+ii,j+jj,k+kk,:]
                                    t2Test[nVox,tcount]=t2[i+ii,j+jj,k+kk]
                                    FATest[nVox,tcount]=FA[i+ii,j+jj,k+kk]
                                else:
                                    dwiTest[nVox, ((ii+1)*9 + (jj+1)*3 + (kk+1))*dwi.shape[3]:((ii+1)*9 + (jj+1)*3 + (kk+1) + 1)*dwi.shape[3]] = dwi[i,j,k,:]
                                    t2Test[nVox,tcount]=t2[i,j,k]
                                    FATest[nVox,tcount]=FA[i,j,k]
                                tcount=tcount+1
                    voxelList[nVox,0] = i
                    voxelList[nVox,1] = j
                    voxelList[nVox,2] = k
                    nVox = nVox + 1
    rows = mask.shape[0]
    cols = mask.shape[1]
    slices = mask.shape[2]
    
    #NDI = np.zeros([rows,cols,slices])
    #ODI = np.zeros([rows,cols,slices])
    fISO = np.zeros([rows,cols,slices])
    
    print("Computing")
    fISOList = clf.predict([dwiTest,t2Test,FATest,constant_input_d]) #fISOList,NDIList, ODIList  = clf.predict([dwiTest,t2Test,FATest,constant_input_d])
    
    for nVox in range(voxelList.shape[0]):
        x = voxelList[nVox,0]
        y = voxelList[nVox,1]
        z = voxelList[nVox,2]
        #NDI[x,y,z] = NDIList[nVox,0]
        #ODI[x,y,z] = ODIList[nVox,0]
        fISO[x,y,z] = fISOList[nVox,0]
            
    hdr = dwi_nii.header
    #NDI_nii = nib.Nifti1Image(NDI, dwi_nii.get_affine(), hdr)
    #NDI_name = os.path.join(directory,str(iMask)+"_DictNet_NDI.nii.gz")
    #NDI_nii.to_filename(NDI_name)
    
    #ODI_nii = nib.Nifti1Image(ODI, dwi_nii.get_affine(), hdr)
    #ODI_name = os.path.join(directory,str(iMask)+"_DictNet_ODI.nii.gz")
    #ODI_nii.to_filename(ODI_name)
    
    fISO_nii = nib.Nifti1Image(fISO, dwi_nii.get_affine(), hdr)
    fISO_name = os.path.join(directory,str(iMask)+"_DictNet_fISO.nii.gz")
    fISO_nii.to_filename(fISO_name)
    del dwi_nii

end = time.time()
print("Test time %d" % (end-start))
