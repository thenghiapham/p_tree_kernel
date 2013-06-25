'''
Created on Jun 25, 2013

@author: thenghiapham
'''
import unittest
from tree.syntactic_tree import SyntacticTree


class SyntacticTreeTest(unittest.TestCase):


    def setUp(self):
        self.xml_string1 = '''
        <ccg>
          <rule type="fa" cat="S[dcl]\NP">
            <lf start="1" span="1" word="plays" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
            <rule type="lex" cat="NP">
              <lf start="2" span="1" word="guitar" lemma="guitar" pos="NN" chunk="I-NP" entity="O" cat="N" />
            </rule>
          </rule>
        </ccg>'''
        
        self.xml_string2 = '''
        <ccg>
          <rule type="fa" cat="S[dcl]\NP">
            <lf start="1" span="1" word="plays" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
            <rule type="lex" cat="NP">
              <lf start="2" span="1" word="instrument" lemma="instrument" pos="NN" chunk="I-NP" entity="O" cat="N" />
            </rule>
          </rule>
        </ccg>'''
        self.tree_string1 = "(S[dcl]\\NP (<S[dcl]\\NP>/NP plays) (NP (N guitar)))"
        self.tree_string2 = "(S[dcl]\\NP (<S[dcl]\\NP>/NP plays) (NP (N instrument)))"


    def tearDown(self):
        pass


    def test_parse_tree(self):
        test_cases = [(self.xml_string1,self.tree_string1),
                     (self.xml_string2,self.tree_string2)]
        for xml_string, tree_string in test_cases:
            syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
            output_tree_string = str(syntactic_tree)
            self.assertEqual(tree_string,output_tree_string, 
                             "tree strings must be the same")
    def test_read_tree(self):
        test_cases = [self.tree_string1,
                      self.tree_string2]
        for tree_string in test_cases:
            syntactic_tree = SyntacticTree.read_tree(tree_string)
            output_tree_string = str(syntactic_tree)
            self.assertEqual(tree_string,output_tree_string, 
                             "tree strings must be the same")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()