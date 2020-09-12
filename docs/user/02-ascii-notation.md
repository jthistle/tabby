# ASCII guitar tab notation

## The Basics

ASCII guitar tab notation greatly resembles 'normal' tab notation. Consider this:

```
e|-------5-7-----7--|-8-----8-2-----2--|-0---------0------|-------------------|
B|-----5-----5------|---5-------3------|---1---1-----1----|-0-1-1-------------|
G|---5---------5----|-----5-------2----|-----2------------|-0-2-2-------------|
D|-7-------6--------|-5-------4--------|-3----------------|-------------------|
A|------------------|------------------|------------------|-2-0-0-----0-/8-7--|
E|------------------|------------------|------------------|-------------------|
```

On the left we have the string tunings, with the lowest-pitched string at the bottom.

The rows of `-----` indicate strings, mimicking staff lines.

On each string we can see notes indicated by numbers. The number is the number of the fret
on which the finger is held down. If no finger is held down (i.e. open string), the number
is `0`.

Notes are played together (as a chord) if they are in the same column. For example,
at the start, the notes are played one after the other. However, in the last bar,
the notes are in the same column, so are played as a chord.

```
e|-0---------0------|-------------------|
B|---1---1-----1----|-0-1-1-------------|
G|-----2------------|-0-2-2-------------|
D|-3----------------|-------------------|
A|------------------|-2-0-0-------------|
E|------------------|-------------------|

   ^ play separately  ^ play together
```

A column of `|` indicates the end of a bar. A bar is an almost arbitrary way of
separating out music so that it's easier to read and remember (oh, and if you're
American, a bar is called a 'measure').

## Symbols

Other symbols are used in ASCII notation to denote certain things. Normally, a 'key'
describing what each symbol means will be included at the end of a tab, but here
are some common usages:

### Hammer-on, pull-off, and bends

```
e|-4h6--------------|
B|-----6p5----------|
G|------------------|
D|------------------|
A|------------------|
E|----------0b3-----|
```

The characters `h`, `p` or `b` in between notes indicate that you should perform a 'hammer-on',
'pull-off', or 'bend' respectively. A hammer-on consists of playing the first note as normal, and
making the second note sound by 'hitting' it with another fretting finger. A pull-off is the
opposite: you play the first note normally, but play the second one by pulling one of your
fretting fingers away. A bend is simply when you pull or push the string to raise its pitch from
that of the first note to that of the second note.

### Slides

```
e|---------12\9-----|
B|-----1/4------7\--|
G|-----3/6----------|
D|-----1/4----------|
A|------------------|
E|-0/7--------------|
```

A slide is indicated by a slash. `/` usually indicates an upwards slide, and `\` a downwards one,
but they may be used interchangeably. A slide symbol without either a starting or ending note just
means to slide from or to that general direction.

### Ghost/dead notes

```
e|-------------x-x--|
B|----------x--x-x--|
G|-x--------x--x-x--|
D|-x-5-5----x-------|
A|-x-5-5----x-------|
E|-x-3-3----x-------|
```

A ghost (or 'dead') note is indicated by an `x`. This means that the string should be muted with
the fretting finger when played.


### Vibrato

```
e|-1~------12~-------|
B|-1~------13~-------|
G|-1~------12~-------|
D|-3~----------------|
A|-3~----------------|
E|-1~----------------|
```

Vibrato is often indicated with a `~` symbol.

### Annotations

```
   S SP S SP S SP  SSS
G|----3----3----3------|
D|---------------------|
A|-----------3-3---431-|
E|-3-3--3-3------------|
```

Often notes will have letters written above them. These can mean many things - in the above example,
they are slap bass instructions: `S` means 'slap', and `P` means pop. Look in the key at the end of
the tab to see what the author means when you are unsure.

## Conclusion

Again, ASCII tab notation is very loose, so take this as a guide rather than a set of rules. But
do try to follow convention when writing your own tabs - people will much prefer your tab over others
if you do!
