codePath=`pwd`

baseLoc=$codePath"/input/"
for protocol in "P1" "P2" "P3" "P12" "P13" "P23" "Pall"
do 
echo $baseLoc/$protocol/
sed -i "s|<code_loc>|$codePath|g" $baseLoc/$protocol/*.txt 

done

#TEST# sed -i "s|<code_loc>|$codePath|g" List1_train_norm_dwi.txt 
