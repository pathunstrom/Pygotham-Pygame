# Pygame

Goal: Get a novice programmer from zero experience with Pygame to 
capable of building a Pygame application.

## Audience Assumptions

1. Knows basic syntax and programming principles. (Flow control, etc)
2. May not know how long running processes work
3. No experience with Pygame or graphics programming.

## Talk

### Introduction

#### Me

#### PyGame

* SDL library wrapper. 
    * Events
    * Drawing Libraries
    * Sound
* Extra game specific tools.

#### This Talk

* Covers
    * PyGame oddities
        * Installation sucks
        * Where is math?
        * pygame.quit()
    * Basics of long term processes
        * Game loops
        * Event management
    * The PyGame Library
    * Game design patterns
        * Modules, Classes, Single File Games
        * Sprites or Dicts?
* Does not Cover
    * AI Design
    * Specific OS fixes
    * Some Modules
        * Why - I have yet to use them in 2 and a half years
        * List
        
### PyGame

#### Surfaces

Pixel arrays. In memory representation. Think of like a digital canvas
you can draw on.

##### Instantiating a Surface

Call Surface with a resolution and flags.

Significant methods:

* fill

##### The Pygame.display

Surface that represents the display, either windowed or the entire
display.

* set_mode

##### image.load

#### Draw Module

##### Circle

##### Line

##### Rect

#### Rect

#### Sprite

A sprite is a class with a handful of required attributes.

Makes basic game development easier.

##### Requirements

* self.image
* self.rect
* update()

#### Events

##### Event Objects

##### Event Queue

#### Input

##### Keyboard

##### Mouse

##### Joystick

#### Sprite Groups

### Design Patterns

#### Modules: Python Singletons

#### Classes

#### Closures and Lists

50 minutes:

5 minutes intro

20 minutes the library

10 minutes design patterns

10 minutes putting it together

5 minute outro