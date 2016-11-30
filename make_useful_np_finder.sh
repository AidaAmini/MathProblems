#!/bin/bash
# python FeatureFinder_usefull_np.py 0 50 "train_np_type_fv.txt" 0
# python FeatureFinder_usefull_np.py 50 250 "test_np_type_fv.txt" 0
# cp train_np_type_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cp test_np_type_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# java -Xmx2048m -classpath libsvm.jar svm_train 
java -Xmx2048m -classpath libsvm.jar svm_train -w1 8 -w-1 1 -b 1 -c 10 train_np_type_fv.txt m_np_type.txt
java -Xmx2048m -classpath libsvm.jar svm_predict test_np_type_fv.txt m_np_type.txt s_np_type.txt
cp s_np_type.txt /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
cd /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# python normalize_probs_by_weights.py 0
python calcPrecisionRecall.py "s_np_type.txt" "test_np_type_fv.txt" 0 0 50 250
python np_recognize.py 50 250 'type' 0
# python calcPrecisionRecall.py "s_np_type_norm.txt" "test_np_type_fv.txt" 0 0 50 250

# #for entities
# python FeatureFinder_usefull_np.py 0 50 "train_np_entity_fv.txt" 1
# python FeatureFinder_usefull_np.py 50 250 "test_np_entity_fv.txt" 1
# cp train_np_entity_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cp test_np_entity_fv.txt /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# cd /Users/amini91/Documents/workspace/LMAndSRLtestForCat/
# java -Xmx2048m -classpath libsvm.jar svm_train -w1 3 -w-1 1 train_np_entity_fv.txt m_np_entity.txt
# java -Xmx2048m -classpath libsvm.jar svm_predict test_np_entity_fv.txt m_np_entity.txt s_np_entity.txt
# cp s_np_entity.txt /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# cd /Users/amini91/Documents/Docs/UW/Research/cleanFormat/
# python normalize_probs_by_weights.py 1
# python calcPrecisionRecall.py "s_np_entity.txt" "test_np_entity_fv.txt" 0 1 50 250
# python np_recognize.py 50 250 'entity' 1
# python calcPrecisionRecall.py "s_np_entity_norm.txt" "test_np_entity_fv.txt" 0 1 50 250
