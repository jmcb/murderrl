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

# Hair colours
HAIR_RED     = 'red'
HAIR_BLOND   = 'blond'
HAIR_BROWN   = 'brown'
HAIR_BLACK   = 'black'

class Alibi (object):
    """
    Alibi class. Where was a suspect at the time of the murder, and with whom?
    """
    def __init__ (self, place, witness = -1):
        """
        Initialize a suspect's alibi.

        :``place``: A room name. *Required*.
        :``witness``: Index of a suspect who can confirm the alibi, or -1 if none. *Default -1*.
        """
        self.room = place
        self.witness = witness

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

        self.hair = None
        self.rel  = []
        self.title = ''
        self.occupation = ''
        self.alibi = None

    def __str__ (self, desc_hair = False):
        """
        Prints a single-line description of the person.
        """
        job = ''
        if self.occupation:
            job = "%s, " % self.occupation
        hair = ""
        if desc_hair:
            hair = "%s, " % self.describe_hair()

        return "%s (%s), %s%s%s" % (self.get_fullname(),
               self.gender, job, hair, self.age)

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

    def set_random_hair_colour (self, hair_list, exception = None):
        """
        Assigns a random hair colour.

        :``hair_list``: List of allowed hair colours. *Required*.
        :``exception``: Forbidden hair colour, if any. *Default none*.
        """
        while True:
            self.hair = random.choice(hair_list)
            if self.hair != exception:
                break

    def describe_hair (self):
        """
        Returns a description of the person's hair colour.
        """
        if not self.hair:
            return "unknown hair colour"

        if self.hair == HAIR_BLOND:
            return self.hair
        else:
            return "%shaired" % self.hair

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

    def set_alibi (self, room, witness = -1):
        """
        Provides this person with an alibi.

        :``room``: A room name (string). *Required*.
        :``witness``: Suspect list index of another person. *Default -1*.
        """
        self.alibi = Alibi(room, witness)

    def has_alibi_witness (self):
        """
        Returns true if the person has an alibi confirmed by someone else.
        """
        if not self.alibi:
            return False

        if self.alibi.witness == -1:
            return False

        return True

    def get_alibi (self, list):
        if not self.alibi:
            return "unknown"

        a = self.alibi
        witness = ""
        if self.has_alibi_witness():
            witness = "with %s" % list.get_suspect(a.witness).get_name()
        else:
            witness = "alone"
        return "%s, %s" % (a.room, witness)

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

    def is_family (self):
        return (self.role == ROLE_OWNER or self.role == ROLE_FAMILY)

    def get_relationship (self, other_idx, other = None):
        """
        Return a relationship description of the current person
        to a second person with index other_idx.
        """
        rel = self.rel
        num_range = xrange(len(rel))
        for i in num_range:
            r = rel[i]
            if r[0] == other_idx:
                if r[1] == REL_SPOUSE:
                    if self.gender == 'm':
                        return "husband"
                    else:
                        return "wife"
                elif r[1] == REL_ENGAGED:
                    if self.gender == 'm':
                        return "fiance"
                    else:
                        return "fiancee"
                # The other person is a parent.
                elif r[1] == REL_PARENT:
                    if self.gender == 'm':
                        return "son"
                    else:
                        return "daughter"
                # The other person is a child.
                elif r[1] == REL_CHILD:
                    if self.gender == 'm':
                        return "father"
                    else:
                        return "mother"

                return r[1]

        if other != None:
            if other.is_family():
                if self.role == ROLE_FAMILY:
                    return "extended family"
                if self.role == ROLE_GUEST:
                    return "guest"
                if self.role == ROLE_SERVANT:
                    return "servant"
            elif other.role == ROLE_GUEST:
                if self.is_family():
                    return "host"
                if self.role == ROLE_GUEST:
                    return "other guest"

        return "none"

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

    def __init__ (self, max_suspects, rooms = None):
        """
        As long as more suspects are needed, generate new persons
        and, in another loop, also their relatives.

        :``max_suspects``: The maximum number of suspects. *Required*.
        :``rooms``: List of room names. Required for calculating alibis. *Default none*.
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
        if rooms:
            self.get_create_alibis(rooms)
            self.add_hair_colours()

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

    def describe_suspect (self, idx):
        # self.get_suspect(idx).describe(self)
        p = self.get_suspect(idx)
        print p
        print ""
        lcount = 2
        if idx != self.victim:
            print "Relationship to victim:", p.get_relationship(self.victim, self.get_victim())
            lcount += 1
            desc = "Other relationships   :"
        else:
            desc = "Relationships:"

        first = True
        for i in xrange(len(p.rel)):
            r = p.rel[i]
            if r[0] == self.victim:
                continue
            relative = self.get_suspect(r[0])
            print "%s %s (%s)" % (desc, relative.get_fullname(), relative.get_relationship(idx))
            lcount += 1
            if first:
                first = False
                if idx != self.victim:
                    desc = "                       "
                else:
                    desc = "              "

        if first:
            if idx != self.victim:
                print desc, "none"
                print ""
                lcount += 2
        else:
            print ""
            lcount += 1

        print "Hair colour:", p.describe_hair()
        lcount += 1
        if idx == self.victim:
            print "\nThe clue: a %s hair!" % self.get_murderer().hair
            lcount += 2
        else:
            print "Alibi      :", p.get_alibi(self)
            lcount += 1

        fill(lcount)

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
#            elif (s.age >= 25 and
#                    not (s.is_married() or s.has_children())):
                # some more exotic guests
#                if s.age < 50 and one_chance_in(10):
#                    if s.gender == 'm':
#                        s.occupation = 'actor'
#                    else:
#                        s.occupation = 'actress'
#                elif s.gender == 'm' and one_chance_in(10):
#                    s.occupation = 'painter'

    def create_paired_alibi (self, p1, p2, room):
        """
        Set mutual alibis for two suspects confirming one another.

        :``p1``: Index of a suspect. *Required*.
        :``p2``: Index of another suspect. *Required*.
        :``room``: Room name. *Required*.
        """
        self.get_suspect(p1).set_alibi(room, p2)
        self.get_suspect(p2).set_alibi(room, p1)

    def create_alibis (self, rooms):
        """
        Generate alibis for all suspects.

        :``rooms``: A list of possible room names. *Required*.
        """

        suspects = range(0, len(self.suspects))
        # The victim doesn't need an alibi, and the murderer is
        # handled specially.
        suspects.remove(self.victim)
        suspects.remove(self.murderer)

        random.shuffle(suspects)
        # Re-add murderer at the end of the shuffled list.
        suspects.append(self.murderer)

        # First, create alibis for suspects who were together at the time.
        # For ease of computation, only consider pairs of suspects.
        # The number of pairs depends on the total number of suspects.
        N = len(suspects)
        PAIRED = 2 * max(1, random.randint((N+1)/5, (N+1)/3))
        # print "N: %d -> min: %d, max: %d -> pairs: %d" % (N, (N+1)/5, (N+1)/3, PAIRED/2)
        for i in range(0, PAIRED, 2):
            if i+1 >= N:
                break
            room = rooms.pop()
            p1   = suspects[i]
            p2   = suspects[i+1]
            self.create_paired_alibi(p1, p2, room)

        # The remaining suspects don't have a witness.
        # This includes the murderer.
        # TODO: Sometimes allow the murderer to lie about having a witness.
        idx_range = range(PAIRED, N)
        for i in idx_range:
            p = suspects[i]
            self.get_suspect(p).set_alibi(rooms.pop())

    def get_create_alibis (self, rooms):
        """
        Generates alibis for all suspects. Returns a list of Alibis.

        :``rooms``: A list of room names (strings). *Required*.
        """
        self.create_alibis(rooms)
        alibis = []
        for i in xrange(len(self.suspects)):
            p = self.get_suspect(i)
            alibis.append(p.alibi)

        return alibis

    def get_cleared_suspects (self):
        """
        Returns a list of indices of suspects with a confirmed alibi.
        """
        confirmed = []
        for i in xrange(len(self.suspects)):
            if self.get_suspect(i).has_alibi_witness():
                confirmed.append(i)

        return confirmed

    def print_alibis (self, alibis):
        """
        Prints basic alibi statements mentioning room and witness.

        :``alibis``: A list of suspect indices. *Required*.
        """
        for i in xrange(len(alibis)):
            idx = alibis[i]
            p = self.get_suspect(idx)
            print "%s: %s" % (p.get_name(), p.get_alibi(self))

    def add_hair_colours (self):
        """
        Assign hair colours to the suspects in such a way that if both
        the murderer's hair colour and all alibis are known, only the
        murderer remains suspect.
        """
        # First, pick the maximum number of hair colours. The more suspects
        # there are, the likelier is using all 4 colours. Minimum 2.
        max_hair_num = max(2, (len(self.suspects) - 1)/2)
        HAIR_NUM     = min(4, random.randint(2, max_hair_num))

        full_hair_list = [HAIR_RED, HAIR_BLOND, HAIR_BROWN, HAIR_BLACK]
        hair_list      = random.sample(full_hair_list, HAIR_NUM)
        #print "max. hair: %d -> HAIR_NUM: %d -> %s" % (max_hair_num, HAIR_NUM, hair_list)

        # Pick a random hair colour for the murderer.
        self.get_murderer().set_random_hair_colour(hair_list)
        m_hair = self.get_murderer().hair

        # Try to give the victim a hair colour outside of hair list.
        other_list = full_hair_list
        if HAIR_NUM < 4:
            other_list = list(set(full_hair_list) - set(hair_list))
        self.get_victim().set_random_hair_colour(other_list, m_hair)

        # confirmed and unconfirmed alibis
        confirmed      = self.get_cleared_suspects()
        total_suspects = range(0, len(self.suspects))
        unconfirmed    = list(set(total_suspects) - set(confirmed))
        unconfirmed.remove(self.murderer)
        unconfirmed.remove(self.victim)

        # Give each non-cleared suspect a different hair colour than
        # the murderer's.
        for i in xrange(len(unconfirmed)):
            p = unconfirmed[i]
            self.get_suspect(p).set_random_hair_colour(hair_list, m_hair)

        # Make sure there are at least unconfirmed/HAIR_NUM suspects
        # with the same hair colour as the murderer.
        random.shuffle(confirmed)
        expected_hair_count = min(len(unconfirmed)/HAIR_NUM, confirmed)
        for i in xrange(expected_hair_count):
            p = confirmed[i]
            self.get_suspect(p).hair = m_hair

        # Give the remaining suspects a truly random hair colour.
        for i in xrange(expected_hair_count, len(confirmed)):
            p = confirmed[i]
            self.get_suspect(p).set_random_hair_colour(hair_list)

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

def fill (num):
    if num > 24:
        return
    for i in range(num, 24):
        print ""

def print_header (str):
    """
    Outputs a given string and underlines it.
    """
    header = "\n%s:" % (str)
    print header
    print "-" * (len(header) - 1)
