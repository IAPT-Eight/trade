from gluon.sqlhtml import SQLFORM
from gluon.validators import *

def _make_iterable(ob):
    if not hasattr(ob, '__iter__') and not hasattr(ob, '__getitem__'):
        return [ob]
    return ob

class AwesomeSQLFORM(SQLFORM):
    def __init__(self, *args, **kwargs):
        self.table = args[0]
        self.validators = {field : _make_iterable(self.table[field].requires) for field in self.table.fields}

        self.is_update_form = len(args) > 1 or 'record' in kwargs.keys()

        super(AwesomeSQLFORM, self).__init__(*args, **kwargs)

        self._add_requireds()
        self._add_numeric_bounds()
        self._add_textsize_bounds()
        self._add_accepts()

    # To avoid the following error, only add required attribute to select elements
    # that don't have zero=None on the Field's IS_IN_DB validator (if any).
    # Error: The first child option element of a select element with a required
    # attribute, and without a multiple attribute, and without a size attribute whose
    # value is greater than 1, must have either an empty value attribute, or must have
    # no text content. Consider either adding a placeholder option label, or adding a
    # size attribute with a value equal to the number of option elements.
    def _should_add_select_required(self, select_element):
        return not any(isinstance(v, IS_IN_DB) and v.zero == None for v in self.validators.get(select_element["_name"]))

    def _add_requireds(self):
        requireds = {field : self.table[field].required for field in self.table.fields}
        labels = self.elements('label')

        for element in self.elements('input', 'select', 'textarea'):
            if element['_type'] not in {'submit'} and requireds[element['_name']]:
                # Add * next to label for required field
                for label in labels:
                    if label['_for'] == str(self.table)+'_'+element['_name']:
                        label.components.append(' *')
                        break

                # Only add required to upload fields on create forms, not update forms,
                # as it prevents the form from being submitted without changing the file.
                # However, we do want to add the * next to the label even if it isn't
                # technically required (it does already have a value in the system..)
                if element['_type'] == 'file' and self.is_update_form:
                    continue

                if element.tag == 'select' and not self._should_add_select_required(element):
                    continue

                # Add element required attribute
                element['_required'] = ''

    def _add_numeric_bounds(self):
        for element in self.elements('input'):
            for validator in self.validators.get(element['_name'], []):
                if any(isinstance(validator, vclass) for vclass in [IS_INT_IN_RANGE, IS_DECIMAL_IN_RANGE, IS_FLOAT_IN_RANGE]):
                    element['_type'] = 'number'
                    element['_min'] = validator.minimum
                    element['_max'] = validator.maximum

                    if isinstance(validator, IS_INT_IN_RANGE):
                        element['_step'] = 1
                    else:
                        element['_step'] = "any"

    def _add_textsize_bounds(self):
        for element in self.elements('input', 'textarea'):
            for validator in _make_iterable(self.validators.get(element['_name'])):
                if any(isinstance(validator, vclass) for vclass in [IS_LENGTH]):
                    element['_minlength'] = validator.minsize
                    element['_maxlength'] = validator.maxsize

    def _add_accepts(self):
        for element in self.elements('input'):
            for validator in _make_iterable(self.validators.get(element['_name'])):
                if any(isinstance(validator, vclass) for vclass in [IS_IMAGE]):
                    element['_accept'] = ','.join('.{}'.format(e) for e in validator.extensions)
