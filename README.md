# Procedural Eye
The script builds an eyeball procedurally with geometries and shaders. Users can customize the component shapes through an UI.
The whole theory is from [Digital Duct Tape](http://toddpilger.blogspot.com/2012/10/procedural-eye.html).
I wrote this script a long time ago as an exercise when I first started to learn python language and Maya Python Programming.

## Requirements
- Maya
- Mental Ray

## Usage
- Copy `eyeball.py` into your maya script folder
- Run the script below, and the UI will show up.
```python
import eyeball
eyeball.run()
```
![Procedural Eye UI]()
- Select the eyeball controler, and click `"set current"` to activate editting to the eyeball.
- Adjust any attribtue and press `Enter`
- Render with Mental Ray
![Render Result]()