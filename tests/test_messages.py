import pytest
import json
from rushing_turtles.messages import HelloServerMsg, MessageDeserializer

def test_deserialize_should_raise_when_no_message_field():
  deserializer = MessageDeserializer()
  
  with pytest.raises(ValueError):
    deserializer.deserialize('{}')

def test_deserialize_should_raise_when_unknown_message():
  deserializer = MessageDeserializer()
  msg_json = json.dumps({'message': 'unknown type'})

  with pytest.raises(ValueError):
    deserializer.deserialize(msg_json)

def test_deserialize_should_raise_when_not_all_fields_are_present():
  deserializer = MessageDeserializer()
  msg_json = json.dumps({'message': 'hello server'})  

  with pytest.raises(ValueError):
    deserializer.deserialize(msg_json)

def test_deserialize_should_deserialize_hello_server_msg():
  deserializer = MessageDeserializer()
  msg_json = json.dumps({
    'message': 'hello server',
    'player_name': 'Piotr',
    'player_id': 0}
    )

  actual = deserializer.deserialize(msg_json)
  
  assert actual == HelloServerMsg(0, 'Piotr')