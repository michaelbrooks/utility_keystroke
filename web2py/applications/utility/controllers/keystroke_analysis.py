response.generic_patterns = ['html', 'csv']

import random, hashlib, uuid, datetime, time, math
import cStringIO

def index():
    # print out a list of available data files
    links = []
    
    linkTemps = [
        'keystroke_analysis/entry_surveys/%d',
        'keystroke_analysis/post_surveys/%d'
    ]
    
    for study in db().select(db.studies.ALL):
        for t in linkTemps:
            ref = t %(study.id)
            links.append(A(ref, _href=ref));

    return dict(links=links)

def entry_surveys():
    study_id = request.args[0]
    study = db.studies(study_id)
    
    stream=cStringIO.StringIO()
    
    export_entry_surveys(stream, study)
    
    return dump_csv(stream, 'entry_surveys_%s.csv' %(study_id))
    
    
def post_surveys():
    study_id = request.args[0]
    study = db.studies(study_id)
    
    stream=cStringIO.StringIO()
    
    export_post_surveys(stream, study)
    
    return dump_csv(stream, 'post_surveys_%s.csv' %(study_id))


def dump_csv(stream, name='output.csv'):
    response.headers['Content-Type']='application/vnd.ms-excel'
    response.headers['Content-Disposition']='attachment;filename=%s' %(name)
    return stream.getvalue()