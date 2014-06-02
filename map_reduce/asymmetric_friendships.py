import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    name = record[0]
    friend = record[1]
    mr.emit_intermediate(name,friend)
    mr.emit_intermediate(friend,name)

def reducer(key, list_of_friends):
    [mr.emit((key,friend)) for friend in list_of_friends 
                                if list_of_friends.count(friend) == 1]

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

