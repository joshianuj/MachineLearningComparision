SAMPLE_FREQUENCY_COMBO_BOX = {
    '2.86MHz': {
        'value': 2.86*1e6,
        'echo_size': 1024,
    }, '1.14MHz': {
        'value': 1.14*1e6,
        'echo_size': 1024,
    },
    '114MHz': {
        'value': 114*1e6,
        'echo_size': 1024,
    }
}


class Variables():
    def __init__(self):
        self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX['2.86MHz']
        self.LOW_PASS = 30*1e4
        self.HIGH_PASS = 60*1e4
        self.THRESHOLD = 0.15
        self.DATA_HEADERS_SIZE = 9
        self.order = 5
        pass

    def change_selected_element(self, element_name):
        if element_name in SAMPLE_FREQUENCY_COMBO_BOX:
            self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX[element_name]
