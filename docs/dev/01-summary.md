# Tabby development documentation

Documentation is poor right now, but here is a basic project summary:

Tabby is separated into two main modules, located in `/src`:

- **lib** is the data model for a tab and an interface for modifying it through the UndoStack system. This also includes a way of turning the data model into a visible tab, the layout system.
- **ui** is the interface between user input and the lib module. This works out what a certain key press means in a given context, as well as handling the display of the score and cursor to the user.

Other than these modules the project structure is fairly simple:

- the root of the project is reserved for a few files only, such as the license or readme, and any config files.
- **docs** contains documentation files including this one!
- **src** contains the code that is compiled into the Tabby executable.

Within **src**, other than lib and ui:

- **meta** holds simple, constant information about the programme itself: the version, the default file extension, the programme name, etc.
- **util** is currently only for the logger, but may be considered for usage with other things that don't really fit in any other place.

## Encapsulation between lib and ui

There is one rule:

- within ui, you may import from lib, but within lib, you may not import from ui.

Why is this? lib is considered to be its own separate thing. It's the 'engine' of Tabby. In the future, someone may want to make Tabby run using a Qt or Tkinter UI. If lib is encapsulated correctly, all they have to do is ditch the ui module and make their own. However, if lib were to depend on ui, there would be a big mess as they tried to work out how they could model their new ui to satisfy lib's demands.

## logging: working out what's going on

There is a logger set up to write to `/src/debug.log` in `/src/util/logger.py`. You can import it wherever you want, and use it, as so:

```py
from util.logger import logger

def my_bad_func():
    foo = 12
    logger.debug("foo is {}".format(foo))
```

Removing logger imports once you're done is good, but don't worry if you commit it accidently.

## Type hints: yes or no?

You may occasionally see type hints strewn around the code:

```py
def my_func(note: Note) -> str:
    return note.value
```

If you see this, it's probably just to make sure that I don't forget how a function works. They are by no means required, and personally, I frown on using too many in dynamically-typed Python, especially if they're not enforced. They can just make code less readable. That said, if a function feels quite complex, please feel free to make these annotations.
