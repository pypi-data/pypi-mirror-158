import json
import time
import warnings

from sqlalchemy import insert
from sqlalchemy.sql.expression import bindparam

from autocnet.io.db.model import Points, Measures
from autocnet.utils.serializers import object_hook
from autocnet.transformation.spatial import reproject, og2oc

def watch_insert_queue(queue, queue_name, counter_name, engine, stop_event, sleep_time=5):
    """
    A worker process to be launched in a thread that will asynchronously insert or update 
    objects in the Session using dicts pulled from a redis queue. Using this queuing approach
    many cluster jobs are able to push to the redis queue rapidly and then a single writer
    process can push the data back to the database.
    
    This function requires that the function called by the asynchronous cluster job INCR
    (increment) the counter_name key in the redis cache. This counter is INCR (incremented) 
    by cluster jobs to track how many messages have been pushed to the queue (queue_name). 
    This func then reads that many messages and DECR (de-increments) the counter by that
    many messages. This way this function only reads when data is present and reads can occur 
    asynchronously. This works becase the cluster job pushes to the right side of the redis
    list and this function reads n-messages from the left side.
    
    This method uses the sqlalchemy core interface for performance reasons. Therefore, some
    mundging of column names is used to ensure that the model to be processed matches the
    database column names.
    
    Parameters
    ----------
    queue : obj
            A Redis or StrictRedis connection instance
    
    queue_name : str
                 The name of the queue to watch
                 
    counter_name : str
                   The name of the incrementing counter to watch. 
                   
    operation : str
                either 'insert' or 'update'. If 'insert', the sqlalchemy
                bulk_insert_mappings func is used to add new rows. If 'update', 
                the sqlalchemy bulks_update_mappings func is used.
    
    engine : obj
              A sqlalchemy engine. 
              
    stop_event : obj
                 A threading.Event object with set and is_set members. This is the
                 poison pill that can be set to terminate the thread.
    """
    # Use a pipe for efficient reads
    pipe = queue.pipe()
    while not stop_event.is_set():

        # Determine the read length of objects to pull from the cache
        # Cap the read length at 250 messages to improve memory usage and throughput
        read_length = int(queue.get(counter_name))
        if read_length > 250:
            read_length = 250
        # Pull the objects from the cache
        points = []
        measures = []
        
        # Pull the SRID dynamically from the model (database)
        rect_srid = Points.rectangular_srid
        lat_srid = Points.latitudinal_srid
        
        try:
            # Pop the messages off the queue
            for i in range(0, read_length):
                pipe.lpop(queue_name)
                pipe.decr(counter_name)
            msgs = pipe.execute()
        except:
            msgs = []
            time.sleep(5)

        for msg in msgs:
            msg = json.loads(msg, object_hook=object_hook)
            if isinstance(msg, dict):
                # A NULL id is not allowable, so pop if a NULL ID exists
                if msg['id'] == None:
                    msg.pop('id', None)

                # Since this avoids the ORM, need to map the table names manually
                msg['pointType'] = msg['pointtype']  
                adjusted = msg['adjusted']
            
                msg['adjusted'] = f'SRID={rect_srid};' + adjusted.wkt  # Geometries go in as EWKT
                msg['apriori'] = f'SRID={rect_srid};' + adjusted.wkt

                lon_og, lat_og, _ = reproject([adjusted.x, adjusted.y, adjusted.z],
                                    Points.semimajor_rad, Points.semiminor_rad,
                                    'geocent', 'latlon')
                lon, lat = og2oc(lon_og, lat_og, Points.semimajor_rad, Points.semiminor_rad)
                msg['geom'] = f'SRID={lat_srid};Point({lon} {lat})' 

                # Measures are removed and manually added later
                point_measures = msg.pop('measures', [])
                if point_measures:
                    measures.append(point_measures)
                
                points.append(msg)
            
        if not points:
            continue
        
        try:
            # Write the cached objects into the database 
            with engine.connect() as conn:
                resp = conn.execute(
                    insert(Points.__table__).returning(Points.__table__.c.id),points
                )
                pointids = [i[0] for i in resp.all()]

                # Measures are a list of lists. Associate each list with a pointid and then flatten the list
                for i, measure_set in enumerate(measures):
                    for measure in measure_set:
                        measure['pointid'] = pointids[i]
                        measure.pop('id', None)  # As above, remove the NULL id
                        # Remap field names because the ORM is NOT being used
                        measure['serialnumber'] = measure.pop('serial', None)
                        measure['measureType'] = measure.pop('measuretype')
                measures = [measure for sublist in measures for measure in sublist]
                conn.execute(
                    insert(Measures.__table__), measures)
        except:
            try:
                # Pop the messages off the queue
                for i in range(0, read_length):
                    pipe.rpush(queue_name, msgs[i])
                    pipe.incr(counter_name)
                msgs = pipe.execute()
            except:
                warnings.warn('Failed to push to DB and failed to repopulate queue.')
                time.sleep(5)

def watch_update_queue(queue, queue_name, counter_name, engine, stop_event, sleep_time=5):
    """
    A worker process to be launched in a thread that will asynchronously insert or update 
    objects in the Session using dicts pulled from a redis queue. Using this queuing approach
    many cluster jobs are able to push to the redis queue rapidly and then a single writer
    process can push the data back to the database.
    
    This function requires that the function called by the asynchronous cluster job INCR
    (increment) the counter_name key in the redis cache. This counter is INCR (incremented) 
    by cluster jobs to track how many messages have been pushed to the queue (queue_name). 
    This func then reads that many messages and DECR (de-increments) the counter by that
    many messages. This way this function only reads when data is present and reads can occur 
    asynchronously. This works becase the cluster job pushes to the right side of the redis
    list and this function reads n-messages from the left side.
    
    This method uses the sqlalchemy core interface for performance reasons. Therefore, some
    mundging of column names is used to ensure that the model to be processed matches the
    database column names.
    
    Parameters
    ----------
    queue : obj
            A Redis or StrictRedis connection instance
    
    queue_name : str
                 The name of the queue to watch
                 
    counter_name : str
                   The name of the incrementing counter to watch. 
                   
    operation : str
                either 'insert' or 'update'. If 'insert', the sqlalchemy
                bulk_insert_mappings func is used to add new rows. If 'update', 
                the sqlalchemy bulks_update_mappings func is used.
    
    engine : obj
              A sqlalchemy engine. 
              
    stop_event : obj
                 A threading.Event object with set and is_set members. This is the
                 poison pill that can be set to terminate the thread.
    """
    while not stop_event.is_set():
        # Determine the read length of objects to pull from the cache
        read_length = int(queue.get(counter_name))
        # Pull the objects from the cache
        measures = []
        
        for i in range(0, read_length):
            msg = json.loads(queue.lpop(queue_name), object_hook=object_hook)
            if isinstance(msg, dict):
                msg['_id'] = msg.pop('id', None)  # id is reserved by sqlalchemy on insert/update, remapped below
                measures.append(msg)

            # The message was successfully read, so atomically deincrement the counter
            queue.decr(counter_name)
                    
        # Write the updated measures to the db 
        if measures:
            with engine.connect() as conn:
                stmt = Measures.__table__.update().\
                            where(Measures.__table__.c.id == bindparam('_id')).\
                            values({'weight':bindparam('weight'),
                                    'measureIgnore':bindparam('ignore'),
                                    'templateMetric':bindparam('template_metric'),
                                    'templateShift':bindparam('template_shift'),
                                    'line': bindparam('line'),
                                    'sample':bindparam('sample'),
                                    'ChooserName':bindparam('choosername')})
                resp = conn.execute(
                    stmt, measures
                )

    time.sleep(sleep_time)
