import pickle
import settings
import os

class register:
    def __init__(self, root=None):
        self.content = []
        self.roots = []
        self.root = root

    def is_exists(self, key):
        if self.find(key):
            return True
        return False

    def add_root(self, node):
        if self.is_exists(lambda node_: node_.id == node.id):
            self.roots.append(node)

    def add(self, any_node):
        if not self.is_exists(key=lambda _node: _node.id==any_node.id):
            self.content.append(any_node)
            return "200"

    def root_auto_id(self):
        # WTF
        return self.get_auto_id()

    def get_auto_id(self):
        return len(self.content)

    def find(self, key):
        return list(filter(key, self.content))

    def find_gen(self, key):
        for el in self.content:
            if key(el):
                yield el

    def get_by_layer_gen(self, layer):
        for ch in self.find(lambda _node: _node.layer() == layer):
            yield ch

    def get_layers_elements(self, layer):
        return [ch for ch in self.get_by_layer_gen()]

    def max_depth(self):
        return max(self.content, key=lambda node_:node_.calc_layer()).calc_layer() + 1

    def layer_iterator(self, layer_from=0, layer_to=None):
        layer_to = layer_to if layer_to else self.max_depth()
        for l_now in range(layer_from, layer_to):
            for el in self.find_gen(key=lambda node_: node_.calc_layer() == l_now):
                yield el

    def __iter__(self):
        for el in self.layer_iterator():
            yield el



class node:
    def __init__(self, metadata=None, register=True):
        self.register = register
        self.id = self.auto_id()
        self.metadata = metadata
        self.content = []

    def get_by_lambda_gen(self, key):
        for child in self.content:
            if key(child) == True:
                yield child

    def get_by_lambda_list(self, key):
        res_arr = []
        for element in self.get_by_lambda_gen(key=key):
            res_arr.append(element)
        return res_arr

    def __str__(self):
        return f"<node {self.id}>"

    def __repr__(self):
        return str(self)

    def auto_id(self):
        return GOR.get_auto_id()



class root_node(node):
    def __init__(self, metadata={}, register=True):
        super(root_node, self).__init__(metadata)
        self.root = True
        self.register = register

        if self.register:
            GOR.add(self)
            GOR.add_root(self)

    def __str__(self):
        return f"<root_node {self.id}>"

    def calc_layer(self):
        return 0

    def auto_id(self):
        return GOR.root_auto_id()



class simple_node(node):
    def __init__(self, parents=[], metadata={}, register=True):
        super(simple_node, self).__init__(metadata=metadata)
        self.root = False
        self.parents = parents
        if self.register:
            status = GOR.add(self)
            print(status)

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child):
        self.content.append(child)

    def calc_layer(self):
        return self.parents[0].calc_layer() + 1



def auto_commit_name():
    return len(os.listdir(os.path.join(settings.full_path, settings.commits_folder)))

def make_commit(commit_name=None):
    commit_name = commit_name if commit_name else auto_commit_name()
    GOR_dump = pickle.dumps(GOR)
    with open(os.path.join(settings.full_path, settings.commits_folder, commit_name), "wb+") as commit:
        commit.write(GOR_dump)

def load_commit(commit_name=None):
    load_it = commit_name if commit_name else auto_commit_name() - 1
    with open('netbase/commits/'+load_it, "rb") as loading:
        globals().update({"GOR":pickle.loads(loading.read())})




if __name__ != "__main__":
    # GOR is - Global Objects Register
    globals().update({"GOR":register()})
