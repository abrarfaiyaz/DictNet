%% FIGURE 5 (DLpN Manuscript)

%% iso
data='Synth';
type='iso';
PMEDN=false;
protocols=["P1","P2","P3","P12","P13","P23","Pall"];

gTruths=[0 0.12 0.4 .75 1];
figure('Renderer','painters','Position',[202,1138,1348,822]),
c=0;

ndiarr=[0.2,0.4,0.6,0.8];
c1=0;
c2=0;
for ndi=[1,2,3,4] % defined in plot functions (Based on GT NDI in "GroundTruth" directory)
    for gTruth=gTruths
        c=c+1;
        subplot(4,length(gTruths),c) %change(1) below
        switch data
        case 'Synth'
            wd=0.2; % group wise width in plot
            plotdictNet_protocolwise(protocols,type,gTruth,ndi,wd);
            hold on
            plotNODDI_protocolwise(protocols,type,gTruth,ndi,wd);
            if c<=5 %formatting plot title and ylabel
                c2=c2+1;
                title({[char(64+c2)],['f_{ISO} GT= ' num2str(gTruths(c2))] },'fontweight','bold');
            end
            if mod(c,length(gTruths))==1
                c1=c1+1;
                ylabel({['NDI=' num2str(ndiarr(c1))],' f_{ISO}'},'fontweight','bold');
            end
        end
    end
end


sgtitle(["DictNet and NODDI generated f_{ISO} (Synthetic data)", "Shown for NDI 0.2, 0.4, 0.6, 0.8"]);
legend({'DictNet','GT','NODDI'},'Location','best')
% saveas(gcf, 'Figure6_dictnet_iso_NDIwisefISO', 'fig')