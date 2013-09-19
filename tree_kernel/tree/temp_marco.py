from __future__ import print_function
from node import Node
from kernel_utils import type_utils
from tree.syntactic_tree import SyntacticTree
from xml.etree.ElementTree import ParseError
import re
import sys
from composes.semantic_space.space import Space
from composes.utils import io_utils

# This temporary module contains a function to perform lexical
# insertion, to be added as a constructor method to the SemanticNode
# class, and a simple function to test lexical insertion.
#
# More details follow with the various functions.

def adhoc_print_lexitems(infile,vecfilepref,matfilepref,outfilename=None):
# This adhoc function tests lexical insertion given an input file with
# CCG trees as produced by cctools parser using the XML format output
# option, an input file with the vector representations in dense
# matrix format and an input file with the matrix representations in
# dense matrix format (for the vector and matrix files, we request the
# prefix, and expect to find corresponding .dm and .rows
# files). Optionally, output can be sent to a file instead of stdout.

# Each input tree is printed in output, and for each terminal node the
# corresponding string-based and numerical representations are then
# printed

 if not outfilename:
  outfile=sys.stdout
 else:
  outfile=open(outfilename, 'w')
 
#  veclist=[]
#  matlist=[]
#  emptylist=[]

#  adhoc_prepare_dictionaries(infile,veclist,matlist)

 # reading the vector and matrix spaces
 vecspace = Space.build(data = vecfilepref + ".dm",
                       rows = vecfilepref + ".rows",
                       format = "dm")
 matspace = Space.build(data = matfilepref + ".dm",
                       rows = matfilepref + ".rows",
                       format = "dm")

 # processing the trees
 currtree=""
 intree=0
 with open(infile) as data:
  for line in data:
   if re.match("^<ccg>",line):
    currtree = currtree + line
    intree=1
   elif re.match("^</ccg>",line):
    currtree = currtree + line
    # print current tree
    print(currtree.strip('\n'),file=outfile)
    intree=0
    try:
     syntactic_tree = SyntacticTree.parse_tree_from_xml_string(currtree)
    except ParseError:
     print("THIS TREE WAS NOT XML-PARSABLE")
    # reset current tree
    currtree=""

    nodes = syntactic_tree.get_nodes()
    
    # traverse the nodes, if they are terminal nodes, print the node
    # lemma, pos and category, then the string representation of the
    # node semantics, then the corresponding numerical representation
    for node in nodes:
        if node.is_terminal():
         stringrep,numrep=insert_terminal_node_representation(node,vecspace,matspace,use_wordform=0)
         printstring = node.word + " " + node.lemma + " " + node.pos + " " + node.label + " " + str(stringrep) + " "
         for matvec in numrep:
          printstring += str(matvec)
         print (printstring.encode('ascii', 'ignore'),file=outfile)
#         print (node.word + " " + node.lemma + " " + node.pos + " " + node.label + " " + str(stringrep) + " " + str(numrep),file=outfile)
   elif intree:
    currtree = currtree + line
 data.close()
 if not outfilename==None:
  outfile.close()



# def adhoc_prepare_dictionaries(infile,veclist,matlist):
# # For now, this is simply an ad-hoc function reading a CCG XML file
# # and putting all the content word lemmas+shortpos in vector and mat
# # lists, as appropriate. Note that it uses the same POS shortening
# # rules as the lexical insertion function, which makes it very
# # brittle.
#  with open(infile) as data:
#   datalines=(line.rstrip('\n') for line in data)
#   for line in datalines:
#     matched = re.match(".*lemma=\"([^\"]*)\" pos=\"([^\"]*)\".* cat=\"([^\"]*)\"",line)
#     if matched:
#      lexitem=matched.group(1)
#      pos=matched.group(2)
#      label=matched.group(3)

#      matched = re.match("^[JNRV]",pos)
#      if matched:
#       shortpos = matched.group().lower()
#      elif lexitem=="that" and pos=="IN": # this is the mysterious way in
#                                       # which relative that is tagged
#       shortpos="o"
#      elif pos=="IN" or (pos=="TO" and label=="PP/NP"): # to used as preposition
#       shortpos="p"
#      elif pos=="PDT" or pos=="WDT":
#       shortpos="d" # pre-determiner and det, wh- (what, which, whatever, whichever)
#      elif pos=="DT":
#       if label=="NP": # things such as somebody should be
#                       # treated as nouns
#        shortpos="n"
#       else:
#        shortpos="d"
# #     elif pos=="WP": # treat pronouns like nouns
# #      shortpos="n"
#      else:
#       shortpos="o"

#      if not shortpos == "o":
#       lempos=lexitem + '-' + shortpos
#       veclist.append(lempos)
#       if shortpos == "v":
#        matlist.append(lempos + ".subjmat")
#        matlist.append(lempos + ".objmat")
#       elif not shortpos =="n":
#        matlist.append(lempos)

#  data.close()


def insert_terminal_node_representation(termnode,vecspace,matspace,use_wordform=0):
# This is the function performing lexical insertion. It expects a
# terminal syntactic node as input, as well as two DISSECT semantic
# spaces containing vectors and (flattened) matrices, respectively
# (that is, if the vectors have n dimensions, the "matrix" space must
# contain nxn-dimensional vectors).

# The vector space is expected to contain two special vectors, named
# as follows:
#
# - cg.onevec: a vector of 1s
# - cg.zerovec: a vector of 0s
#
# Similarly, the matrix space should contain:
#
# -cg.identmat: the (flattened) identity matrix
# -cg.zeromat: a flattened mmatrix of 0s

# Moreover, for verbs, the flattened matrices are expected to be
# suffixed by the strings .subjmat and .objmat, respectively.

# When looking if a terminal node lexical item is in the relevant
# space(s), by default, we work with lemmas, but there is an option to
# use word forms instead (what we would really need, I suspect, is to
# decide to use word or lemma on a POS-by-POS basis, e.g., we might
# want to distinguish singular from plural nouns, but use lemmas for
# verbs).

# We convert the POS to "shortpos"s that right now include the
# following types: d (determiner, including predeterminer), j
# (adjective), n (noun, including pronoun and proper name), r
# (adverb), p (preposition), o (everything else).

# The function returns a tuple made of two lists. The first list
# contains a string-representation of the vector and 0 or more
# matrices representing the terminal, the second contains the
# corresponding DISSECT objects. Note that for elements that are
# "empty" for our purposes, both lists contain just a string marking
# the fact that the item is empty (the string is prefixed by the node
# lexical item for the string representation, whereas it is just
# "empty" in the "numerical" representation). The naming conventions
# for the first list are as follows (where lempos stands for the
# lexical item -- by default lemma, but wordform if so requested --
# followed by shortpos):

# - lempos.empty: empty terminal for our purposes

# - lempos.lexvec: the item has a vector representation in the lexicon

# - lempos.onevec: the item has no lexical vector representation and
#   is represented by a vector of 1s

# - lempos.zerovec: the item has no lexical vector representation and
#   is represented by a vector of 0s

# - lempos.objmat: the object matrix associated to a verb in the
#   lexicon

# - lempos.subjmat: the subject matrix associated to a verb in the
#   lexicon

# - lempos.lexmat: the lexical matrix associated to a (non-verb) item

# - lempos.identmat: the item has no lexical matrix representation (or
#   not enough of them given its arity) and the identity matrix will
#   be used instead

# - lempos.zeromat: the item has no lexical matrix representation (or
#   not enough of them given its arity) and a matrix of 0s will be
#   used instead

# Note that the function assumes that matrices will be processed in
# stack order (last in, first out), for example, intransitive verbs
# are represented by vector, subject matrix, object matrix, in this
# order.

# TODOS:
#
# - decide if lemma or wordform on a POS-by-POS basis
#
# - add check for dimensionality of vectors/matrices (target
#   dimensionality to be passed as argument)
#
# - generate 0, 1 and identity matrices/vectors instead of getting
#   them from semantic space

 if not termnode.is_terminal():
  raise ValueError("insert_terminal_node_representation called on non-terminal node")
 
 stringstructure = []
 numericalstructure = []
 pos=termnode.pos
 label=termnode.label
 if not use_wordform:
  lexitem=termnode.lemma
 else:
  lexitem=termnode.word


 # retrieving the zero, one and identity matrix/vectors (might be a
 # waste of RAM, but makes code below cleaner)
 onevec=vecspace.get_row("cg.onevec")
 zerovec=vecspace.get_row("cg.zerovec")
 identmat=matspace.get_row("cg.identmat")
 zeromat=matspace.get_row("cg.zeromat")
 

 # get short pos code
 matched = re.match("^[JNRV]",pos)
 if matched:
  shortpos = matched.group().lower()
 elif termnode.lemma=="that" and pos=="IN": # this is the mysterious way in
                                   # which relative that is tagged
  shortpos="o"
 elif pos=="IN" or (pos=="TO" and label=="PP/NP"): # to used as preposition
  shortpos="p"
 elif pos=="PDT" or pos=="WDT":
  shortpos="d" # pre-determiner and det, wh- (what, which, whatever, whichever)
 elif pos=="DT":
  if label=="NP": # things such as somebody should be
                  # treated as nouns
   shortpos="n"
  else:
   shortpos="d"
# elif pos=="WP" or pos=="PRP": # treat pronouns like nouns
 elif pos=="PRP": # treat pronouns like nouns
  shortpos="n"
 else:
  shortpos="o"

 lempos=lexitem + '-' + shortpos

 # processing nouns (both common and proper)
 if shortpos=="n":
  # if the noun is in lexicon, return its vector, if not return the
  # 1-vector
  if lempos in vecspace.row2id:
   stringstructure.append(lempos + '.lexvec')
   numericalstructure.append(vecspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.onevec')
   numericalstructure.append(onevec)
  return (stringstructure,numericalstructure)

 # processing verbs (which might also include auxiliaries!)
 elif shortpos=="v":
  # first look for the vector corresponding to the verb, and insert
  # if no verb in lexicon, insert 0 vector
  if lempos in vecspace.row2id:
   stringstructure.append(lempos + '.lexvec')
   numericalstructure.append(vecspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.zerovec')
   numericalstructure.append(zerovec)
  
  # if verb is passive (including past participle), pick object
  # matrix, or identity if we don't have the verb in the lexicon
  if re.match("^S\[pss\]",label) or (pos == "VBN" and label=="N/N"):
   if lempos + '.objmat' in matspace.row2id:
    stringstructure.append(lempos + '.objmat')
    numericalstructure.append(matspace.get_row(lempos+'.objmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)

  # if verb is regular intransitive or present participle, look for
  # subject matrix in lexicon, if it is not there, insert identity mat
  elif re.match("^S[^\\\\/]*\\\\NP$",label) or label == "N/N":
   if lempos + '.subjmat' in matspace.row2id:
    stringstructure.append(lempos + '.subjmat')
    numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)
  
  # if verb is regular transitive, or tri-argumental with
  # prepositional third argument (that we treat as a normal
  # verb-modifying PP) add, one after the other, subject and object
  # matrix
  elif re.match("^\(S[^\\\\/]*\\\\NP\)/NP$",label) or  re.match("^\(\(S[^\\\\/]*\\\\NP\)/PP\)/NP",label):
   if lempos + '.subjmat' in matspace.row2id:
    stringstructure.append(lempos + '.subjmat')
    numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)
   if lempos + '.objmat' in matspace.row2id:
    stringstructure.append(lempos + '.objmat')
    numericalstructure.append(matspace.get_row(lempos+'.objmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)

  # ditransitive constructions: we insert subj and obj as usual, and
  # use zero (!!!) for the nearest argument (outermost matrix)
  elif re.match(".*S.*NP.*NP.*NP$",label):
   if lempos + '.subjmat' in matspace.row2id:
    stringstructure.append(lempos + '.subjmat')
    numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)
   if lempos + '.objmat' in matspace.row2id:
    stringstructure.append(lempos + '.objmat')
    numericalstructure.append(matspace.get_row(lempos+'.objmat'))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)
   # this is the innermost argument matrix
   stringstructure.append(lempos + '.zeromat')
   numericalstructure.append(zeromat)
  
  # "to be" (at least) can take a prepositional phrase as direct
  # object (to be in the park): since the preposition ins this case is
  # indistinguishable from the one that modifies VPs or adjectives, we
  # treat "to be" when it has category (S[dcl]\NP)/PP as a zero vector
  # and an identity matrix: this will result in the combination of "to
  # be" and the PP being the PP vector and the identity matrix
  # (identity matrix from to be plust zero matrix from PP), the
  # identity matrix will then be multiplied by the subject vector,
  # resulting in the sentence being represented by the sum of the
  # subject and PP vectors
  elif re.match("^\(S[^\\\\/]*\\\\NP\)/PP$",label): 
   stringstructure=[lempos + '.zerovec',lempos + '.identmat']
   numericalstructure=[zerovec,identmat]

  # finally, auxiliary and the like (including some pro constructions
  # that probably shouldn't be treated this way), if I'm right, are
  # always treated as VP modifiers, and we'll convert them to empty
  # elements
  elif re.match("^\(*S[^\\\\/]*\\\\NP\)/\(S[^\\\\/]*\\\\NP\)$",label):
   stringstructure=[lempos + '.empty']
   numericalstructure=["empty"]

  return (stringstructure,numericalstructure)
  # end of verb processing

 # processing adjectives and determiners 
 # we treat them in the same way, i.e., one vector (possibly 0) and
 # one matrix
 elif shortpos=="j" or shortpos=="d":
  # a vector from the lexicon or a 0 vector 
  if lempos in vecspace.row2id:
   stringstructure.append(lempos + '.lexvec')
   numericalstructure.append(vecspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.zerovec')
   numericalstructure.append(zerovec)
  
  # and now matrix, from lexicon or identity
  if lempos in matspace.row2id:
   stringstructure.append(lempos + '.lexmat')
   numericalstructure.append(matspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.identmat')
   numericalstructure.append(identmat)

  return (stringstructure,numericalstructure)
  # done with adjectives and determiners

 # handling adverbs
 elif shortpos=="r":

  # if the vector has no contentful matrix associated to it, we might
  # as well treat is as an empty element (NB: this means that we will
  # for now treat cases such as "John is here" as identical to
  # "John"!)
  if not (lempos in matspace.row2id):
   return ([lempos + '.empty'],["empty"])

  # a vector from the lexicon or a zero vector
  if lempos in vecspace.row2id:
   stringstructure.append(lempos + '.lexvec')
   numericalstructure.append(vecspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.zerovec')
   numericalstructure.append(zerovec)

  # NOT NEEDED FOR FOLLOWING BLOCK FOR NOW, AS WE DO NOT HANDLE THE
  # "is here" CASE!
  ## in predicative constructions
  ## this is all we need (this is here)
  # if re.match("S[^\\\\/]*\\\\NP$"):
  #  return (stringstructure,numericalstructure)
 
  # when adverb is sentence modifier (sadly he did it), we must add its 
  # matrix
  if re.match("^S[^\\\\/]*[\\\\/]S[^\\\\/]*$",label):
   stringstructure.append(lempos + '.lexmat')
   numericalstructure.append(matspace.get_row(lempos))

  # if the adverb is modifying an adjective or a VP, we must add as
  # inner matrix a 0 matrix that will be summed to the matrix of the
  # adj or VP, and an outer matrix as above (note that this should be
  # the only other case, so there is no need (I hope) for special
  # regexps!!!)
  # examples:
  #  <lf Astart="2" span="1" word="not" lemma="not" pos="RB" chunk="I-VP" entity="O" cat="(S\NP)\(S\NP)" />
  #  <lf start="2" span="1" word="not" lemma="not" pos="RB" chunk="I-ADJP" entity="O" cat="(S[adj]\NP)/(S[adj]\NP)" />
  #  <lf start="1" span="1" word="very" lemma="very" pos="RB" chunk="I-NP" entity="O" cat="(N/N)/(N/N)" />
  else:
   stringstructure.append(lempos + '.zeromat')
   numericalstructure.append(zeromat)
   stringstructure.append(lempos + '.lexmat')
   numericalstructure.append(matspace.get_row(lempos))

  return (stringstructure,numericalstructure)
  # done with adverbs

 # processing prepositions
 elif shortpos=="p":

  # a vector from the lexicon or a zero vector
  if lempos in vecspace.row2id:
   stringstructure.append(lempos + '.lexvec')
   numericalstructure.append(vecspace.get_row(lempos))
  else:
   stringstructure.append(lempos + '.zerovec')
   numericalstructure.append(zerovec)

  # if preposition is modifying a noun/np or sentence, we just need to
  # insert its meaningful lexical matrix, or identity
  if re.match("^\(NP\\\\NP\)/NP$",label) or re.match("^\(S/S\)/NP$",label):
   if lempos in matspace.row2id:
    stringstructure.append(lempos + '.lexmat')
    numericalstructure.append(matspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)

  # if instead preposition is modifying anything else (VP modifier, PP
  # argument of triargumental verb, adjective modifier, copula
  # argument), we must first insert a 0 matrix (to be combined with
  # the verb/adj matrix by summing), and then the contentful matrix
  # categories:
  # - VP modifier: ((S\NP)\(S\NP))/NP
  # - PP argument of tri-argumental verb: PP/NP
  # - copula argument: PP/NP
  # - adjective modifier: PP/NP
  else:
   stringstructure.append(lempos + '.zeromat')
   numericalstructure.append(zeromat)
   if lempos in matspace.row2id:
    stringstructure.append(lempos + '.lexmat')
    numericalstructure.append(matspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)

  return (stringstructure,numericalstructure)
  # done with preposition processing

 # default: we return an empty item
 return ([lempos + '.empty'],["empty"])
