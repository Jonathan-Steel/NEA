class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node
    
  def get_value(self):
    return self.value
  
  def get_next_node(self):
    return self.next_node
  
  def set_next_node(self, next_node):
    self.next_node = next_node

class LinkedList:
  def __init__(self, value=None):
    self.head_node = Node(value)
  
  def get_head_node(self):
    return self.head_node
  
  def insert_beginning(self, new_value):
    new_node = Node(new_value)
    new_node.set_next_node(self.head_node)
    self.head_node = new_node
    
  def stringify_list(self):
    string_list = ""
    current_node = self.get_head_node()
    while current_node:
      if current_node.get_value() != None:
        string_list += str(current_node.get_value()) + "\n"
      current_node = current_node.get_next_node()
    return string_list
  
  def remove_node(self, value_to_remove):
    current_node = self.get_head_node()
    if current_node.get_value() == value_to_remove:
      self.head_node = current_node.get_next_node()
    else:
      while current_node:
        next_node = current_node.get_next_node()
        if next_node.get_value() == value_to_remove:
          current_node.set_next_node(next_node.get_next_node())
          current_node = None
        else:
          current_node = next_node
  def remove_all_nodes(self, value_to_remove):
    current_node = self.get_head_node()
    if current_node.get_value() == value_to_remove:
      self.head_node = current_node.get_next_node()
    while current_node:
      next_node = current_node.get_next_node()
      if next_node.get_value() == value_to_remove:
        current_node.set_next_node(next_node.get_next_node())
        current_node = None
      else:
        current_node = next_node

## Main Code
ll = LinkedList(0)

ll.insert_beginning('3')
ll.insert_beginning('6')
ll.insert_beginning('3')

print(ll.stringify_list())

ll.remove_all_nodes('3')

print(ll.stringify_list())


# class HashMap:
#   def __init__(self, array_size):
#     self.array_size = array_size
#     self.array = [None for item in range(array_size)]

#   def hash(self, key, count_collisions=0):
#     key_bytes = key.encode()
#     hash_code = sum(key_bytes)
#     return hash_code + count_collisions

#   def compressor(self, hash_code):
#     return hash_code % self.array_size

#   def assign(self, key, value):
#     array_index = self.compressor(self.hash(key))
#     current_array_value = self.array[array_index]

#     if current_array_value is None:
#       self.array[array_index] = [key, value]
#       return

#     if current_array_value[0] == key:
#       self.array[array_index] = [key, value]
#       return

#     # Collision!

#     number_collisions = 1

#     while(current_array_value[0] != key):
#       new_hash_code = self.hash(key, number_collisions)
#       new_array_index = self.compressor(new_hash_code)
#       current_array_value = self.array[new_array_index]

#       if current_array_value is None:
#         self.array[new_array_index] = [key, value]
#         return

#       if current_array_value[0] == key:
#         self.array[new_array_index] = [key, value]
#         return

#       number_collisions += 1

#     return

#   def retrieve(self, key):
#     array_index = self.compressor(self.hash(key))
#     possible_return_value = self.array[array_index]

#     if possible_return_value is None:
#       return None

#     if possible_return_value[0] == key:
#       return possible_return_value[1]

#     retrieval_collisions = 1

#     while (possible_return_value != key):
#       new_hash_code = self.hash(key, retrieval_collisions)
#       retrieving_array_index = self.compressor(new_hash_code)
#       possible_return_value = self.array[retrieving_array_index]

#       if possible_return_value is None:
#         return None

#       if possible_return_value[0] == key:
#         return possible_return_value[1]

#       retrieval_collisions += 1

#     return

# hash_map = HashMap(15)

# hash_map.assign('gabbro', 'igneous')
# hash_map.assign('sandstone', 'sedimentary')
# hash_map.assign('gneiss', 'metamorphic')

# print(hash_map.retrieve('gabbro'))
# print(hash_map.retrieve('sandstone'))
# print(hash_map.retrieve('gneiss'))

# def merge_sort(items):
#   if len(items) <= 1:
#     return items

#   middle_index = len(items) // 2
#   left_split = items[:middle_index]
#   right_split = items[middle_index:]

#   left_sorted = merge_sort(left_split)
#   right_sorted = merge_sort(right_split)

#   return merge(left_sorted, right_sorted)

# def merge(left, right):
#   result = []

#   while (left and right):
#     if left[0] < right[0]:
#       result.append(left[0])
#       left.pop(0)
#     else:
#       result.append(right[0])
#       right.pop(0)

#   if left:
#     result += left
#   if right:
#     result += right

#   return result

# unordered_list1 = [356, 746, 264, 569, 949, 895, 125, 455]
# unordered_list2 = [787, 677, 391, 318, 543, 717, 180, 113, 795, 19, 202, 534, 201, 370, 276, 975, 403, 624, 770, 595, 571, 268, 373]
# unordered_list3 = [860, 380, 151, 585, 743, 542, 147, 820, 439, 865, 924, 387]

# ordered_list1 = merge_sort(unordered_list1)
# ordered_list2 = merge_sort(unordered_list2)
# ordered_list3 = merge_sort(unordered_list3)

# print(ordered_list1)
# print(ordered_list2)
# print(ordered_list3)