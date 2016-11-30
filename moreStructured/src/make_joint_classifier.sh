# python FeatureFinder_joint_learner.py 0 35 "train_joint_fv.txt"
# python FeatureFinder_joint_learner.py 35 50 "test_joint_fv.txt"
# cp train_joint_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cp test_joint_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# java -Xmx2048m -classpath libsvm.jar svm_train -w1 20 -w0 1 -w2 10 -b 1 train_joint_fv.txt m.txt
# java -Xmx2048m -classpath libsvm.jar svm_predict -b 1 test_joint_fv.txt m.txt s.txt
# cp s.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
# cp test_joint_fv.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
cd /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
python normalize_probs_by_weights.py
python calcPrecisionRecall.py "s_norm_joint.txt" "test_joint_fv.txt"