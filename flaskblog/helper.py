#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
import functools

markdown = functools.partial(markdown.markdown,
                             safe_mode='remove',
                             output_format="html")
