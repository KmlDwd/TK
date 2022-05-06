from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget

from utils import DirWalker, send_request
from core.model import Model
from core.results_presentation import ResultsPresentation, get_name
from .filter_selector_widget import FilterSelectorWidget
from .filter_selector_widget import ParametersWindow
from gui.parameter_windows.select_animal_window import SelectAnimalWindow
from gui.parameter_windows.select_format_window import SelectFormatWindow
from .parameter_windows.select_body_window import SelectBodyWindow
from .parameter_windows.select_style_window import SelectStyleWindow
from .similar_image_widget import SimilarImageWidget
from .select_directory_widget import SelectDirectoryWidget
from .path_template_widget import PathTemplateWidget
from .format_parameters_window import FormatParametersWindow




class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setFixedSize(1000, 800)
        self.model = model
        self.layout = QVBoxLayout()
        self.widgets = []
        form_widget = SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        self.layout.addWidget(form_widget)
        select_template_path_widget = PathTemplateWidget(parent=self, callback=self.model.update_template_path)
        self.layout.addWidget(select_template_path_widget)
        self.add_filter_selectors()
        paste_image_widget = SimilarImageWidget(parent=self, callback=lambda x: self.model.update_filters('similar', x))
        self.layout.addWidget(paste_image_widget)
        self.combo_box = self.add_results_presentation_selector()
        btn = QPushButton("Run", parent=self)
        btn.setGeometry(10, 450, 50, 30)
        btn.clicked.connect(self.run)
        self.layout.addWidget(btn)
        self.setLayout(self.layout)
        self.setWindowTitle("Image finder")
        self.show()

    def add_filter_selectors(self):
        self.add_selector(
            'File format',
            SelectFormatWindow(lambda x: self.model.update_filters('format', x)),
            100,
            False,
            'format',
        )
        self.add_selector(
            'Animal',
            SelectAnimalWindow(lambda x: self.model.update_filters('animal', x)),
            150,
            True,
            'animal',
        )
        self.add_selector(
            'Style',
            SelectStyleWindow(lambda x: self.model.update_filters('style', x)),
            200,
            False,
            'style',
        )
        self.add_selector(
            'Body parts',
            SelectBodyWindow(lambda x: self.model.update_filters('body', x)),
            250,
            True,
            'body',
        )

    def add_selector(self, label, window, ay, with_weight, model_label):
        widget = FilterSelectorWidget(
            label,
            window,
            ay,
            with_weight,
            lambda x: self.set_weight(model_label, x),
            model_label,
            self,
        )
        self.widgets.append(widget)
        self.layout.addWidget(widget)

    def add_results_presentation_selector(self):
        combo_box = QComboBox(self)
        for pres in [p for p in ResultsPresentation]:
            combo_box.addItem(get_name(pres))
        combo_box.currentIndexChanged.connect(self.selection_change)
        combo_box.setGeometry(10, 400, 100, 25)
        self.layout.addWidget(combo_box)
        return combo_box

    def get_enabled_components(self):
        return [widget.model_label for widget in self.widgets if widget.checkbox.isChecked()]

    def selection_change(self):
        self.model.update_results_presentation(self.combo_box.currentIndex())

    def set_weight(self, label, value):
        try:
            weight = int(value)
        except ValueError:
            weight = None
        self.model.update_weights(label, weight)

    def run(self):
        self.model.results = []
        walker = DirWalker(self.model.selected_directory, self.send_and_process)
        walker.walk()
        print(self.model.results)

    # def send_and_process(self, path):
    #     chosen_filters = {k: v for k, v in self.model.chosen_filters.items() if k in self.get_enabled_components()}
    #     for filter in chosen_filters:
    #         result = send_request(filter, chosen_filters[filter], path)
    #         if filter == 'format':
    #             if not result:
    #                 return
    #         if filter == 'body':
    #             if result > self.model.chosen_weights['body']:
    #                 return
    #         if filter == 'animal':
    #             correct = False
    #             for weight in result:
    #                 if weight > self.model.chosen_weights['animal']:
    #                     correct = True
    #             if not correct:
    #                 return
    #         self.model.update_results(path)

    def send_and_process(self, path):
        chosen_filters = {k: v for k, v in self.model.chosen_filters.items() if k in self.get_enabled_components()}
        results = send_request(chosen_filters, path)
        for filter in results.keys():
            if filter == 'animal':
                correct = False
                for weight in results['animal']:
                    if weight > self.model.chosen_weights['animal']:
                        correct = True
                if not correct:
                    return
            if filter == 'format':
                if not results['format']:
                    return
            if filter == 'body':
                if results['body'] < self.model.chosen_weights['body']:
                    return
            self.model.update_results(path)
