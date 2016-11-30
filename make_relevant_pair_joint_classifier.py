# python Feature_finder_relevant_pairs.py 50 100 "train_fv_pair.txt" 0
# python Feature_finder_relevant_pairs.py 100 250 "test_fv_pair.txt" 0
# cp train_fv_pair.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cp test_fv_pair.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
java -Xmx2048m -classpath libsvm.jar svm_train -w1 14 -w-1 1 -c 0.10 train_fv_pair.txt m_pair.txt
java -Xmx2048m -classpath libsvm.jar svm_predict test_fv_pair.txt m_pair.txt s_pair.txt
cp s_pair.txt /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
cd /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
python normalize_probs_by_weights.py 2
python calcPrecisionRecall.py "s_pair.txt" "test_fv_pair.txt" 1 0 100 250