#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import abort, request
from math import ceil


from utils import list_data_file, get_data_config

BASE_DIR = os.path.dirname(__file__)


class ProductInfo(object):
    __slots__ = ['name', 'time', 'url', 'command', 'email']

    def __init__(self, name, time, url, command, email):
        self.name = name
        self.time = time
        self.url = url
        self.command = command
        self.email = email


class EmailInfo(object):
    __slots__ = ['username', 'password', 'smtpserver', 'smtpport']

    def __init__(self, username, password, smtpserver, smtpport):
        self.username = username
        self.password = password
        self.smtpserver = smtpserver
        self.smtpport = smtpport


class ProductDB(object):
    """
        convert mini/data file  to  object, and add method for op
    """

    def __init__(self):
        self.products = self.query()

    def query(self):
        return [self.get_option_value(file) for file in list_data_file()]

    @classmethod
    def get_option_value(cls, file):
        cfg = get_data_config(filename=file)
        section = cfg.sections()[0]
        return ProductInfo(
            name=cfg.get(section, 'name'),
            time=cfg.get(section, 'time'),
            url=cfg.get(section, 'url'),
            # command="\n".join(cfg.get(section, 'command')),
            command="<br>".join(eval(cfg.get(section, 'command'))),
            email=cfg.get(section, 'email')
        )

    def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
        if request:
            if page is None:
                try:
                    page = int(request.args.get('page', 1))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    page = 1

            if per_page is None:
                try:
                    per_page = int(request.args.get('per_page', 20))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    per_page = 20
        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                abort(404)
            else:
                page = 1

        if per_page < 0:
            if error_out:
                abort(404)
            else:
                per_page = 20

        items = self.products[per_page*(page-1):per_page*page]

        if not items and page != 1 and error_out:
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = per_page

        return Pagination(self, page, per_page, total, items)


class Pagination(object):
    def __init__(self, query, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


if __name__ == '__main__':
    pdb = ProductDB()
    # 找出 触发url的那个文件

    file = [i for i in pdb.products if i.url == 'abort(404)']
    print(file[0].name)