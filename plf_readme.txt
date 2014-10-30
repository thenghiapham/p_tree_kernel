The source code for plf model is at
https://github.com/thenghiapham/p_tree_kernel

Examples of how to use the code are in examples/train_plf.py, examples/compute_sentence_vectors_papfunc.py, examples/compute_sentence_symbolic_representation.py
In order to use the code, you need to download DISSECT (https://github.com/composes-toolkit/dissect) and add the path to this code (and DISSECT) to your PYTHONPATH 

STRUCTURE OF THE CODE
tree_kernel directory contains code for computing vectors for sentences. Two subdirectories are of use here.

+ /examples: contains example scripts that use our class code.
  In this subdirectory: There are 3 important files and 1 subdirectory
  - compute_sentence_symbolic_representation.py:  is a script that computes and writes to file symbolic representations of vector-matrix structures. It takes as command line arguments the name of a file with CCG parsed sentences, an output file name, and spaces of lexical vectors and matrices. Details on how to use it are in the comments near the beginning of the file
  - compute_sentence_vectors_papfunc.py:  is a script that computes and writes to file vector-matrix structures, both in symbolic and in numeric representation. It takes as command line arguments the name of a directory with xml files that contain CCG parsed sentences, an output file name prefix, and spaces of lexical vectors and matrices. Details on how to use it are in the comments near the beginning of the file
  - train_plf.py: a script that trains the matrices for adjs, determiners, prepositions, verbs for the plf model. Again, details on how to use it are in the comments near the beginning of the file
  - resource: a subdirectory that contains the sample data for the above scripts
  Some other files:
  - simple_test_papfunc.py	a simple test of Papfunc_SemanticNode (the main class) code
  - syntactic_tree_examples.py	a test of SyntacticTree code


+ /tree: contains the code of Papfunc class, the class of syntactic nodes with recursively computed compositional vector representations based on the practical lexical function composition model. There are several files in that directory:

  - papfunc.py:	the file containing Papfunc_SemanticNode class definition. Papfunc_SemanticNode, in addition to attributes of SemanticNode, is characterized by vector-matrix structures, represented in two ways. First, there is the numrep attribute, whose values are lists containing a vector and 0 or more matrices. Second, there is the matrep attribute, which contains symbolic representations of vector-matrix structures, encoded as a list of strings. Elements that we ignore in semantic computation are called 'empty'. Their matrep is ["empty"] and their numrep is an empty list.
  - node.py:	class definitions for the node class, which represents a node in a tree, which Papfunc_SemanticNode ultimately inherits
  - syntactic_node.py:	class definitions of SyntacticNode, which represents a node in a syntactic tree
  - syntactic_tree.py:	class definitions of SyntacticTree, a tree structure of syntactic nodes
  - semantic_node.py:	class definitions of SemanticNode, subclass of SyntaticNode; the key difference is that SemanticNode has the vector attribute, which contains the vector representation of the phrase dominated by the node
  - semantic_tree.py:	the code for trees of semantic nodes (syntactic trees with vector attribute)   
  - papfunc_intercept.py:	a version of papfunc for matrices trained with intercept
  


