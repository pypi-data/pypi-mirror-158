# py-avataaars - Python component for Avataaars

**FORK OF https://github.com/kebu/py-avataaars**


## Changes
- Switched from setup.py to Poetry
- Removed svg2png-dependency -> **No PNG-support**

## Original README

Python port of https://github.com/fangpenlin/avataaars

> The core React component for [Avataaars Generator](https://getavataaars.com/) developed by [Fang-Pen Lin](https://twitter.com/fangpenlin), based on the Sketch library [Avataaars](https://avataaars.com/) designed by [Pablo Stanley](https://twitter.com/pablostanley). 

### Features
* SVG based
* Light weight
* Easy to use

### Install
```shell script
pip install py-avataaars
```

### Usage

Basic usage:

```python
from py_avataaars import PyAvataaar

avatar = PyAvataaar()
avatar_svg = avatar.render_svg()
```

Specify each part of avatar:
```python
import py_avataaars as pa
avatar = pa.PyAvataaar(
    style=pa.AvatarStyle.CIRCLE,
    skin_color=pa.SkinColor.LIGHT,
    hair_color=pa.HairColor.BROWN,
    facial_hair_type=pa.FacialHairType.DEFAULT,
    facial_hair_color=pa.HairColor.BLACK,
    top_type=pa.TopType.SHORT_HAIR_SHORT_FLAT,
    hat_color=pa.Color.BLACK,
    mouth_type=pa.MouthType.SMILE,
    eye_type=pa.EyesType.DEFAULT,
    eyebrow_type=pa.EyebrowType.DEFAULT,
    nose_type=pa.NoseType.DEFAULT,
    accessories_type=pa.AccessoriesType.DEFAULT,
    clothe_type=pa.ClotheType.GRAPHIC_SHIRT,
    clothe_color=pa.Color.HEATHER,
    clothe_graphic_type=pa.ClotheGraphicType.BAT,
)
avatar_svg = avatar.render_svg()
```
