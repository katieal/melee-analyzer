from enum import Enum, StrEnum, auto

# input field variables
MAX_URL_LENGTH = 100
MAX_NAME_LENGTH = 20
MAX_INPUT_LENGTH = 30



INPUT_PATTERNS = {
    'Start.gg': [r'^https://www.start.gg/'],
    'Challonge': [r'^https://challonge.com/', r'^https://www.challonge.com/'],
    'Other': [r'^https://']
}


APP_IDS = {
    # app.py
    'success_modal': 'success-modal',

    #add_tournament.py
    'add_tournament': {
        'input': {
            'name': {'type': 'input-field', 'element': 'name-input', 'key': 'name'},
            'date': {'type': 'alt-input-field', 'element': 'date-picker'},
            'location': {'type': 'input-field', 'element': 'location-input', 'key': 'location'},
            'format': {'type': 'input-field', 'element': 'format-select', 'key': 'format'},
            'theme': {'type': 'input-field', 'element': 'theme-input', 'key': 'theme'},
            'winner': {'type': 'input-field', 'element': 'winner-input', 'key': 'winner'},
            'website': {'type': 'input-field', 'element': 'website-select', 'key': 'website'},
            'bracket_type': {'type': 'bracket-type-select', 'element': 'add-bracket'}
        },

        'button': {
            'add_theme': {'type': 'dynamic-add', 'element': 'theme'},
            'delete_theme': {'type': 'dynamic-delete', 'element': 'theme'},
            'add_website': {'type': 'dynamic-add', 'element': 'website'},
            'delete_website': {'type': 'dynamic-delete', 'element': 'website'},
            'add_manual': {'type': 'dynamic-add', 'element': 'bracket'},
            'delete_manual': {'type': 'dynamic-delete', 'element': 'bracket'},
            'add_bracket': 'add-bracket-button',
            'delete_bracket': 'delete-bracket-button', # unused currently?
        },

        'container': {
            'theme': {'type': 'dynamic-input', 'element': 'theme'}
        },
    }

}


class ElementType(StrEnum):
    LABEL = auto()
    INPUT = auto()
    BUTTON = auto()
    CONTAINER = auto()