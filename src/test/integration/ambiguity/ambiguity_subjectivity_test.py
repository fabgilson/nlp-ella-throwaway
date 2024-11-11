import pytest

from main.resources.AmbiguityErrorMessages import AmbiguityErrorMessages
from main.resources.AmbiguityErrorTypes import AmbiguityErrorTypes

@pytest.fixture
def ambiguity_defect_types():
    return AmbiguityErrorTypes()

@pytest.fixture
def ambiguity_error_messages():
    return AmbiguityErrorMessages()

def helper(response):
    """
    Transforms what is returned by the API to the expected format
    """
    defects = response.json
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["description"]
    return transformed_defects

### NOTE: GOING VIA THE USER STORY ENDPOINT TO TEST THE AMBIGUITY STUFF BUT SAME THING OCCURS ON THE AC ENDPOINT ###


@pytest.mark.parametrize("story_text", [
    "As a user and as a writer I want to login to my account so that I can access my account.",
    "As a user and as a developer I want to redesign the page so that the page matches the new Broker design styles.",
    "as a dev and as a user I want to be able to share user feedback so that users are aware of contributions to making Broker."
])
def test_no_superlatives_has_no_superlative_issues(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity not in data


@pytest.mark.parametrize("story_text", [
    "The newer models are even more cheaper and more efficient.",
    "These apples are much fresher, and those oranges are juicier than any I've had before.",
    "The book was more interesting, but the movie adaptation was the most captivating."
])
def test_comparison_has_errors(test_client, ambiguity_defect_types, story_text, ambiguity_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "comparative" in "".join(data[ambiguity_defect_types.ambiguity])


@pytest.mark.parametrize("story_text", [
    "Alice is by far the smartest student in the class.",
    "This is the most interesting book I have ever read.",
    "He drives by far the fastest car in the race.",
    "Of all the students, she is the most hardworking and the most punctual.",
    "This is the best and the most reliable option available."
])
def test_superlatives_has_errors(test_client, ambiguity_defect_types, story_text, ambiguity_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "superlative" in "".join(data[ambiguity_defect_types.ambiguity])


@pytest.mark.parametrize("story_text", [
    "This is the most expensive item, but it’s also better",
    "This path is the worst, but it is a lot shorter."
])
def test_superlatives_and_comparitives_has_errors(test_client, ambiguity_defect_types, story_text, ambiguity_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "comparative" in "".join(data[ambiguity_defect_types.ambiguity])
    assert "superlative" in "".join(data[ambiguity_defect_types.ambiguity])