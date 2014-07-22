'''
Created on Nov 2, 2013

@author: pham
'''

#import sys
import numpy as np
from os.path import exists

from composes.transformation.scaling.row_normalization import RowNormalization
from composes.composition.lexical_function import LexicalFunction
from composes.utils.regression_learner import RidgeRegressionLearner
from composes.semantic_space.space import Space
from composes.utils import io_utils
from composes.utils.space_utils import list2dict

from examples import lexical_space


def get_training_list(observe_space, split_position, function_pos):
    phrase_list = observe_space.id2row
    training_list = []
    for phrase in phrase_list:
        elements = phrase.split("_")
        first_word = "_".join(elements[0:split_position])
        second_word = "_".join(elements[split_position:])
        if function_pos == 0:
            training_list.append((first_word, second_word, phrase))
        else:
            training_list.append((second_word, first_word, phrase))
    print "training data sample:"
    print training_list[0]
    return training_list

def train_one_space(core_space, per_space, func_pos, no_log_space):
    param_range = np.logspace(-1,1,no_log_space)
    training_list = get_training_list(per_space, 1, func_pos)
    per_space = per_space.apply(RowNormalization())
    composition_model = LexicalFunction(
                        learner=RidgeRegressionLearner(param_range=param_range,
                                                       intercept=False))
    composition_model.train(training_list, core_space, per_space)
    return composition_model.function_space


def train_all_spaces(core_space, an_dn_space, pn_space, sv_space, vo_space, cn_space, normed):
    core_space = core_space.apply(RowNormalization())
    print "train adj, det"
    a_d_space = train_one_space(core_space, an_dn_space, 0, 3)
    print "train prep"
    prep_space = train_one_space(core_space, pn_space, 1, 3)
    print "train vo"
    v_obj_space = train_one_space(core_space, vo_space, 0, 4)
    print "train sv"
    v_subj_space = train_one_space(core_space, sv_space, 1, 4)
    
    new_v_obj_rows = [row + ".objmat" for row in v_obj_space.id2row]
    v_obj_space._id2row = new_v_obj_rows
    v_obj_space._row2id = list2dict(new_v_obj_rows)
    
    new_v_subj_rows = [row + ".subjmat" for row in v_subj_space.id2row]
    v_subj_space._id2row = new_v_subj_rows
    v_subj_space._row2id = list2dict(new_v_subj_rows)
    
    all_mat_space = Space.vstack(a_d_space, prep_space)
    all_mat_space = Space.vstack(v_obj_space, all_mat_space)
    all_mat_space = Space.vstack(v_subj_space, all_mat_space)
    return all_mat_space

def train_from_core(core_file, output_file_prefix):
    an_dn_file = core_file.replace("core","sick_an_dn")
    pn_file = core_file.replace("core","sick_pn")#.replace(".pkl",".dm")
    sv_file = core_file.replace("core","sick_sv")#.replace(".pkl",".dm")
    vo_file = core_file.replace("core","sick_vo")#.replace(".pkl",".dm")
    
    if (not exists(core_file) or not exists(pn_file) or not exists(sv_file)
        or not exists(vo_file) or not exists(an_dn_file)):
        print "some file doesn't exist"
        print core_file, an_dn_file, pn_file, sv_file, vo_file
    
    print "load core"
    core_space = io_utils.load(core_file, Space)
    print "load an dn"
    
    an_dn_space = io_utils.load(an_dn_file, Space)
    print "load pn"
    pn_space = io_utils.load(pn_file, Space)
    print "load sv"
    sv_space = io_utils.load(sv_file, Space)
    print "load vo"
    vo_space = io_utils.load(vo_file, Space)
    
    print "start training"
    all_mat_space_normed = train_all_spaces(core_space, an_dn_space, 
                                     pn_space, sv_space, vo_space,
                                     True)
    print "exporting trained file"
    all_mat_space_normed.export(output_file_prefix, format="dm")
    del all_mat_space_normed
    print "DONE"
    
if __name__ == '__main__':
    
    train_from_core(lexical_space)
