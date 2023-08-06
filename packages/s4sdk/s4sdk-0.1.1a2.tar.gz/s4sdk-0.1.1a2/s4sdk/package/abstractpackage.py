import abc
from s4sdk import resource


class AbstractPackage(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__stbl_cache = None

    @abc.abstractmethod
    def scan_index(self, filter=None):
        pass

    @abc.abstractmethod
    def _get_content(self, resource):
        """Retrieve the content from Resource (which is guaranteed to have
        been returned from a __getitem__ call to this package)

        """

    @abc.abstractmethod
    def __getitem__(self, item):
        """Maps from a ResourceID to a Resource. Any other usage is an error.

        This method MUST NOT use any caches that are flushed by
        flush_index_cache.

        """

    def flush_index_cache(self):
        """Flush the index cache to save memory. This method is optional; some
        database formats may not need an index cache due to use of an
        efficient file format."""

    @property
    def stbl(self):
        if self.__stbl_cache is None:
            self.__stbl_cache = {}
            for stblid in self.scan_index(
                    resource.ResourceFilter(type=0x220557DA)):
                for key, value in stbl.read_stbl(self[stblid]):
                    self.__stbl_cache[key] = value
        return self.__stbl_cache

    def close(self):
        """Close the package, freeing any OS-level resources if necessary"""
        self.commit()

    def commit(self):
        """Commit any outstanding changes to disk without closing the
        file. Does not need to be called for read-only package access.

        """
