# DictNet
Stochastic Sparse Dictionary based Learner for DLpN.



This is the code repository for the study <b>"DLpN: Single-Shell NODDI Using Deep Learner Estimated Isotropic Volume Fraction"</b>

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Graphical_Abstract.tiff)


To get access to the example HCP data and Synthetic Data with DLpN and DictNet Codes, Please follow-
https://rochester.box.com/s/lm30dl28tu60mok6dykr5khxefb3han2

# Prerequisites
  - Python (v2.7.16)
  - Keras (v2.0.5)
  - MATLAB 2019a (MathWorks Inc., Natick, MA, USA)
  - FSL (v6.0.0) and 
  - ANTs (v2.1.0). 
# Application on (low SNR) clinical CSVD dataset
## Comparison of DLpN derived NDI and fISO maps with NODDI_{Pall} in CSVD 
Coronal slices from a test subject with CSVD (characterized by high Fazekas score of 3, and lesion volume of 1.77 cm3). The NDI and fISO maps were computed with DLpN (single shell b=2000 s/mm2) and original NODDI (two-shells b=1000, 2000 s/mm2), and corresponding T2 FLAIR images showing lesions (indicated by red arrows). Lesions in both NDI and f_{ISO} maps are clearly visible. However, DLpN derived f_{ISO} shows better conspicuity than NODDI derived f_{ISO}.

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Application_on_CSVD.tiff)
## Data Quality Comparison (HCP vs CSVD)

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Data_SNR_Comaparison.png)

For additional queries or troubleshoot, please contact- afaiyaz@ur.rochester.edu

