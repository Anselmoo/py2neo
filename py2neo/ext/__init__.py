#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2016, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from py2neo.graph import GraphError
from py2neo.remoting import Remote, remote


class ServerPlugin(object):
    """ Base class for server plugins.
    """

    def __init__(self, graph, name):
        self.graph = graph
        self.name = name
        remote_graph = remote(self.graph)
        metadata = remote_graph.get_json(force=False)
        extensions = metadata["extensions"]
        try:
            self.resources = {key: Remote(value) for key, value in extensions[self.name].items()}
        except KeyError:
            raise LookupError("No plugin named %r found on graph <%s>" % (self.name, remote_graph.uri))


class UnmanagedExtension(object):
    """ Base class for unmanaged extensions.
    """

    def __init__(self, graph, path):
        self.graph = graph
        dbms_uri = remote(self.graph.graph_service).uri
        self.remote = Remote(dbms_uri.rstrip("/") + path)
        try:
            self.remote.get_json(force=True)
        except GraphError:
            raise NotImplementedError("No extension found at path %r on "
                                      "graph <%s>" % (path, remote(self.graph).uri))
