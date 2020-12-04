function plotdictNet_protocolwise(protocols,type,gTruth,NDI_number,width)
 
    m=[];s=[];
    for p=protocols
        protocol=char(p);
        switch type
            case 'iso' % b1000
                if NDI_number==100
                    idx=[ 1 2 3 4 5 6 7 8 ];
                else
                    idx=[0 3]+NDI_number;
                end          
                tmpgT=niftiread([pwd '/GroundTruth/fiso.nii' ]);

                if length(protocol)>2 % If multishell, get result without the use of FA and S0
                    tmp=niftiread([pwd '/input/' protocol '/DictNet_withoutFA_T2/0_DictNet_fISO.nii.gz' ]);
                else 
                    tmp=niftiread([pwd '/input/' protocol '/DictNet_Out/0_DictNet_fISO.nii.gz' ]);
                end
                %isos=[0 0.12 0.25 0.4 0.50 0.75 0.9 1];
                gt_iso=tmpgT(:,:,idx);
                out_iso=tmp(:,:,idx);
                m=[m,mean(out_iso(gt_iso==gTruth))];
                s=[s,std(out_iso(gt_iso==gTruth))];

        end


    end

    x=1:length(protocols);
    e=errorbar(x-width,m,s,'^'); %,'MarkerFaceColor','b');
    e.LineWidth=1;
    % e.Color='b';
    e.MarkerFaceColor=e.Color;
    xticks(x);
    axis([0 length(protocols)+1 0 1])
    for p=1:length(protocols)
            labels{p}=string([char(protocols(p))]);
    end
     xticklabels(labels);
     xtickangle(45)
     yticks(0:0.2:1);
    % grid on
    hold on
    yT = gTruth;


    xT=-1:(max(x)+1);
    plot(xT,yT*ones(size(xT)),'k--','LineWidth',1.5)
    hold off
end