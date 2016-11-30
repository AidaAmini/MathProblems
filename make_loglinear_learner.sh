# python FeatureFinder_LogLinear_learner.py 0 350 "trainl.txt" 1 1 0
# python FeatureFinder_LogLinear_learner.py 350 400 "testl.txt" 1 1 1
cp trainl.txt loglinearPKG/
cp testl.txt loglinearPKG/
cp fv_label_map.txt loglinearPKG/
cd loglinearPKG/
python loglinear_procedure.py
# # mv score.txt s_joint.txt
cp score.txt ../
cd ../
python normalize_probs_by_weights.py 5
python calcPrecisionRecall.py "s_joint_norm.txt" "test_bin.txt" 3 0 200 249

# # cp loglinearPKG/score.txt .
# # python calcPrecisionRecall.py "score.txt" "test.txt" 3 0 150 249