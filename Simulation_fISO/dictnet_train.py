'''
@ DictNet Author - Abrar Faiyaz (abrarfaiyaz.iutcse@gmail.com)
@ Nov, 2019

'''


# Stochastic Initializer Seed Value. (Defined same for training and test cases.)
# Helps to reproduce training cases.

seedvalue=47;

# Setting up all Imports 
# Keras Version- keras/2.0.5
# GPU library Version- cudnn/9.0-7 (Optional)


import os
import sys
import time
import numpy as np
import nibabel as nib
from keras.optimizers import Adam
from keras.models import Sequential, Model
from keras.layers.advanced_activations import ThresholdedReLU
from keras.layers import merge, Dense, Input, Activation, add, multiply
from keras.constraints import nonneg
from keras.layers.merge import add
from keras.constraints import nonneg
from keras.callbacks import EarlyStopping



# Initialization
dwis = None;masks = None;t2List=None;faList=None;
ndiList = None; isoList = None; odiList = None;
directory = None;
protocol=None;


# Fetch arguments
if len(sys.argv) == 11:
    dwis = sys.argv[1]
    masks = sys.argv[2]
    t2List= sys.argv[3]
    faList=sys.argv[4]
    ndiList = sys.argv[5]
    isoList = sys.argv[6]
    odiList = sys.argv[7]
    directory = sys.argv[8]
    protocol= sys.argv[9]
    seedvalue= int(sys.argv[10])
else:
    print("Check Input Arguments")

if os.path.exists(directory) == False:
    os.mkdir(directory)

# Timer Init
start = time.time()

#### Training Phase

print("... Training Phase ...")    

# Load Images

print("Load Images ...")    

with open(dwis) as f:
    allDwiLocs = f.readlines()
    allDwiLocs = [ x.strip('\n') for x in allDwiLocs ]

with open(masks) as f:
    allMaskLocs = f.readlines()
    allMaskLocs = [ x.strip('\n') for x in allMaskLocs ]

with open(t2List) as f:
    allT2Locs = f.readlines()
    allT2Locs = [ x.strip('\n') for x in allT2Locs ]

with open(faList) as f:
    allFALocs = f.readlines()
    allFALocs = [ x.strip('\n') for x in allFALocs ]

with open(ndiList) as f:
    allNDILocs = f.readlines()
    allNDILocs = [ x.strip('\n') for x in allNDILocs ]
with open(isoList) as f:
    allISOLocs = f.readlines()
    allISOLocs = [ x.strip('\n') for x in allISOLocs ]
with open(odiList) as f:
    allODILocs = f.readlines()
    allODILocs = [ x.strip('\n') for x in allODILocs ]


# Setting Up voxels 
nVox = 0
for iMask in range(len(allMaskLocs)):
    print("Subject- %d" % iMask)
    mask = nib.load(allMaskLocs[iMask]).get_data()
    # Count number of voxels
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            for k in range(mask.shape[2]):
                if mask[i,j,k] > 0:
                    nVox = nVox + 1
     
neighbor_size = 27        
dwi = nib.load(allDwiLocs[0]).get_data()  
comps = dwi.shape[3]     
featurenumbers=3            
dwiTraining = np.zeros([nVox, dwi.shape[3]])   #dwiTraining = np.zeros([nVox, dwi.shape[3]*neighbor_size])
t2Training = np.zeros([nVox, 1])
FATraining = np.zeros([nVox, 1])
icvfTraining = np.zeros([nVox, 1])
isoTraining = np.zeros([nVox, 1])
odTraining = np.zeros([nVox, 1])
constant_input_d=np.zeros([nVox, dwi.shape[3]])

print("Initializing Voxel List")
   
nVox = 0
np.random.seed(seedvalue)
np_var = np.random.uniform(0, 1, size=(1,comps)) 


for iMask in range(len(allDwiLocs)):
    print("Setting Voxel List for Subject: %d" % iMask)
    dwi_nii = nib.load(allDwiLocs[iMask])
    dwi = dwi_nii.get_data()
    mask = nib.load(allMaskLocs[iMask]).get_data()
    t2 = nib.load(allT2Locs[iMask]).get_data()
    FA = nib.load(allFALocs[iMask]).get_data()
    icvf = nib.load(allNDILocs[iMask]).get_data()
    iso = nib.load(allISOLocs[iMask]).get_data()
    od = nib.load(allODILocs[iMask]).get_data()
    # number of voxels
    for i in range(dwi.shape[0]):
        for j in range(dwi.shape[1]):
            for k in range(dwi.shape[2]):
                if mask[i,j,k] > 0:
                    icvfTraining[nVox,0] = icvf[i,j,k]
                    isoTraining[nVox,0] = iso[i,j,k]
                    odTraining[nVox,0] = od[i,j,k]
                    t2Training[nVox,0] = t2[i,j,k]
                    FATraining[nVox,0] = FA[i,j,k]
                    # Here getting the neighbour information in one input array for each voxel prediction 27*length of dwi data
                    constant_input_d[nVox,:]=np_var;
                    dwiTraining[nVox, :] = dwi[i, j, k, :]
                    nVox = nVox + 1

#%%
                
### DictNet Architecture (Author : Abrar Faiyaz)                  
print "Setup DictNet..."

nDict1 = 200
nDict2 = 50

ReLUThres = 0.01


inputs = Input(shape=(dwiTraining.shape[1],))
t2in=Input(shape=(1,))
FAin=Input(shape=(1,))
I = Sequential()
I.add(Dense(comps, activation='relu', bias = True, input_shape=(comps,))) #I is a network to address 3x3x3 neighbouring voxels --> *neighbor_size
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

#4 47
nL=1

L_T2 = Sequential() 
L_T2.add(Dense(nDict2, activation='sigmoid', use_bias = True,input_shape=(1,)))
L_T2.add(Dense(nL, activation='relu'))

o_T2=L_T2(t2in)

L_FA = Sequential() 
L_FA.add(Dense(nDict2, activation='sigmoid', use_bias = True,input_shape=(1,)))
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

epoch = 10
weight = [1.0] #weight = [1.0,0.0,0.0]

print "ReLUThres, epoch, nDict1, nDict2: ", \
ReLUThres, epoch, nDict1, nDict2


# Fit                  
print("Fitting...")
clf = Model(input=[inputs,t2in,FAin,d],output=[o_fISO]) #clf = Model(input=[inputs,t2in,d],output=[o_fISO,o_NDI,o_ODI])

load=0
if load==1:
    #protocol="P3"
    clf.load_weights("DictNet_" + protocol +"_"+ str(seedvalue)+ ".h5")

clf.compile(optimizer=Adam(lr=0.001), loss='mse', loss_weights = weight)

hist = clf.fit([dwiTraining,t2Training,FATraining,constant_input_d], [isoTraining], batch_size=128, nb_epoch=epoch, verbose=1, validation_split=0.15) 
#hist = clf.fit([dwiTraining,t2Training,constant_input_d], [isoTraining,icvfTraining, odTraining ], batch_size=128, nb_epoch=epoch, verbose=1, validation_split=0.1) 
print(hist.history)
end = time.time()
print("Training took %f" % (end-start))



####### Save Trained Network  #######
print("Save weights for Test Phase")    

start = time.time()

#save_model
save=1
if save==1:
    clf.save_weights("DictNet_"+ protocol +"_"+str(seedvalue)+".h5")

end = time.time()
print("Save Time - %d" % (end-start))
