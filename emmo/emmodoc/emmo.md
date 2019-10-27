;
; This file
; This is Markdown file, except of lines starting with a semi-colon will
; be stripped off.
;

*emmo* is a class representing the collection of all the individuals
(signs) that are used in the ontology. Individuals are declared by the
EMMO users when they want to apply the EMMO to represent the world.


## emmo
The root of all classes used to represent the world.  It has two children;
*collection* and *item*.

*collection* is the class representing the collection of all the
individuals (signs) that represents a collection of non-connected real world
objects.

*item* Is the class that collects all the individuals that are members
of a set (it's the most comprehensive set individual).  It is the
branch of parthood (mereotopology).

;  - based on *has_part* mereological relation that can be axiomatically defined
;  - a fusion is the sum of its parts (e.g. a car is made of several
;    mechanical parts, an molecule is made of nuclei and electrons)
;  - a fusion is of the same entity type as its parts (e.g. a physical
;    entity is made of physical entities parts)
;  - a fusion can be partitioned in more than one way


;## spacetime
;The space and time that the real world manifest itself in (the Universe).
;
;It has several important subclasses:
;
;  - **physical**: is declared to be `EquivalentTo: field or matter`
;  - **matter**: a subclass of *spacetime* that expresses some mass property
;  - **field**: a subclass of *spacetime* that can be perceived by the
;    ontologist, but expresses no mass property
;  - **vacuum**: is a field that has no *elementary* parts
;  - **void**: a vacuum that has no *field* parts


## physical

## process

;## participant

## semiotic

## state

## matter

;## elementary



## sign


## symbolic

## symbol

## formula

## mathematical

## quantitative_property


;## model


## property

;## extensive_property

;## intensive_property

;## base_unit

;## derived_unit
