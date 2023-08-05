
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND EQUAL GT GTE LIKE LT LTE NOT_EQUAL OR QUOTE_STRING STRINGmerge : filter AND filter\n                 | filter OR filter\n                 | merge AND filter\n                 | merge OR filter\n                 | filter\n        filter : factor EQUAL factor\n                  | factor NOT_EQUAL factor\n                  | factor GTE factor\n                  | factor GT factor\n                  | factor LTE factor\n                  | factor LT factor\n                  | factor LIKE factor\n        factor : QUOTE_STRING\n                  | STRING\n        '
    
_lr_action_items = {'QUOTE_STRING':([0,6,7,8,9,10,11,12,13,14,15,16,],[4,4,4,4,4,4,4,4,4,4,4,4,]),'STRING':([0,6,7,8,9,10,11,12,13,14,15,16,],[5,5,5,5,5,5,5,5,5,5,5,5,]),'$end':([1,2,4,5,17,18,19,20,21,22,23,24,25,26,27,],[0,-5,-13,-14,-3,-4,-1,-2,-6,-7,-8,-9,-10,-11,-12,]),'AND':([1,2,4,5,17,18,19,20,21,22,23,24,25,26,27,],[6,8,-13,-14,-3,-4,-1,-2,-6,-7,-8,-9,-10,-11,-12,]),'OR':([1,2,4,5,17,18,19,20,21,22,23,24,25,26,27,],[7,9,-13,-14,-3,-4,-1,-2,-6,-7,-8,-9,-10,-11,-12,]),'EQUAL':([3,4,5,],[10,-13,-14,]),'NOT_EQUAL':([3,4,5,],[11,-13,-14,]),'GTE':([3,4,5,],[12,-13,-14,]),'GT':([3,4,5,],[13,-13,-14,]),'LTE':([3,4,5,],[14,-13,-14,]),'LT':([3,4,5,],[15,-13,-14,]),'LIKE':([3,4,5,],[16,-13,-14,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'merge':([0,],[1,]),'filter':([0,6,7,8,9,],[2,17,18,19,20,]),'factor':([0,6,7,8,9,10,11,12,13,14,15,16,],[3,3,3,3,3,21,22,23,24,25,26,27,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> merge","S'",1,None,None,None),
  ('merge -> filter AND filter','merge',3,'p_merge','query.py',161),
  ('merge -> filter OR filter','merge',3,'p_merge','query.py',162),
  ('merge -> merge AND filter','merge',3,'p_merge','query.py',163),
  ('merge -> merge OR filter','merge',3,'p_merge','query.py',164),
  ('merge -> filter','merge',1,'p_merge','query.py',165),
  ('filter -> factor EQUAL factor','filter',3,'p_filter','query.py',173),
  ('filter -> factor NOT_EQUAL factor','filter',3,'p_filter','query.py',174),
  ('filter -> factor GTE factor','filter',3,'p_filter','query.py',175),
  ('filter -> factor GT factor','filter',3,'p_filter','query.py',176),
  ('filter -> factor LTE factor','filter',3,'p_filter','query.py',177),
  ('filter -> factor LT factor','filter',3,'p_filter','query.py',178),
  ('filter -> factor LIKE factor','filter',3,'p_filter','query.py',179),
  ('factor -> QUOTE_STRING','factor',1,'p_factor','query.py',184),
  ('factor -> STRING','factor',1,'p_factor','query.py',185),
]
