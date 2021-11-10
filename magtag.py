import gc

import board

from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from displayio import Bitmap, Group, OnDiskBitmap, Palette, TileGrid
from terminalio import FONT

import simpleio

from adafruit_debouncer import Debouncer

from adafruit_display_text.bitmap_label import Label

class MagTag:
    def __init__(self) -> None:
        self.display = board.DISPLAY
        self.root = Group()
        self.button_inputs = None
        self.buttons = None

        self._background = Group()
        self._background_file = None

        self.set_background(color=0xFFFFFF)

        self.root.append(self._background)

        self.display.show(self.root)

        self._labels = {}

        # Battery Monitor
        self._battery_monitor = AnalogIn(board.BATTERY)

        # Speaker Enable
        self._speaker_enable = DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.direction = Direction.OUTPUT
        self._speaker_enable.value = False

    def init_buttons(self):
        self.button_inputs = []
        self.buttons = []

        for pin in (board.BUTTON_A, board.BUTTON_B, board.BUTTON_C, board.BUTTON_D):
            button = DigitalInOut(pin)
            button.switch_to_input(pull=Pull.UP)

            self.button_inputs.append(button)
            self.buttons.append(Debouncer(button))

    def deinit_buttons(self):
        for i in self.button_inputs:
            i.deinit()

        self.button_inputs = None
        self.buttons = None

        gc.collect()

    def play_tone(self, frequency, duration):
        """
        Automatically Enable/Disable the speaker and play a tone at the
        specified frequency for the specified duration. It will attempt
        to play the sound up to 3 times in the case of an error.
        """
        if frequency <= 0:
            raise ValueError("The frequency has to be greater than 0.")

        self._speaker_enable.value = True

        for _ in range(3):
            try:
                simpleio.tone(board.SPEAKER, frequency, duration)

                break
            except NameError:
                pass

        self._speaker_enable.value = False

    def add_text(
        self,
        name: str,
        text_font=FONT,
        text="",
        text_color=0x000000,
        text_anchor_point=(0, 0.5),
        text_position=(0, 0),
        text_scale=1,
        line_spacing=1.25,
    ) -> None:
        """
        Add text labels with settings

        :param str name: The string identifier for this label.
        :param str text_font: The path to your font file for your data text display.
        :param str text: If this is provided, it will set the initial text of the label.
        :param text_color: The color of the text, in 0xRRGGBB format. Can be a list of colors for
                           when there's multiple texts. Defaults to ``None``.
        :param (float,float) text_anchor_point: Values between 0 and 1 to indicate where the text
                                                position is relative to the label
        :param text_position: The position of your extracted text on the display in an (x, y) tuple.
                              Can be a list of tuples for when there's a list of json_paths, for
                              example.
        :param int text_scale: The factor to scale the default size of the text by
        :param float line_spacing: The factor to space the lines apart
        """
        self._labels[name] = Label(
            text_font,
            text=text,
            color=text_color,
            anchor_point=text_anchor_point,
            anchored_position=text_position,
            scale=text_scale,
            line_spacing=line_spacing,
        )

        self.root.append(self._labels[name])

    def set_text(self, name: str, text: str) -> None:
        """
        Update label text by string identifier.

        :param str name: The string identifier
        :param str val: The text to be displayed
        """
        self._labels[name].text = text

    def remove_text(self, name: str) -> None:
        """
        Remove label by string identifier.

        :param str name: The string identifier
        """
        self.root.remove(self._labels[name])

        del self._labels[name]

    def set_background(self, *, file=None, color=None, position=None):
        """
        The background image to a bitmap file.

        :param str file: The filename of the chosen background image.
        :param int color: The hex color.
        :param tuple position: Optional x and y coordinates to place the background at.
        """
        while self._background:
            self._background.pop()

        if not file and not color:
            return  # we're done, no background desired

        if not position:
            position = (0, 0)  # default in top corner

        if self._background_file:
            self._background_file.close()

        if file and isinstance(file, str):  # its a filenme:
            self._background_file = open(file, "rb")
            background = OnDiskBitmap(self._background_file)
            self._background_sprite = TileGrid(
                background,
                pixel_shader=background.pixel_shader,
                x=position[0],
                y=position[1],
            )
        elif color and isinstance(color, int):
            # Make a background color fill
            color_bitmap = Bitmap(self.display.width, self.display.height, 1)
            color_palette = Palette(1)
            color_palette[0] = color
            self._background_sprite = TileGrid(
                color_bitmap,
                pixel_shader=color_palette,
                x=position[0],
                y=position[1],
            )
        else:
            raise RuntimeError("Unknown type of background")

        self._background.append(self._background_sprite)

        gc.collect()

    @property
    def battery(self):
        """Return the voltage of the battery"""
        return (self._battery_monitor.value / 65535.0) * 3.3 * 2
