cd cards_mu_Exp;
sed -i 's/0.0  2.0/0.0  1.0/g' *600*txt;
sed -i 's/Wjet_Norm_m   lnN     -         -    1.041     -      -        -/Wjet_Norm_m lnN - - 1.042 - - -\nCMS_scale_j lnN 1.029 1.044 0.983\/1.027 1.040\/0.960 1.041\/0.959 1.026\/0.974\nCMS_res_j lnN 1.008 1.035 0.992\/1.008 1.004\/0.996 1.009\/0.991 1.007\/0.993/g' *txt;
sed -i '/intf_vbfH/c\interf_qqH  lnN    -          1.100        -        -      -    -  ' *txt;
sed -i 's/intf_ggH/interf_ggH/g' *txt;
cd ..;
cd cards_el_Exp;
sed -i 's/Wjet_Norm_e   lnN     -         -    1.086     -      -        -/Wjet_Norm_e lnN - - 1.087 - - -\nCMS_scale_j lnN 1.034 1.072 0.979\/1.021 1.042\/0.958 1.044\/0.956 1.031\/0.969\nCMS_res_j lnN 1.007 1.030 0.989\/1.011 1.004\/0.996 1.014\/0.986 1.004\/0.996/g' *txt;
sed -i '/intf_vbfH/c\interf_qqH  lnN    -          1.100        -        -      -    -  ' *txt;
sed -i 's/0.0  2.0/0.0  1.0/g' *600*txt;
sed -i 's/intf_ggH/interf_ggH/g' *txt;
cd ..;
cd cards_em_Exp;
sed -i 's/Wjet_Norm_2jet lnN     -           -         1.218      -       -        -        -/Wjet_Norm_2jet lnN - - 1.215 - - - -\nCMS_scale_j lnN 1.050 1.045 0.959\/1.041 1.071\/0.929 1.071\/0.929 1.075\/0.925 1.046\/0.954\nCMS_res_j lnN 1.080 1.116 0.981\/1.019 1.051\/0.949 1.084\/0.916 1.043\/0.957 1.063\/0.937/g' *txt;
sed -i '/intf_vbfH/c\interf_qqH  lnN    -          1.100        -        -      -    -    - ' *txt;
sed -i 's/0.0  2.0/0.0  1.0/g' *600*txt;
sed -i 's/intf_ggH/interf_ggH/g' *txt;


