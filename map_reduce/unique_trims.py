import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    key = record[1][:-10]
    mr.emit_intermediate(key,1)

def reducer(key, list_of_friends):
    mr.emit(key)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)


