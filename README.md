### Parts-of-Speech-Tagging
#### Aim of this project is to identify the parts of speech tag for each word in a sentence.
For Training annotated data Penn Treebank is used. (Training data and Testing data attached in this repository)

 **Methodology:**
 1. Tag sequence, and word tag sequence extraction from the training data
 2. Viterbi algorithm is used to get the parts of speech tag for each word for a given word in sequence.
 3. For missing tag on test set, top 5 frequent tag is assigned in viterbi algorithm and most probable tag will assigned as per viterbi algorithm

**Result**
* On large training set:*
  * Viterbi Accuracy on Test Set : 92.28%
  * Baseline Program Accuracy: 85.18% (Assigning the frequent tag)
