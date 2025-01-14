# Joner - A Sightreading Practice App

Joner is a web application that can be used to practice sightreading of sheet music. It was created by Jakob Daniel Deschauer for his bachelor thesis at the University of Vienna.

## Get Started
The web app uses the flask framework. To get it to work you need to have Python installed, navigate to the folder containing app.py and run this command:
```
pip install -r requirements.txt
```
After that, you can start the app with:
```
flask run
```
Copy the displayed url into the search bar of your browser to access the app.

## Modes
The web app features 3 distinct Modes that can be used to practice in a way that suits your needs best. They are:
- ### Simple Read Practice
	- Practice reading and playing a single note at a time. 
	- Best suited for Monophonic instruments
	- Note Range: C4 - D#6
- ### Chord Read Practice
	- Practice reading and playing one chord at a time. (Chords you can practice are: Major, Minor, sus2, sus4, diminished, augmented)
	- Best suited for Polyphonic instruments
	- Note Range: C3 - F#5
- ### Full Read Practice
	- Practice reading and playing a whole piece of sheet music. The sheet music is randomly generated using Etudes Generator by Martin Karanitsch: https://git01lab.cs.univie.ac.at/martink97/etudes-generator
	- Best suited for Monophonic instruments
	- Note Range: C4 - C6

## License

MIT License

Copyright (c) 2025 - Jakob Daniel Deschauer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.