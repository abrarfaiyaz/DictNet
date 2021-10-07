# ***DLpN: Single-Shell NODDI using dictionary learner estimated isotropic volume fraction***
Stochastic Sparse Dictionary based Learner for DLpN.



This is the code repository for the study <b>"DLpN: Single-Shell NODDI Using Deep Learner Estimated Isotropic Volume Fraction"</b>

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Graphical_Abstract.tiff)

https://rochester.box.com/s/lm30dl28tu60mok6dykr5khxefb3han2

## Prerequisites
  - Python (v2.7.16)
  - Keras (v2.0.5)
  - MATLAB 2019a (MathWorks Inc., Natick, MA, USA)
  - FSL (v6.0.0) and 
  - ANTs (v2.1.0). 
## Method
![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Method.tiff)
  (A) DictNet Training with at least two subjects with multishell data required. Training protocol must be multi-shelled, complementary to single shell test data.
  (B) NODDI (NDI and ODI) Estiamtion with f<sub>ISO</sub> derived from DictNet.

## Simulation (f<sub>ISO</sub> Estimation)
  - DictNet
  - FW (Pasternak<sup>[1](#1)</sup> algorithm used for single shell data and DIPY for multishell<sup>[2](#2)</sup>)
  - NODDI<sup>[3](#3)</sup>
  - PMEDN<sup>[4](#4)</sup>
![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/fISO_simulation.tiff)
## Application on (low SNR) clinical CSVD dataset
### Comparison of DLpN derived NDI and f<sub>ISO</sub> maps with NODDI<sub>Pall</sub> in CSVD 
Coronal slices from a test subject with CSVD (characterized by high Fazekas score of 3, and lesion volume of 1.77 cm<sup>3</sup>). The NDI and f<sub>ISO</sub> maps were computed with DLpN (single shell b=2000 s/mm<sup>2</sup>) and original NODDI (two-shells b=1000, 2000 s/mm<sup>2</sup>), and corresponding T2 FLAIR images showing lesions (indicated by red arrows). Lesions in both NDI and f<sub>ISO</sub> maps are clearly visible. However, DLpN derived f<sub>ISO</sub> shows better conspicuity than NODDI derived f<sub>ISO</sub>.

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Application_on_CSVD.tiff)
### Data Quality Comparison (HCP vs CSVD)

![Graphical Abstract](https://github.com/abrarfaiyaz/DictNet/blob/main/Data_SNR_Comparison.png)


### **Citation**

If you find our work useful in your research, please consider citing the pre-print (The peer reviwed article will be soon available online (Publisher: ***NMR in Biomedicine*** , Wiley)):

``` {.w3-panel .w3-leftbar .w3-light-grey}
@misc{faiyaz2021singleshell,
      title={Single-Shell NODDI Using Dictionary Learner Estimated Isotropic Volume Fraction}, 
      author={Abrar Faiyaz and Marvin Doyley and Giovanni Schifitto and Jianhui Zhong and Md Nasir Uddin},
      year={2021},
      eprint={2102.02772},
      archivePrefix={arXiv},
      primaryClass={physics.med-ph}
}
```
For additional queries or troubleshoot, please contact- afaiyaz@ur.rochester.edu

## References
<a id="1">[1]</a> 
Pasternak O, Sochen N, Gur Y, Intrator N, Assaf Y. Free water elimination and mapping from diffusion MRI. Magnetic Resonance in Medicine: An Official Journal of the International Society for Magnetic Resonance in Medicine. 2009;62(3):717-730.

<a id="2">[2]</a> 
Garyfallidis E, Brett M, Amirbekian B, et al. Dipy, a library for the analysis of diffusion MRI data. Frontiers in neuroinformatics. 2014;8:8

<a id="3">[3]</a> 
Zhang H, Schneider T, Wheeler-Kingshott CA, Alexander DC. NODDI: practical in vivo neurite orientation dispersion and density imaging of the human brain. Neuroimage. 2012;61(4):1000-1016.

<a id="4">[4]</a> 
Ye C. Estimation of tissue microstructure using a deep network inspired by a sparse reconstruction framework. Paper presented at: International Conference on Information Processing in Medical Imaging2017.
