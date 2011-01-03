********
MurderRL
********
**A rogue-like murder mystery game in Python.**

Mansion Generation
==================

Specification
-------------

The resultant "mansion" is defined as something one might find in an Agatha
Christie novel. Obviously, the generation needn't be limited to such a specific
scope, but initially this seems to be a good target.

Some examples of what the resultant manor house should look like:

1. `Dixton Manor`_. (Link to PDFs).
2. `Stepne Manor`_. (PDF)
3. `Trewince Manor`_. (PDF)

These examples present us with several interesting facts:

- Houses can either consist of:

  a. rooms which open onto other rooms and provide thoroughfare
  b. rooms that open out onto corridors, with corridors providing thoroughfare
  c. a combination of the above

In Dixton Manor, we see the combination described above: the entrance hall opens
out onto a corridor, which leads around a corner; from this corridor is accessed
the library, drawing room, study, dining room, pantry and kitchen. This is what
is described by *b* above.

The kitchen thereafter provides access to the larder, laundry room, boot room,
snooker room and lobby. Indeed, the kitchen opens out into another corridor, but
as it has to be traversed to access this corridor, it clearly acts as a
thoroughfare itself, satisfying point *a* above.

Therefore, Dixton Manor combines both of these aspects, as described by point
*c*.

Finally, it can be presumed that Dixton Manor, described as a modern house with
modern rooms many of which whose purpose may have changed since its inception,
was divided into two sections: the "formal" part of the house, denoted by the
roughly rectangular section on the right, and the "informal" or possibly
"servant's" part, denoted by the section on the left and accessed via the
kitchen.

In this instance, the upper story, dedicated to the bedrooms, would have
likewise been segregated; the presumably large stair case in the "formal"
section provided access to the owner's rooms, guest rooms, and so-on, while the
stair case located in the kitchen provided access to the "staff" areas.

Hermann Muthesius[Muthesius]_ simply states that every room in the English house is
either a bedroom or a sitting room. Presumably he is here referring to purely
domestic rooms, rather than utility rooms.

Thus, aside from bedrooms, the following would possibly be present in a large
country house (though not necessarily all of them; information drawn from
Muthesius):

- Drawing room, the "domain of the Mistress of the house", where conversation,
  reading take place; here is where guests will gather before and after meals.
  In the afternoons, is it the exclusive domain of the lady of the house.
  Smoking is not allowed in the drawing room, nor are children, unless as
  individual guests. It is usually the sunniest room, and there is often a door
  leading from it to the terrace.
- Dining room, presumably located near to the kitchen so that meals can be
  quickly ferried and remain hot; if the kitchen is down stairs, it is near to
  the bottom of the stairs, and the dining room itself near to the top of the
  stairs. Men will smoke here after dining, and the ladies have retired to the
  drawing room, before joining them.
- Library, a room for smoking in; according to Muthesius, large English houses
  do not have studies; this is something reserved for vicarages and houses of
  the clergy (an interesting parallel with the vicarage in Christie's Murder at
  the Vicarage, where the eponymous murder occurs in the study).
- Morning room; a smaller version of the drawing room, and exclusively used in
  the morning or when the guests are reduced in number.
- Breakfast room, a dining room exclusively for the use of breakfast time.
- Ingle-nook, an alcoved fire place wherein the sides are furnished with seats.
  Quite small.
- Boudoir, a room for the exclusive use of ladies and only visited by them and
  their housekeepers; it is some distance away from the rest of the house.
- Business room, near to the front of the house; here, low-class visitors are
  received, and it links directly to the servant's quarters so that tradesmen
  and the like entering from the front of the house can easily access the staff
  areas.
- Smoking room, a very small and snugly furnished room designed to relieve the
  pressure on the library as a smoking room.
- Billiard room, containing within it a billiards table.
- Conservatory, a room containing plants and the like, which is not necessarily
  directly connected to the house.
- Picture gallery, a room hung with portraits but also providing chairs for the
  inspection or long-term taking in of the art.
- The hall, a transition from residential rooms to connecting rooms; it is
  directly accessed via the entrance of the house. Staircases are *not* located
  within the hall, but are separate from them; most rooms open out onto this
  hall; it can sometimes be replaced by a picture gallery, this providing the
  purpose of a hall.
- Passages and corridors that form connecting rooms.
- Entrance hall, directly access from the front door of the house, or via a
  vestibule. Spacious, well-lit.
- Cloak room, accessed directly from the entrance hall.
- Lavatory or wash room, access directly from the cloak room.
- Porch: a covered entry-way to the house.

The second floor of the house is exclusively private and the location of
bedrooms; men dress in an adjoining dressing room, whereas women dress
specifically in the bedroom. For spare rooms, this obviously does not obligate a
combination of dressing room and bedroom per spare bedroom.

Bathrooms attached to each bedroom are uncommon in England, as opposed to
America; similarly to some hotels installing en-suite bathrooms to allow for
American visitors, some large houses might have rooms specifically for these
American guests.

The lavatory is never found within the bathroom. It is always ancillary.

Bedrooms are sometimes linked by private, small, circular staircases to sitting
rooms underneath. These could be considered "hidden staircases" in that their
use was primarily for the occupants of the house rather than their guests.

Children are specifically segregated and are never encountered by guests; their
nurseries and bedrooms are separate, and it would appear that the children
themselves would not interact with guests in common areas such as libraries,
etc.

Cloak rooms are used specifically by men. Women never leave their cloaks here,
but instead, guests place their cloaks in the master bedroom and take use of
mirrors, etc; if they are otherwise house guests, presumably they would use
their own bedroom for cloak storage.

Staircases are segregated into the main staircase, for the owners of the house
and their guests, and a secondary staircase for servants and children.

Utilitarian rooms are as follows:

- The kitchen, located not so far from the dining room that it would cause the
  food to be too cold upon arrival, but not so close that the noises and smells
  from it would escape into the dining room.
- Scullery, directly next to the kitchen.
- The tradesman's entrance is also located near the kitchen.
- Store rooms are located near to the kitchen so as to provide easy access to
  them when fetching ingredients.
- The servant's hall would appear to be a formal dining room but also an area
  where the servants might mingle in their free time.





.. [Muthesius] Muthesius, Hermann. *The English House, Volume 2*. `Web`_. December, 2010.

.. Links
.. =====

.. _Web: http://books.google.com/books?id=EWTEhEXmCAkC&pg=PA27&lpg=PA27&dq=english+home+layout&source=bl&ots=TZRkbzDHXB&sig=GP4A1uhO9OpzQUN5_j49Da2YTuQ&hl=en&ei=FzFCTM_pMoa8sQPvo7y7DA&sa=X&oi=book_result&ct=result&resnum=3&ved=0CB0Q6AEwAg#v=onepage&q&f=false

.. _Dixton Manor: http://www.dixtonmanor.co.uk/manor_floorplans.htm

.. _Stepne Manor: http://www.brittlandestates.com/docs/floorplans_stepne.pdf

.. _Trewince Manor: http://www.stags.co.uk/files/Market/Trtrewincemanor.pdf
