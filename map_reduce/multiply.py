import MapReduce
import sys
from itertools import groupby
from operator import itemgetter, mul
# matrix dimensions are 5x5
max_rows = 5
max_cols = 5

mr = MapReduce.MapReduce()

def mapper(record):
    # from matrix a grab rows, from b columns
    # it's sparse, so missing are 0
    # might need to know the size to emit the value for all
    which_matrix = record[0]
    row, col, val = record[1:]
    if which_matrix == 'a':
        [mr.emit_intermediate(str(row) + str(c),['a',col,val]) for c in xrange(max_cols)]
    else:
        [mr.emit_intermediate(str(r) + str(col),['b',row,val]) for r in xrange(max_rows)]

def reducer(key, matrix_map):
    # data passed is in this format: [m,x,v]
    # where m is char indicating which matrix (a or b)
    # x is the row or column and v is the value at that location
    # group by the rows/columns for matrix a we send the col while
    # for matrix b we send the row. This way we can do the matrix mul
    groups =  groupby(sorted(matrix_map,key=itemgetter(1)),itemgetter(1))
    values = [[itemgetter(2)(x) for x in v] for k, v in groups]
    # also filter out values where 1 of the values is 0, i.e. len != 2
    matrix_prod = sum(map(lambda y: y[0]*y[1],[x for x in values if len(x) == 2]))

    mr.emit((int(itemgetter(0)(key)), int(itemgetter(1)(key)), matrix_prod))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

