import csv
import gluon.contrib.simplejson as json

options.keystroke = {
    'price' : [0.05, 0.10, 0.20],
    'reject_chance': [0.00, 0.05, 0.10, 0.33, 0.66],
    'delay_time': [0.1, 3, 10],
    'message_length': ['terse', 'medium', 'verbose'],
    'work_limit' : 51,
    'mystery_task' : True
    }


db.define_table('ks_entry_surveys',
                db.Field('study', db.studies),
                db.Field('hitid', 'text'),
                db.Field('workerid', 'text'),
                db.Field('assid', 'text'),
                db.Field('time', 'datetime', default=now),
                db.Field('ip', 'text'),
                db.Field('condition', db.conditions),
                db.Field('age', 'integer'),
                db.Field('gender', 'text'),
                db.Field('occupation', 'text'),
                db.Field('biometric', 'text'),
                db.Field('verification', 'text'),
                db.Field('duration', 'integer'),
                migrate=migratep, fake_migrate=fake_migratep)

db.define_table('ks_post_surveys',
                db.Field('study', db.studies),
                db.Field('hitid', 'text'),
                db.Field('workerid', 'text'),
                db.Field('assid', 'text'),
                db.Field('time', 'datetime', default=now),
                db.Field('ip', 'text'),
                db.Field('condition', db.conditions),
                db.Field('completed', 'integer'),
                db.Field('attempts', 'integer'),
                db.Field('duration', 'integer'),
				db.Field('m_lively', 'double'),
				db.Field('m_drowsy', 'double'),
				db.Field('m_happy', 'double'),
				db.Field('m_grouchy', 'double'),
				db.Field('m_sad', 'double'),
				db.Field('m_peppy', 'double'),
				db.Field('m_tired', 'double'),
				db.Field('m_nervous', 'double'),
				db.Field('m_caring', 'double'),
				db.Field('m_calm', 'double'),
				db.Field('m_content', 'double'),
				db.Field('m_loving', 'double'),
				db.Field('m_gloomy', 'double'),
				db.Field('m_fedup', 'double'),
				db.Field('m_jittery', 'double'),
				db.Field('m_active', 'double'),
                db.Field('m_frustrated', 'double'),
                db.Field('m_satisfied', 'double'),
				db.Field('m_overall', 'double'),
                db.Field('mood_time', 'double'),
				db.Field('free_write_text', 'text'),
                db.Field('free_write_time', 'double'),
				db.Field('associations', 'text'),
                db.Field('association_times', 'text'),
                migrate=migratep, fake_migrate=fake_migratep)

def record_entry_survey(post):
    hit = request.hitid
    worker = request.workerid
    ass = request.assid
    ip = request.env.remote_addr
    condition = get_condition(request.condition)
    duration = time.time() - session.start_time
    
    age = post.age
    gender = post.gender
    occupation = post.occupation
    biometric = sj.dumps(post.biometric)
    verification = post.verify
    
    db.ks_entry_surveys.insert(study=request.study,
                      hitid=hit,
                      workerid=worker,
                      assid=ass,
                      ip=ip,
                      condition=condition,
                      age=age,
                      gender=gender,
                      occupation=occupation,
                      biometric=biometric,
                      verification=verification,
                      duration=duration)
                      
def record_post_survey():
    hit = request.hitid
    worker = request.workerid
    ass = request.assid
    ip = request.env.remote_addr
    condition = get_condition(request.condition)
    duration = time.time() - session.start_time
    
    attempts = hit_session.attempts
    completed = hits_done(request.workerid, request.study)
    
    m_lively = hit_session.mood_form.m_lively
    m_drowsy = hit_session.mood_form.m_drowsy
    m_happy = hit_session.mood_form.m_happy
    m_grouchy = hit_session.mood_form.m_grouchy
	
    m_sad = hit_session.mood_form.m_sad
    m_peppy = hit_session.mood_form.m_peppy
    m_tired = hit_session.mood_form.m_tired
    m_nervous = hit_session.mood_form.m_nervous
	
    m_caring = hit_session.mood_form.m_caring
    m_calm = hit_session.mood_form.m_calm
    m_content = hit_session.mood_form.m_content
    m_loving = hit_session.mood_form.m_loving
	
    m_gloomy = hit_session.mood_form.m_gloomy
    m_fedup = hit_session.mood_form.m_fedup
    m_jittery = hit_session.mood_form.m_jittery
    m_active = hit_session.mood_form.m_active
    
    m_frustrated = hit_session.mood_form.m_frustrated
    m_satisfied = hit_session.mood_form.m_satisfied
    
    m_overall = hit_session.mood_form.m_overall
    
    mood_time = hit_session.mood_form.mood_time
    
    free_write_text = hit_session.free_write_text
    free_write_time = hit_session.free_write_time
    associations = hit_session.associations
    association_times = hit_session.association_times
	
    db.ks_post_surveys.insert(study=request.study,
                    hitid=hit,
                    workerid=worker,
                    assid=ass,
                    ip=ip,
                    condition=condition,
                    completed=completed,
                    attempts=attempts,
                    duration=duration,
                    m_lively=m_lively,
                    m_drowsy=m_drowsy,
                    m_happy=m_happy,
                    m_grouchy=m_grouchy,
                    m_sad=m_sad,
                    m_peppy=m_peppy,
                    m_tired=m_tired,
                    m_nervous=m_nervous,
                    m_caring=m_caring,
                    m_calm=m_calm,
                    m_content=m_content,
                    m_loving=m_loving,
                    m_gloomy=m_gloomy,
                    m_fedup=m_fedup,
                    m_jittery=m_jittery,
                    m_active=m_active,
                    m_frustrated=m_frustrated,
                    m_satisfied=m_satisfied,
                    m_overall=m_overall,
                    mood_time=mood_time,
                    free_write_text=free_write_text,
                    free_write_time=free_write_time,
                    associations=associations,
                    association_times=association_times
                      )


def experimental_vars(study):
    conditions = json.loads(study.conditions)
    vars = conditions.keys()
    return [x for x in vars
            if isinstance(conditions[x], (list, tuple))]

# this does not help generate the UI
biometrics = [
    dict(name='Fingerprints', value='fingerprint'),
    dict(name='Iris or retina scans', value='eye'),
    dict(name='Face recognition', value='face'),
    dict(name='Voice recognition', value='voice'),
    dict(name='Signature recognition', value='signature'),
    dict(name='Keystroke (typing) pattern', value='keystroke'),
    dict(name='Other biometric systems', value='other')
]
            
def export_entry_surveys(stream, study):

    writer = csv.writer(stream)

    conditions = json.loads(study.conditions)
    variables = experimental_vars(study)
    biometricValues = [x['value'] for x in biometrics]
    
    header = ['id', 'run_length', 'start_time', 'end_time', 'workerid', 'censored', 'other']
    header += variables
    header += ['age', 'gender', 'occupation', 'duration']
    header += biometricValues
    header += ['post_survey_count', 'attempts_sum', 'experienced_rejection_rate', 'duration_mean', 
        'm_frustrated_mean', 'm_satisfied_mean', 'm_happy_mean', 
        'm_sad_mean', 'm_overall_mean', 'mood_time_mean',
        'free_write_time_mean']
        
    writer.writerow(header)
    
    studyMatches = (db.runs.study==study) & \
                   (db.ks_entry_surveys.study == study)
                   
    join = (db.runs.workerid == db.ks_entry_surveys.workerid)
    
    entries = db(studyMatches & join).select(
        db.runs.ALL,
        db.ks_entry_surveys.ALL
    )
    
    for entry in entries:
        run = entry.runs
        es = entry.ks_entry_surveys
        
        conditions = (db.ks_post_surveys.study == study) & (db.ks_post_surveys.workerid == run.workerid)
        ps = db(conditions).select(
            db.ks_post_surveys.id.count().with_alias('post_survey_count'), 
                db.ks_post_surveys.attempts.sum().with_alias('attempts_sum'),
                db.ks_post_surveys.duration.avg().with_alias('duration_mean'),
            db.ks_post_surveys.m_frustrated.avg().with_alias('m_frustrated_mean'),
                db.ks_post_surveys.m_satisfied.avg().with_alias('m_satisfied_mean'),
                db.ks_post_surveys.m_happy.avg().with_alias('m_happy_mean'),
            db.ks_post_surveys.m_sad.avg().with_alias('m_sad_mean'),
                db.ks_post_surveys.m_overall.avg().with_alias('m_overall_mean'), 
                db.ks_post_surveys.mood_time.avg().with_alias('mood_time_mean'),
            db.ks_post_surveys.free_write_time.avg().with_alias('free_write_time_mean'),
            groupby=db.ks_post_surveys.workerid
        ).first()
        
        if ps:
            experienced_rejection_rate = float(ps.attempts_sum - ps.post_survey_count) / ps.attempts_sum
        else:
            # defaults for simplicity
            ps = Storage({
                'post_survey_count': 0,
                'attempts_sum': 0,
                'duration_mean': 'NA',
                'm_frustrated_mean': 'NA',
                'm_satisfied_mean': 'NA',
                'm_happy_mean': 'NA',
                'm_sad_mean': 'NA',
                'm_overall_mean': 'NA',
                'mood_time_mean': 'NA',
                'free_write_time_mean': 'NA'
            })
            experienced_rejection_rate = 'NA'
        
        condition = json.loads(run.condition.json)
        vals = ([run.id, run.length, run.start_time, run.end_time, run.workerid, run.censored, run.other] 
                + [condition[key] for key in variables]
                + [es.age, es.gender, es.occupation, es.duration]
                + [v in es.biometric for v in biometricValues]
                + [ps.post_survey_count, ps.attempts_sum, experienced_rejection_rate, ps.duration_mean, 
                    ps.m_frustrated_mean, ps.m_satisfied_mean, ps.m_happy_mean,
                    ps.m_sad_mean, ps.m_overall_mean, ps.mood_time_mean,
                    ps.free_write_time_mean])
        writer.writerow(vals)
    
def export_post_surveys(stream, study):
    writer = csv.writer(stream)

    conditions = json.loads(study.conditions)
    variables = experimental_vars(study)
    biometricValues = [x['value'] for x in biometrics]
    
    header = ['id', 'run_length', 'start_time', 'end_time', 'workerid', 'censored', 'other']
    header += variables
    header += ['age', 'gender', 'occupation', 'duration']
    header += biometricValues
    header += ['time', 'survey_number', 'attempts', 'duration', 
        'm_frustrated', 'm_satisfied', 'm_happy', 'm_sad', 'm_overall', 'mood_time',
        'free_write_text', 'free_write_time', 'associations', 'association_times']
    
    writer.writerow(header)
    
    studyMatches = (db.runs.study==study) & \
                   (db.ks_post_surveys.study == study) & \
                   (db.ks_entry_surveys.study == study)
                   
    join = (db.runs.workerid == db.ks_post_surveys.workerid) & \
           (db.runs.workerid == db.ks_entry_surveys.workerid)
           
    entries = db(studyMatches & join).select(
        db.runs.ALL,
        db.ks_post_surveys.ALL,
        db.ks_entry_surveys.ALL,
        orderby=db.runs.start_time|db.ks_post_surveys.time
    )
    
    for entry in entries:
        run = entry.runs
        es = entry.ks_entry_surveys
        ps = entry.ks_post_surveys
        
        condition = json.loads(run.condition.json)
        vals = ([run.id, run.length, run.start_time, run.end_time, run.workerid, run.censored, run.other] 
                + [condition[key] for key in variables]
                + [es.age, es.gender, es.occupation, es.duration]
                + [v in es.biometric for v in biometricValues]
                + [ps.time, ps.completed, ps.attempts, ps.duration, 
                    ps.m_frustrated, ps.m_satisfied, ps.m_happy, ps.m_sad, ps.m_overall, ps.mood_time,
                    ps.free_write_text, ps.free_write_time, ps.associations, ps.association_times])
        writer.writerow(vals)
    

def create_indices_on_postgres_ks():
    '''Creates a set of indices if they do not exist'''
    ## Edit this list of table columns to index
    ## The format is [('table', 'column')...]
    indices = [('runs', 'workerid'),
               ('ks_entry_surveys', 'workerid'),
               ('ks_post_surveys', 'workerid')]
               
    for table, column in indices:
        index_exists = db.executesql("select count(*) from pg_class where relname='%s_%s_idx';"
                                     % (table, column))[0][0] == 1
        if not index_exists:
            db.executesql('create index %s_%s_idx on %s (%s);'
                          % (table, column, table, column))
        db.commit()
    
def process_keystroke_runs(study):
    db((db.runs.study==study)
       & (db.runs.length==0)).delete()
    db(db.runs.study==study).update(length=db.runs.length-1)
    db.commit()
