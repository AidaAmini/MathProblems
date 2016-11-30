python Feature_Finder_eq_noRel.py 140 170 "train_eq_no_fv.txt"
python Feature_Finder_eq_noRel.py 170 199 "test_eq_no_fv.txt"
cp test_eq_no_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cp train_eq_no_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
java -Xmx2048m -classpath libsvm.jar svm_train -w1 100 -w-1 1 train_eq_no_fv.txt m_eq.txt
java -Xmx2048m -classpath libsvm.jar svm_predict test_eq_no_fv.txt m_eq.txt s_eq.txt
cp s_eq.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
cp test_eq_no_fv.txt /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
cd /Users/amini91/Documents/Docs/UW/Research/PythonRikSuggestedFormat/
# python normalize_probs_by_weights.py
python calcPrecisionRecall.py "s_eq.txt" "test_eq_no_fv.txt"
