# python FeatureFinder_joint_learner.py 0 350 "train_joint_fv.txt" 0
# python FeatureFinder_joint_learner.py 350 400 "test_joint_fv.txt" 0
# cp train_joint_fv.txt /Users/amini91/Documents/workspace/LMAndSsRLtestForCat/
# cp test_joint_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# # java -Xmx2048m -classpath libsvm.jar svm_train
# java -Xmx2048m -classpath libsvm.jar svm_train -w1 50 -w0 1 -w2 40 -w3 30 -b 1  train_joint_fv.txt m_joint.txt
# java -Xmx2048m -classpath libsvm.jar svm_predict -b 1 test_joint_fv.txt m_joint.txt s_joint2.txt
# cp s_joint2.txt /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# cd /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# python normalize_probs_by_weights.py 4
python calcPrecisionRecall.py "s_joint_norm.txt" "test_joint_fv.txt" 3 0 350 400
# python calcPrecisionRecall.py "score.txt" "test.txt" 3 0 150 249

# # # python Feature_finder_struct_disjoint.py 50 150 "train_joint_fv.txt" 0
# # # python Feature_finder_struct_disjoint.py 150 250 "test_str.txt" 0



# cp train_sanity.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cp test_sanity.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# # # java -Xmx2048m -classpath libsvm.jar svm_train
# java -Xmx2048m -classpath libsvm.jar svm_train -w1 50 -w-1 1 -h 0 train_sanity.txt m_sanity.txt
# java -Xmx2048m -classpath libsvm.jar svm_predict test_joint_fv.txt m_sanity.txt s_joint_test.txt
# cp s_joint_test.txt /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# cd /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# # python normalize_probs_by_weights.py 4
# python calcPrecisionRecall.py "s_joint_test.txt" "test_sanity.txt" 1 0 350 400
# # # python calcPrecisionRecall.py "score.txt" "test.txt" 3 0 150 249
