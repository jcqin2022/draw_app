from PySide6.QtGui import QAction

class WBMenu:
    def __init__(self, whiteboard):
        """
        Initialize the WBMenu with a reference to the whiteboard instance.

        :param whiteboard: Instance of the whiteboard to interact with.
        """
        self.whiteboard = whiteboard
        self.menus = {}
        self.create_menu()

    def create_menu(self):
        """Create the menu bar for selecting shapes and colors."""
        menu_bar = self.whiteboard.menuBar()

        # Shapes menu
        shapes_menu = menu_bar.addMenu("Shapes")
        line_action = QAction("Line", self.whiteboard)
        line_action.triggered.connect(lambda: self.whiteboard.set_drawing_tool("line"))
        shapes_menu.addAction(line_action)

        dotted_line_action = QAction("Dotted Line", self.whiteboard)
        dotted_line_action.triggered.connect(lambda: self.whiteboard.set_drawing_tool("dotted_line"))
        shapes_menu.addAction(dotted_line_action)

        circle_action = QAction("Circle", self.whiteboard)
        circle_action.triggered.connect(lambda: self.whiteboard.set_drawing_tool("circle"))
        shapes_menu.addAction(circle_action)

        rect_action = QAction("Rectangle", self.whiteboard)
        rect_action.triggered.connect(lambda: self.whiteboard.set_drawing_tool("rect"))
        shapes_menu.addAction(rect_action)

        curve_action = QAction("Curve", self.whiteboard)
        curve_action.triggered.connect(lambda: self.whiteboard.set_drawing_tool("curve"))
        shapes_menu.addAction(curve_action)

        # Colors menu
        colors_menu = menu_bar.addMenu("Colors")
        black_action = QAction("Black", self.whiteboard)
        black_action.triggered.connect(lambda: self.whiteboard.set_pen_color("#000000"))
        colors_menu.addAction(black_action)

        red_action = QAction("Red", self.whiteboard)
        red_action.triggered.connect(lambda: self.whiteboard.set_pen_color("#FF0000"))
        colors_menu.addAction(red_action)

        green_action = QAction("Green", self.whiteboard)
        green_action.triggered.connect(lambda: self.whiteboard.set_pen_color("#00FF00"))
        colors_menu.addAction(green_action)

        blue_action = QAction("Blue", self.whiteboard)
        blue_action.triggered.connect(lambda: self.whiteboard.set_pen_color("#0000FF"))
        colors_menu.addAction(blue_action)

    def add_menu(self, menu_name, options):
        """
        Add a menu with a list of options.

        :param menu_name: Name of the menu.
        :param options: List of options for the menu.
        """
        self.menus[menu_name] = options

    def display_menu(self, menu_name):
        """
        Display the menu options.

        :param menu_name: Name of the menu to display.
        """
        if menu_name in self.menus:
            print(f"Menu: {menu_name}")
            for index, option in enumerate(self.menus[menu_name], start=1):
                print(f"{index}. {option}")
        else:
            print(f"Menu '{menu_name}' does not exist.")

