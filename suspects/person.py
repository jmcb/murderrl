#!/usr/bin/env python
"""
Set up characters, their basic traits and relationships.
"""

import random, math
from randname import *

# Roles, in plural as they're currently only used as header listing.
ROLE_OWNER   = 'Owners'
ROLE_FAMILY  = 'Family'
ROLE_GUEST   = 'Guests'
ROLE_SERVANT = 'Staff'

# Relationships
REL_SPOUSE   = 'spouse'
REL_ENGAGED  = 'engaged'
REL_PARENT   = 'parent'
REL_CHILD    = 'child'

class Person (object):
    """
    Person class. To define persons and access their characteristics.
    """

    # Relationships to other characters
    rel = []
    def __init__ (self, role = 'ROLE_GUEST', gender = None, last = None, age = None):
        """
        Initialize a new person.

        :``role``: One of ``ROLE_OWNER``, ``ROLE_FAMILY``, ``ROLE_GUEST`` or ``ROLE_SERVANT``. *Default ``ROLE_GUEST``*.
                   The role influences the choice of surname, age, and honorifics.
        :``gender``: Gender: ``'m'`` or ``'f'``. *Default random*.
        :``last``: Last name. *Default random*.
        :``age``: Age. *Default random*.

        In addition, the hair colour is randomly chosen.
        """
        self.role   = role
        self.gender = gender or random.choice(('m', 'f'))
        self.first  = get_random_first_name(self.gender)

        self.set_random_last_name(last)
        self.set_random_age(age)
        self.set_random_hair_colour()

        self.rel = []
        self.title = ''
        self.occupation = ''

    def __str__ (self):
        """
        Prints a single-line description of the person.
        """
        job = ''
        if self.occupation:
            job = "%s, " % self.occupation
        return "%s (%s), %s%shaired, aged %s" % (self.get_fullname(),
               self.gender, job, self.hair, self.age)

    def set_random_last_name (self, last = None):
        """
        Sets a person's appropriate last name (upperclass, middleclass,
        lowerclass) depending on their role.

        :``last``: Last name. *Default random*.
        """
        if last:
            self.last = last
        elif self.role == ROLE_OWNER:
            self.last = get_random_lastname_upperclass()
        elif self.role == ROLE_SERVANT:
            self.last = get_random_lastname_lowerclass()
        else:
            self.last = get_random_lastname_middleclass()

    def set_random_age (self, age = None):
        """
        Sets a person's appropriate age depending on their role.

        :``age``: Age. *Default random*.
        """
        if age:
            self.age = age
        elif self.role == ROLE_OWNER:
            self.age = random.randint(40,70)
        elif self.role == ROLE_SERVANT:
            self.age = random.randint(20,60)
        else:
            self.age = random.randint(25,70)

    def set_random_hair_colour (self):
        """
        Assigns a random hair colour.
        """
        hair = ['red', 'blond', 'brown', 'black']
        self.hair = random.choice(hair)

    def set_relative (self, idx, type):
        """
        Add a relative to this person's relationship list.
        Requires suspects[] index and relationship type
        ('spouse', 'parent', 'child', 'engaged').

        :``idx``: The current person's index in the suspect list. *Required*.
        :``type``: The type of the relationship: ``REL_SPOUSE``,
                   ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.
        """
        self.rel.append((idx, type))

    def get_name (self):
        """
        Returns a person's full name, excluding titles.
        """
        return "%s %s" % (self.first, self.last)

    def get_fullname (self):
        """
        Returns a person's full name, including titles.
        """
        return "%s%s" % (self.title, self.get_name())

    def describe_relations (self, list):
        """
        Prints a listing of this person's relatives.

        :``list``: An object of type SuspectList. *Required*.
        """
        if self.rel:
            print "    related to:",
            num_range = xrange(len(self.rel))
            for i in num_range:
                r = self.rel[i]
                if i:
                    print "               ",
                print "%d. %s (%s)" % (r[0]+1, list.get_suspect(r[0]).get_name(), r[1])

    def describe (self, list):
        """
        Prints the person's description and lists their relationships.

        :``list``: An object of type SuspectList. *Required*.
        """
        print self
        self.describe_relations(list)

    def get_mirrored_gender (self):
        """
        Returns the opposite gender to the current person one's.
        Used to decide spouses' genders.
        """
        if self.gender == 'm':
            return 'f'
        else:
            return 'm'

    def check_has_relative (self, type):
        """
        Returns whether a given relationship type exists for this
        person.

        :``type``: The type of the relationship: ``REL_SPOUSE``,
                   ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.
        """
        for r in self.rel:
            if r[1] == type:
               return True
        return False

    def is_married (self):
        """
        Returns whether a person is married.
        """
        return self.check_has_relative(REL_SPOUSE)

    def has_children (self):
        """
        Returns whether a person has children.
        """
        return self.check_has_relative(REL_CHILD)

    def is_servant (self):
        """
        Returns whether a person is part of the staff.
        """
        return self.role == ROLE_SERVANT

    def get_relative (self, type):
        """
        Returns the first relative (suspects[] index) that matches a
        given relationship type. Only really makes sense for binary
        relationships, i.e. spouses or fiances.

        :``type``: The type of the relationship: ``REL_SPOUSE``,
                   ``REL_PARENT``, ``REL_CHILD`` or ``REL_ENGAGED``. *Required*.
        """
        for r in self.rel:
            if r[1] == type:
               return r[0]
        return -1

    def chance_of_spouse (self):
        """
        Returns True if we should generate a spouse.
        """
        # More likely for the landlord.
        if self.role == ROLE_OWNER:
            return not one_chance_in(4)

        # Could be age dependent, but 50% works okay.
        return coinflip()

    def chance_of_children (self):
        """
        Returns True if we should generate children.
        """
        # Servants don't have children
        if self.role == ROLE_SERVANT:
            return False
        # More likely for the owner or if the spouse is also at the party.
        elif self.role == ROLE_OWNER or self.is_married():
            return not one_chance_in(3)
        else:
            # Lower likelihood of children if no spouse around.
            return one_chance_in(3)

    def create_spouse (self):
        """
        Generates a husband or wife for the current person.
        """
        # Opposite gender.
        g = self.get_mirrored_gender()

        # Similar age range, the men usually older.
        a = self.age + random.randint(-1,10)
        if g == 'f':
            a = max(18, self.age + random.randint(-10,1))

        rel = REL_SPOUSE
        # Younger characters may sometimes only be engaged.
        if self.age < 30 and one_chance_in(3):
            spouse = Person(self.role, gender = g, age = a)
            rel = REL_ENGAGED
        elif (self.gender == 'f'
                and self.check_has_relative(REL_PARENT)):
            spouse = Person(self.role, gender = g, age = a)
            # Update surname if female and (now) married.
            self.last = spouse.last
        else:
            # Apply the current surname to the spouse.
            spouse = Person(self.role, gender = g, age = a, last = self.last)

        return spouse, rel

    def create_child (self):
        """
        Generates a child for the current person.
        """
        a = max(19, self.age - (19 + random.randint(0, 8)))
        role = self.role
        if role == ROLE_OWNER:
            role = ROLE_FAMILY
        child = Person(role, age = a, last = self.last)

        return child

###############################################################
# Lists of suspects, plus victim and murderer.

class SuspectList (object):
    """
    A representation of all suspects, in form of a list of Persons
    and the indices of victim and murderer.
    """

    suspects = []

    def __init__ (self, max_suspects):
        """
        As long as more suspects are needed, generate new persons
        and, in another loop, also their relatives.

        :``max_suspects``: The maximum number of suspects. *Required*.
        """
        # Define function shortcut for speed-up.
        sappend  = self.suspects.append

        # There are approximately between N/5 and N/3 servants.
        num_servants = random.randint(math.floor(max_suspects/5),
                                      math.floor(max_suspects/3))

        # One of them is going to get killed...
        MAX_PERSONS = max_suspects + 1
        limit = MAX_PERSONS - num_servants

        count = 0
        role  = ROLE_OWNER
        while self.no_of_suspects() < MAX_PERSONS:
            p = Person(role)
            sappend(p)

            if not count:
                role = ROLE_FAMILY

            count = self.add_relatives(role, limit, count)

            if count >= limit:
                role = ROLE_SERVANT
                limit = MAX_PERSONS
            elif role == ROLE_FAMILY:
                role = ROLE_GUEST

        self.ensure_unique_names()
        self.add_honorifics()
        self.add_occupation()
        self.pick_victim()
        self.pick_murderer()

    def get_suspect_list (self):
        """
        Returns the suspects list of type Person[].
        """
        return self.suspects

    def no_of_suspects (self):
        """
        Returns the length of the suspects list.
        """
        return len(self.suspects)

    def real_no_of_suspects (self):
        """
        Returns the real number of suspects, i.e. excludes the victim.
        """
        return self.no_of_suspects() - 1

    def get_suspect (self, idx):
        """
        Returns a Person object matching the given index in the
        suspects[] list.

        :``idx``: An index of the suspects[] list. *Required*.
        """
        if idx < 0 or idx >= self.no_of_suspects():
            raise IndexError, "Index %d exceeds list of size %s." % (idx, self.no_of_suspects())
        return self.suspects[idx]

    def pick_victim (self):
        """
        Randomly pick the victim. Staff are excluded.
        """
        idx = -1
        while idx < 0 or self.get_suspect(idx).is_servant():
            idx = random.randint(0, self.no_of_suspects()-1)
        self.victim = idx

    def pick_murderer (self):
        """
        Randomly pick the murderer.
        """
        idx = -1
        while idx < 0 or self.is_victim(idx):
            idx = random.randint(0, self.no_of_suspects()-1)
        self.murderer = idx

    def get_victim (self):
        """
        Returns the victim in form of a Person object.
        """
        return self.get_suspect(self.victim)

    def get_murderer (self):
        """
        Returns the murderer in form of a Person object.
        """
        return self.get_suspect(self.murderer)

    def is_victim (self, idx):
        """
        Returns True if the given index matches the victim.

        :``idx``: An index of the suspects[] list. *Required*.
        """
        return self.victim == idx

    def is_murderer (self, idx):
        """
        Returns True if the given index matches the murderer.

        :``idx``: An index of the suspects[] list. *Required*.
        """
        return self.murderer == idx

    def add_spouse (self, idx):
        """
        Generates a husband or wife for a given person, and sets the
        necessary relationship.

        :``idx``: The index of the current person in the suspects[] list. *Required*.
        """
        curr = self.get_suspect(idx)
        spouse, rel = curr.create_spouse()
        spouse.set_relative(idx, rel)
        curr.set_relative(self.no_of_suspects(), rel)
        self.suspects.append(spouse)

    def add_child (self, parent_idx):
        """
        Generates a child for a given person, and sets the necessary
        relationship.

        :``idx``: The current person's index in the suspects[] list. *Required*.
        """
        parent = self.get_suspect(parent_idx)
        child  = parent.create_child()
        child.set_relative(parent_idx, REL_PARENT)
        parent.set_relative(self.no_of_suspects(), REL_CHILD)
        self.suspects.append(child)

    def update_child (self, idx_parent, idx_child):
        """
        Updates relationship and age range for a parent and child,
        passed as indices.

        :``idx_parent``: The parent's index in the suspects[] list. *Required*.
        :``idx_child``: The child's index in the suspects[] list. *Required*.
        """
        parent = self.get_suspect(idx_parent)
        child  = self.get_suspect(idx_child)
        parent.set_relative(idx_child, REL_CHILD)
        child.set_relative(idx_parent, REL_PARENT)
        # Up the parent's age, if necessary.
        if parent.age - child.age < 18:
            parent.age = child.age + 18

    def add_relatives (self, role, max_persons, count):
        """
        Given the current index (count), generates more persons
        related to the people already in the sub-list suspects[count:].

        :``role``: One of ``ROLE_OWNER``, ``ROLE_FAMILY``, ``ROLE_GUEST``
                   or ``ROLE_SERVANT``. *Required*.
        :``max_persons``: The maximum total number of suspects. *Required*.
        :``count``: The index of the first person to begin the iteration
                    over the suspects[] list. *Required*.
        """

        # define a shortcut for speedups
        sappend = self.suspects.append

        while count < self.no_of_suspects():
            curr = self.get_suspect(count)

            has_parents = curr.check_has_relative(REL_PARENT)
            if curr.check_has_relative(REL_ENGAGED):
                # nothing to be done
                pass
            elif curr.is_married():
                spouse = self.get_suspect(curr.get_relative(REL_SPOUSE))
                # Make sure the children are mutual and that the
                # age differences make sense.
                for r in spouse.rel:
                    if r[1] == REL_CHILD:
                        self.update_child(count, r[0])
            elif self.no_of_suspects() < max_persons:
                if curr.chance_of_spouse():
                    self.add_spouse(count)

                # Roll for children:
                # Suspects can have children even if not married because
                # they could be widowed or the spouse could be absent
                # from the party for any number of reasons.
                if (curr.age >= 40 and self.no_of_suspects() < max_persons
                    and curr.chance_of_children()):

                    # Still, pretend a woman _was_ married at some point,
                    # and change her last name.
                    if (has_parents and curr.gender == 'f'
                            and not curr.is_married()):
                        curr.set_random_last_name()

                    children = random.randint(1,2)
                    for k in xrange(children):
                        self.add_child(count)
                        if self.no_of_suspects() >= max_persons:
                            break

            count = count + 1

        return count

    def ensure_unique_names (self):
        """
        Reroll names that start with the same letters as names already
        in the list. This greatly reduces the danger of the player
        getting the characters mixed up.
        """

        # Don't even bother if we have more than 21 suspects.
        # Names starting with Q, X, Y, Z are rare to nonexistent.
        if self.no_of_suspects() > 21:
            return

        names = []
        n_append = names.append
        for s in self.suspects:
            while s.first[0] in names:
                oldname = s.first
                s.first = get_random_first_name(s.gender)
                # Return early if the names stop changing.
                if oldname == s.first:
                    return
            n_append(s.first[0])

    def add_honorifics (self):
        """
        Add honorifics to some of the suspects, as befits their role.
        """
        for s in self.suspects:
            if s.role == ROLE_OWNER:
                if s.gender == 'm':
                    s.title = 'Lord '
                else:
                    s.title = 'Lady '
            elif (s.role != ROLE_SERVANT and s.gender == 'm'
                    and s.age >= 30):
                if one_chance_in(5):
                    s.title = 'Dr. '
                elif s.age >= 50 and one_chance_in(5):
                    s.title = 'Major '
                elif s.age >= 40 and one_chance_in(8):
                    s.title = 'Reverend '

#          if not s.title:
#               if s.gender == 'm':
#                   s.title = 'Mr '
#               elif s.is_married():
#                  s.title = 'Mrs '
#               else:
#                   s.title = 'Miss '

    def add_occupation (self):
        """
        Add occupations for the staff, and also to some of the other
        suspects, as befits their role.
        """
        # TODO: These really should take into account age and the
        #       available rooms.
        jobs_staff_female = ['cook', 'parlourmaid', 'housekeeper']
        jobs_staff_male   = ['gardener', 'butler', 'secretary', 'valet']

        for s in self.suspects:
            if s.title:
                continue

            if s.role == ROLE_SERVANT:
                if s.gender == 'f':
                    s.occupation = random.choice(jobs_staff_female)
                else:
                    s.occupation = random.choice(jobs_staff_male)
            elif (s.age >= 25 and
                    not (s.is_married() or s.has_children())):
                # some more exotic guests
                if s.age < 50 and one_chance_in(10):
                    if s.gender == 'm':
                        s.occupation = 'actor'
                    else:
                        s.occupation = 'actress'
                elif s.gender == 'm' and one_chance_in(10):
                    s.occupation = 'painter'

    def print_suspects (self):
        """
        Prints the complete list of suspects and their relationships.
        """
        role = 'None'
        for i in xrange(self.no_of_suspects()):
            s = self.suspects[i]
            if s.role != role:
                role = s.role
                print_header(role)
            else:
                print ""
            if self.is_victim(i):
                print "***VICTIM***"
            elif self.is_murderer(i):
                print "***MURDERER***"
            print "Suspect %s:" % (i+1),
            s.describe(self)

##############################################
# Global methods

def print_header (str):
    """
    Outputs a given string and underlines it.
    """
    header = "\n%s:" % (str)
    print header
    print "-" * (len(header) - 1)

def main (num = 10):
    """
    Generate a list of suspects and display them.

    :``num``: The number of suspects to be generated. *Default 10*.
    """
    sl = SuspectList(num)
    sl.print_suspects()

if __name__ == "__main__":
    """
    Generate a list of suspects and display them.

    :``max_suspects``: The number of suspects to be generated. *Default 10*.
    """
    import sys

    # As each letter can only be used once, there's a fixed cap
    # at 26 suspects, but seeing how some letters are really rare
    # (or have no names assigned) we should not try for more than
    # around 20.
    max_suspects = 10
    if len(sys.argv) > 1:
        try:
            max_suspects = min(int(sys.argv[1]), 20)
        except ValueError:
            sys.stderr.write("Warning: Expected integer argument, using default value %d\n" % max_suspects)
            pass

    main(max_suspects)
