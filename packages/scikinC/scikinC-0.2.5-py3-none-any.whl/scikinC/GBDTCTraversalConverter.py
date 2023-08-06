import sys
from scikinC import BaseConverter
import numpy as np

from scikinC._tools import array2c

#class SmartFloat2Int:
#  def __init__(self, low, high):
#    self.low = low
#    self.high = high
#
#  def __call__(self, val):
#    low, high = self.low, self.high
#    if val > high: return 10000
#    if val < low : return -10000
#    return int((val - low)/(high - low) * 20000 - 10000)
#
#  def toC (self, x):
#    return (
#        "%(x)s < %(low).20f ? -10000 : "
#        "( %(x)s > %(high).20f ? 10000 : "
#        "int ((%(x)s - %(low).20f)/(%(high).20f - %(low).20f) * 20000 - 10000))"
#        ) % dict(x=x, low=self.low, high=self.high)


class GBDTCTraversalConverter (BaseConverter):
  """
  GradientBoostingDecision Tree converter, with tree traversal in C functions
  """

#  def _singletree(self, tree, node):
#    "Single-tree traversal"
#    if tree.feature[node] >= 0:
#      return "(x[%d] <= %d ? %s : %s)" % (tree.feature[node],
#          self.converter[tree.feature[node]](tree.threshold[node]),
#          self._singletree(tree, tree.children_left[node]),
#          self._singletree(tree, tree.children_right[node]))
#    else:
#      return str(tree.value[node][0][0])
#
#
#  def _singletree_explicit(self, instruction, tree, node, indent=3):
#    "Single-tree traversal"
#    if tree.feature[node] >= 0:
#      ret = [
#      "if (x[%d] <= %d) { ", 
#      " %s ",
#      "} ",
#      "else { ",
#      " %s",
#      "}"
#      ]
#
#      ret = [ret[0]] + [" "*indent+line for line in ret[1:]]
#      ret = '\n'.join(ret)
#
#      return ret % (
#        tree.feature[node],
#        self.converter[tree.feature[node]](tree.threshold[node]),
#        self._singletree_explicit(instruction, tree, tree.children_left[node], indent+1),
#        self._singletree_explicit(instruction, tree, tree.children_right[node], indent+1))
#      
#    else:
#      return instruction.format(leaf = str(tree.value[node][0][0])) 
#

  @ staticmethod
  def _get_limits(bdt):
    mins=[None] * bdt.n_features_
    maxs=[None] * bdt.n_features_

    for treeset in bdt.estimators_:
      for tree in treeset:
        for feature in range(bdt.n_features_):
          features=tree.tree_.feature
          if feature not in features: continue
          min_=np.min(tree.tree_.threshold[features == feature])
          if mins[feature] is None or min_ < mins[feature]:
            mins[feature]=min_

          max_=np.max(tree.tree_.threshold[features == feature])
          if maxs[feature] is None or max_ > maxs[feature]:
            maxs[feature]=max_

    return mins, maxs




  def convert(self, bdt, name=None):
    n_classes=bdt.n_classes_ if bdt.n_classes_ > 2 else 1
    lines=self.header()

    if n_classes > 1:
      for iClass in range(n_classes):
        lines.append("/*  ret [ %d ]   is the probability for category:  %-15s */" %
            (iClass,  str(bdt.classes_[iClass])))

    min_, max_=self._get_limits(bdt)
    #self.converter = [SmartFloat2Int(l, h) for l, h in zip(min_, max_)]

    nX = bdt.n_features_ 

    retvar="FLOAT_T ret[%d]" % n_classes
    invar="FLOAT_T inp[%d]" % nX
    lines += [
        "#include <math.h>",
        "extern \"C\"",
        """FLOAT_T __%(name)s_traversal (
          const FLOAT_T* probe, 
          const FLOAT_T* value, 
          const FLOAT_T* threshold, 
          const int*     feature, 
          const int*     left,
          const int*     right 
          )
        {
          int node = 0; 
          while (feature[node] >= 0)
          {
            if (probe[feature[node]] <= threshold[node])
              node = left[node];
            else
              node = right[node];
          }
          return value[node]; 
        }

        """ % dict(name=name or "bdt"),
        ]

    for iTree, tree in enumerate(bdt.estimators_):
      lines.append ( "  /**TREE %03d **/" % iTree ) 
      lines.append ( '  extern "C" ' ) 
      lines.append ( "  void update_%s_tree%03d (double *accumulator, const FLOAT_T* inp) " % (name or bdt, iTree)) 
      lines.append ( "  { ") 
      for iClass in range (n_classes):
        feature = [f for f in tree[iClass].tree_.feature]
        threshold = [t for t in tree[iClass].tree_.threshold] #[self.converter[f](t) for f, t in zip(feature, tree[iClass].tree_.threshold)]
        lines.append ( """ 
          const FLOAT_T v%(iTree)03d_%(iClass)02d [] = %(value)s;
          const FLOAT_T t%(iTree)03d_%(iClass)02d [] = %(threshold)s;
          const int     f%(iTree)03d_%(iClass)02d [] = %(feature)s;
          const int     l%(iTree)03d_%(iClass)02d [] = %(left)s;
          const int     r%(iTree)03d_%(iClass)02d [] = %(right)s;
          """ % dict(
          learningrate = bdt.learning_rate,
          maxlen = len (tree[iClass].tree_.feature), 
          iClass = iClass,
          iTree = iTree,
          name = name or "bdt",
          value = array2c ([v[0][0] for v in tree[iClass].tree_.value]), 
          threshold = array2c (threshold, "%.20f"), 
          feature = array2c (feature, "%.0f"), 
          left = array2c ([l for l in tree[iClass].tree_.children_left], "%.0f"), 
          right = array2c ([r for r in tree[iClass].tree_.children_right], "%.0f"), 
          ))


      for iClass in range (n_classes):
        lines.append ( "    "    
          "accumulator[%(iClass)d] += %(learningrate).10f * __%(name)s_traversal ( inp, "
          "  v%(iTree)03d_%(iClass)02d, t%(iTree)03d_%(iClass)02d, f%(iTree)03d_%(iClass)02d, l%(iTree)03d_%(iClass)02d, r%(iTree)03d_%(iClass)02d );  "
         % dict(
          learningrate = bdt.learning_rate,
          maxlen = len (tree[iClass].tree_.feature), 
          iClass = iClass,
          iTree = iTree,
          name = name or "bdt",
          value = array2c ([v[0][0] for v in tree[iClass].tree_.value]), 
          threshold = array2c (threshold, "%.20f"), 
          feature = array2c (feature, "%.0f"), 
          left = array2c ([l for l in tree[iClass].tree_.children_left], "%.0f"), 
          right = array2c ([r for r in tree[iClass].tree_.children_right], "%.0f"), 
          ))

      lines.append ("  }") 


    lines += [
        "extern \"C\"",
        "FLOAT_T *%s (%s, const %s)" % (name or "bdt", retvar, invar),
        "{",
        "  int i; ",
#        "  int x[%d];" % nX, 
        "  double acc[%d];" % n_classes, 
        "  for (short i=0; i < %d; ++i) ret[i] = 0.f;" % n_classes,
        "  for (short i=0; i < %d; ++i) acc[i] = 0.f;" % n_classes,
      ]
    for iTree, tree in enumerate(bdt.estimators_):
      lines.append("  update_%s_tree%03d (acc, inp); " % (name or bdt, iTree))


    # preprocessing
    # for feature in range(nX):
    #   lines.append ( "  x[%d] = %s; " % (feature, self.converter[feature].toC('inp[%d]' % feature)) )


#    for iTree, tree in enumerate(bdt.estimators_):
#      lines += [" /** TREE %03d **/" % iTree]
#      ## for iClass in range(n_classes):
#      ##   lines += [
#      ##      "  ret[%d] += %f * (%s); " % (iClass, bdt.learning_rate,
#      ##                          self._singletree(tree[iClass].tree_, 0))
#      ##    ]
#
#      for iClass in range (n_classes):
#        lines.append ( 
#            self._singletree_explicit (
#              "  ret[%d] += %f * ({leaf});" % (iClass, bdt.learning_rate),
#              tree[iClass].tree_, 0))


    

    if n_classes > 1:
      lines += [
          "  short argmax = 0; ",
          "  for (int i = 0; i < %d; ++i) if (acc[i] > acc[argmax]) argmax = i; " % n_classes,
          "  if (acc[argmax] > 1e10) { ",
          "    for (int i = 0; i < %d; ++i) ret[i] = (i==argmax ? 1.: 0.); " % n_classes,
          "    return ret; ",
          "  }",
          "  for (short i=0; i < %d; ++i) acc[i] = exp(acc[i]);" % n_classes,
          "  for (short i=0; i < %d; ++i) acc[i] = (acc[i] > 1e300?1e300:acc[i]);" % n_classes,
          "  long double sum = 0;",
          "  for (short i=0; i < %d; ++i) sum += acc[i];" % n_classes,
          "  for (short i=0; i < %d; ++i) acc[i] /= sum;" % n_classes,
        ]
    else:
      lines += [
        "  if (acc[0] > 1e10) acc[0] = 1.;",
        "  acc[0] = 1. / (1 + exp(-acc[0]));"
      ]


    lines += [
        "  for (int i = 0; i < %d; ++i) ret[i] = acc[i];" % n_classes, 
        "  return ret;", "}"
        ]

    return "\n".join(lines)

