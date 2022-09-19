# smart-bin

Small GUI Applet written with the TKinter Python Library to interact with Smart Bin system via Raspberry Pi.

Provides the user with a touch-screen virtual keyboard to input the product name:

![image](https://user-images.githubusercontent.com/40435390/189649232-abc433f4-f4e0-413a-b5c9-1b0faaccc99a.png)

Users can type the product name or scan the barcode of a product with a connected (USB) barcode scanner.


### Getting Started

1. First clone this repository: `git clone [This repository URL]`.
2. Go into the newly created folder: `cd smart-bin`
3. Install required packages: `pip install -r requirements.txt`
4. Run the GUI application: `python gui.py`

### Initialization File
A JSON file can be used to specify the correct bin for a set of items. This file must be specified using the `--init / -i` option when running `gui.py` and must follow the following format:

```JSON
{
  "items": [
    {
      "name": "",
      "barcode": "",
      "notes": "",
      "bin": 0
    }, ...
  ]
}
```