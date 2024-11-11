import pytest

from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

def helper(response):
    """
    Transforms response into expected format
    """
    defects = response.json[0]["defects"]
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["descriptions"]
    return transformed_defects


@pytest.mark.parametrize("acs", [
    ["Given I am on the edit profile form, and I enter a first name or last name that is more than 64 characters, when I click the “Submit” button, then an error message tells me “{First/Last} name must be 64 characters long or less”."],
    ["Given I am on the edit profile form, and I enter an empty or malformed email address (i.e. an email address that does not have a prefix, second-level domain, and top-level domain or has invalid characters), when I click the “Submit” button, then an error message tells me “Email address must be in the form ‘jane@doe.nz’”."],
    ["Given I am on the edit garden form, and I enter an empty or invalid (i.e. non-alphanumeric characters other than spaces, dots, commas, dot, hyphens, or apostrophes) garden name, when I click “Submit”, then an error message tells me “Garden name cannot by empty” or “Garden name must only include letters, numbers, spaces, dots, hyphens or apostrophes”"],
    ["Given I am on the login form, and I enter a malformed (i.e. an email address that does not have a prefix, second-level domain, and top-level domain or has invalid characters) or empty email address, when I hit the login button, then an error message tells me “Email address must be in the form ‘jane@doe.nz’”."],
    ["Given I am on the edit profile form, and I enter valid values for my first name, last name, email address, and date of birth, when I click the “Submit” button, then my new details are saved and I am taken back to my profile page."],
    ["Given I am logged in, when I click on the “My Profile” button, then I am taken to a page with all my details i.e. my first and last names, date of birth and email address."],
    ["Given I enter an invalid description (i.e. more than 512 characters long, or contains only special characters and numbers), when I submit the form, then an error message tells me that “Description must be 512 characters or less and contain some text” and the description is not persisted."],
    ["Given I am on the edit profile form, and I enter invalid values (i.e. an empty first name, an empty or blank last name without checking the “I have no surname” checkbox, non-alphabetical characters except hyphen, space or apostrophe for either first or last name), when I click the “Submit” button, then an error message tells me “{First/Last} name cannot by empty” or “{First/Last} name must only include letters, spaces, hyphens or apostrophes”."],
    ["Given I am on the edit profile form, and I enter an empty or malformed email address (i.e. an email address that does not have a prefix, second-level domain, and top-level domain or has invalid characters), when I click the “Submit” button, then an error message tells me “Email address must be in the form ‘jane@doe.nz’”."],
    ["Given I am on the change password form, and I enter a weak password (e.g., contains any other fields from the user profile form, is below 8 char long, does not contain a variation of different types of characters with one lowercase letter, one uppercase letter, one digit, one special character), when I hit the save button, then an error message tells “Your password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.”"],
    ["Given I am on the create new Garden form, and I enter valid values for the name, location, and optionally a size, when I click “Create”, then a new Garden is created and I am taken to the Garden details page."],
    ["Given I am on the create new Garden form, and I enter an empty (including made of blank characters only) or invalid (i.e. non-alphanumeric characters other than spaces, dots, commas, dots, hyphens, or apostrophes) garden name, when I click “Create”, then an error message tells me “Garden name cannot by empty” or “Garden name must only include letters, numbers, spaces, dots, hyphens or apostrophes”."],
    ["Given I am on the create new Garden form, and enter an empty location or a location with invalid characters (i.e. non-alphanumeric characters other than spaces, commas, dots, hyphens, or apostrophes), when I click “Create”, then an error message tells me “Location cannot be empty” or “Location name must only include letters, numbers, spaces, commas, dots, hyphens or apostrophes”."],
    ["Given I am on the create new Garden form, and enter an invalid (i.e. any character other than numbers, and a single dot or single comma) size in m^2, when I click “Create”, then an error message tells me “Garden size must be a positive number”"],
    ["Given I am on the edit garden form, and I enter valid values for the name, location, and optionally a size, when I click “Submit”, then the Garden details are updated and I am taken back to the Garden page."],
    ["Given I am on the edit garden form, and I enter an empty or invalid (i.e. non-alphanumeric characters other than spaces, dots, commas, dot, hyphens, or apostrophes) garden name, when I click “Submit”, then an error message tells me “Garden name cannot by empty” or “Garden name must only include letters, numbers, spaces, dots, hyphens or apostrophes”"],
    ["Given I am on the edit garden form, and enter an empty location or a location with invalid characters (i.e. non-alphanumeric characters other than spaces, dots, commas, hyphens, or apostrophes), when I click “Submit”, then an error message tells me “Location cannot be empty” or “Location name must only include letters, numbers, spaces, dots, hyphens or apostrophes”."],
    ["Given I am on the create edit garden form, and enter an invalid (i.e. any character other than numbers, and a single dot or single comma) size in m^2, when I click “Submit”, then an error message tells me “Garden size must be a positive number”."],
    ["Given I am on the add plant form, and I enter valid values for the name and optionally a number (i.e. count), description, and a planted-on date , when I click the “Submit” button, then a new plant record is added to the garden, and I am taken back to the garden details page."],
    ["Given I am on the add new plant form, and I enter an empty or invalid (i.e. non-alphanumeric characters other than spaces, dots, commas, hyphens, or apostrophes) plant name, when I click “Submit” then an error message tells me “Plant name cannot by empty and must only include letters, numbers, spaces, dots, hyphens or apostrophes”."],
    ["Given I am on the garden details page for a garden I own, then there is a list of all plants I have recorded in the garden with their name, a default image, and count and description (if provided)."],
    ["Given I am on the edit plant form, and I enter valid values for the name and optionally a number (i.e. count), description, and a planted-on date , when I click the “Submit” button, then the plant record is updated, and I am taken back to the garden details page."],
    ["Given I have entered a tag that is more than 25 characters, when I click the “+” button or press enter, then an error message tells me “A tag cannot exceed 25 characters”, and no tag is added to my garden and no tag is added to the user defined tags the system knows."]
])
def test_singularity_has_lists_marked_as_not_singular(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.singularity in data
    assert acceptance_criteria_error_messages.list_in_ac in data[acceptance_criteria_defect_types.singularity]


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the change password form, when I enter fully compliant details, when I click the “Submit” button, then my password is updated, and an email is sent to my email address to confirm that my password was updated."],
    ["Given I am on the change password form, when I hit the cancel button, then I am sent back to my view details page, and no changes have been made to my password."],
    ["Given I am on the add new plant form, when I click the “Cancel” button, I am taken back to the garden details page, and no changes are made."],
    ["Given I am on the registration form, and I enter a date of birth for someone older than 120 years old, when I click the “Sign up” button, then an error message tells me “The maximum age allowed is 120 years”"],
    ["Given I am on the registration form, and I enter a date of birth for someone younger than 13 years old, when I click the “Sign up” button, then an error message tells me, “You must be 13 years or older to create an account”"],
    ["Given I am on the edit profile form, if I have already indicated that I do not have a last name, then this field defaults to being disabled and the “I have no surname” checkbox is marked as checked."],
    ["Given I am on the edit profile form, and I enter a date of birth for someone younger than 13 years old, when I click the “Submit” button, then an error message tells me, “You must be 13 years or older to create an account”."],
    ["Given I am on the edit profile form, and I enter a date of birth for someone older than 120 years old, when I click the “Submit” button, then an error message tells me “The maximum age allowed is 120 years”."],
    ["Given I submit a fully valid registration form, when I click the “Register” button, then a confirmation email is sent to my email address, and a unique registration token is included in the email in the form of a unique signup code and I’m presented with a page asking for the signup code"],
    ["Given I received a signup code, when I want to log in to the system for the first time, then I must use the signup code."],
    ["Given I am on the add new plant form, and I enter a description that is longer than 512 characters, when I click “Submit” and error message tells me “Plant description must be less than 512 characters”."],
    ["Given I am on the edit plant form, and I enter a description that is longer than 512 characters, when I click “Submit” and error message tells me “Plant description must be less than 512 characters”."],
    ["Given I see a record for a plant in one of my gardens, when I click the semi-transparent “+” button at the top right of the image, then I am prompted to upload an image."],
    ["Given I see a matching person for the search I made, when I hit the “invite as friend ” button, then the other user receives an invite that will be shown in their “manage friends” page."],
    ["Given I see autocomplete options, when I click on one suggestion, then that tag should be added to my garden and the textbox cleared."],
    ["Given the submitted tag is evaluated for appropriateness, when it is flagged as inappropriate, then an error message tells me that the submitted word is not appropriate and the tag is not added to the list of user-defined tags."],
    ["Given I am viewing autocomplete suggestions for my input, when I click on a suggestion, then the tag is added to my current selection, and the text field is cleared."],
    ["Given my account is blocked, when I try to log into the system with valid credentials, then I receive a message telling me that my account is blocked for X days, where X is the number of remaining days my account is blocked for."],
    ["Given I am creating a new garden, when I add an optional description of the garden, and I submit the form, and the description is valid, then the description is persisted."],
    ["Given I am on my “manage friends” page, when I have pending request that I have sent, then I can cancel my friend request, and the other user cannot see the friend request, and the other user cannot accept the request anymore."],
    ["Given I am on the edit profile form, when I click the “Cancel” button, I am taken back to my profile page, and no changes have been made to my profile."],
])
def test_singularity_has_no_lists_marked_as_singular(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.singularity not in data
