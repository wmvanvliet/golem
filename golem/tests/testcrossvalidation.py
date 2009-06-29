import unittest, operator
import numpy as np
from .. import cv, data

class TestCrossValidation(unittest.TestCase):
  def setUp(self):
    self.d = data.gaussian_dataset([30, 20, 10])

  def test_stratified_split(self):
    '''Test stratified splitting of a DataSet'''
    d = self.d

    subsets = cv.stratified_split(d, 10)
    self.assertEqual(len(subsets), 10)
    for s in subsets:
      self.assertEqual(s.ninstances_per_class, [3, 2, 1])
    
    self.check_disjoint(subsets)

    d2 = reduce(operator.add, subsets)
    self.assertEqual(d.sorted(), d2.sorted())
  
  def test_sequential_split(self):
    '''Test sequentially splitting of a DataSet'''
    d = self.d
    for K in [3, 9, 10]:
      subsets = cv.sequential_split(d, K)
      self.assertEqual(len(subsets), K)
      for s in subsets:
        self.assert_(s.ninstances >= np.floor(d.ninstances/float(K)))
        self.assert_(s.ninstances <= np.ceil(d.ninstances/float(K)))
      
      self.check_disjoint(subsets)
      d2 = reduce(operator.add, subsets)
      self.assertEqual(d.sorted(), d2.sorted())
  
  def test_crossvalidation_sets(self):
    '''Test the generation of cross-validation training and test sets'''
    subsets = cv.stratified_split(self.d, 8)
    cv_sets = [tu for tu in cv.cross_validation_sets(subsets)]
    self.assertEqual(len(cv_sets), 8)
    for (tr, te) in cv_sets:
      self.assertEqual((tr + te).sorted(), self.d.sorted()) # tr + te == d

  def check_disjoint(self, subsets):
    '''Test that subsets are disjoint datasets'''
    for (tr, te) in cv.cross_validation_sets(subsets):
      intersection = set(tr.ids.flatten()).intersection(te.ids.flatten()) 
      self.assertEqual(len(intersection), 0)
