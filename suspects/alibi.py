#!/usr/bin/env python
"""
Generate random first, last and full names from various building blocks.
"""

import random, sys
import database.database as db

class Alibi (object):
    """
    Alibi class. Where was a suspect at the time of the murder, and with whom?
    """
    def __init__ (self, rid, rname, witness = -1):
        """
        Initialize a suspect's alibi.

        :``rid``: A room index. *Required*.
        :``rname``: A room name. *Required*.
        :``witness``: Index of a suspect who can confirm the alibi, or -1 if none. *Default -1*.
        """
        self.rid     = rid
        self.rname   = rname
        self.witness = witness

##################################################
# Database files: ../database/alibi.db/<file>.db

DB_ALIBI_WITNESS = 'alibi.statement_witness'
DB_ALIBI_ALONE   = 'alibi.statement_nowitness'
DB_SYNONYM_TIME  = 'alibi.synonyms_time'
DB_SYNONYM_ALONE = 'alibi.synonyms_alone'

def db_get_entry (db_name):
    """
    Helper method returning a random database entry for a given database.

    :``db_name``: The database's name. *Required*
    """
    return db.get_database(db_name).random()

def db_get_alibi_statement (room, witness = None):
    """
    Returns a randomized alibi statement containing room and witness.

    :``room``: The alibi room. *Required*
    :``witness``: The witness' name, if any. *Default None*
    """

    if witness:
        alibi = db_get_entry(DB_ALIBI_WITNESS)
        alibi = alibi.replace("<witness>", witness)
    else:
        alibi = db_get_entry(DB_ALIBI_ALONE)
        if alibi.rfind("<alone>") != -1:
            alibi = alibi.replace("<alone>", db_get_entry(DB_SYNONYM_ALONE))

    alibi = alibi.replace("<room>", room)

    if alibi.rfind("<time>") != -1:
        alibi = alibi.replace("<time>", db_get_entry(DB_SYNONYM_TIME))

    alibi = alibi[0].capitalize() + alibi[1:].replace(",.", ".")

    return alibi
