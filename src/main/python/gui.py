"""Scrutini GUI."""
import datetime
import sys
import os
import PyQt6.QtWidgets as qt
# from fbs_runtime.application_context.PyQt6 import ApplicationContext
import PyQt6.QtCore as qc
import PyQt6.QtGui as qg
from sWidgets import SPushButton, on_button_clicked, verify, ask_save
from sWidgets import is_float, get_formatted_date
from resultsc import ResultsViewWindow
from scores import ScoreEntryWindow
from dancers import DancerEditor
from groups import GroupEditor as DancerGroupEditor
from groups import GroupMenu as DancerGroupMenu
from competitions import CompetitionEditor, CompetitionSelector
from importWindow import ImportWindow
from judges import JudgeSelector
# import platform


class SMainWindow(qt.QMainWindow):
    def __init__(self, app, db):
        super(SMainWindow, self).__init__()
        self.app = app
        self.db = db
        # (sysname, network_name, release, version, machine) = platform.uname()
        # self.db.competition = None
        self.toolbar = SToolBar(self)
        self.addToolBar(qc.Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self.toolbar.buttons.disable_all()
        self.set_competition()
        self.setUnifiedTitleAndToolBarOnMac(True)
        # self.setUnifiedTitleAndToolBarOnMac(False)
        # Set title based on selected competition
        if self.db.competition is not None:
            title_text = ('Scrutini - %s %8s, %s' % (self.db.competition.name,get_formatted_date(self.db.competition.event_date),self.db.competition.location))
        else:
            title_text = ('Scrutini')
        # font = qg.QFont("Lucida Grande")
        # self.setFont(font)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        print(scriptDir)
        # icon = qg.QIcon(scriptDir + os.path.sep + '../icons/mac/256.png')
        # self.setWindowIcon(icon)
        # tray = qg.QSystemTrayIcon()
        # tray.setIcon(icon)
        # tray.setVisible(True)
        # self.setWindowIcon(qg.QIcon("../icons/linux/1024.png"))
        print(scriptDir + os.path.sep + '../icons/linux/1024.png')
        self.setGeometry(0, 0, 1200, 800)
        self.statusBar()
        self.statusBar().show()
        self.menubar = SMenuBar(None, self)
        self.setMenuBar(menubar)
        if self.db.get_competition() is None:
            self.db.competition = self.select_competition()
        self.set_competition()
        if self.db.competition is not None:
            self.toolbar.buttons.enable_all()

    def press(self, endpoint):
        if self.centralWidget() is not None:
            self.centralWidget().hide()
        if self.db.s.verbose:
            print(type(endpoint))
        window = endpoint(
            self, self.db)
        window.show()
        window.exec()

    def edit_competition(self, sender=False):
        if self.centralWidget() is not None:
            self.centralWidget().hide()
        competition_editor = CompetitionEditor(self, self.db)
        competition_editor.show()
        competition_editor.exec()

    def edit_dancer_group(self, dancer_group):
        if self.centralWidget() is not None:
            self.centralWidget().hide()
        dancer_group_editor = DancerGroupEditor(self, dancer_group, self.db)
        dancer_group_editor.show()
        dancer_group_editor.exec()

    def retrieve_competition(self):
        competitions_list = self.db.t.competition.get_all_ids()
        if self.db.s.last_comp in competitions_list:
            self.db.competition = self.db.t.competitions.get(
                self.db.s.last_comp)
            return self.db.competition
        else:
            self.select_competition()
            if self.db.competition is not None:
                self.db.s.last_comp = self.db.competition.iid
                return self.db.competition
            else:
                return self.new_competition()

    def set_competition(self, iid=None):
        if iid is not None:
            self.db.competition = self.db.t.competition.get(iid)
        if self.db.competition is not None:
            label_text = ('<center>Competition:<br><strong>%s</strong>\
                               <br>%8s<br>%s</center>' %
                               (self.db.competition.name,
                                get_formatted_date(
                                    self.db.competition.event_date),
                                self.db.competition.location))
            self.toolbar.set_label(label_text)
            self.db.s.last_comp = self.db.competition.iid
            self.toolbar.buttons.enable_all()
            return self.db.competition
        else:
            label_text = ('<center>No Competition Selected</center>')
            self.toolbar.set_label(label_text)
            self.toolbar.buttons.disable_all()
            return None

    def select_competition(self):
        if self.centralWidget() is not None:
            self.centralWidget().hide()
        window = CompetitionSelector(self, self.db)
        window.show()
        window.exec()

    def delete_competition(self):
        verity = verify('Are you sure you want to delete this competition?',
                        ('This will delete all data for the given '\
                         'competition. This cannot be undone.'))
        if verity:
            if self.db.s.verbose:
                print('Will delete competition %d' % self.db.competition.iid)
            self.db.t.competition.remove(self.db.competition.iid)
            self.db.competition = None
            self.set_competition()
            self.select_competition()
        else:
            print('Nothing deleted')

    def exit_app(self, sender):
        self.db.close_connection()
        if self.centralWidget() is not None:
            self.centralWidget().hide()
        print(f"Exit 0")
        self.close()
        # self.app.exit()

    def new_competition(self):
        self.db.competition = self.db.t.competition.new()
        self.edit_competition()
        return self.db.competition


class SMenuBar(qt.QMenuBar):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setNativeMenuBar(True)
        # False means in same window, but I hate how it looks. The other way
        # doesn't really work on Mac OS
        # self.addSeparator()
        file_menu = self.addMenu(' &File')
        self.competition(file_menu)
        self.file(file_menu)
        scores_menu = self.addMenu(' &Scores')
        self.scores(scores_menu)
        dancers_menu = self.addMenu(' &Dancers')
        self.competitors(dancers_menu)
        view_menu = self.addMenu(' &View')
        self.views(view_menu)

    def file(self, file_menu):
        exit_action = qg.QAction(' &Quit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Application')
        exit_action.triggered.connect(self.main_window.exit_app)
        file_menu.addAction(exit_action)

    def competition(self, competition_menu):
        change_competition_action = qg.QAction(' Select Competition', self)
        change_competition_action.setStatusTip(
            'Choose a different competition or make a new one.')
        change_competition_action.triggered.connect(
            lambda: self.main_window.press(CompetitionSelector))
        edit_competition_action = qg.QAction(' &Edit Competition', self)
        edit_competition_action.setStatusTip('Edit Competition Details.')
        edit_competition_action.triggered.connect(
            lambda: self.main_window.press(CompetitionEditor))
        judges_action = qg.QAction(' Add/Edit &Judges', self)
        judges_action.setStatusTip('Edit competition judge list.')
        judges_action.triggered.connect(
            lambda: self.main_window.press(JudgeSelector))
        delete_action = qg.QAction(' &Delete Competition', self)
        delete_action.setStatusTip(
            'Delete the current competition and all data.')
        delete_action.triggered.connect(self.main_window.delete_competition)
        competition_menu.addActions([change_competition_action,
                                     edit_competition_action, judges_action,
                                     delete_action])

    def scores(self, scores_menu):
        enter_scores_action = qg.QAction(' &Enter Scores', self)
        enter_scores_action.setStatusTip(
            'Enter competitor scores for the current competition.')
        enter_scores_action.triggered.connect(
            lambda: self.main_window.press(ScoreEntryWindow))
        view_scores_action = qg.QAction(' &View/Print Results', self)
        view_scores_action.setStatusTip(
            'View the event results, print or save to PDF.')
        view_scores_action.triggered.connect(
            lambda: self.main_window.press(ResultsViewWindow))
        scores_menu.addActions([enter_scores_action, view_scores_action])

    def competitors(self, dancers_menu):
        dancers_action = qg.QAction(' &Add/Edit Competitors', self)
        dancers_action.setStatusTip('Edit competitor details.')
        dancers_action.triggered.connect(
            lambda: self.main_window.press(DancerEditor))
        groups_action = qg.QAction(' Define Competitor &Groups && Dances', self)
        groups_action.setStatusTip(
            'Choose which competitors are in which groups.')
        groups_action.triggered.connect(
            lambda: self.main_window.press(DancerGroupMenu))
        import_action = qg.QAction(' &Import CSV', self)
        import_action.setStatusTip(
            'Import dancer information from a CSV spreadsheet.')
        import_action.triggered.connect(
            lambda: self.main_window.press(ImportWindow))
        dancers_menu.addActions([dancers_action, groups_action, import_action])

    def views(self, view_menu):
        showhide_action = qg.QAction(' Show/&Hide Toolbar', self)
        showhide_action.triggered.connect(self.main_window.toolbar.show_hide)
        view_menu.addActions([showhide_action])


class SToolBar(qt.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.is_hidden = False
        self.buttons = STButtons(self)
        label_text = ''
        self.label = qt.QLabel(label_text)
        self.addWidget(self.label)
        for button in self.buttons.buttons:
            self.addWidget(button)
        self.setOrientation(qc.Qt.Orientation.Horizontal)
        self.label.show()
        self.hidden_toolbar = STHiddenToolBar(self)
        self.parent.addToolBar(qc.Qt.ToolBarArea.LeftToolBarArea, self.hidden_toolbar)

    def show_hide(self, todo=''):
        if self.is_hidden or todo=='show':
            self.hidden_toolbar.hide()
            self.show()
            self.is_hidden = False
        elif not self.is_hidden or todo=='hide':
            self.hide()
            self.hidden_toolbar.show()
            self.is_hidden = True

    def set_label(self, text):
        self.hide()
        self.label.hide()
        self.label.setText(text)
        self.label.show()
        self.show()


class STHiddenToolBar(qt.QToolBar):
    def __init__(self, toolbar):
        super().__init__(toolbar.parent)
        self.parent = toolbar.parent
        self.setOrientation(qc.Qt.Orientation.Vertical)
        self.toolbar = toolbar
        self.setHidden(True)
        expand_button = qt.QPushButton('>>', self)
        expand_button.clicked.connect(self.show_toolbar)
        expand_button.resize(20, self.parent.width())
        expand_button.setEnabled(True)
        if self.toolbar.is_hidden:
            self.show()
        else:
            self.hide()

    def show_toolbar(self):
        self.toolbar.show_hide(todo='show')


class STButtons(qt.QWidget):
    def __init__(self, toolbar):
        super().__init__(toolbar)
        self.toolbar = toolbar
        scrutineer = qt.QPushButton('Enter &Scores', self)
        scrutineer.setStatusTip(
            'Enter competitor scores during the competition')
        view_scores = qt.QPushButton('&View/Print Results', self)
        change_competition = qt.QPushButton('&Change Competition', self)
        edit_competition = qt.QPushButton('&Edit Competition Details', self)
        dancers = qt.QPushButton('&Add/Edit Competitors', self)
        judges = qt.QPushButton('Add/Edit &Judges', self)
        dancer_groups = qt.QPushButton(
            'Define Competitor &Groups && Dances', self)
        btn_import = qt.QPushButton('&Import CSV', self)
        delete = qt.QPushButton('&Delete Competition', self)
        exit = qt.QPushButton(' E&xit', self)
        scrutineer.clicked.connect(
            lambda: toolbar.parent.press(ScoreEntryWindow))
        view_scores.clicked.connect(
            lambda: toolbar.parent.press(ResultsViewWindow))
        edit_competition.clicked.connect(
            lambda: toolbar.parent.press(CompetitionEditor))
        change_competition.clicked.connect(
            lambda: toolbar.parent.press(CompetitionSelector))
        dancers.clicked.connect(lambda: toolbar.parent.press(DancerEditor))
        judges.clicked.connect(lambda: toolbar.parent.press(JudgeSelector))
        dancer_groups.clicked.connect(
            lambda: toolbar.parent.press(DancerGroupMenu))
        btn_import.clicked.connect(lambda: toolbar.parent.press(ImportWindow))
        delete.clicked.connect(toolbar.parent.delete_competition)
        exit.clicked.connect(toolbar.parent.exit_app)
        hide_button = qt.QPushButton(' &Hide Toolbar', self)
        hide_button.clicked.connect(self.toolbar.show_hide)
        self.buttons = [scrutineer, view_scores, change_competition,
                        edit_competition, dancers, judges, dancer_groups,
                        btn_import, delete, exit, hide_button]

    def enable_all(self):
        if self.toolbar.parent.db.s.verbose:
            print("Enable All Buttons")
        for button in self.buttons:
            button.setEnabled(True)

    def disable_all(self):
        if self.toolbar.parent.db.s.verbose:
            print("Disable All Buttons")
        for button in self.buttons:
            button.setEnabled(False)


class App(qg.QGuiApplication):
    def __init__(self, db):
        super().__init__(sys.argv)
        self.db = db
        qg.qt_set_sequence_auto_mnemonic(True)
        font = qg.QFont("Lucida Grande")
        self.setFont(font)
        self.setObjectName("Scrutini")
        self.setApplicationDisplayName("Scrutini")
        self.main_window = SMainWindow(self, db)

    def start(self):
        self.main_window.show()

    def exit(self):
        self.db.s.write()
        print("Exit Interface")
        self.closeAllWindows()
        sys.exit(0)
