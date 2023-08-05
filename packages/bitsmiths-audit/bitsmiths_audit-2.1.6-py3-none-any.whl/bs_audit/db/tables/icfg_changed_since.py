# This file was generated by mettle.genes.db.GenPy3 [ver 2.1] on Wed Jul  6 10:16:56 2022
#

import datetime
import uuid
import time
import dataclasses
import typing
import mettle.io
import mettle.db

@dataclasses.dataclass
class iCfgChangedSince(mettle.io.ISerializable):

    since: typing.Optional[datetime.datetime] = dataclasses.field(default=None, compare=False)
    criteria: str = dataclasses.field(default='', compare=False)

    def clear(self):
        """
        Clears all member variables for this database record.
        """
        self.since = None
        self.criteria = ''

    def _name(self) -> str:
        """
        Name of the record.

        :return: The name.
        """
        return 'iCfgChangedSince'

    def _serialize(self, _w: mettle.io.IWriter, _oname: str = None):
        """
        Serialize record to a stream.

        :param _w:
        :param _oname:
        """
        if _oname == None:
            _oname = self._name()

        _w.write_start(_oname)
        _w.write_datetime("since", self.since)
        _w.write_string("criteria", self.criteria)
        _w.write_end(_oname)

    def _deserialize(self, _r: mettle.io.IReader, _oname: str = None):
        """
        Deserialize record from a stream.

        :param _r:
        :param _oname:
        """
        if _oname == None:
            _oname = self._name()

        _r.read_start(_oname)
        self.since = _r.read_datetime("since")
        self.criteria = _r.read_string("criteria")
        _r.read_end(_oname)

    def _copy_from(self, rec: "iCfgChangedSince"):
        """
        Copies the column from the rec into this record.

        :param rec: The source record.
        """
        self.since = rec.since
        self.criteria = rec.criteria

    @staticmethod
    def _cache_davs(dvc=None):
        """
        Cache the DAV into the dav cache (or create one) and return it.

        :param dvc: (mettle.lib.DavCache), target cache, if None a new one is created and returned.
        """
        if dvc is None:
            dvc = mettle.lib.DavCache()

        dvc.add_targ("id", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))
        dvc.add_targ("since", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))
        dvc.add_targ("criteria", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))

        return dvc

    def _get_davs(self, dvc=None):
        iCfgChangedSince._cache_davs(dvc)


    class List(list, mettle.io.ISerializable):
        """
        List Class
        """

        def _name(self) -> str:
            """
            Name of the list.

            :return: The name
            """
            return 'iCfgChangedSince.List'

        def _serialize(self, _w: mettle.io.IWriter, _oname: str = None):
            """
            Serialize the list to a stream.

            :param _w:
            :param _oname:
            """
            if _oname == None:
                _oname = self._name()

            _w.write_start_list(_oname, len(self))

            for _rec in self:
                _rec._serialize(_w)

            _w.write_end(_oname)

        def _deserialize(self, _r: mettle.io.IReader, _oname: str = None):
            """
            Deserialize the list from a stream.

            :param _r:
            :param _oname:
            """
            if _oname == None:
                _oname = self._name()

            _cnt = _r.read_start_list(_oname)

            while _cnt >= 1:
                _rec  = iCfgChangedSince()
                _cnt -= 1
                _rec._deserialize(_r)
                self.append(_rec)

            _r.read_end(_oname)

        def _get_davs(self, dvc=None):
            return iCfgChangedSince._cache_davs(dvc)

