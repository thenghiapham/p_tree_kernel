'''
Created on Apr 26, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from tree.semantic_tree import SemanticTree
from tree.syntactic_tree import SyntacticTree
from kernel_utils.type_utils import assert_type
from kernel_utils.tree_utils import syntactic_tree_2_semantic_tree


from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity
from composes.composition.weighted_additive import WeightedAdditive

class SemanticTreeKernel(SyntacticTreeKernel):
    '''
    classdocs
    '''
    kernel_name = "semantic_kernel"

    def __init__(self, lambda_):
        '''
        Constructor
        '''
        super(SemanticTreeKernel, self).__init__(lambda_)
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree2, SemanticTree)
        return super(SemanticTreeKernel, self).dot_product(tree1,tree2)

    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if (node1.is_terminal() and node2.is_terminal() 
            and node1._label == node2._label):
            # TODO: word or lemma?
            if node1._word == node2._word: 
                delta_matrix[node2id1[node1],node2id2[node2]] = 1
            else:
                delta_matrix[node2id1[node1],node2id2[node2]] = CosSimilarity().get_sim(node1._vector,
                                                                                        node2._vector)
        else:
            SyntacticTreeKernel._delta(self, node1, node2, node2id1, node2id2, delta_matrix)
    
    
        
            
def test():
    #syntactic_tree1 = SyntacticTree.read_tree("VP (VBZ play-v) (NP (N guitar-n))")
    #syntactic_tree2 = SyntacticTree.read_tree("VP (VBZ play-v) (NP (N instrument-n))")
    
    xml_string1 = '''
    <ccg>
      <rule type="fa" cat="S[dcl]\NP">
        <lf start="1" span="1" word="play-v" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
        <rule type="lex" cat="NP">
          <lf start="2" span="1" word="guitar-n" lemma="guitar" pos="NN" chunk="I-NP" entity="O" cat="N" />
        </rule>
      </rule>
    </ccg>'''
    xml_string2 = '''
    <ccg>
      <rule type="fa" cat="S[dcl]\NP">
        <lf start="1" span="1" word="play-v" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
        <rule type="lex" cat="NP">
          <lf start="2" span="1" word="instrument-n" lemma="instrument" pos="NN" chunk="I-NP" entity="O" cat="N" />
        </rule>
      </rule>
    </ccg>'''
    syntactic_tree1 = SyntacticTree.parse_tree_from_xml_string(xml_string1)
    syntactic_tree2 = SyntacticTree.parse_tree_from_xml_string(xml_string2)
    lexical_space = io_utils.load("/home/thenghiapham/work/project/tree_kernel/spaces/lexical_ppmi_svd300.pkl")
    kernel = SemanticTreeKernel(1.0)
    composition_model = WeightedAdditive()
    semantic_tree1 = syntactic_tree_2_semantic_tree(syntactic_tree1, lexical_space, composition_model)
    semantic_tree2 = syntactic_tree_2_semantic_tree(syntactic_tree2, lexical_space, composition_model)
    print semantic_tree1
    print semantic_tree2
    print [node._label for node in semantic_tree1.get_nodes()] 
    print [node._label for node in semantic_tree2.get_nodes()]
    print "kernel:\n", kernel.dot_product(semantic_tree1, semantic_tree1)   
    print "kernel:\n", kernel.dot_product(semantic_tree1, semantic_tree2)   

if __name__ == '__main__':
    test()
    