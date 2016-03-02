from gluon.sqlhtml import SQLFORM

class AwesomeSQLFORM(SQLFORM):
    def __init__(self, *args, **kwargs):
        self.table = args[0]

        super(AwesomeSQLFORM, self).__init__(*args, **kwargs)

        self._add_requireds()

    def _add_requireds(self):
        requireds = {field : self.table[field].required for field in self.table.fields}
        labels = self.elements('label')

        for element in self.elements('input', 'select', 'textarea'):
            # TODO: Make it so that file is required on create forms but not update forms
            # currently disabled as it prevents submitting an update form without changing
            # the image
            if element['_type'] not in {'submit', 'file'} and requireds[element['_name']]:
                # Add element required attribute
                element['_required'] = ''

                # Add * next to label for required field
                for label in labels:
                    if label['_for'] == str(self.table)+'_'+element['_name']:
                        label.components[0] = '{} *'.format(label.components[0])
                        break
