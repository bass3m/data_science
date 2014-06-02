import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    tbl_type = record[0] # order or line_item
    order_id = record[1] # order id
    mr.emit_intermediate(order_id, {tbl_type : record})

def reducer(key, list_of_orders_map):
    total = [list_of_orders_map[0]['order'] + rec['line_item'] 
             for rec in list_of_orders_map if rec.has_key('line_item')]
    [mr.emit(r) for r in total]

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
