import json
import os
from unittest import mock
from unittest.mock import patch

import numpy as np
import pytest
import logging

from autocnet.utils.serializers import JsonEncoder, object_hook
from autocnet.graph import cluster_submit
from autocnet.graph.node import NetworkNode
from autocnet.graph.edge import NetworkEdge
from autocnet.io.db.model import Points, JobsHistory

log = logging.getLogger(__name__)

@pytest.fixture
def args():
    arg_dict = {'working_queue':'working',
                'processing_queue':'processing',
                'queue':False}
    return arg_dict

@pytest.fixture
def simple_message():
    return json.dumps({"job":"do some work",
                       'args' : ["arg1", "arg2"],
                       'kwargs' : {"k1" : "foo", "k2" : "bar"},
                       'func':'autocnet.place_points',
                       'results' :[{"status" : 'success'}] }, cls=JsonEncoder
    )

@pytest.fixture
def complex_message():
    return json.dumps({'job':'do some complex work',
                      'arr':np.ones(5),
                      'results' :[{"status" : 'success'}], 
                      'args' : ["arg1", "arg2"],
                      'kwargs' : {"k1" : "foo", "k2" : "bar"},
                      'func':'autocnet.place_points'}, cls=JsonEncoder)

def test_manage_simple_messages(args, queue, simple_message, mocker, capfd, ncg):
    queue.rpush(args['processing_queue'], simple_message)

    response_msg = {'success':True, 
                    'results':'Things were good.', 
                    'kwargs' : {'Session' : ncg.Session}}
    mocker.patch('autocnet.graph.cluster_submit.process', return_value=response_msg)
    mocker.patch.dict(os.environ, {"SLURM_JOB_ID": "1000"}) 

    cluster_submit.manage_messages(args, queue)
    
    # Check that logging to stdout is working
    out, err = capfd.readouterr()
    print('OE', out, err)
    assert out.strip() == str(response_msg).strip() 

    # Check that the messages are finalizing
    assert queue.llen(args['working_queue']) == 0

def test_manage_complex_messages(args, queue, complex_message, mocker, capfd, ncg):
    queue.rpush(args['processing_queue'], complex_message)

    response_msg = {'success':True, 'results':'Things were good.', 'kwargs' : {'Session' : ncg.Session}}
    mocker.patch('autocnet.graph.cluster_submit.process', return_value=response_msg)
    mocker.patch.dict(os.environ, {"SLURM_JOB_ID": "1000"}) 
 
    cluster_submit.manage_messages(args, queue)
    
    # Check that logging to stdout is working
    out, err = capfd.readouterr()
    assert out.strip() == str(response_msg).strip()

    # Check that the messages are finalizing
    assert queue.llen(args['working_queue']) == 0


'''def test_job_history(args, queue, complex_message, mocker, capfd, ncg):
    queue.rpush(args['processing_queue'], complex_message)

    response_msg = {'success':True, 
                    'args' : ["arg1", "arg2"],
                    'kwargs' : {"k1" : "foo", "k2" : "bar", "Session" : ncg.Session}}
    mocker.patch('autocnet.graph.cluster_submit.process', return_value=response_msg)
    mocker.patch.dict(os.environ, {"SLURM_JOB_ID": "1000"}) 
    
    cluster_submit.manage_messages(args, queue)
    
    message_json = json.loads(complex_message)
    with ncg.Session() as session: 
        resp = session.query(JobsHistory).first()
        assert resp.functionName == "autocnet.place_points"
        assert resp.jobId == 1000
        assert resp.args == {"args" : message_json["args"], "kwargs" : message_json["kwargs"]}
        assert resp.logs.strip() == str(response_msg).strip()'''

def test_transfer_message_to_work_queue(args, queue, simple_message):
    queue.rpush(args['processing_queue'], simple_message)
    cluster_submit.transfer_message_to_work_queue(queue, args['processing_queue'], args['working_queue'])
    msg = queue.lpop(args['working_queue'])
    assert msg.decode() == simple_message

def test_finalize_message_from_work_queue(args, queue, simple_message):
    remove_key = simple_message
    queue.rpush(args['working_queue'], simple_message)
    cluster_submit.finalize_message_from_work_queue(queue, args['working_queue'], remove_key)
    assert queue.llen(args['working_queue']) == 0
    
def test_no_msg(caplog,args, queue):
    cluster_submit.manage_messages(args, queue)
    expected_log = 'Expected to process a cluster job, but the message queue is empty.'
    assert expected_log in caplog.text
    


# Classes and funcs for testing job submission.
class Foo():
    def test(self, *args, **kwargs):
        return True

def _do_nothing(*args, **kwargs): 
    return True

def _generate_obj(msg, ncg):
    return Foo()

@pytest.mark.parametrize("along, func, msg_additions", [
                            ('edge', _do_nothing, {'id':(0,1), 'image_path':('/foo.img', '/foo2.img')}),  # Case: callable func
                            ('node', _do_nothing, {'id':0, 'image_path':'/foo.img'}),   # Case: callable func
                            ('edge', 'test', {'id':(0,1), 'image_path':('/foo.img', '/foo2.img')}),  # Case: method on obj
                            ('node', 'test', {'id':0, 'image_path':'/foo.img'}),   # Case: method on obj
                            ('edge', 'graph.tests.test_cluster_submit._do_nothing', {'id':(0,1), 'image_path':('/foo.img', '/foo2.img')}),  # Case: imported func
                            ('node', 'graph.tests.test_cluster_submit._do_nothing', {'id':0, 'image_path':'/foo.img'}),   # Case: imported func
                        ])
def test_process_obj(along, func, msg_additions, mocker):
    msg = {'along':along,
          'config':{},
          'func':func,
          'args':[],
          'kwargs':{}}
    msg ={**msg, **msg_additions}
    mocker.patch('autocnet.graph.cluster_submit._instantiate_obj', side_effect=_generate_obj)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.Session', return_value=True)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.config_from_dict')

    msg = cluster_submit.process(msg)
    
    # Message result should be the same as 
    assert msg['results'] == True
    
    cluster_submit._instantiate_obj.assert_called_once()

@pytest.mark.parametrize("along, func, msg_additions", [
    ('points', _do_nothing, {}),
    ('measures', _do_nothing, {}),
    ('overlaps', _do_nothing, {}),
    ('images', _do_nothing, {})
])
def test_process_row(along, func, msg_additions, mocker):
    msg = {'along':along,
        'config':{},
        'func':func,
        'args':[],
        'kwargs':{}}
    msg ={**msg, **msg_additions}
    mocker.patch('autocnet.graph.cluster_submit._instantiate_row', side_effect=_generate_obj)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.Session', return_value=True)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.config_from_dict')
    msg = cluster_submit.process(msg)
    
    # Message result should be the same as 
    assert msg['results'] == True
    
    cluster_submit._instantiate_row.assert_called_once()

@pytest.mark.parametrize()
def _do_something(log_level):
    return getattr(log, log_level)(f'Logging at the {log_level}')

def test_do_something(caplog):
    log_levels = ["critical", "error", "warning", "info", "debug"]
    
    for level in log_levels:
        os.environ["AUTOCNET_LOGLEVEL"] = level
        _do_something(os.environ["AUTOCNET_LOGLEVEL"])

        for record in caplog.records:
            # casting the env var and record level to a string for comparison 
            assert(str(os.environ["AUTOCNET_LOGLEVEL"]).upper() == str(record.levelname).upper())
            caplog.clear()


@pytest.mark.parametrize("along, func, msg_additions",[
                        ([1,2,3,4,5], _do_nothing, {})
                        ])
def test_process_generic(along, func, msg_additions, mocker):
    msg = {'along':along,
        'config':{},
        'func':func,
        'args':[],
        'kwargs':{}}
    msg ={**msg, **msg_additions}
    mocker.patch('autocnet.graph.cluster_submit._instantiate_row', side_effect=_generate_obj)
    mocker.patch('autocnet.graph.cluster_submit._instantiate_obj', side_effect=_generate_obj)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.Session', return_value=True)
    mocker.patch('autocnet.graph.network.NetworkCandidateGraph.config_from_dict')
    
    assert not cluster_submit._instantiate_row.called
    assert not cluster_submit._instantiate_obj.called

    msg = cluster_submit.process(msg)

    # Message result should be the same as 
    assert msg['results'] == True

@pytest.mark.parametrize("msg, expected", [
                            ({'along':'node','id':0, 'image_path':'/foo.img'}, NetworkNode),
                            ({'along':'edge','id':(0,1), 'image_path':('/foo.img', '/foo2.img')}, NetworkEdge)
                            ])
def test_instantiate_obj(msg, expected):
    obj = cluster_submit._instantiate_obj(msg, None)
    assert isinstance(obj, expected)

@pytest.mark.parametrize("msg, expected", [
                            ({'along':'points','id':0}, Points),
                            ])

def test_instantiate_row(msg, expected, mocker):
    mock_ncg = mocker.MagicMock()
    # Mock the db query to return a row of the requested type
    mock_ncg.apply_iterable_options.return_value = {'points':Points}
    mock_ncg.session_scope.return_value.__enter__.return_value.query.return_value.filter.return_value.one.return_value = expected()

    obj = cluster_submit._instantiate_row(msg, mock_ncg)
    assert isinstance(obj, expected)