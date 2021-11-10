# eInkFlashcards
MagTag Flashcards

## Usage
There are 2 interfaces "Flashcard" and "Menu".

### Flashcard
In this interface, the MagTag renders the screen with the word and goes into deep sleep. Upon pressing either the "Menu"
button or the "Next Word" button the device will wake up. Because of an [issue][1] in CircuitPython, the "Menu" and
"Next Word" buttons must be held until you hear a beep, otherwise the screen will refresh without changing. This is the
default interface.

### Menu
In this interface, the MagTag renders the menu and polls input in a loop. The up, down and right arrow buttons adjust the
settings while the "Exit" button goes back to the Flashcard interface. This interface allows the selection of word banks
and weeks within each bank (i.e. spelling vs sight words for each week).

### Deck
When the MagTag is plugged into the computer you can edit the deck (`deck.json`). The JSON document has two keys "modes" and
"cards". The "modes" key is a list of names for each of the word banks. The "cards" key is 3D array of words, where the first
dimension is the word bank, the second demension is the week and the third is the list of words. Clear as mud!

## CircuitPython
Use the latest 7.x+ version of [CircuitPython][2]. Then just copy all of files in the repository to the CircuitPython drive.
You will also need the [libraries][3] (`Bundle for Version 7.x`). Here is a list of the libraries to copy to the `lib` folder
on the CircuitPython drive:

- `adafruit_bitmap_font`
- `adafruit_display_text`
- `adafruit_debouncer.mpy`
- `neopixel.mpy`
- `simpleio.mpy`

[1]: https://github.com/adafruit/circuitpython/issues/5343
[2]: https://circuitpython.org/board/adafruit_magtag_2.9_grayscale/
[3]: https://circuitpython.org/libraries
