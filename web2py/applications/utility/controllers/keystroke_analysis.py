response.generic_patterns = ['html', 'csv']

import random, hashlib, uuid, datetime, time, math
import gluon.contrib.simplejson
import re, csv

def ks_entry_surveys():
    
    entries = db().select(
        db.ks_entry_surveys.ALL, 
        db.conditions.json,
        join=db.conditions.on(db.conditions.id == db.ks_entry_surveys.condition)
    )
    return dict(data=as_obj(entries))
    # return dict(data=entries.as_list(), export_to_csv_file=export_to_csv_file)

def ks_post_surveys():
    entries = db().select(db.ks_entry_surveys.ALL);
    return dict(data=entries)

def as_obj(rows, mode='object', default=None):
    """
    serializes the table to a list of objects
    """

    items = [record.as_dict() for record in rows]

    return items
    
# def export_to_csv_file(dictList, ofile, null='<NULL>', *args, **kwargs):
    # """
    # export data to csv, the first line contains the column names

    # :param ofile: where the csv must be exported to
    # :param null: how null values must be represented (default '<NULL>')
    # :param delimiter: delimiter to separate values (default ',')
    # :param quotechar: character to use to quote string values (default '"')
    # :param quoting: quote system, use csv.QUOTE_*** (default csv.QUOTE_MINIMAL)
    # :param represent: use the fields .represent value (default False)
    # :param colnames: list of column names to use (default self.colnames)
                     # This will only work when exporting rows objects!!!!
                     # DO NOT use this with db.export_to_csv()
    # """
    # delimiter = kwargs.get('delimiter', ',')
    # quotechar = kwargs.get('quotechar', '"')
    # quoting = kwargs.get('quoting', csv.QUOTE_MINIMAL)
    # represent = kwargs.get('represent', False)
    # writer = csv.writer(ofile, delimiter=delimiter,
                        # quotechar=quotechar, quoting=quoting)
                        
    # # rows are 2 layers deep - one layer for table, one for field
    # colnames = []
    # for t, tval in tables.iteritems():
        # if (isinstance(tval, dict)
        # for f, fval in tval.iteritems():
            # colnames.append(t + '.' + f)
            
    # colnames = kwargs.get('colnames', dictList[0].keys())
    # write_colnames = kwargs.get('write_colnames',True)
    # # a proper csv starting with the column names
    # if write_colnames:
        # writer.writerow(colnames)

    # def none_exception(value):
        # """
        # returns a cleaned up value that can be used for csv export:
        # - unicode text is encoded as such
        # - None values are replaced with the given representation (default <NULL>)
        # """
        # if value is None:
            # return null
        # elif isinstance(value, unicode):
            # return value.encode('utf8')
        # elif isinstance(value,Reference):
            # return long(value)
        # elif hasattr(value, 'isoformat'):
            # return value.isoformat()[:19].replace('T', ' ')
        # elif isinstance(value, (list,tuple)): # for type='list:..'
            # return bar_encode(value)
        # return value

    # for record in dictList:
        # row = []
        # for col in colnames:
            # (t, f) = col.split('.')
            # if t in record and f in record[t]:
                # value = record[t][f]
            # else:
                # value = record[f]
            
            # field = db[t][f]
            # if field.type=='blob' and not value is None:
                # value = base64.b64encode(value)
            # elif represent and field.represent:
                # value = field.represent(value)
            # row.append(none_exception(value))
        # writer.writerow(row)