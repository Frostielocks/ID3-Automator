# ID3-Automator
Program that automatically adds meta data to mp3 files in the current directory given a wikipedia album link.

**Example:**
```
1. Initial
directory = [ID3-Automator, test.txt, Nas - N.Y. State of Mind.mp3, Nas - Ether.mp3, Ed Sheeran - Perfect.mp3]
With no metadata on any of the files.

2. After executing ID3-Automator with https://en.wikipedia.org/wiki/Illmatic as argument
directory = [ID3-Automator, test.txt, Nas - N.Y. State of Mind.mp3, Nas - Ether.mp3, Ed Sheeran - Perfect.mp3]
With all metadata added for Nas - N.Y. State of Mind.mp3, but no metadata on any of the other files.
```          

## Usage
Program that automatically adds meta data to mp3 files in the current directory given a wikipedia album link.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**ID3-Automator** *[album wikipedia link] [NULL | general tag override file name]*

**[album wikipedia link]** = wikipedia link af the album of which metadata should be added
<br/>**[general tag override file name]** = link to override file. Useful if you wish to override inferred album general tags such as genre, song tags cannot be overridden. The syntax of the override file should be as followed:
```
album artist name
album name
album genre
album label
album release year
debug (True or False) = Shows output confirmation.
```


## Getting Started

### Prerequisites

* Windows OS or [Python 3.*](https://www.python.org/download/releases/3.0/)

### Installing

* **Basic Install:** Only install the executable.
  <br/>**IMPORTANT:** If you wish to execute the executable, python35.dll must always be located in the same directory as the executable. The executable should also named ID3Automator.exe NOT ID3-Automator.exe, this is because (-) is a special character in windows.

```
1. Navigate to ID3-Automator/Release/
2. Right click ID3Automator.exe
3. Click save link as...
4. Save as executable in your preferred destination
5. Right click python35.dll
6. Click save link as...
7. Save in the same destination as the executable
```

* **Python Install:** Only install the .py file.

```
1. Right click ID3-Automator.py
2. Click save link as...
3. Save as .py in your preferred destination
```

## Running

```
1. Navigate to the directory where you saved ID3Automator
2. Open the terminal
3. If running executable: type ID3Automator.exe with command line arguments as specified in Usage
3. If running .py: type python ID3-Automator.py with command line arguments as specified in Usage
```


## Contributing

Everyone can contribute.


## Authors

* **Mathijs Hubrechtsen** - *Majority Contributor*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

* [eyeD3](https://eyed3.readthedocs.io/en/latest/): Tool that powers this program.
