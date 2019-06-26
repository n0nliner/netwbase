import node

node.load_commit(commit_name="test commit")

for r in node.GOR:
    print(r, r.calc_layer())
