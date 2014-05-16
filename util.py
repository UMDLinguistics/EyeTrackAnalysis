# library for shared functions
import re
from csv import DictWriter


def ask_user_questions(question_sequence):
    '''Given a sequence of items (can be a list or a dictionary, anything
    that supports iteration), prints prompts for every item in the shell
    so that the user can input a value for every item.
    Returns a dictionary of (item_name : user_input) pairings.
    '''
    # set tab auto-completion, but only for current folder
    readline.parse_and_bind("tab: complete")
    # define question prompt template and return variable
    q_template = 'Please enter the {} below:\n'
    answers = {}

    for question in question_sequence:
        answers[question] = input(q_template.format(question))
    
    return answers


def write_to_csv(file_name, data, header, **kwargs):
    '''Writes data to file specified by filename.

    :type file_name: string
    :param file_name: name of the file to be created
    :type data: iterable
    :param data: some iterable of dictionaries each of which
    must not contain keys absent in the 'header' argument
    :type header: list
    :param header: list of columns to appear in the output
    :type **kwargs: dict
    :param **kwargs: parameters to be passed to DictWriter.
    For instance, restvals specifies what to set empty cells to by default or
    'dialect' loads a whole host of parameters associated with a certain csv
    dialect (eg. "excel").
    '''
    with open(file_name, 'w') as f:
        output = DictWriter(f, header, **kwargs)
        output.writeheader()
        output.writerows(data)


def create_row_dict(fields, item):
    # IK: this should go into a separate file, I think
    length_difference = len(fields) - len(item)
    error_message = 'There are more items than labels for them: {0}'
    if length_difference < 0:
        print('Here are the column labels', fields)
        print('Here are the items', item)
        raise Exception(error_message.format(length_difference))
    elif length_difference > 0:
        item = item + ('NA',) * length_difference

    return dict(zip(fields, item))


def get_subj_num(file_name):
    '''Given a filename string returns any substring that consists of digits.
    If multiple such substrings are found, returns the first one.
    If no such substrings are found, returns empty string.
    '''
    subj_n_rgx = re.compile('\d+')
    # we don't want to risk finding digits from file extensions
    extensionless = file_name.split('.')[0]
    matches = subj_n_rgx.findall(extensionless)

    if not matches:
        warning = "Unable to find subject number in this file name: \n{0}"
        print(warning.format(file_name))
        return ''

    elif len(matches) > 1:
        warning = "Found several numbers in '{0}', using the first one out of: \n{1}"
        print(warning.format(file_name, matches))

    return matches[0]