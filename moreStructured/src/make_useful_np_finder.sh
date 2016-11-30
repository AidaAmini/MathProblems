# #!/bin/bash
python FeatureFinder_usefull_np.py 50 140 "train_np_fv.txt"
python FeatureFinder_usefull_np.py 0 50 "test_np_fv.txt"
cp train_np_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cp test_np_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# # java -Xmx2048m -classpath libsvm.jar svm_train -w1 2 -w-1 1 -b 1 -s 1 train_np_fv.txt m_np.txt 
java -Xmx2048m -classpath libsvm.jar svm_train -w1 4 -w-1 1 -c 50 -b 1 train_np_fv.txt m_np.txt
java -Xmx2048m -classpath libsvm.jar svm_predict -b 1 test_np_fv.txt m_np.txt s_np.txt
cp s_np.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
cp test_np_fv.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
cd /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
python normalize_probs_by_weights.py
python calcPrecisionRecall.py "s_norm.txt" "test_np_fv.txt"
python np_recognize.py
# python calcPrecisionRecall.py "s_norm.txt" "test_joint_fv.txt"
