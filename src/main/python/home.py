import datetime
import classes as sc
import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qc
import PyQt6.QtGui as qg
from sWidgets import SPushButton, get_formatted_date, ask_save, sanitize
# import pdb


class HomePage(qt.QDialog):
    def __init__(self, main_window, db):
        super().__init__()
        self.db = db
        v = self.db.settings.verbose
        self.main_window = main_window
        self.main_window.setCentralWidget(self)
        # self.db.competition = self.db.t.competition.get(competition_id)
        self.changes_made = False
        self.layout = qt.QVBoxLayout()
        self.label_name = qt.QLabel('Name:')
        self.layout.addWidget(self.label_name)
        self.competition_list = qt.QListWidget()
        self.layout.addWidget(self.competition_list)
        self.setLayout(self.layout)
        self.main_window.show()
        self.show()

    def save(self):
        self.db.competition.name = sanitize(self.field_name.text())
        self.db.competition.location = sanitize(self.field_location.text())
        self.db.competition.event_date = (self.calendar_competition_event
                            .selectedDate().toString('yyyy-MM-dd 00:00:00'))
        self.db.competition.deadline = (self.calendar_competition_deadline
                            .selectedDate().toString('yyyy-MM-dd 00:00:00'))
        self.db.competition.competition_type = (self
                                             .selector_competition_type
                                             .currentIndex())
        self.db.t.competition.update(self.db.competition)
        self.main_window.set_competition(self.db.competition.iid)
        self.changes_made = False
        self.hide()

    def exit_button(self, sender=None):
        if self.changes_made:
            save_result = ask_save()
        else:
            save_result = 'discard'
        if self.db.settings.verbose:
            print(f"save_result: {save_result}")
        if save_result == 'discard':
            self.hide()
        elif save_result == 'save':
            self.save()
            self.hide()
        else:
            pass

    def item_changed(self, sender=None):
        self.changes_made = True