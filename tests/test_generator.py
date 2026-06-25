import pytest
from datetime import datetime
from app.generator import IdeaGenerator
from unittest.mock import MagicMock

def test_generator_can_be_created():
    generator = IdeaGenerator(api_key="test_key")
    assert generator.client is not None

def test_generate_return_ideas():
    generator = IdeaGenerator(api_key="test_key")

    mock_message = MagicMock()
    mock_message.content[0].text = '["ideja1", "ideja2", "ideja3"]'
    generator.client.messages.create = MagicMock(return_value=mock_message)

    result = generator.generate(topic="test topic", count=3)

    assert result == '["ideja1", "ideja2", "ideja3"]'


def test_save_create_file():
    generator = IdeaGenerator(api_key="test_key")
    test_ideas = ["ideja1", "ideja2", "ideja3"]
    test_topic="test ideas"

    saved_file = generator.save(topic=test_topic, ideas=test_ideas)

    assert saved_file.exists()

def test_history_returns_list():
    generator = IdeaGenerator(api_key="test_key")
    result = generator.history()
    assert isinstance(result, list)