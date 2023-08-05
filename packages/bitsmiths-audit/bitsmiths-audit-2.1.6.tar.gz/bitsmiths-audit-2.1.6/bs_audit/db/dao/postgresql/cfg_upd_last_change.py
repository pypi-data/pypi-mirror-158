# This file was generated by mettle.genes.db.GenPy3 [ver 2.1] on Wed Jul  6 10:16:56 2022
#  Target Database = postgresql
#
import datetime
import uuid
import time
import mettle.lib
import mettle.io
import mettle.db

from bs_audit.db.tables.icfg_upd_last_change import iCfgUpdLastChange

class dCfgUpdLastChange:

    def __init__(self, dbcon: mettle.db.IConnect):
        """
        Constructor.

        :param dbcon: Mettle database connection object.
        """
        self._dbcon   = dbcon
        self._dbstmnt = None
        self.irec     = iCfgUpdLastChange()
    def __enter__(self):
        """
        With statement enter.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        With statement exit.
        """
        self._destroy()

    def _destroy(self):
        self._dbstmnt = None

    def exec_deft(self,
                  idcrit: str) -> "dCfgUpdLastChange":
        """
        Execute the query by setting all the inputs.

        :param idcrit: str
        :return: Self for convenience.
        """
        self.irec.idcrit = idcrit

        return self.exec()

    def exec(self, irec: iCfgUpdLastChange = None) -> "dCfgUpdLastChange":
        """
        Execute the query, optionally passing in the input rec.

        :param irec:
        :return: Self for convenience.
        """
        if irec:
            self.irec._copy_from(irec)

        self._destroy()

        self._dbstmnt = self._dbcon.statement("CfgUpdLastChange", self._dbcon.STMNT_TYPE_CUD)

        self._dbstmnt.sql("""update
  audit.cfg c
set
  last_chg = current_timestamp
where
  c.id in ( [idcrit] )""")

        self._dbstmnt.dynamic("[idcrit]", self.irec.idcrit)

        self._dbcon.execute(self._dbstmnt)

        if irec:
            irec._copy_from(self.irec)

        return self

