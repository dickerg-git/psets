#!/usr/bin/env python

import json   # Used when TRACE=jsonp
import os     # Used to get the TRACE environment variable
import re     # Used when TRACE=jsonp
import sys    # Used to smooth over the range / xrange issue.

# Python 3 doesn't have xrange, and range behaves like xrange.
if sys.version_info >= (3,):
    xrange = range

# Circuit verification library.

class Wire(object):
  """A wire in an on-chip circuit.
  
  Wires are immutable, and are either horizontal or vertical.
  """
  
  def __init__(self, name, x1, y1, x2, y2):
    """Creates a wire.
    
    Raises an ValueError if the coordinates don't make up a horizontal wire
    or a vertical wire.
    
    Args:
      name: the wire's user-visible name
      x1: the X coordinate of the wire's first endpoint
      y1: the Y coordinate of the wire's first endpoint
      x2: the X coordinate of the wire's last endpoint
      y2: the Y coordinate of the wire's last endpoint
    """
    # Normalize the coordinates.
    if x1 > x2:
      x1, x2 = x2, x1
    if y1 > y2:
      y1, y2 = y2, y1
    
    self.name = name
    self.x1, self.y1 = x1, y1
    self.x2, self.y2 = x2, y2
    self.object_id = Wire.next_object_id()
    
    if not (self.is_horizontal() or self.is_vertical()):
      raise ValueError(str(self) + ' is neither horizontal nor vertical')
  
  def is_horizontal(self):
    """True if the wire's endpoints have the same Y coordinates."""
    return self.y1 == self.y2
  
  def is_vertical(self):
    """True if the wire's endpoints have the same X coordinates."""
    return self.x1 == self.x2
  
  def intersects(self, other_wire):
    """True if this wire intersects another wire."""
    # NOTE: we assume that wires can only cross, but not overlap.
    if self.is_horizontal() == other_wire.is_horizontal():
      return False 
    
    if self.is_horizontal():
      h = self
      v = other_wire
    else:
      h = other_wire
      v = self
    return v.y1 <= h.y1 and h.y1 <= v.y2 and h.x1 <= v.x1 and v.x1 <= h.x2
  
  def __repr__(self):
    # :nodoc: nicer formatting to help with debugging
    return('<wire ' + self.name + ' (' + str(self.x1) + ',' + str(self.y1) + 
           ')-(' + str(self.x2) + ',' + str(self.y2) + ')>')
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the wire."""
    return {'id': self.name, 'x': [self.x1, self.x2], 'y': [self.y1, self.y2]}

  # Next number handed out by Wire.next_object_id()
  _next_id = 0
  
  @staticmethod
  def next_object_id():
    """Returns a unique numerical ID to be used as a Wire's object_id."""
    id = Wire._next_id
    Wire._next_id += 1
    return id

class WireLayer(object):
  """The layout of one layer of wires in a chip."""
  
  def __init__(self):
    """Creates a layer layout with no wires."""
    self.wires = {}
  
  def wires(self):
    """The wires in the layout."""
    self.wires.values()
  
  def add_wire(self, name, x1, y1, x2, y2):
    """Adds a wire to a layer layout.
    
    Args:
      name: the wire's unique name
      x1: the X coordinate of the wire's first endpoint
      y1: the Y coordinate of the wire's first endpoint
      x2: the X coordinate of the wire's last endpoint
      y2: the Y coordinate of the wire's last endpoint
    
    Raises an exception if the wire isn't perfectly horizontal (y1 = y2) or
    perfectly vertical (x1 = x2)."""
    if name in self.wires:
        raise ValueError('Wire name ' + name + ' not unique')
    self.wires[name] = Wire(name, x1, y1, x2, y2)
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the layout."""
    return { 'wires': [wire.as_json() for wire in self.wires.values()] }
  
  @staticmethod
  def from_file(file):
    """Builds a wire layer layout by reading a textual description from a file.
    
    Args:
      file: a File object supplying the input
    
    Returns a new Simulation instance."""

    layer = WireLayer()
    
    while True:
      command = file.readline().split()
      if command[0] == 'wire':
        coordinates = [float(token) for token in command[2:6]]
        layer.add_wire(command[1], *coordinates)
      elif command[0] == 'done':
        break
      
    return layer




class BST_Node_KWP:
  """Model a node in the BST structure"""

  def __init__(self,key):
    """Initialize the BST Node structure"""
    self.leftChild = None
    self.rightChild = None
    self.kwp_key = key
    #self.kwp_index = []

  def insert(self,kwp):
    """Insert a KWP into the Binary Tree structure."""
    new_data = kwp.wire.y1

    #Make sure the not is not a duplicate by using unique wire id field.
    if self.kwp_key == kwp:
        print("Dup:", self.kwp_key)
        return False

    # See if the new value goes into the Left subtree...
    elif self.kwp_key > kwp:
        if self.leftChild:
          return self.leftChild.insert(kwp)
        else:
          self.leftChild = BST_Node_KWP(kwp)
          print("Inserted left:", self.leftChild.kwp_key)
          return True

    # Insert into the Right subtree.
    else:
        if self.rightChild:
          return self.rightChild.insert(kwp)
        else:
          self.rightChild = BST_Node_KWP(kwp)
          print("Inserted right:", self.rightChild.kwp_key)
          return True


  def bst_search(self, kwp):
    """Search the BST structure to find the node matching the sweep position.
       RETURNS: kwp_index, List of kwp items.
    """
    #print("bst_search:", kwp.wire.y1)
    if self.kwp_key == kwp:
           #print("Case 1")
           return self.kwp_key

    elif self.kwp_key > kwp:
        if self.leftChild:
           #print("Case L")
           return self.leftChild.bst_search(kwp)
#        else:
#          return self.kwp_index

    else:
        if self.rightChild:
           #print("Case R")
           return self.rightChild.bst_search(kwp)
#        else:
#          return self.kwp_index

  def node_list(self):
      nodes = list()

      if self.leftChild:
          nodes.extend(self.leftChild.node_list())
      nodes.append(self.kwp_key)
      if self.rightChild:
          nodes.extend(self.rightChild.node_list())
      return nodes


class BSTree(object):
  """Binary Search Tree implementation."""

  def __init__(self):
    """Initialize the BST structure"""
    self.root = None

  def insert(self, key):
    """Insert a KeyWirePair object into a node
       indexed to the mid-Y coordinate of a Horizontal wire.
    """
    if self.root:
          return self.root.insert(key)
    else:
          self.root = BST_Node_KWP(key)
          print("Inserted root:", self.root.kwp_key)
          return True

  def remove(self, kwp):
    """Remove a node from the BST tree"""
    parent = None
    node = self.root
    #print("Checking:", node.kwp_key)

    while node and node.kwp_key != kwp:
          parent = node
          if kwp < node.kwp_key:
             node = node.leftChild
          else:
             node = node.rightChild
          #print("Following:", node.kwp_key)

    if node is self.root:
          print("removed ROOT!")
    print("Removed: ", node.kwp_key)

    #Case 1: The node value was not found!!!
    if node is None or node.kwp_key != kwp:
          return False

    #case 2: The node has NO children
    elif node.leftChild is None and node.rightChild is None:
          if node is self.root:
              self.root = None
          elif kwp < parent.kwp_key:
              parent.leftChild = None
          else:
              parent.rightChild = None
          print("Removed, case 2")
          return True

    #Case 3, 4: The node has only ONE child node.
    elif node.leftChild and node.rightChild is None:
          if node is self.root:
              self.root = node.leftChild
          elif kwp < parent.kwp_key:
              parent.leftChild = node.leftChild
          else:
              parent.rightChild = node.leftChild
          print("Removed, case 3")
          return True

    elif node.leftChild is None and node.rightChild:
          if node is self.root:
              self.root = node.rightChild
          elif kwp < parent.kwp_key:
              parent.leftChild = node.rightChild
          else:
              parent.rightChild = node.rightChild
          print("Removed, case 4")
          return True

    #Case 5: The node has TWO roots!
    else:
          delNodeParent = node
          delNode = node.rightChild

          #Find the lowest leftChild to find the next greater node.
          while delNode.leftChild:
              delNodeParent = delNode
              delNode = delNode.leftChild
          #Replace the deleted node value with the next greater node value
          node.kwp_key = delNode.kwp_key

          #Remove the Right Child
          if delNode.rightChild:
              if delNodeParent.kwp_key > delNode.kwp_key:
                  delNodeParent.leftChild = delNode.rightChild
              elif delNodeParent.kwp_key < delNode.kwp_key:
                  delNodeParent.rightChild = delNode.rightChild
              return True
          #Remove the Left Child
          else:
              if delNode.kwp_key < delNodeParent.kwp_key:
                  delNodeParent.leftChild = None
              else:
                  delNodeParent.rightChild = None
              return True

          print("Remove failed...")
          return False

  def findKey(self,kwp):
    """Look into the BST for a node searching for the Y point of a H-wire."""

    return self.root.bst_search(kwp)

  def inorder_list(self):

      if self.root:
        return self.root.node_list()



class RangeIndex(object):
  """Array-based range index implementation."""
  
  def __init__(self):
    """Initially empty range index."""
    self.data = []
    self.bst_data = BSTree()
  
  def add(self, key):
    """Inserts a key in the range index."""
    if key is None:
        raise ValueError('Cannot insert nil in the index')
    self.data.append(key)
    self.bst_data.insert(key)
    #print( key )
  
  def remove(self, key):
    """Removes a key from the range index."""
    print( "remove:  ", key)
    print( self.bst_data.remove(key) )
  
  def list(self, first_key, last_key):
    """List of values for the keys that fall within [first_key, last_key]."""
    kwp_list = []
    #while True:
    #kwp_list = self.bst_data.inorder_list()
    #print("List:", len(kwp_list))
    #return [key for key in  kwp_list if first_key <= key <= last_key]
    return [key for key in self.data if first_key <= key <= last_key]
  
  def count(self, first_key, last_key):
    """Number of keys that fall within [first_key, last_key]."""
    result = 0
    for key in self.data:
      if first_key <= key <= last_key:
        result += 1
    return result
  
class TracedRangeIndex(RangeIndex):
  """Augments RangeIndex to build a trace for the visualizer."""
  
  def __init__(self, trace):
    """Sets the object receiving tracing info."""
    RangeIndex.__init__(self)
    self.trace = trace
  
  def add(self, key):
    self.trace.append({'type': 'add', 'id': key.wire.name})
    RangeIndex.add(self, key)
  
  def remove(self, key):
    self.trace.append({'type': 'delete', 'id': key.wire.name})
    RangeIndex.remove(self, key)
  
  def list(self, first_key, last_key):
    result = RangeIndex.list(self, first_key, last_key)
    self.trace.append({'type': 'list', 'from': first_key.key,
                       'to': last_key.key,
                       'ids': [key.wire.name for key in result]}) 
    return result
  
  def count(self, first_key, last_key):
    result = RangeIndex.count(self, first_key, last_key)
    self.trace.append({'type': 'list', 'from': first_key.key,
                       'to': last_key.key, 'count': result})
    return result

class ResultSet(object):
  """Records the result of the circuit verifier (pairs of crossing wires)."""
  
  def __init__(self):
    """Creates an empty result set."""
    self.crossings = []
  
  def add_crossing(self, wire1, wire2):
    """Records the fact that two wires are crossing."""
    self.crossings.append(sorted([wire1.name, wire2.name]))
  
  def write_to_file(self, file):
    """Write the result to a file."""
    for crossing in self.crossings:
      file.write(' '.join(crossing))
      file.write('\n')

class TracedResultSet(ResultSet):
  """Augments ResultSet to build a trace for the visualizer."""
  
  def __init__(self, trace):
    """Sets the object receiving tracing info."""
    ResultSet.__init__(self)
    self.trace = trace
    
  def add_crossing(self, wire1, wire2):
    self.trace.append({'type': 'crossing', 'id1': wire1.name,
                       'id2': wire2.name})
    ResultSet.add_crossing(self, wire1, wire2)

class KeyWirePair(object):
  """Wraps a wire and the key representing it in the range index.
  
  Once created, a key-wire pair is immutable."""
  
  def __init__(self, key, wire):
    """Creates a new key for insertion in the range index."""
    self.key = key
    if wire is None:
      raise ValueError('Use KeyWirePairL or KeyWirePairH for queries')
    self.wire = wire
    self.wire_id = wire.object_id

  def __lt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id < other.wire_id))
  
  def __le__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id <= other.wire_id))  

  def __gt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id > other.wire_id))
  
  def __ge__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id >= other.wire_id))

  def __eq__(self, other):
    # :nodoc: Delegate comparison to keys.
    return self.key == other.key and self.wire_id == other.wire_id
  
  def __ne__(self, other):
    # :nodoc: Delegate comparison to keys.
    return self.key != other.key or self.wire_id != other.wire_id

  def __hash__(self):
    # :nodoc: Delegate comparison to keys.
    return hash([self.key, self.wire_id])

  def __repr__(self):
    # :nodoc: nicer formatting to help with debugging
    return '<key: ' + str(self.key) + ' wire: ' + str(self.wire) + '>'

class KeyWirePairL(KeyWirePair):
  """A KeyWirePair that is used as the low end of a range query.
  
  This KeyWirePair is smaller than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    self.wire_id = -1000000000

class KeyWirePairH(KeyWirePair):
  """A KeyWirePair that is used as the high end of a range query.
  
  This KeyWirePair is larger than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    # HACK(pwnall): assuming 1 billion objects won't fit into RAM.
    self.wire_id = 1000000000

class CrossVerifier(object):
  """Checks whether a wire network has any crossing wires."""
  
  def __init__(self, layer):
    """Verifier for a layer of wires.
    
    Once created, the verifier can list the crossings between wires (the 
    wire_crossings method) or count the crossings (count_crossings)."""

    self.events = []
    self._events_from_layer(layer)
    self.events.sort()
    if len(self.events) < 10:
       for w in self.events:
          print(w)

    self.index = RangeIndex()
    self.result_set = ResultSet()
    self.performed = False
  
  def count_crossings(self):
    """Returns the number of pairs of wires that cross each other."""
    if self.performed:
      raise 
    self.performed = True
    return self._compute_crossings(True)

  def wire_crossings(self):
    """An array of pairs of wires that cross each other."""
    if self.performed:
      raise 
    self.performed = True
    return self._compute_crossings(False)

  def _events_from_layer(self, layer):
    """Populates the sweep line events from the wire layer."""
    left_edge = min([wire.x1 for wire in layer.wires.values()])
    for wire in layer.wires.values():
      if wire.is_horizontal():
        #if wire.x1 > left_edge: left_edge = wire.x1
        left_edge = wire.x1
        self.events.append([left_edge, 0, wire.object_id, 'add', wire])
        self.events.append([wire.x2, 2, wire.object_id, 'delete', wire])
      else:
        self.events.append([wire.x1, 1, wire.object_id, 'query', wire])

  def _compute_crossings(self, count_only):
    """Implements count_crossings and wire_crossings.
       Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
187590314  222.183    0.000  343.936    0.000 circuit2.py:55(intersects)
    20000  141.616    0.007  284.753    0.014 circuit2.py:157(list)
562840882  121.779    0.000  121.779    0.000 circuit2.py:47(is_horizontal)
        1   92.105   92.105  726.545  726.545 circuit2.py:336(_compute_crossings)
299400000   84.416    0.000   84.416    0.000 circuit2.py:246(__le__)
261444830   58.721    0.000   58.721    0.000 circuit2.py:256(__ge__)
124719049    5.666    0.000    5.666    0.000 {method 'append' of 'list' objects}
        1    0.126    0.126    0.335    0.335 circuit2.py:119(from_file)
    34970    0.088    0.000    0.126    0.000 circuit2.py:20(__init__)
        1    0.064    0.064    0.084    0.084 circuit2.py:327(_events_from_layer)

    """
    if count_only:
      result = 0
    else:
      result = self.result_set

    for event in self.events:
      event_x, event_type, wire = event[0], event[3], event[4]
      print(event_type, event_x, wire.x1, wire.name)

      if event_type == 'add':
        self.index.add(KeyWirePair(wire.y1, wire))
      elif event_type == 'delete':
        self.index.remove(KeyWirePair(wire.y1, wire))
      elif event_type == 'query':
        self.trace_sweep_line(event_x)
        cross_wires = []
        for kwp in self.index.list(KeyWirePairL(wire.y1),KeyWirePairH(wire.y2)):
          if wire.intersects(kwp.wire):
            cross_wires.append(kwp.wire)
        if count_only:
          result += len(cross_wires)
        else:
          for cross_wire in cross_wires:
            result.add_crossing(wire, cross_wire)

    return result
  
  def trace_sweep_line(self, x):
    """When tracing is enabled, adds info about where the sweep line is.
    
    Args:
      x: the coordinate of the vertical sweep line
    """
    # NOTE: this is overridden in TracedCrossVerifier
    pass

class TracedCrossVerifier(CrossVerifier):
  """Augments CrossVerifier to build a trace for the visualizer."""
  
  def __init__(self, layer):
    CrossVerifier.__init__(self, layer)
    self.trace = []
    self.index = TracedRangeIndex(self.trace)
    self.result_set = TracedResultSet(self.trace)
    
  def trace_sweep_line(self, x):
    self.trace.append({'type': 'sweep', 'x': x})
    
  def trace_as_json(self):
    """List that obeys the JSON format restrictions with the verifier trace."""
    return self.trace

# Command-line controller.
if __name__ == '__main__':
    import sys
    layer = WireLayer.from_file(sys.stdin)
    verifier = CrossVerifier(layer)
    
    if os.environ.get('TRACE') == 'jsonp':
      verifier = TracedCrossVerifier(layer)
      result = verifier.wire_crossings()
      json_obj = {'layer': layer.as_json(), 'trace': verifier.trace_as_json()}
      sys.stdout.write('onJsonp(')
      json.dump(json_obj, sys.stdout)
      sys.stdout.write(');\n')
    elif os.environ.get('TRACE') == 'list':
      verifier.wire_crossings().write_to_file(sys.stdout)
    else:
      sys.stdout.write(str(verifier.count_crossings()) + " Crosses!!!\n")
