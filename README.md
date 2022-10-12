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

### Config File
A JSON file can be used to specify the correct bin for a set of items. This file's location must be specified in `config.py` and should follow the following format:

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

### Bin Numbers
Each bin is specified by an integer ranging from 0 - 4, as follows:
 - 0 = Landfill
 - 1 = Recycling
 - 2 = Compost
 - 3 = Containers for Change
 
 ### Recording Item Disposals
 
 _Not yet implemented_
 
 Any time an item is disposed using the Smart Bin system, its disposal is recorded to an external key-value pair database, providing the following information:
 
```JSON
{
  "Id": "bd5a6d7d-814a-484e-ae23-e06a34b75e64", // String (uuidv4)
  "Time": "2022-09-19T02:22:29Z", //String (ISO8601)
  "Name": "Example Item", //String
  "BinNumber": 0 // Number (0-3)
}
```
 
### Setting up Local DynamoDB (for testing)
Follow the instructions found on [this page](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) to start a local DynamoDB instance.

